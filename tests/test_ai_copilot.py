"""Unit tests for AI incident triage and post-mortem generation."""
from src.ai_copilot import ai_copilot

def test_triage_incident_heuristic():
    res = ai_copilot.triage_incident(
        title="PostgreSQL replica lag high and blocking queries",
        service="Primary PostgreSQL DB",
        logs_or_description="Lag is 180s. Lock contention detected.",
        affected_users=2000
    )
    assert res["recommended_severity"] == "P1 - Critical"
    assert "blast_radius_score" in res
    assert "remediation_checklist" in res
    assert len(res["remediation_checklist"]) > 0

def test_generate_post_mortem():
    report = ai_copilot.generate_post_mortem(
        incident_id="INC-1001",
        title="Payment Gateway Timeout",
        service="Payment Gateway",
        severity="P2 - High",
        root_cause="Third-party rate limits",
        duration_minutes=45,
        affected_users=1200
    )
    assert "Incident Post-Mortem" in report
    assert "INC-1001" in report
    assert "Payment Gateway" in report

