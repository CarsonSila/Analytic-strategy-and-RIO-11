"""Operational Analytics, SLA Compliance, and ML Anomaly Detection."""
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from src.config import config

def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate key executive operational metrics from the incident dataframe."""
    if df.empty:
        return {
            "total_incidents": 0,
            "open_incidents": 0,
            "resolved_incidents": 0,
            "critical_open": 0,
            "sla_compliance_rate": 100.0,
            "overall_mttr_minutes": 0.0,
            "total_affected_users": 0,
            "sla_breaches": 0,
        }

    total_incidents = len(df)
    open_mask = df["status"].isin(["Open", "In Progress"])
    open_incidents = int(open_mask.sum())
    resolved_mask = df["status"] == "Resolved"
    resolved_incidents = int(resolved_mask.sum())

    critical_open = int((open_mask & df["severity"].isin(["P1 - Critical", "P2 - High"])).sum())

    # SLA Compliance
    breaches = int((df["sla_status"] == "Breached").sum())
    evaluated_incidents = total_incidents
    sla_compliance_rate = round(((evaluated_incidents - breaches) / evaluated_incidents) * 100, 1) if evaluated_incidents > 0 else 100.0

    # MTTR (for resolved incidents with positive duration)
    resolved_df = df[resolved_mask & df["duration_minutes"].notna()]
    overall_mttr = round(float(resolved_df["duration_minutes"].mean()), 1) if not resolved_df.empty else 0.0

    total_affected_users = int(df["affected_users"].sum()) if "affected_users" in df.columns else 0

    return {
        "total_incidents": total_incidents,
        "open_incidents": open_incidents,
        "resolved_incidents": resolved_incidents,
        "critical_open": critical_open,
        "sla_compliance_rate": sla_compliance_rate,
        "overall_mttr_minutes": overall_mttr,
        "total_affected_users": total_affected_users,
        "sla_breaches": breaches,
    }

def calculate_mttr_by_severity(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate MTTR grouped by severity level."""
    resolved_df = df[df["status"] == "Resolved"].copy()
    if resolved_df.empty or "duration_minutes" not in resolved_df.columns:
        return pd.DataFrame(columns=["severity", "count", "avg_mttr_min", "sla_target_min"])

    grouped = resolved_df.groupby("severity").agg(
        count=("incident_id", "count"),
        avg_mttr_min=("duration_minutes", "mean"),
        sla_target_min=("sla_target_minutes", "first")
    ).reset_index()

    grouped["avg_mttr_min"] = grouped["avg_mttr_min"].round(1)
    return grouped

def calculate_service_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate incident counts and breach rates per service."""
    if df.empty:
        return pd.DataFrame(columns=["service", "total_incidents", "breaches", "breach_rate_pct"])

    grouped = df.groupby("service").agg(
        total_incidents=("incident_id", "count"),
        breaches=("sla_status", lambda s: (s == "Breached").sum()),
    ).reset_index()

    grouped["breach_rate_pct"] = ((grouped["breaches"] / grouped["total_incidents"]) * 100).round(1)
    return grouped.sort_values(by="total_incidents", ascending=False)

def detect_operational_anomalies(df: pd.DataFrame, contamination: float | None = None) -> pd.DataFrame:
    """Detect statistical and ML-based operational anomalies using IsolationForest."""
    if contamination is None:
        contamination = config.current_contamination

    # Ensure contamination is within valid (0, 0.5] range
    contamination = max(0.01, min(0.49, float(contamination)))

    df_copy = df.copy()
    if df_copy.empty or len(df_copy) < 5:
        df_copy["is_anomaly"] = False
        df_copy["anomaly_reason"] = "Insufficient data points for ML detection"
        return df_copy

    # Prepare features for ML anomaly detection: duration and affected users
    features = []
    # Fill duration for active incidents with current elapsed time or median
    median_duration = df_copy["duration_minutes"].median() if df_copy["duration_minutes"].notna().any() else 60
    duration_series = df_copy["duration_minutes"].fillna(median_duration).astype(float)
    users_series = df_copy["affected_users"].fillna(0).astype(float)
    
    feature_matrix = np.column_stack([duration_series, users_series])

    try:
        iso_forest = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        preds = iso_forest.fit_predict(feature_matrix)
        scores = iso_forest.decision_function(feature_matrix)
        
        df_copy["is_anomaly"] = preds == -1
        df_copy["anomaly_score"] = np.round(-scores, 3) # higher score = more anomalous
    except Exception:
        # Fallback to standard 2-sigma z-score threshold
        dur_mean, dur_std = duration_series.mean(), duration_series.std()
        df_copy["is_anomaly"] = (duration_series > dur_mean + 2 * (dur_std if dur_std > 0 else 1))
        df_copy["anomaly_score"] = 0.5

    # Generate human-readable explanation for anomalies
    reasons = []
    for _, row in df_copy.iterrows():
        if row["is_anomaly"]:
            dur = row["duration_minutes"] if pd.notna(row["duration_minutes"]) else median_duration
            target = row["sla_target_minutes"] if pd.notna(row["sla_target_minutes"]) else 60
            users = row["affected_users"]
            if dur > target * 2:
                reasons.append(f"Excessive Duration ({int(dur)}m vs {int(target)}m SLA target)")
            elif users > 1000:
                reasons.append(f"Severe User Blast Radius ({int(users):,} affected users)")
            else:
                reasons.append("Multi-variate statistical outlier (ML Flagged)")
        else:
            reasons.append("Normal Operational Bounds")

    df_copy["anomaly_reason"] = reasons
    return df_copy

def get_at_risk_active_incidents(df: pd.DataFrame) -> pd.DataFrame:
    """Identify active incidents currently approaching or exceeding SLA limits."""
    open_df = df[df["status"].isin(["Open", "In Progress"])].copy()
    if open_df.empty:
        return pd.DataFrame()

    now = pd.Timestamp.now()
    open_df["created_at_dt"] = pd.to_datetime(open_df["created_at"])
    open_df["elapsed_minutes"] = ((now - open_df["created_at_dt"]).dt.total_seconds() / 60).astype(int)
    open_df["sla_budget_used_pct"] = ((open_df["elapsed_minutes"] / open_df["sla_target_minutes"]) * 100).round(1)
    
    # Flag risk levels
    def flag_risk(row):
        if row["sla_budget_used_pct"] >= 100:
            return "Critical Breach"
        elif row["sla_budget_used_pct"] >= 75:
            return "Imminent Breach Risk"
        else:
            return "Healthy"

    open_df["risk_level"] = open_df.apply(flag_risk, axis=1)
    return open_df.sort_values(by="sla_budget_used_pct", ascending=False)

