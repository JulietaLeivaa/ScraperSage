# Development Guide

This document provides comprehensive technical documentation for ScraperSage development, architecture, and deployment.

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ScraperSage                            │
├─────────────────────────────────────────────────────────────┤
│  Public API Layer                                           │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ scrape_and_     │  │ Configuration   │                  │
│  │ summarize.run() │  │ Management      │                  │
│  └─────────────────┘  └─────────────────┘                  │
├─────────────────────────────────────────────────────────────┤
│  Core Services Layer                                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Search      │ │ Web Scraper │ │ AI          │           │
│  │ Orchestrator│ │ Engine      │ │ Summarizer  │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
├─────────────────────────────────────────────────────────────┤
│  Data Access Layer                                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Google      │ │ DuckDuckGo  │ │ Playwright  │           │
│  │ Search API  │ │ Search API  │ │ Browser     │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
├─────────────────────────────────────────────────────────────┤
│  External Services                                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Serper API  │ │ DDGS API    │ │ Gemini AI   │           │
│  │ (Google)    │ │ (Anonymous) │ │ API         │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Query → Search Engines → URL Collection → Content Scraping → AI Summarization → JSON Output
     ↓              ↓               ↓                ↓                    ↓              ↓
   Input         Google +        Unique URL      Playwright          Gemini AI     Structured
Validation    DuckDuckGo        Deduplication    Scraping           Processing      Response
                API Calls                        (Parallel)                        + File Save
```

## 🔧 Core Components

### 1. Main Class: `scrape_and_summarize`

#### Class Structure
```python
class scrape_and_summarize:
    """Main orchestrator class for web scraping and summarization."""
    
    def __init__(self, serper_api_key: str = None, gemini_api_key: str = None):
        """Initialize with API credentials and configure services."""
        
    def run(self, params: dict) -> dict:
        """Main execution method - orchestrates the entire pipeline."""
        
    # Private methods
    def _search_google(self, query: str, max_results: int) -> List[str]:
    def _search_duckduckgo(self, query: str, max_results: int) -> List[str]:
    def _scrape_url(self, url: str) -> dict:
    def _summarize_content(self, content: str) -> str:
    def _generate_overall_summary(self, summaries: List[str]) -> str:
```

#### Initialization Process
1. **API Key Validation**: Check for required environment variables or parameters
2. **Service Configuration**: Initialize Gemini AI client with API key
3. **Default Settings**: Set up retry mechanisms, timeouts, and limits
4. **Error Handler Setup**: Configure logging and exception handling

#### Main Execution Flow (`run` method)
```python
def run(self, params: dict) -> dict:
    # 1. Input validation and parameter extraction
    # 2. Parallel search execution (Google + DuckDuckGo)
    # 3. URL deduplication and filtering
    # 4. Concurrent web scraping with Playwright
    # 5. Content processing and individual summarization
    # 6. Overall summary generation
    # 7. Result compilation and optional file saving
    # 8. Error handling and graceful degradation
```

### 2. Search Integration

#### Google Search (Serper API)
```python
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def _search_google(self, query: str, max_results: int = 5) -> List[str]:
    """
    Search Google using Serper API with retry mechanism.
    
    Features:
    - Exponential backoff retry
    - Rate limiting protection
    - Error handling for API failures
    - Result filtering and validation
    """
```

**API Integration Details:**
- **Endpoint**: `https://google.serper.dev/search`
- **Authentication**: X-API-KEY header
- **Rate Limit**: Depends on plan (2,500 free searches)
- **Response Format**: JSON with organic results
- **Error Handling**: Network timeouts, API quotas, invalid responses

#### DuckDuckGo Search (DDGS)
```python
def _search_duckduckgo(self, query: str, max_results: int = 5) -> List[str]:
    """
    Search DuckDuckGo using ddgs library.
    
    Features:
    - Anonymous searching (no API key required)
    - Built-in rate limiting
    - Automatic retry on failures
    - Clean URL extraction
    """
```

**Implementation Details:**
- **Library**: `duckduckgo-search` (ddgs)
- **No Authentication**: Anonymous requests
- **Rate Limiting**: Built-in protection
- **Safesearch**: Moderate filtering enabled
- **Region**: Global results (configurable)

### 3. Web Scraping Engine

#### Playwright Integration
```python
def _scrape_url(self, url: str) -> dict:
    """
    Scrape URL content using Playwright browser automation.
    
    Features:
    - JavaScript execution support
    - Mobile and desktop user agents
    - Content sanitization
    - Timeout handling
    - Memory-efficient processing
    """
```

