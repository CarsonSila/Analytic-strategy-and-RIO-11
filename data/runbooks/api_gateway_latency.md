# API Gateway High Latency & 504 Gateway Timeout Runbook

## Symptoms & Alerts
- Alert: `APIGateway_p99_Latency_Exceeded` (> 800ms for 3 consecutive minutes)
- Alert: `504_Gateway_Timeout_Spike` (> 2% total HTTP requests)
- Customer Impact: Slow page renders, mobile app request timeouts, increased retry loops.

## Immediate Triage & Diagnostics
1. **Identify Upstream Service**:
   - Inspect Datadog APM Service Map or AWS CloudWatch API Gateway metrics.
   - Correlate latency spikes with specific upstream backend microservices (e.g., `user-service`, `catalog-service`).
2. **Examine Rate Limiting & Throttling**:
   - Verify if WAF or token-bucket rate limits are rejecting valid user traffic.
3. **Inspect Thread Pool & Connection Exhaustion**:
   - Check if downstream microservice connection pools are saturated.

## Mitigation & Remediation Procedures
1. **Enable Circuit Breaking & Fallbacks**:
   - Trigger circuit breaker to return cached responses for non-critical GET endpoints.
2. **Auto-Scale Backend Workloads**:
   - Scale Kubernetes deployment pods: `kubectl scale deployment/catalog-service --replicas=12 -n production`.
3. **Flush Invalidation Cache**:
   - Invalidate edge Redis cache layer if cache stampede or cold cache is detected.
4. **Traffic Shedding**:
   - Apply rate limit throttling to non-essential bot or batch API traffic.

