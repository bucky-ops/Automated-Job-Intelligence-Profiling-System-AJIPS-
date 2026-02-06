# Automated Job Intelligence Profiling System (AJIPS)

AJIPS is a starter implementation for analyzing job postings and generating structured profiles with focus areas, inferred skills, and requirement critiques.

## Features
- Accepts job posting URLs or pasted descriptions.
- Extracts explicit skills and infers hidden skills.
- Produces a structured report with focus areas and critiques.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn ajips.app.main:app --reload
```

Then call the API:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"job_posting": {"text": "We need a backend engineer with Python, PostgreSQL, and AWS."}}'
```

## Project Structure
```
ajips/
  app/
    api/           # FastAPI routes + schemas
    services/      # Ingestion, normalization, extraction, enrichment
    data/          # Taxonomies and benchmarks (placeholders)
  core/            # Models, embeddings, pipelines
  scripts/         # Dataset ingestion helpers
  tests/           # Unit/integration tests
  ui/              # Frontend placeholders
```

## Status
This repository contains a functional API scaffold with lightweight heuristics. Replace service logic with production NLP pipelines as needed.