**Browser Configuration:**
```python
browser_config = {
    "headless": True,
    "viewport": {"width": 1280, "height": 720},
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "timeout": 30000,  # 30 seconds
    "ignore_https_errors": True
}
```

**Content Processing Pipeline:**
1. **URL Loading**: Navigate to URL with timeout
2. **JavaScript Execution**: Wait for dynamic content
3. **Content Extraction**: Get page HTML and title
4. **Sanitization**: Remove scripts, styles, and unwanted elements
5. **Size Limiting**: Truncate content to prevent memory issues
6. **Error Handling**: Capture and log failures

#### BeautifulSoup Post-processing
```python
# Clean extracted HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Remove unwanted elements
for element in soup(['script', 'style', 'nav', 'footer']):
    element.decompose()

# Extract clean text
clean_text = soup.get_text(separator=' ', strip=True)
```

### 4. AI Summarization

#### Gemini AI Integration
```python
def _summarize_content(self, content: str) -> str:
    """
    Generate summary using Google Gemini AI.
    
    Features:
    - Context-aware summarization
    - Configurable summary length
    - Error handling for API failures
    - Content preprocessing
    """
```

**Prompt Engineering:**
```python
summarization_prompt = f"""
Please provide a comprehensive summary of the following content. 
Focus on key points, main ideas, and important details. 
Keep the summary informative but concise.

Content: {content[:4000]}  # Limit content size
"""
```

**API Configuration:**
- **Model**: `gemini-2.0-flash` (latest stable version)
- **Temperature**: 0.3 (balanced creativity vs consistency)
- **Max Tokens**: Auto-configured based on content
- **Safety Settings**: Default filtering enabled

#### Summary Generation Strategy

**Individual Summaries:**
- Process each scraped page independently
- Generate focused summaries (200-400 words)
- Extract key insights and facts
- Maintain source attribution

**Overall Summary:**
- Combine all individual summaries
- Identify common themes and patterns  
- Generate comprehensive overview (500-800 words)
- Remove redundancy and conflicts

### 5. Concurrent Processing

#### ThreadPoolExecutor Implementation
```python
def process_urls_concurrently(self, urls: List[str]) -> List[dict]:
    """Process multiple URLs in parallel for improved performance."""
    
    with ThreadPoolExecutor(max_workers=min(8, len(urls))) as executor:
        # Submit all scraping tasks
        future_to_url = {
            executor.submit(self._scrape_url, url): url 
            for url in urls
        }
        
        # Collect results as they complete
        results = []
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {url}: {e}")
                
        return results
```

**Performance Optimizations:**
- **Worker Limits**: Max 8 concurrent workers to prevent overwhelming
- **Memory Management**: Process results as they complete
- **Error Isolation**: Individual failures don't stop overall processing
- **Resource Cleanup**: Automatic cleanup of browser instances

## 📁 Code Structure

### Project Organization
```
ScraperSage/
├── ScraperSage/                 # Main package
│   ├── __init__.py             # Package initialization
│   └── scraper_sage.py         # Core implementation
├── tests/                      # Test suite (future)
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── test_scraper_sage.py   # Main tests
│   ├── test_search.py         # Search functionality tests
│   ├── test_scraping.py       # Web scraping tests
│   ├── test_summarization.py  # AI summarization tests
│   └── fixtures/              # Test data
├── examples/                   # Usage examples
│   ├── basic_usage.py
│   ├── advanced_config.py
│   └── batch_processing.py
├── docs/                      # Documentation
│   ├── api_reference.md
│   ├── examples.md
│   └── troubleshooting.md
├── requirements.txt           # Dependencies
├── requirements-dev.txt       # Development dependencies
├── setup.py                   # Package setup
├── pyproject.toml            # Modern Python packaging
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore patterns
└── README.md                # Main documentation
```

### Module Dependencies
```python
# Core dependencies (required)
import os                      # Environment variables
import json                   # Data serialization
import time                   # Timing and delays
from typing import List, Optional, Dict, Any  # Type hints
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third-party dependencies
import requests              # HTTP requests (Serper API)
from ddgs import DDGS        # DuckDuckGo search
from playwright.sync_api import sync_playwright  # Web scraping
import google.generativeai as genai  # AI summarization
from bs4 import BeautifulSoup  # HTML processing
from tenacity import retry, stop_after_attempt, wait_exponential  # Retry logic
```

### Error Handling Strategy

#### Exception Hierarchy
```python
class ScraperSageError(Exception):
    """Base exception for ScraperSage."""
    pass

class APIKeyError(ScraperSageError):
    """Raised when API keys are missing or invalid."""
    pass

class SearchError(ScraperSageError):
    """Raised when all search engines fail."""
    pass

class ScrapingError(ScraperSageError):
    """Raised when web scraping fails."""
    pass

class SummarizationError(ScraperSageError):
    """Raised when AI summarization fails."""
    pass
```

