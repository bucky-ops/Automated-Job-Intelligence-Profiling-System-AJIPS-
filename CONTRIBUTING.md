# Contributing to AJIPS

Thank you for your interest in contributing to the **Automated Job Intelligence Profiling System (AJIPS)**! We welcome contributions from the community.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)
- [Community](#community)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, or virtualenv)

### Setup Development Environment

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/Auto-JIPS.git
cd Auto-JIPS

# 3. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
pip install -e .

# 5. Install pre-commit hooks (recommended)
pre-commit install

# 6. Verify setup
pytest tests/ -v
```

## 🔧 Development Workflow

### 1. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or create a bug fix branch
git checkout -b fix/issue-description
```

**Branch Naming Conventions:**
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions/updates

### 2. Make Changes

- Write clear, maintainable code
- Follow our code style guidelines
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add salary extraction for hourly rates

- Implement regex patterns for hourly salary formats
- Add tests for various hourly rate formats
- Update documentation"
```

**Commit Message Format (Conventional Commits):**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Code style changes (formatting, semicolons, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### 4. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

## 📝 Code Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Use type hints
def extract_salary(text: str) -> Optional[Dict[str, int]]:
    """
    Extract salary information from job posting text.
    
    Args:
        text: Job posting text to analyze
        
    Returns:
        Dictionary with 'min' and 'max' salary values, or None if not found
        
    Example:
        >>> extract_salary("Salary: $50,000 - $100,000")
        {'min': 50000, 'max': 100000}
    """
    # Implementation here
    pass
```

### Code Quality Tools

Before committing, run:

```bash
# Format code
black ajips/ tests/

# Sort imports
isort ajips/ tests/

# Lint code
flake8 ajips/ tests/ --max-line-length=127

# Type checking (if using mypy)
mypy ajips/

# Run tests
pytest tests/ -v --cov=ajips
```

### Pre-commit Hooks

We use pre-commit to ensure code quality:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=127']
```

## 🧪 Testing Guidelines

### Test Structure

```python
# tests/test_feature.py
import pytest
from ajips.app.services.extraction import extract_salary_range


class TestSalaryExtraction:
    """Test suite for salary extraction functionality."""
    
    def test_salary_range_dollar_format(self):
        """Test extraction of salary range in dollar format."""
        text = "We offer a salary of $50,000 to $100,000 per year"
        result = extract_salary_range(text)
        assert result is not None
        assert result["min"] == 50000
        assert result["max"] == 100000
    
    @pytest.mark.parametrize("input_text,expected_min,expected_max", [
        ("$50k-$100k", 50000, 100000),
        ("$75,000", 75000, 75000),
    ])
    def test_salary_parametrized(self, input_text, expected_min, expected_max):
        """Test various salary formats."""
        result = extract_salary_range(input_text)
        assert result["min"] == expected_min
        assert result["max"] == expected_max
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=ajips --cov-report=html

# Run specific test file
pytest tests/test_extraction.py -v

# Run specific test class
pytest tests/test_extraction.py::TestSalaryExtraction -v

# Run specific test method
pytest tests/test_extraction.py::TestSalaryExtraction::test_salary_range -v

# Run with verbose output and show locals on failure
pytest tests/ -v --tb=short --showlocals
```

### Test Coverage

Aim for:
- **Minimum 80%** overall coverage
- **100%** coverage for critical paths
- All edge cases covered

## 📚 Documentation

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int = 0) -> bool:
    """
    Brief description of the function.
    
    Longer description if needed, explaining the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2. Defaults to 0.
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
        TypeError: When param2 is not an integer
        
    Example:
        >>> function_name("test", 5)
        True
    """
```

### README Updates

When adding features:
1. Update the main README.md
2. Add examples if applicable
3. Update API documentation
4. Add to CHANGELOG.md

## 🔍 Pull Request Process

1. **Ensure tests pass**
   ```bash
   pytest tests/ -v --cov=ajips
   ```

2. **Update documentation**
   - README.md
   - Docstrings
   - CHANGELOG.md

3. **Fill out the PR template completely**

4. **Request review**
   - At least one maintainer approval required
   - Address review comments
   - Keep discussions constructive

5. **Merge**
   - Squash and merge for clean history
   - Delete branch after merge

## 📦 Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Tag with semantic version (e.g., `v1.2.0`)
5. CI/CD will deploy automatically

## 👥 Community

### Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Stack Overflow**: Tag questions with `ajips`

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Added to the project's Hall of Fame (for significant contributions)

## 🎯 Priority Areas

We especially welcome contributions in:

1. **Additional job board integrations**
2. **Machine learning model improvements**
3. **Performance optimizations**
4. **Documentation and tutorials**
5. **Bug fixes and testing**
6. **UI/UX enhancements**

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Clear description** of the bug
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Environment details** (OS, Python version, AJIPS version)
6. **Logs or error messages**
7. **Sample input** that triggers the bug

## 💡 Feature Requests

For feature requests:

1. Check existing issues first
2. Describe the use case
3. Explain the benefits
4. Propose implementation (optional)

---

## 📄 License

By contributing to AJIPS, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AJIPS! 🚀**
