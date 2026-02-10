# Getting Started with AJIPS

## 🎯 Quick Start (5 minutes)

### 1. Installation

```bash
# Clone repository
git clone https://github.com/bucky-ops/Auto-JIPS.git
cd Auto-JIPS/Automated-Job-Intelligence-Profiling-System-AJIPS--main

# Setup environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run server
uvicorn ajips.app.main:app --reload
```

Access the UI at: **http://localhost:8000**

### 2. API Usage

#### Analyze a Job Posting

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_posting": {
      "text": "Senior Python Developer with 5+ years experience. Required: Python, Django, PostgreSQL, AWS, Docker."
    }
  }'
```

#### Response Example

```json
{
  "title": "Senior Python Developer",
  "explicit_skills": ["Python", "Django", "PostgreSQL", "AWS", "Docker"],
  "hidden_skills": ["REST APIs", "CI/CD", "Microservices"],
  "salary_range": null,
  "interview_stages": [],
  "quality_score": 0.75,
  "focus_areas": [
    {
      "name": "Backend Development",
      "weight": 0.85,
      "skills": ["Python", "Django", "PostgreSQL"]
    }
  ],
  "critiques": [
    {
      "severity": "info",
      "message": "Consider specifying salary range to attract more qualified candidates."
    }
  ],
  "resume_alignment": null,
  "summary": "Senior Python Developer | Requires extensive backend expertise"
}
```

### 3. Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI |
| `/docs` | GET | API Documentation (Swagger) |
| `/health` | GET | Health check |
| `/health/detailed` | GET | Detailed health status |
| `/version` | GET | Version information |
| `/analyze` | POST | Analyze job posting |

### 4. Advanced Features

#### Extract Salary Range

```json
{
  "job_posting": {
    "text": "We offer $80,000 to $120,000 per year for this role"
  }
}
```

Response includes:
```json
{
  "salary_range": {
    "min": 80000,
    "max": 120000,
    "currency": "USD"
  }
}
```

#### Detect Interview Process

```json
{
  "job_posting": {
    "text": "Interview process: phone screen, technical interview, system design, final behavioral round"
  }
}
```

Response includes:
```json
{
  "interview_stages": ["phone", "technical", "system_design", "behavioral"],
  "estimated_rounds": 4
}
```

#### Match Against Resume

```json
{
  "job_posting": {
    "text": "Python, Django, AWS required"
  },
  "resume_text": "5 years Python experience, Django expert, AWS certified"
}
```

Response includes:
```json
{
  "resume_alignment": 0.92
}
```

---

## 📊 Understanding the Output

### Explicit Skills
Skills that are directly mentioned in the job posting.

### Hidden Skills
Skills inferred from explicitly mentioned technologies:
- React → JavaScript, HTML, CSS, TypeScript
- Docker → Linux, DevOps, Containerization
- AWS → Cloud, DevOps, Networking

### Quality Score (0-1)
- **0.0-0.3**: Poor (vague, incomplete)
- **0.3-0.6**: Fair (basic information)
- **0.6-0.8**: Good (clear requirements)
- **0.8-1.0**: Excellent (comprehensive, specific)

### Critiques
Potential issues with the job posting:
- **INFO**: Suggestions for improvement
- **WARNING**: Potential concerns
- **CRITICAL**: Impossible requirements

---

## 🔧 Configuration

### Environment Variables

```bash
# CORS origins (comma-separated)
export AJIPS_ALLOWED_ORIGINS="http://localhost:3000,https://myapp.com"

# Logging level
export LOGLEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Rate limiting
export RATE_LIMIT="30/minute"
```

### Rate Limiting

Default: **30 requests per minute per IP**

To modify, edit `ajips/app/main.py`:
```python
@limiter.limit("50/minute")  # Change this value
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_comprehensive.py::TestSalaryExtraction -v

# Run with coverage
pytest tests/ --cov=ajips
```

---

## 📚 Documentation

- [API Reference](#api-reference)
- [Architecture](./ARCHITECTURE.md)
- [Contributing](./CONTRIBUTING.md)
- [Changelog](./CHANGELOG.md)
- [Security](./SECURITY.md)

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Use different port
uvicorn ajips.app.main:app --port 8001
```

### Import Errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Tests Failing
```bash
# Install test dependencies
pip install pytest pytest-cov responses

# Run tests with verbose output
pytest tests/ -vv
```

---

## 🚀 Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Analyze job postings**: Use the web UI or API
3. **Read the docs**: Check [CONTRIBUTING.md](./CONTRIBUTING.md)
4. **Deploy**: See [Deployment Guide](#deployment)

---

**Need help?** Open an issue on GitHub!
