# Contributing to ScraperSage

Thank you for your interest in contributing to ScraperSage! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up development environment** (see [Development Setup](#development-setup))
4. **Create a feature branch** for your changes
5. **Make your changes** following our guidelines
6. **Test your changes** thoroughly
7. **Submit a pull request**

## 📋 Table of Contents

- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Code Review Process](#code-review-process)
- [Release Process](#release-process)
- [Community Guidelines](#community-guidelines)

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Text editor or IDE (VS Code recommended)

### Environment Setup

1. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ScraperSage.git
   cd ScraperSage
   ```

2. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/akillabs/ScraperSage.git
   ```

3. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install development dependencies:**
   ```bash
   pip install -e .
   pip install -r requirements.txt
   
   # Install development tools
   pip install pytest black flake8 mypy pre-commit
   
   # Install Playwright browsers
   playwright install chromium
   ```

5. **Set up environment variables:**
   ```bash
   # Create .env file (never commit this!)
   echo "SERPER_API_KEY=your_test_key_here" > .env
   echo "GEMINI_API_KEY=your_test_key_here" >> .env
   ```

6. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

### Verification

Test your setup:
```bash
# Run basic import test
python -c "from ScraperSage import scrape_and_summarize; print('✅ Setup successful')"

# Run code quality checks
black --check ScraperSage/
flake8 ScraperSage/
mypy ScraperSage/
```

## 📏 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specific guidelines:

#### Formatting
- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings, single quotes for internal
- **Imports**: Organized using isort

#### Code Organization
```python
# Standard library imports
import os
import json
from typing import List, Dict, Optional

# Third-party imports
import requests
from playwright.sync_api import sync_playwright

# Local imports  
from .utils import helper_function
```

#### Documentation
- **Docstrings**: Google style for all public functions/classes
- **Type hints**: Required for all function signatures
- **Comments**: Explain why, not what

#### Example Function
```python
def search_web(
    query: str, 
    max_results: int = 5,
    engines: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Search the web using multiple search engines.
    
    Args:
        query: The search query string
        max_results: Maximum number of results per engine
        engines: List of search engines to use. Defaults to all available.
        
    Returns:
        Dict containing search results and metadata
        
    Raises:
        ValueError: If query is empty or invalid
        ConnectionError: If all search engines fail
        
    Example:
        >>> results = search_web("python tutorial", max_results=3)
        >>> print(f"Found {len(results['urls'])} results")
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")
    
    # Implementation here
    return {"urls": [], "metadata": {}}
```

### Code Quality Tools

We use these tools to maintain code quality:

```bash
# Code formatting
black ScraperSage/ tests/ examples/

# Import sorting
isort ScraperSage/ tests/ examples/

# Linting
flake8 ScraperSage/ tests/ examples/

# Type checking
mypy ScraperSage/

# Security scanning
bandit -r ScraperSage/
```

### Naming Conventions

- **Classes**: PascalCase (`ScrapeSummarize`)
- **Functions/Variables**: snake_case (`search_results`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`)
- **Private methods**: Leading underscore (`_internal_method`)
- **Files/Modules**: snake_case (`scraper_sage.py`)

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration
├── test_scraper_sage.py     # Main functionality tests
├── test_search.py           # Search engine tests
├── test_summarization.py    # AI summarization tests
├── test_integration.py      # End-to-end tests
└── fixtures/               # Test data
    ├── sample_html.html
    └── mock_responses.json
```

### Writing Tests

Use pytest with these patterns:

```python
import pytest
from unittest.mock import patch, MagicMock
from ScraperSage import scrape_and_summarize

class TestScrapeSummarize:
    """Test cases for scrape_and_summarize class."""
    
    @pytest.fixture
    def scraper(self):
        """Create a scraper instance for testing."""
        return scrape_and_summarize(
            serper_api_key="test_key",
            gemini_api_key="test_key"
        )
    
    def test_initialization_success(self, scraper):
        """Test successful initialization with API keys."""
        assert scraper.serper_api_key == "test_key"
        assert scraper.gemini_api_key == "test_key"
    
    def test_initialization_missing_keys(self):
        """Test initialization fails without API keys."""
        with pytest.raises(ValueError, match="Missing required API keys"):
            scrape_and_summarize()
    
    @patch('ScraperSage.scraper_sage.requests.post')
    def test_search_google_success(self, mock_post, scraper):
        """Test successful Google search."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "organic": [{"link": "https://example.com"}]
        }
        mock_post.return_value = mock_response
        
        results = scraper._search_google("test query")
        assert len(results) > 0
        assert "https://example.com" in results
    
    @pytest.mark.integration
    def test_full_workflow(self, scraper):
        """Integration test for complete workflow."""
        # This test requires real API keys
        if not all([scraper.serper_api_key, scraper.gemini_api_key]):
            pytest.skip("API keys not available for integration test")
        
        result = scraper.run({
            "query": "test query",
            "max_results": 1,
            "max_urls": 1
        })
        
        assert result["status"] == "success"
        assert "overall_summary" in result
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ScraperSage --cov-report=html

# Run specific test file
pytest tests/test_scraper_sage.py

# Run tests with specific marker
pytest -m integration

# Run tests in parallel
pytest -n auto

# Verbose output
pytest -v
```

### Test Categories

- **Unit tests**: Test individual functions/methods
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete workflows
- **Performance tests**: Test speed and memory usage
- **Mock tests**: Test with external service mocks

### Coverage Requirements

- Minimum 80% code coverage for new code
- All public functions must have tests
- Edge cases and error conditions must be tested

## 🔄 Pull Request Process

### Before Submitting

1. **Update your branch:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run quality checks:**
   ```bash
   black ScraperSage/ tests/
   flake8 ScraperSage/ tests/
   mypy ScraperSage/
   pytest --cov=ScraperSage
   ```

3. **Test your changes:**
   ```bash
   # Run existing tests
   pytest
   
   # Manual testing
   python examples/test_changes.py
   ```

### Pull Request Template

Use this template for your PR description:

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issues
Fixes #(issue number)
Relates to #(issue number)

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Code coverage maintained/improved

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Screenshots/Examples
If applicable, add screenshots or code examples.

## Additional Notes
Any additional information or context about the changes.
```

### Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by at least one maintainer
3. **Testing** in staging environment (for major changes)
4. **Documentation** updates reviewed
5. **Final approval** and merge

## 🐛 Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Initialize scraper with...
2. Call method with parameters...
3. See error

**Expected Behavior**
A clear description of what you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. Windows 10, macOS 12, Ubuntu 20.04]
- Python Version: [e.g. 3.9.5]
- ScraperSage Version: [e.g. 1.0.0]
- Dependencies: [relevant package versions]

**Error Messages**
```
Paste any error messages or stack traces here
```

**Additional Context**
Add any other context about the problem here.
```

### Feature Requests

Use the feature request template:

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Use Cases**
Specific use cases where this feature would be helpful.

**Implementation Ideas**
If you have ideas about how to implement this feature.

**Additional Context**
Any other context or screenshots about the feature request.
```

## 👥 Code Review Process

### For Reviewers

#### Review Checklist

- [ ] **Functionality**: Does the code work as intended?
- [ ] **Style**: Follows coding standards and conventions?
- [ ] **Performance**: No obvious performance issues?
- [ ] **Security**: No security vulnerabilities introduced?
- [ ] **Testing**: Adequate test coverage?
- [ ] **Documentation**: Code is well-documented?
- [ ] **Compatibility**: Works with supported Python versions?

#### Review Comments

Use constructive feedback:

```markdown
# Good examples

## Suggestion
Consider using a context manager here for better resource management:
```python
with open(file_path, 'r') as f:
    content = f.read()
```

## Question  
Why did you choose this approach over using the built-in `requests` retry functionality?

## Nitpick
Minor style issue - consider using f-strings for better readability:
```python
message = f"Found {count} results"  # instead of "Found {} results".format(count)
```

## Praise
Nice use of type hints and comprehensive docstring! 👍
```

### For Contributors

#### Responding to Reviews

- Address all feedback promptly
- Ask for clarification if feedback is unclear
- Explain your reasoning for implementation choices
- Be open to suggestions and changes
- Update the PR description if scope changes

## 🚢 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (1.1.0): New features (backwards compatible)
- **PATCH** (1.0.1): Bug fixes (backwards compatible)

### Release Checklist

1. **Version bump** in `setup.py` and `__init__.py`
2. **Update changelog** with new features/fixes
3. **Run full test suite** on all supported Python versions
4. **Update documentation** if needed
5. **Create release branch** from main
6. **Tag release** with version number
7. **Build and upload** to PyPI
8. **Create GitHub release** with release notes

### Pre-release Testing

Major releases require testing on:
- Multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
- Different operating systems (Windows, macOS, Linux)
- Various dependency versions

## 🌟 Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

### Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community discussions
- **Pull Request Comments**: Code-specific discussions
- **Email**: security@akillabs.com (for security issues only)

### Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes and changelog
- README acknowledgments (for significant contributions)
- Hall of fame (for long-term contributors)

## 🏆 Contributor Recognition

### Types of Contributions

We value all types of contributions:

- **Code**: Bug fixes, features, performance improvements
- **Documentation**: README, guides, API docs, examples
- **Testing**: Writing tests, manual testing, bug reports
- **Design**: UI/UX improvements, graphics, branding
- **Community**: Answering questions, mentoring, organizing

### Contribution Levels

- **First-time contributor**: Made their first contribution
- **Regular contributor**: Multiple valuable contributions
- **Core contributor**: Significant ongoing contributions
- **Maintainer**: Trusted with repository access and decisions

## 📚 Resources

### Learning Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Git Workflow Guide](https://www.atlassian.com/git/tutorials/comparing-workflows)

### Tools and Extensions

Recommended VS Code extensions:
- Python
- Pylance
- Black Formatter
- GitLens
- Python Test Explorer

### Getting Help

- **Documentation**: Read existing docs first
- **Search**: Check existing issues/discussions
- **Ask**: Create an issue or discussion
- **Connect**: Reach out to maintainers

---

**Thank you for contributing to ScraperSage! 🎉**

Your contributions help make this project better for everyone in the community.