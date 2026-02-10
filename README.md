# Automated Job Intelligence Profiling System (AJIPS)

<div align="center">

![AJIPS Banner](https://img.shields.io/badge/AJIPS-v1.1.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.112+-teal?style=for-the-badge&logo=fastapi)
![Production Ready](https://img.shields.io/badge/Production-Ready-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**AI-Powered Job Posting Analysis with Production-Grade Features**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [API](#api-reference) • [What's New](#whats-new-v110) • [Contributing](#contributing)

</div>

---

## 🎯 Overview

AJIPS is an advanced job posting analysis system that uses AI and NLP to extract skills, identify hidden requirements, and provide expert critiques on job descriptions. It helps both job seekers and recruiters understand job requirements more deeply.

### Key Capabilities

- **200+ Skill Detection**: Comprehensive skill database covering programming languages, frameworks, tools, and soft skills
- **Hidden Skill Inference**: Discovers implied skills using role-based templates and skill clustering
- **Requirement Critique**: Identifies contradictions, unrealistic expectations, and missing information
- **Salary Extraction**: Automatically detects and parses salary ranges from job postings
- **Interview Analysis**: Identifies interview stages and estimates process timeline
- **Focus Area Analysis**: Categorizes requirements into technology domains
- **Resume Matching**: Compares your resume against job requirements
- **Quality Scoring**: Grades job postings on clarity and completeness
- **Structured Logging**: JSON logging for production debugging
- **Rate Limiting**: DoS protection with configurable limits

---

## ✨ Features

### 🔍 Intelligent Skill Extraction
- Detects technical skills (languages, frameworks, databases, cloud platforms)
- Identifies soft skills (leadership, communication, teamwork)
- Recognizes multi-word skills and technology stacks
- Categorizes skills by domain (Backend, Frontend, DevOps, Data, etc.)

### 💡 Hidden Skill Inference
- **Direct Mapping**: Infers related skills based on explicit mentions
- **Role-Based Templates**: Applies skill bundles for detected job roles
- **Skill Clustering**: Identifies technology stacks (MERN, AWS, ML, etc.)

### 💰 Salary Intelligence
- **Multi-Format Support**: Parses $50k, 50k-100k, $50,000-$100,000 formats
- **Range Detection**: Identifies min/max compensation
- **Currency Support**: Standardizes salary data

### 📋 Interview Process Analysis
- **Stage Detection**: Identifies phone, technical, system design, behavioral stages
- **Round Estimation**: Estimates total interview rounds
- **Timeline Extraction**: Detects interview process duration

### ⚠️ Comprehensive Critiques
- Experience level contradictions (e.g., "entry-level with 5+ years")
- Technology age vs. experience requirements
- Vague or ambiguous requirements
- Missing salary and location information
- Unrealistic skill combinations
- Buzzword detection

### 📊 Focus Areas
Automatically categorizes requirements into:
- Backend Development
- Frontend Development
- Cloud & Infrastructure
- Data Engineering
- Data Science & ML
- Database Management
- DevOps & CI/CD
- Mobile Development
- Security
- Project Management

### 🔒 Production-Grade Features
- **JSON Structured Logging**: Integration-ready logging for monitoring
- **Rate Limiting**: 30 requests/minute per IP
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Graceful error recovery
- **Health Checks**: `/health` and `/health/detailed` endpoints

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

```bash
# Clone the repository
git clone https://github.com/bucky-ops/Auto-JIPS.git
cd Auto-JIPS/Automated-Job-Intelligence-Profiling-System-AJIPS--main

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn ajips.app.main:app --reload
```

The application will be available at:
- **Web UI**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health
- **Version Info**: http://127.0.0.1:8000/version
- **Health Check**: http://127.0.0.1:8000/health

---

## 📖 Usage

### Web Interface

1. **Navigate to** http://127.0.0.1:8000
2. **Choose input method**:
   - Paste job description text
   - Provide job posting URL
3. **Optional**: Add your resume for matching analysis
4. **Click "Analyze Job Posting"**
5. **Review comprehensive results**:
   - Focus areas with skill breakdown
   - Explicit and hidden skills
   - Requirement critiques
   - Resume match score (if provided)

### API Usage

#### Analyze Job Posting

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_posting": {
      "text": "We are seeking a Senior Backend Engineer with 5+ years of experience in Python, PostgreSQL, and AWS. Must have experience with Docker and Kubernetes."
    },
    "resume_text": "Experienced software engineer with Python, AWS, and Docker expertise..."
  }'
