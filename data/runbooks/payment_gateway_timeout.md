# Payment Gateway Timeout & Webhook Failure Runbook

## Symptoms & Alerts
- Alert: `Stripe_Webhook_Delivery_Failures` (> 10 failures in 5m)
- Alert: `Checkout_Transaction_Failure_Rate` (> 3%)
- Customer Impact: Customers cannot complete purchases, orders stuck in "Pending Payment".

## Immediate Triage & Diagnostics
1. **Check Third-Party Payment Processor**:
   - Inspect Stripe / Adyen / PayPal external status API.
2. **Inspect Webhook Processing Queue**:
   - Check SQS / RabbitMQ dead-letter queues (`dlq-payment-webhooks`).
3. **Verify API Credentials & Merchant Keys**:
   - Ensure webhook secret signing keys have not been altered or revoked.

## Mitigation & Remediation Procedures
1. **Enable Redundant Payment Provider Fallback**:
   - Switch active merchant routing to secondary gateway provider (e.g., Stripe -> Adyen) in payment config.
2. **Replay Dead-Letter Queue (DLQ)**:
   - Run DLQ replay script to reprocess stranded transaction notifications: `python scripts/replay_dlq.py --queue payment-events`.
3. **Increase Gateway Client Timeout**:
   - Dynamically bump HTTP timeout from 5000ms to 12000ms in payment worker configs.
4. **Notify Customer Support Lead**:
   - Post update in `#ops-incidents` and update external status page.

