# Contributing to AJIPS

Thank you for your interest in contributing to the Automated Job Intelligence Profiling System!

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
4. **Make your changes** and commit them (`git commit -m 'Add amazing feature'`)
5. **Push to your fork** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

## Development Setup

```bash
# Clone the repository
git clone https://github.com/bucky-ops/Auto-JIPS.git
cd Auto-JIPS/Automated-Job-Intelligence-Profiling-System-AJIPS--main

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies with dev tools
pip install -r requirements.txt
pip install -e .

# Run tests
pytest tests/ -v --cov=ajips

# Start development server
uvicorn ajips.app.main:app --reload
```

## Code Style

- Follow PEP 8
- Use type hints for all functions
- Add docstrings to all modules and functions
- Run `black` for formatting (if available)

## Testing

All new features must include tests:

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_comprehensive.py::TestSalaryExtraction -v

# Run with coverage
pytest tests/ --cov=ajips --cov-report=html
```

## Pull Request Process

1. Update README.md with any new features
2. Add tests for new functionality
3. Ensure all tests pass locally
4. Update documentation
5. Submit PR with clear description

## Issues

Found a bug? Please [open an issue](https://github.com/bucky-ops/Auto-JIPS/issues) with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details

## Feature Requests

Have an idea? [Open a discussion](https://github.com/bucky-ops/Auto-JIPS/discussions) describing:
- The use case
- Expected benefits
- Proposed implementation (optional)

## Questions?

Feel free to open a GitHub discussion or issue with the label `question`.

---

**Happy Contributing! 🎉**
