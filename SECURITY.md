# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Here are the versions currently supported:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :x:                |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability within AJIPS, please report it to us as soon as possible.

### How to Report

**Please do NOT create a public GitHub issue for security vulnerabilities.**

Instead, please report security vulnerabilities via:

1. **Email**: Send an email to [security@example.com] with:
   - Description of the vulnerability
   - Steps to reproduce (if applicable)
   - Potential impact
   - Suggested fix (if any)

2. **GitHub Security Advisories**: Use [GitHub's private vulnerability reporting](https://github.com/bucky-ops/Auto-JIPS/security/advisories/new)

### What to Expect

- **Acknowledgment**: We'll acknowledge receipt within 48 hours
- **Investigation**: We'll investigate and validate the vulnerability
- **Updates**: We'll provide updates on our progress every 72 hours
- **Resolution**: We'll work on a fix and coordinate disclosure

### Disclosure Policy

- We'll work with you to understand and resolve the issue
- We'll credit you in the security advisory (unless you prefer anonymity)
- We'll disclose the vulnerability after a fix is released
- Typical timeline: 90 days from report to public disclosure

## Security Measures

AJIPS implements several security measures:

### SSRF Protection

- URL validation before fetching
- Blocklist for private IP ranges
- Domain allowlist for job boards
- Timeout on all external requests

### Rate Limiting

- 30 requests per minute per IP
- Configurable limits
- Rate limit headers in responses

### Input Validation

- Comprehensive request validation using Pydantic
- Content length limits
- Sanitization of user inputs

### CORS Protection

- Configurable CORS origins
- Default restricted to localhost
- Environment-based configuration

### Logging

- Structured JSON logging
- No sensitive data in logs
- Audit trail for API calls

## Security Best Practices for Deployment

### Production Checklist

- [ ] Use HTTPS only
- [ ] Set strong, random secrets
- [ ] Configure CORS origins explicitly
- [ ] Enable rate limiting
- [ ] Set up monitoring and alerting
- [ ] Regular security updates
- [ ] Use Docker non-root user
- [ ] Network segmentation

### Environment Variables

Never commit these to version control:

```bash
# Secrets
SECRET_KEY=your-secret-key-here
API_KEY=your-api-key

# Database
DATABASE_URL=postgresql://user:pass@host/db

# External Services
SENTRY_DSN=https://...
```

### Docker Security

```dockerfile
# Use specific version, not 'latest'
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 ajips
USER ajips

# Don't run as root
CMD ["uvicorn", "ajips.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Security Contacts

- **Security Team**: security@example.com
- **Project Maintainers**: See [MAINTAINERS.md](MAINTAINERS.md)

## Acknowledgments

We thank the following security researchers for their contributions:

- [Your Name] - [Description of contribution]

---

**Version**: 1.1.0  
**Last Updated**: February 10, 2026
