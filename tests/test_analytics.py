"""Unit tests for analytics calculations, SLA metrics, and anomaly detection."""
import pytest
import pandas as pd
from src.analytics import (
    calculate_kpis,
    calculate_mttr_by_severity,
    calculate_service_breakdown,
    detect_operational_anomalies,
    get_at_risk_active_incidents,
)
from src.config import config
from src.data_generator import generate_incidents_data

@pytest.fixture
def sample_df():
    return generate_incidents_data(num_records=50, seed=123)

def test_calculate_kpis(sample_df):
    kpis = calculate_kpis(sample_df)
    assert "total_incidents" in kpis
    assert kpis["total_incidents"] == 50
    assert 0 <= kpis["sla_compliance_rate"] <= 100
    assert kpis["overall_mttr_minutes"] >= 0
    assert kpis["open_incidents"] >= 0

def test_calculate_kpis_empty():
    empty_df = pd.DataFrame()
    kpis = calculate_kpis(empty_df)
    assert kpis["total_incidents"] == 0
    assert kpis["sla_compliance_rate"] == 100.0

def test_calculate_mttr_by_severity(sample_df):
    mttr_df = calculate_mttr_by_severity(sample_df)
    assert not mttr_df.empty
    assert "severity" in mttr_df.columns
    assert "avg_mttr_min" in mttr_df.columns

def test_calculate_service_breakdown(sample_df):
    svc_df = calculate_service_breakdown(sample_df)
    assert not svc_df.empty
    assert "service" in svc_df.columns
    assert "total_incidents" in svc_df.columns
    assert "breach_rate_pct" in svc_df.columns

def test_detect_operational_anomalies(sample_df):
    anomaly_df = detect_operational_anomalies(sample_df, contamination=0.1)
    assert "is_anomaly" in anomaly_df.columns
    assert "anomaly_reason" in anomaly_df.columns
    assert anomaly_df["is_anomaly"].dtype == bool

def test_get_at_risk_active_incidents(sample_df):
    at_risk = get_at_risk_active_incidents(sample_df)
    assert isinstance(at_risk, pd.DataFrame)

def test_config_anomaly_contamination_setting():
    # Test setting and clamping
    config.set_anomaly_contamination(0.15)
    assert config.current_contamination == 0.15

    # Test lower bound clamp
    config.set_anomaly_contamination(0.001)
    assert config.current_contamination == config.MIN_ANOMALY_CONTAMINATION

    # Test upper bound clamp
    config.set_anomaly_contamination(0.99)
    assert config.current_contamination == config.MAX_ANOMALY_CONTAMINATION

    # Reset to default
    config.set_anomaly_contamination(config.DEFAULT_ANOMALY_CONTAMINATION)

def test_detect_operational_anomalies_default_config(sample_df):
    # Test execution when contamination is None (uses config.current_contamination)
    config.set_anomaly_contamination(0.05)
    anomaly_df = detect_operational_anomalies(sample_df, contamination=None)
    assert "is_anomaly" in anomaly_df.columns
    assert "anomaly_score" in anomaly_df.columns

