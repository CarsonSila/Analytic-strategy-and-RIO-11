"""Automated Daily Executive Operations Report Generator."""
from datetime import datetime
import pandas as pd
from src.analytics import calculate_kpis, calculate_service_breakdown, calculate_mttr_by_severity

def generate_executive_daily_report(df: pd.DataFrame, report_date: str | None = None) -> str:
    """Generate a clean, structured Executive Operations Daily Briefing report in Markdown."""
    if report_date is None:
        report_date = datetime.now().strftime("%Y-%m-%d")

    kpis = calculate_kpis(df)
    svc_df = calculate_service_breakdown(df)
    mttr_df = calculate_mttr_by_severity(df)

    top_breached_services = svc_df[svc_df["breaches"] > 0].head(3)
    breach_summary = ""
    if not top_breached_services.empty:
        for _, r in top_breached_services.iterrows():
            breach_summary += f"- **{r['service']}**: {int(r['breaches'])} breach(es) ({r['breach_rate_pct']}% breach rate)\n"
    else:
        breach_summary = "- Zero service-level SLA breaches recorded in this reporting window.\n"

    # Severity MTTR breakdown table
    mttr_table = "| Severity | Resolved Incidents | Avg MTTR (min) | Target SLA (min) |\n| :--- | :--- | :--- | :--- |\n"
    for _, r in mttr_df.iterrows():
        mttr_table += f"| {r['severity']} | {int(r['count'])} | {r['avg_mttr_min']}m | {r['sla_target_min']}m |\n"

    # Executive Status Indicator
    status_emoji = "🟢 **HEALTHY**" if kpis["sla_compliance_rate"] >= 95 else ("🟡 **ELEVATED RISK**" if kpis["sla_compliance_rate"] >= 85 else "🔴 **CRITICAL ACTION REQUIRED**")

    report = f"""# 📊 Daily Executive Operations Briefing
**Report Date:** {report_date}  
**Overall System Health:** {status_emoji}  
**Prepared By:** OpsPulse AI Automated Engine  

---

## 1. Executive Headline Metrics
| Metric | Value | Target Benchmark | Status |
| :--- | :--- | :--- | :--- |
| **Global SLA Compliance** | **{kpis['sla_compliance_rate']}%** | ≥ 95.0% | {"✅ Met" if kpis['sla_compliance_rate'] >= 95 else "⚠️ Below Target"} |
| **Mean Time to Resolution (MTTR)** | **{kpis['overall_mttr_minutes']} min** | ≤ 60.0 min | {"✅ Optimal" if kpis['overall_mttr_minutes'] <= 60 else "⚠️ Elevated"} |
| **Total Incidents Recorded** | **{kpis['total_incidents']}** | N/A | Total Volume |
| **Active / In-Flight Incidents** | **{kpis['open_incidents']}** | < 5 | {"✅ Controlled" if kpis['open_incidents'] < 5 else "⚠️ High Backlog"} |
| **Critical Active (P1/P2)** | **{kpis['critical_open']}** | 0 | {"✅ 0 Critical" if kpis['critical_open'] == 0 else "🚨 Active P1/P2"} |
| **Total Customer Blast Radius** | **{kpis['total_affected_users']:,} users** | Low | Cumulative Impact |

---

## 2. MTTR Performance by Severity
{mttr_table}

---

## 3. SLA Breach Hotspots by Service
{breach_summary}

---

## 4. Key Operational Recommendations & Next Steps
1. **Capacity Scaling**: Evaluate autoscaling rules on top-breaching services to reduce MTTR under peak load.
2. **Alert Tuning**: Adjust early warning thresholds for database replication and API gateway latency.
3. **Runbook Automation**: Accelerate automated self-healing scripts for Redis session eviction and dead-letter queue replays.
4. **On-Call Review**: Conduct weekly retrospective on all P1 incidents to close out action items.

---
*OpsPulse AI - Automated Daily Operations Intelligence Report*
"""
    return report