#### Error Recovery Mechanisms
```python
def handle_errors_gracefully(self, operation: str, error: Exception) -> dict:
    """
    Handle errors with graceful degradation.
    
    Strategy:
    1. Log detailed error information
    2. Attempt alternative approaches
    3. Return partial results when possible
    4. Provide clear error messages to users
    """
```

## 🧪 Testing Framework

### Test Categories

#### 1. Unit Tests
```python
class TestScrapeSummarizeUnit:
    """Unit tests for individual methods."""
    
    def test_init_with_api_keys(self):
        """Test initialization with explicit API keys."""
        
    def test_init_missing_keys(self):
        """Test initialization failure with missing keys."""
        
    def test_search_google_success(self):
        """Test successful Google search with mocked response."""
        
    def test_search_duckduckgo_success(self):
        """Test successful DuckDuckGo search."""
        
    def test_scrape_url_success(self):
        """Test successful URL scraping with mocked browser."""
```

#### 2. Integration Tests
```python
class TestScrapeSummarizeIntegration:
    """Integration tests for component interactions."""
    
    @pytest.mark.integration
    def test_search_integration(self):
        """Test search engines working together."""
        
    @pytest.mark.integration  
    def test_scraping_summarization_pipeline(self):
        """Test scraping → summarization pipeline."""
        
    @pytest.mark.integration
    def test_full_workflow_success(self):
        """Test complete workflow with real APIs."""
```

#### 3. Performance Tests
```python
class TestPerformance:
    """Performance and load testing."""
    
    def test_concurrent_scraping_performance(self):
        """Test performance with multiple URLs."""
        
    def test_memory_usage_large_content(self):
        """Test memory handling with large content."""
        
    def test_timeout_handling(self):
        """Test proper timeout behavior."""
```

### Mock Framework
```python
@pytest.fixture
def mock_serper_response():
    """Mock successful Serper API response."""
    return {
        "organic": [
            {"link": "https://example1.com", "title": "Example 1"},
            {"link": "https://example2.com", "title": "Example 2"}
        ]
    }

@pytest.fixture  
def mock_browser(monkeypatch):
    """Mock Playwright browser for testing."""
    class MockPage:
        def goto(self, url): pass
        def content(self): return "<html><body>Test content</body></html>"
        def title(self): return "Test Title"
        
    class MockBrowser:
        def new_page(self): return MockPage()
        def close(self): pass
        
    monkeypatch.setattr("playwright.sync_api.sync_playwright", 
                       lambda: MockBrowser())
```

## 🚀 Deployment

### Package Building

#### Setup.py Configuration
```python
from setuptools import setup, find_packages

setup(
    name="ScraperSage",
    version="1.0.0",
    description="Web scraping and AI summarization library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="AkilLabs",
    author_email="contact@akillabs.com",
    url="https://github.com/akillabs/ScraperSage",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "duckduckgo-search>=3.8.0", 
        "playwright>=1.30.0",
        "google-generativeai>=0.3.0",
        "beautifulsoup4>=4.11.0",
        "tenacity>=8.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "pytest-cov>=3.0.0"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Text Processing :: General"
    ]
)
```

#### PyPI Deployment
```bash
# Build distribution
python setup.py sdist bdist_wheel

# Upload to TestPyPI (testing)
python -m twine upload --repository testpypi dist/*

# Upload to PyPI (production)
python -m twine upload dist/*
```

### Continuous Integration

