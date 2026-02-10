# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Production-ready GitHub templates (ISSUE_TEMPLATE, PR_TEMPLATE)
- Comprehensive CONTRIBUTING.md with development guidelines
- CODE_OF_CONDUCT.md for community standards
- Enhanced CI/CD workflows
- Pre-commit hooks configuration
- Security documentation (SECURITY.md)

### Changed
- Enhanced salary extraction to properly handle 'k' format (50k -> 50000)
- Expanded interview stage detection keywords
- Fixed education requirements regex to include plural forms
- Updated CORS origins test to match actual configuration

### Fixed
- Salary extraction for 'k' format returning incorrect values
- Interview stages extraction missing short keywords (phone, code, design, culture)
- CORS origins test assertion mismatch
- Education requirements not detecting 'certifications' plural form

## [1.1.0] - 2026-02-10

### Added
- **JSON Structured Logging**: Production-ready logging with `pythonjsonlogger`
- **Rate Limiting**: DoS protection with slowapi (30 req/min per IP)
- **Salary Range Extraction**: Parses multiple salary formats ($50k, 50k-100k, $50,000-$100,000)
- **Interview Stage Detection**: Identifies phone, technical, system_design, behavioral stages
- **Comprehensive Test Suite**: 12+ test cases for new features
- **Constants Configuration**: Centralized configuration management
- **Enhanced Documentation**: Contributing guide, changelog, security policy

### Changed
- Updated README with new features
- Enhanced requirements.txt with production dependencies
- Improved API documentation with examples

### Dependencies Added
- `python-json-logger==2.0.7`
- `slowapi==0.1.9`
- `cachetools==5.3.2`
- `responses==0.24.1`

## [1.0.0] - 2026-01-15

### Initial Release
- Core skill extraction (200+ skills)
- Hidden skill inference
- Requirement critique engine
- Focus area analysis
- Job profile pipeline
- Resume matching
- Premium web UI
- FastAPI backend
- Comprehensive test suite

---

## Release Notes Template

When creating a new release, use this template:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security-related changes
```

---

## Semantic Versioning Guide

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.Y.0): Added functionality (backwards-compatible)
- **PATCH** version (0.0.Z): Backwards-compatible bug fixes

---

For the complete list of commits, see the [commit history](https://github.com/bucky-ops/Auto-JIPS/commits/main).
