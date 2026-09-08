# Database Failover & Replication Lag Runbook

## Symptoms & Alerts
- Alert: `DB_Replica_Lag_High` (> 120 seconds)
- Alert: `DB_Primary_Unhealthy` or Connection Timeout > 5000ms
- Customer Impact: Read/write latency degradation, 500 Internal Server Errors on checkout & profile updates.

## Immediate Triage & Diagnostics
1. **Check Primary DB Health**:
   - Run `SELECT * FROM pg_stat_activity WHERE state != 'idle';`
   - Inspect active long-running queries (> 30s) or locked transactions (`pg_locks`).
2. **Examine Replication Status**:
   - Run `SELECT client_addr, state, sync_state, replay_lag FROM pg_stat_replication;`
3. **Inspect Disk & CPU Spikes**:
   - Verify IOPS exhaustion on Aurora/RDS instance.

## Mitigation & Remediation Procedures
1. **Kill Blocking Queries**:
   - Identify PID of blocking query and execute `SELECT pg_terminate_backend(<PID>);`
2. **Promote Read Replica (Failover)**:
   - If Primary CPU is locked at 100% or storage corruption is suspected, initiate automated failover via AWS CLI / Cloud Console:
     `aws rds reboot-db-instance --db-instance-identifier prod-db-primary --force-failover`
3. **Scale Read Capacity**:
   - Temporarily route analytical/read-heavy endpoints to secondary read-replicas.
4. **Post-Recovery Verification**:
   - Confirm connection pool stabilization in PgBouncer.
   - Monitor error rate drop below 0.01% in Datadog/Grafana.

