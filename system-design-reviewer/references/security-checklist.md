# Security Checklist

Quick security review checklist for system designs.

## Authentication & Authorization

- ✓ **Strong Authentication**: JWT, OAuth 2.0, or similar
- ✓ **Password Security**: bcrypt/argon2 hashing (never store plain text)
- ✓ **Session Management**: Secure tokens, proper expiration
- ✓ **RBAC/ABAC**: Role or attribute-based access control
- ✓ **MFA**: Multi-factor authentication for sensitive operations
- ✓ **API Keys**: Secure generation, rotation, and storage

## Data Protection

- ✓ **Encryption at Rest**: Encrypt sensitive data in databases and storage
- ✓ **Encryption in Transit**: TLS 1.2+ for all communications
- ✓ **Data Masking**: Mask sensitive data in logs and error messages
- ✓ **PII Compliance**: GDPR/CCPA compliance for personal data
- ✓ **Secret Management**: Use vault/secret manager, never hardcode
- ✓ **Data Retention**: Automated cleanup of old sensitive data

## Vulnerability Prevention (OWASP Top 10)

- ✓ **SQL Injection**: Use parameterized queries/ORMs
- ✓ **XSS**: Input sanitization, output encoding, CSP headers
- ✓ **CSRF**: CSRF tokens for state-changing operations
- ✓ **Authentication Bypass**: Proper session validation
- ✓ **Security Misconfiguration**: Secure defaults, minimal permissions
- ✓ **Sensitive Data Exposure**: Encrypt, don't expose in URLs/logs
- ✓ **Broken Access Control**: Verify authorization on every request
- ✓ **Dependency Vulnerabilities**: Regular security scanning (Snyk, Dependabot)

## Security Headers

```http
Content-Security-Policy: default-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000
X-XSS-Protection: 1; mode=block
```

## Rate Limiting

- **Authentication**: 5-10 attempts/minute per IP
- **API Endpoints**: 100-1000 requests/minute per user
- **Password Reset**: 3 requests/hour per email

## Secrets Scanning

Never commit these patterns:
- API keys: `api_key=`, `apiKey:`, `API_KEY=`
- Passwords: `password=`, `passwd=`, `pwd=`
- Tokens: `token=`, `auth_token=`, `bearer`
- Private keys: `BEGIN PRIVATE KEY`, `BEGIN RSA PRIVATE KEY`
