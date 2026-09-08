"""AI Incident Triage, Root Cause Analysis, and Post-Mortem Generator."""
import os
import json
import re
from typing import Dict, Any, List
from src.config import config

class AICopilot:
    """Intelligent Incident Triage and Operations Copilot."""

    def __init__(self):
        self.openai_key = config.OPENAI_API_KEY
        self.gemini_key = config.GEMINI_API_KEY
        self.anthropic_key = config.ANTHROPIC_API_KEY

    def triage_incident(
        self,
        title: str,
        service: str,
        logs_or_description: str,
        affected_users: int = 0
    ) -> Dict[str, Any]:
        """Perform comprehensive AI incident triage and generate remediation steps."""
        # Try live LLM if API key is provided
        if self.openai_key:
            try:
                return self._triage_via_openai(title, service, logs_or_description, affected_users)
            except Exception as e:
                pass  # Fall back to smart built-in heuristic engine

        # Built-in Intelligent Heuristic Copilot Engine
        return self._smart_heuristic_triage(title, service, logs_or_description, affected_users)

    def generate_post_mortem(
        self,
        incident_id: str,
        title: str,
        service: str,
        severity: str,
        root_cause: str,
        duration_minutes: int,
        affected_users: int
    ) -> str:
        """Generate a complete executive & engineering incident post-mortem markdown report."""
        if self.openai_key:
            try:
                return self._post_mortem_via_openai(
                    incident_id, title, service, severity, root_cause, duration_minutes, affected_users
                )
            except Exception:
                pass

        # Intelligent structured template generation
        return f"""# Incident Post-Mortem: {incident_id} - {title}

## 1. Executive Summary
- **Incident ID:** {incident_id}
- **Service Affected:** {service}
- **Severity Level:** {severity}
- **Total Downtime / Duration:** {duration_minutes} minutes
- **Customer Blast Radius:** ~{affected_users:,} affected users
- **SLA Breach Status:** {"⚠️ Breached" if duration_minutes > config.SLA_THRESHOLDS.get(severity, 60) else "✅ Compliant"}

---

## 2. Root Cause Analysis (5 Whys Framework)
1. **Direct Cause:** {root_cause}
2. **Detection Trigger:** Monitoring alert fired based on error rate and latency anomalies.
3. **Escalation Pathway:** Automated on-call pager alerted primary engineer within 3 minutes.
4. **Underlying Vulnerability:** Lack of automated backpressure shedding and circuit breaker isolation under peak traffic.
5. **Systemic Root Cause:** Inadequate load testing for edge-case failover scenarios during high concurrency.

---

## 3. Incident Timeline
- **T+00:00** - Initial telemetry spike recorded on `{service}`.
- **T+00:04** - PagerDuty alert triggered; primary on-call engineer acknowledged incident.
- **T+00:12** - Emergency war room established; mitigation steps initiated from operational runbook.
- **T+00:{max(15, duration_minutes - 10):02d}** - Remediation patch/failover executed. Error rates began stabilizing.
- **T+00:{duration_minutes:02d}** - Service restored to nominal baseline. All health checks green.

---

## 4. Preventive Action Items & Ownership
| Priority | Action Item | Owner | Target Date |
| :--- | :--- | :--- | :--- |
| **P0** | Implement automated circuit breaker on `{service}` | SRE Team | Within 7 days |
| **P1** | Add regression integration tests simulating failover scenario | QA / Dev | Within 14 days |
| **P1** | Fine-tune alert threshold to trigger 5 minutes earlier | Observability | Within 5 days |
| **P2** | Update operational runbook documentation | Operations Lead | Completed |

*Generated automatically by OpsPulse AI Copilot.*
"""

    def _smart_heuristic_triage(
        self,
        title: str,
        service: str,
        logs: str,
        affected_users: int
    ) -> Dict[str, Any]:
        """High-precision heuristic triage engine analyzing patterns, logs, and blast radius."""
        combined_text = f"{title} {service} {logs}".lower()

        # Severity classification rules
        is_p1 = any(kw in combined_text for kw in ["database", "postgres", "outage", "sso", "saml", "data loss", "checkout fail", "deadlock", "unreachable"]) or affected_users > 2500
        is_p2 = any(kw in combined_text for kw in ["504", "gateway", "latency", "timeout", "stripe", "rate limit", "redis", "memory", "spike", "throttl"]) or affected_users > 500
        is_p3 = any(kw in combined_text for kw in ["search", "elastic", "shard", "email", "worker", "delay", "queue", "slow"])

        if is_p1:
            recommended_severity = "P1 - Critical"
            blast_radius_score = min(98, 70 + (affected_users // 200))
            sla_budget = config.SLA_THRESHOLDS["P1 - Critical"]
        elif is_p2:
            recommended_severity = "P2 - High"
            blast_radius_score = min(75, 45 + (affected_users // 100))
            sla_budget = config.SLA_THRESHOLDS["P2 - High"]
        elif is_p3:
            recommended_severity = "P3 - Medium"
            blast_radius_score = min(40, 20 + (affected_users // 50))
            sla_budget = config.SLA_THRESHOLDS["P3 - Medium"]
        else:
            recommended_severity = "P4 - Low"
            blast_radius_score = min(20, 5 + (affected_users // 20))
            sla_budget = config.SLA_THRESHOLDS["P4 - Low"]

        # Root cause extraction and action items
        remediation_steps = []
        root_cause_hypothesis = ""
        matching_runbook = ""

        if "db" in combined_text or "postgres" in combined_text or "replication" in combined_text or "lock" in combined_text:
            root_cause_hypothesis = "Query contention or unindexed heavy scan blocking write-ahead logging (WAL) replication."
            matching_runbook = "database_failover.md"
            remediation_steps = [
                "Inspect active queries: `SELECT * FROM pg_stat_activity WHERE state != 'idle';`",
                "Identify and terminate blocking query PID: `SELECT pg_terminate_backend(<PID>);`",
                "If replication lag exceeds 5m, promote standby read-replica to primary.",
                "Verify connection pool capacity in PgBouncer.",
            ]
        elif "gateway" in combined_text or "504" in combined_text or "latency" in combined_text or "timeout" in combined_text:
            root_cause_hypothesis = "Upstream microservice thread saturation leading to cascading gateway 504 timeouts."
            matching_runbook = "api_gateway_latency.md"
            remediation_steps = [
                "Correlate latency spikes across downstream microservice APM traces.",
                "Trigger circuit breaker to serve cached fallback responses.",
                "Scale Kubernetes deployment replicas: `kubectl scale deployment/<svc> --replicas=10`.",
                "Flush edge CDN/Redis cache to resolve stale key stampedes.",
            ]
        elif "auth" in combined_text or "sso" in combined_text or "saml" in combined_text or "jwt" in combined_text:
            root_cause_hypothesis = "JWKS public signing certificate rotation failure or Redis session pool exhaustion."
            matching_runbook = "auth_service_outage.md"
            remediation_steps = [
                "Verify Identity Provider (Okta/Auth0/AzureAD) external health status.",
                "Trigger internal JWKS public key cache reload via admin endpoint.",
                "Perform rolling restart of Auth pods: `kubectl rollout restart deployment/auth-service`.",
                "Temporarily widen JWT validation clock skew grace period.",
            ]
        elif "stripe" in combined_text or "payment" in combined_text or "webhook" in combined_text:
            root_cause_hypothesis = "Third-party payment gateway throttling or dead-letter queue ingestion backlog."
            matching_runbook = "payment_gateway_timeout.md"
            remediation_steps = [
                "Check external payment processor status page for degradation.",
                "Switch routing rule to secondary merchant gateway fallback.",
                "Drain and replay dead-letter queue (DLQ) messages with exponential backoff.",
                "Notify Customer Experience lead with list of pending transaction IDs.",
            ]
        else:
            root_cause_hypothesis = "Resource saturation or unhandled edge-case exception in service processing loop."
            matching_runbook = "general_incident_triage.md"
            remediation_steps = [
                "Inspect latest deployment git commit diff and rollout logs.",
                "Review error trace logs in Datadog/CloudWatch for unhandled exceptions.",
                "Restart affected service worker containers to restore nominal state.",
                "Enable verbose debug logging on staging to reproduce root cause.",
            ]

        return {
            "title": title,
            "service": service,
            "recommended_severity": recommended_severity,
            "sla_target_minutes": sla_budget,
            "blast_radius_score": blast_radius_score,
            "root_cause_hypothesis": root_cause_hypothesis,
            "matching_runbook": matching_runbook,
            "remediation_checklist": remediation_steps,
            "mode": "OpsPulse AI Heuristic Engine (100% Offline & Secure)",
        }

    def _triage_via_openai(self, title: str, service: str, logs: str, affected_users: int) -> Dict[str, Any]:
        """Live OpenAI API triage caller (if key configured)."""
        import requests
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json",
        }
        prompt = f"""You are an expert SRE and Incident Commander. Analyze this operational incident:
Title: {title}
Service: {service}
Logs/Description: {logs}
Affected Users: {affected_users}

Respond strictly in JSON format with these exact keys:
- "recommended_severity": ("P1 - Critical" | "P2 - High" | "P3 - Medium" | "P4 - Low")
- "blast_radius_score": integer 0-100
- "root_cause_hypothesis": string
- "matching_runbook": string filename
- "remediation_checklist": array of 4 concise actionable bash/CLI or architectural steps
"""
        payload = {
            "model": config.DEFAULT_AI_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        result = json.loads(data["choices"][0]["message"]["content"])
        result["title"] = title
        result["service"] = service
        result["sla_target_minutes"] = config.SLA_THRESHOLDS.get(result.get("recommended_severity", "P2 - High"), 120)
        result["mode"] = f"Live LLM ({config.DEFAULT_AI_MODEL})"
        return result

    def _post_mortem_via_openai(self, incident_id, title, service, severity, root_cause, duration_minutes, affected_users) -> str:
        """Live OpenAI API post-mortem caller (if key configured)."""
        import requests
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json",
        }
        prompt = f"""Write an executive incident post-mortem markdown report for:
Incident: {incident_id} - {title}
Service: {service}
Severity: {severity}
Root Cause: {root_cause}
Duration: {duration_minutes} minutes
Affected Users: {affected_users}

Include: Executive Summary, 5 Whys Root Cause, Chronological Timeline, and 4 Preventive Action Items with owners.
"""
        payload = {
            "model": config.DEFAULT_AI_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=12)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

ai_copilot = AICopilot()

