# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