```

#### Response Example

```json
{
  "title": "Backend Engineer",
  "summary": "**Backend Engineer** (Senior Level) | Key skills: python, postgresql, aws, docker, kubernetes",
  "focus_areas": [
    {
      "name": "Backend Development",
      "weight": 0.6,
      "skills": ["python", "postgresql", "api"]
    },
    {
      "name": "Cloud & Infrastructure",
      "weight": 0.4,
      "skills": ["aws", "docker", "kubernetes"]
    }
  ],
  "explicit_skills": ["python", "postgresql", "aws", "docker", "kubernetes"],
  "hidden_skills": ["testing", "pip", "pytest", "iam", "vpc", "s3", "containerization"],
  "critiques": [
    {
      "severity": "info",
      "message": "No salary or compensation information provided."
    }
  ],
  "resume_alignment": 0.75
}
```

---

## 🏗️ Project Structure

```
ajips/
├── app/
│   ├── api/
│   │   ├── routes.py          # API endpoints
│   │   └── schemas.py         # Request/response models
│   ├── services/
│   │   ├── ingestion.py       # URL fetching and parsing
│   │   ├── extraction.py      # Skill extraction (200+ skills)
│   │   ├── enrichment.py      # Hidden skill inference
│   │   ├── critique.py        # Requirement analysis
│   │   ├── profiling.py       # Focus area building
│   │   ├── normalization.py   # Text processing
│   │   └── resume_match.py    # Resume alignment
│   └── main.py                # FastAPI application
├── core/
│   └── pipelines/
│       └── job_profile.py     # Analysis orchestration
├── ui/
│   ├── index.html             # Web interface
│   ├── styles.css             # Premium styling
│   └── app.js                 # Frontend logic
└── tests/                     # Unit and integration tests
```

---

## 🔧 API Reference

### Endpoints

#### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "ok"
}
```

#### `POST /analyze`
Analyze a job posting

**Request Body:**
```json
{
  "job_posting": {
    "url": "string (optional)",
    "text": "string (optional)"
  },
  "resume_text": "string (optional)"
}
```

**Response:** See [Response Example](#response-example) above

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ajips

# Run specific test file
pytest tests/test_extraction.py
```

---

## 🎨 Technology Stack

- **Backend**: FastAPI, Python 3.8+
- **NLP**: spaCy, scikit-learn, NLTK
- **Data Processing**: Pandas, NumPy
- **Web Scraping**: BeautifulSoup, Requests
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API Documentation**: OpenAPI/Swagger

---

## 📊 Skill Database

The system recognizes 200+ skills across categories:
- **Languages**: Python, Java, JavaScript, TypeScript, Go, Rust, etc.
- **Web Frameworks**: React, Angular, Vue, Django, Flask, FastAPI, etc.
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, etc.
- **Cloud**: AWS, Azure, GCP, Heroku, etc.
- **DevOps**: Docker, Kubernetes, Terraform, Ansible, etc.
- **Data Tools**: Spark, Airflow, Kafka, Tableau, etc.
- **Methodologies**: Agile, Scrum, TDD, Microservices, etc.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- NLP powered by [spaCy](https://spacy.io/)
- Inspired by modern job market challenges

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

<div align="center">

**Made with ❤️ for job seekers and recruiters**

</div>
