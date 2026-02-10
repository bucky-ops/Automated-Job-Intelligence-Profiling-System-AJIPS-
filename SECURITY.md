# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in AJIPS, please **do not open a public issue**. Instead, email the maintainers directly with:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

We will acknowledge your report within 48 hours and work on a fix.

## Security Best Practices

### For Developers
- Always use the latest version
- Keep dependencies up to date: `pip install --upgrade -r requirements.txt`
- Use environment variables for sensitive data (API keys, credentials)
- Never commit secrets to the repository
- Use type hints to catch potential issues

### For Deployments
- Run AJIPS behind a reverse proxy (nginx, Apache)
- Enable rate limiting (configured by default)
- Use HTTPS/TLS for all connections
- Validate and sanitize all inputs
- Monitor logs for suspicious activity
- Keep Python and dependencies updated

### Configuration
```bash
# Environment variables
export AJIPS_ALLOWED_ORIGINS="https://yourdomain.com"
export LOGLEVEL="INFO"
export RATE_LIMIT="30/minute"
```

## Supported Versions

| Version | Status | Security Support |
|---------|--------|------------------|
| 1.1.x | Active | Yes |
| 1.0.x | Maintenance | Limited |
| < 1.0 | Deprecated | No |

## Known Security Considerations

- Input validation is performed on all job posting text
- Logs do not contain sensitive user data
- Rate limiting protects against DoS attacks
- CORS is configurable for security

## Security Updates

Security patches are released as soon as they're available. We recommend:
- Enabling automatic updates where possible
- Subscribing to security notifications
- Reviewing the CHANGELOG regularly

---

**Version**: 1.1.0  
**Last Updated**: February 10, 2026