#### GitHub Actions Workflow
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.8, 3.9, "3.10", 3.11, 3.12]
        
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Install dependencies
      run: |
        pip install -e .
        pip install -r requirements-dev.txt
        playwright install chromium
        
    - name: Run quality checks
      run: |
        black --check ScraperSage/
        flake8 ScraperSage/
        mypy ScraperSage/
        
    - name: Run tests
      run: |
        pytest --cov=ScraperSage --cov-report=xml
        
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    - name: Build and publish
      run: |
        pip install build twine
        python -m build
        twine upload dist/*
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

### Docker Support
```dockerfile
# Dockerfile for containerized deployment
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install ScraperSage
COPY . /app
WORKDIR /app
RUN pip install -e .
RUN playwright install chromium

# Set environment variables
ENV PYTHONPATH="/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python", "-c", "from ScraperSage import scrape_and_summarize; print('Ready!')"]
```

## 🔍 Debugging

### Debug Mode Configuration
```python
import logging

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable specific debug flags
os.environ["SCRAPER_DEBUG"] = "true"
os.environ["PLAYWRIGHT_DEBUG"] = "1"
```

### Common Debug Scenarios

#### 1. API Key Issues
```python
def debug_api_keys():
    """Debug API key configuration."""
    print(f"Serper API Key: {'✓' if os.getenv('SERPER_API_KEY') else '✗'}")
    print(f"Gemini API Key: {'✓' if os.getenv('GEMINI_API_KEY') else '✗'}")
    
    # Test API connectivity
    try:
        scraper = scrape_and_summarize()
        print("✓ API keys valid and accessible")
    except ValueError as e:
        print(f"✗ API key error: {e}")
```

#### 2. Network Connectivity
```python
def debug_network():
    """Debug network connectivity to external services."""
    services = {
        "Serper API": "https://google.serper.dev",
        "Google AI": "https://generativelanguage.googleapis.com"
    }
    
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            print(f"✓ {name}: {response.status_code}")
        except Exception as e:
            print(f"✗ {name}: {e}")
```

#### 3. Browser Issues
```python
def debug_playwright():
    """Debug Playwright browser setup."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Visible for debugging
            page = browser.new_page()
            page.goto("https://example.com")
            print(f"✓ Browser title: {page.title()}")
            browser.close()
    except Exception as e:
        print(f"✗ Playwright error: {e}")
```

### Performance Monitoring
```python
import time
from functools import wraps

def monitor_performance(func):
    """Decorator to monitor function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        memory_before = psutil.Process().memory_info().rss
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        memory_after = psutil.Process().memory_info().rss
        
        print(f"{func.__name__}:")
        print(f"  Time: {end_time - start_time:.2f}s")
        print(f"  Memory: {(memory_after - memory_before) / 1024 / 1024:.2f}MB")
        
        return result
    return wrapper
```

## 📊 Performance Optimization

### Optimization Strategies

#### 1. Concurrent Processing
- **Thread Pool Management**: Optimal worker count based on system resources
- **Async Operations**: Non-blocking I/O for network requests
- **Resource Pooling**: Reuse browser instances when possible

#### 2. Memory Management
- **Content Limiting**: Restrict scraped content size per URL
- **Lazy Loading**: Load and process content on-demand
- **Garbage Collection**: Explicit cleanup of large objects

#### 3. Network Optimization
- **Connection Pooling**: Reuse HTTP connections
- **Request Batching**: Batch API calls when possible  
- **Caching**: Cache search results and summaries temporarily

#### 4. Algorithm Efficiency
- **URL Deduplication**: Efficient set-based URL filtering
- **Text Processing**: Optimized content cleaning and extraction
- **Summary Caching**: Avoid regenerating identical summaries

### Benchmarking
```python
def benchmark_full_workflow():
    """Benchmark complete workflow performance."""
    import time
    import psutil
    
    process = psutil.Process()
    start_memory = process.memory_info().rss
    start_time = time.time()
    
    scraper = scrape_and_summarize()
    result = scraper.run({
        "query": "test query",
        "max_results": 10,
        "max_urls": 15
    })
    
    end_time = time.time()
    end_memory = process.memory_info().rss
    
    print(f"Performance Metrics:")
    print(f"  Total Time: {end_time - start_time:.2f}s")
    print(f"  Memory Usage: {(end_memory - start_memory) / 1024 / 1024:.2f}MB")
    print(f"  Sources Processed: {result.get('successfully_scraped', 0)}")
    print(f"  Success Rate: {result.get('successfully_scraped', 0) / result.get('total_sources_found', 1) * 100:.1f}%")
```

## 🔒 Security Considerations

### API Key Management
- **Environment Variables**: Never hardcode API keys in source code
- **Key Rotation**: Regularly rotate API keys
- **Access Control**: Limit API key permissions to minimum required
- **Monitoring**: Track API usage and anomalies

### Web Scraping Ethics
- **Rate Limiting**: Respect website rate limits and robots.txt
- **User Agent**: Use appropriate user agent strings
- **Content Respect**: Only scrape publicly available content
- **Legal Compliance**: Follow applicable laws and regulations

### Data Privacy
- **Temporary Storage**: Minimize data retention time
- **Sensitive Content**: Filter out personal or sensitive information
- **Logging**: Avoid logging sensitive data
- **Compliance**: Follow GDPR, CCPA, and other privacy regulations

---

This development guide provides the technical foundation for contributing to and extending ScraperSage. For additional information, see the [API Reference](API_REFERENCE.md) and [Contributing Guidelines](CONTRIBUTING.md).