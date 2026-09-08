"""Synthetic incident and operations dataset generator."""
import random
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
from src.config import config, DATA_DIR

SERVICES = [
    "API Gateway",
    "Auth & SSO Service",
    "Payment Gateway",
    "Primary PostgreSQL DB",
    "Redis Cache Cluster",
    "Search & Elastic Cluster",
    "Checkout Pipeline",
    "Notification & Email Worker",
]

SEVERITY_LEVELS = ["P1 - Critical", "P2 - High", "P3 - Medium", "P4 - Low"]

TEAMS = ["Platform Infra", "Core Backend", "Security & IAM", "Payment & Billing", "Data Engineering"]

INCIDENT_SCENARIOS = [
    {
        "title": "High replication lag on Postgres primary",
        "service": "Primary PostgreSQL DB",
        "severity": "P1 - Critical",
        "root_cause": "Long-running analytical unindexed query blocked write WAL threads.",
        "resolution": "Terminated blocking PID and adjusted connection pool settings.",
    },
    {
        "title": "504 Gateway Timeout spike across REST endpoints",
        "service": "API Gateway",
        "severity": "P2 - High",
        "root_cause": "Upstream catalog microservice thread pool exhaustion.",
        "resolution": "Scaled Kubernetes replicas from 3 to 10 and enabled fallback caching.",
    },
    {
        "title": "Okta SSO SAML assertion signature mismatch",
        "service": "Auth & SSO Service",
        "severity": "P1 - Critical",
        "root_cause": "JWKS signing certificate auto-rotation failed during midnight cron.",
        "resolution": "Manually triggered JWKS cache refresh and reloaded cert authority.",
    },
    {
        "title": "Stripe webhook 429 rate limit errors",
        "service": "Payment Gateway",
        "severity": "P2 - High",
        "root_cause": "Bulk recurring billing batch triggered webhook concurrency limit.",
        "resolution": "Enabled exponential backoff retry queue in SQS dead-letter worker.",
    },
    {
        "title": "Redis cluster memory usage exceeded 95%",
        "service": "Redis Cache Cluster",
        "severity": "P2 - High",
        "root_cause": "Unbounded user session TTLs on marketing campaign referral links.",
        "resolution": "Enforced maxmemory allkeys-lru eviction policy and trimmed keys.",
    },
    {
        "title": "Elasticsearch cluster yellow status due to unassigned shards",
        "service": "Search & Elastic Cluster",
        "severity": "P3 - Medium",
        "root_cause": "Disk threshold exceeded on node search-03 triggering shard reroute lock.",
        "resolution": "Expanded EBS volume capacity and rebalanced indices.",
    },
    {
        "title": "Email dispatch delay on order confirmation receipts",
        "service": "Notification & Email Worker",
        "severity": "P3 - Medium",
        "root_cause": "SendGrid API rate limiter throttling transactional batches.",
        "resolution": "Switched to multi-pool IP routing and flushed pending queue.",
    },
    {
        "title": "Minor styling asset 404 in admin dashboard",
        "service": "API Gateway",
        "severity": "P4 - Low",
        "root_cause": "CDN cache invalidation hash discrepancy on static frontend build.",
        "resolution": "Purged Cloudflare edge asset cache.",
    },
    {
        "title": "Checkout cart session sync delay during flash sale",
        "service": "Checkout Pipeline",
        "severity": "P1 - Critical",
        "root_cause": "Distributed lock contention on inventory reservation table.",
        "resolution": "Optimized optimistic locking strategy and enabled Redis atomic counters.",
    },
    {
        "title": "Scheduled data warehouse sync job failure",
        "service": "Data Engineering",
        "severity": "P4 - Low",
        "root_cause": "Upstream schema column rename in staging pipeline.",
        "resolution": "Updated dbt model schema mapping.",
    },
]

ENGINEERS = ["Alice M.", "Bob K.", "Carlos R.", "Dana W.", "Evan L.", "Farah H.", "George T."]

def generate_incidents_data(num_records: int = 120, seed: int = 42) -> pd.DataFrame:
    """Generate a realistic dataframe of historical operational incidents and SLA metrics."""
    random.seed(seed)
    base_time = datetime.now() - timedelta(days=30)
    records = []

    for i in range(1, num_records + 1):
        incident_id = f"INC-{1000 + i}"
        scenario = random.choice(INCIDENT_SCENARIOS)
        
        # Pick severity with realistic weighting (more P3/P4 than P1)
        severity = random.choices(
            SEVERITY_LEVELS,
            weights=[0.12, 0.28, 0.40, 0.20],
            k=1
        )[0]
        
        service = scenario["service"] if scenario["service"] in SERVICES else random.choice(SERVICES)
        title = scenario["title"]
        team = random.choice(TEAMS)
        engineer = random.choice(ENGINEERS)
        
        # Incident timing
        created_time = base_time + timedelta(
            days=random.uniform(0, 30),
            hours=random.uniform(0, 23),
            minutes=random.uniform(0, 59)
        )
        
        # Target SLA for this severity
        sla_target = config.SLA_THRESHOLDS.get(severity, 120)
        
        # Determine status: 85% Resolved, 10% In Progress, 5% Open
        status = random.choices(["Resolved", "In Progress", "Open"], weights=[0.85, 0.10, 0.05], k=1)[0]
        
        if status == "Resolved":
            # Real MTTR with occasional SLA breach (15-20% breach chance)
            is_breach = random.random() < 0.18
            if is_breach:
                duration_minutes = int(sla_target * random.uniform(1.15, 2.8))
                sla_status = "Breached"
            else:
                duration_minutes = int(sla_target * random.uniform(0.15, 0.92))
                sla_status = "Compliant"
            resolved_time = created_time + timedelta(minutes=duration_minutes)
        else:
            elapsed_minutes = int((datetime.now() - created_time).total_seconds() / 60)
            duration_minutes = None
            resolved_time = None
            sla_status = "Breached" if elapsed_minutes > sla_target else "Within SLA"

        impact_users = int(random.uniform(10, 5000)) if severity in ["P1 - Critical", "P2 - High"] else int(random.uniform(0, 150))
        
        records.append({
            "incident_id": incident_id,
            "title": title,
            "service": service,
            "severity": severity,
            "team": team,
            "status": status,
            "assigned_engineer": engineer,
            "created_at": created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "resolved_at": resolved_time.strftime("%Y-%m-%d %H:%M:%S") if resolved_time else None,
            "duration_minutes": duration_minutes,
            "sla_target_minutes": sla_target,
            "sla_status": sla_status,
            "affected_users": impact_users,
            "root_cause": scenario["root_cause"],
            "resolution_summary": scenario["resolution"] if status == "Resolved" else "Investigation ongoing.",
        })

    df = pd.DataFrame(records)
    # Sort chronologically by created_at descending
    df["created_at_dt"] = pd.to_datetime(df["created_at"])
    df = df.sort_values(by="created_at_dt", ascending=False).drop(columns=["created_at_dt"])
    return df

def ensure_sample_data_file() -> Path:
    """Ensure data/sample_incidents.csv exists on disk."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = config.SAMPLE_DATA_PATH
    if not file_path.exists():
        df = generate_incidents_data(num_records=120)
        df.to_csv(file_path, index=False)
    return file_path

if __name__ == "__main__":
    path = ensure_sample_data_file()
    print(f"Sample incidents data generated at: {path}")

