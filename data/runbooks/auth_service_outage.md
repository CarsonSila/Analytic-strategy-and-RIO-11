# Authentication & SSO Service Outage Runbook

## Symptoms & Alerts
- Alert: `Auth_Service_5xx_ErrorRate` (> 5%)
- Alert: `JWT_Validation_Failure_Spike`
- Customer Impact: Users logged out, unable to log in, enterprise SSO SAML/OIDC auth failing.

## Immediate Triage & Diagnostics
1. **Check Identity Provider (IdP) Status**:
   - Verify Okta, Auth0, or Azure AD status pages and webhook endpoints.
2. **Inspect Certificate Expiration & JWKS endpoint**:
   - Check if public signing key rotation failed or certificate expired.
3. **Inspect Redis Auth Session Cache**:
   - Check memory consumption and connection counts in Redis session clusters.

## Mitigation & Remediation Procedures
1. **Rotate/Refresh JWKS Cache**:
   - Trigger manual JWKS sync: `curl -X POST https://auth-internal.prod.local/admin/refresh-jwks`.
2. **Restart Unhealthy Auth Pods**:
   - `kubectl rollout restart deployment/auth-service -n production`.
3. **Failover to Secondary IdP Connection**:
   - Toggle backup SAML endpoint configuration in Feature Flags.
4. **Session Extension Grace Period**:
   - Temporarily increase JWT expiry grace window by 15 minutes during active recovery.

