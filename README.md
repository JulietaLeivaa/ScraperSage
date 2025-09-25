# ScraperSage

A comprehensive web scraping and content summarization library that combines Google/DuckDuckGo search with web scraping and AI-powered summarization using Google Gemini.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI Version](https://img.shields.io/badge/PyPI-Coming%20Soon-orange.svg)](#installation)

## 🚀 Features

- **Multi-Engine Search**: Combines Google (via Serper API) and DuckDuckGo search results
- **Advanced Web Scraping**: Uses Playwright for robust, JavaScript-enabled web scraping  
- **AI-Powered Summarization**: Leverages Google Gemini AI for intelligent content summarization
- **Parallel Processing**: Concurrent scraping and summarization for improved performance
- **Retry Mechanisms**: Built-in retry logic for reliable operations
- **Structured Output**: Clean JSON output format for easy integration
- **Error Handling**: Comprehensive error handling and graceful degradation
- **Configurable Parameters**: Flexible configuration for different use cases
- **Real-time Processing**: Live status updates during processing

## 📖 Table of Contents

- [Installation](#installation)
- [API Keys Setup](#api-keys-setup)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Output Format](#output-format)
- [Error Handling](#error-handling)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 📦 Installation

### From PyPI (Recommended)

Install the latest stable version from PyPI:

```bash
pip install ScraperSage
```

### From Source (Development)

1. Clone this repository:
```bash
git clone https://github.com/akillabs/ScraperSage.git
cd ScraperSage
```

2. Install the package in development mode:
```bash
pip install -e .
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright Browsers (Required)

After installation, you must install the Playwright browsers:

```bash
playwright install chromium
```

> **Note**: This step is crucial for web scraping functionality. The library uses Chromium for JavaScript-enabled scraping.

## 🔑 API Keys Setup

```python
import os
import json
from ScraperSage import scrape_and_summarize

# Set your API keys
os.environ["SERPER_API_KEY"] = "your_serper_api_key"
os.environ["GEMINI_API_KEY"] = "your_gemini_api_key"

# Initialize scrape_and_summarize
scraper = scrape_and_summarize()

# Define search parameters
params = {
    "query": "AI in healthcare",
    "max_results": 5,
    "save_to_file": False
}

# Run the scraper
result = scraper.run(params)

# Print results
print(json.dumps(result, indent=2))
```

You need two API keys to use this library:

### 1. Serper API Key (for Google Search)
1. Visit [Serper.dev](https://serper.dev)
2. Sign up for a free account (includes 2,500 free searches)
3. Navigate to your dashboard
4. Copy your API key
5. Set as environment variable:
   ```bash
   # Windows (PowerShell)
   $env:SERPER_API_KEY="your_serper_api_key_here"
   
   # Windows (Command Prompt)
   set SERPER_API_KEY=your_serper_api_key_here
   
   # Linux/Mac
   export SERPER_API_KEY="your_serper_api_key_here"
   ```

### 2. Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key
5. Set as environment variable:
   ```bash
   # Windows (PowerShell)
   $env:GEMINI_API_KEY="your_gemini_api_key_here"
   
   # Windows (Command Prompt)
   set GEMINI_API_KEY=your_gemini_api_key_here
   
   # Linux/Mac
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

### Alternative: Set Keys in Code
```python
from ScraperSage import scrape_and_summarize

# Initialize with explicit API keys
scraper = scrape_and_summarize(
    serper_api_key="your_serper_key",
    gemini_api_key="your_gemini_key"
)
```

## ⚡ Quick Start

## 📚 Usage Guide

### Basic Usage

```python
from ScraperSage import scrape_and_summarize
import os

# Initialize (uses environment variables)
scraper = scrape_and_summarize()

# Simple search
result = scraper.run({
    "query": "artificial intelligence trends 2024"
})

# Check results
if result["status"] == "success":
    print(f"✅ Successfully scraped {result['successfully_scraped']} sources")
    print(f"📄 Summary: {result['overall_summary']}")
else:
    print(f"❌ Error: {result['message']}")
```

### Advanced Configuration

```python
# Advanced parameters
params = {
    "query": "machine learning in healthcare",
    "max_results": 8,        # Max results per search engine (default: 5)
    "max_urls": 12,          # Max URLs to scrape (default: 8)
    "save_to_file": True     # Save results to JSON (default: False)
}

result = scraper.run(params)
```

### Batch Processing

```python
queries = [
    "AI in healthcare",
    "blockchain technology",
    "renewable energy solutions"
]

results = []
for query in queries:
    result = scraper.run({"query": query, "max_results": 3})
    results.append(result)
    time.sleep(1)  # Rate limiting
```

## ⚙️ Configuration

### Parameters Reference

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `query` | str | **Required** | - | The search query to process |
| `max_results` | int | 5 | 1-20 | Maximum search results per engine |
| `max_urls` | int | 8 | 1-50 | Maximum URLs to scrape and summarize |
| `save_to_file` | bool | False | - | Save results to timestamped JSON file |

### Environment Variables

```bash
# Required
SERPER_API_KEY=your_serper_api_key
GEMINI_API_KEY=your_gemini_api_key

# Optional (for debugging)
SCRAPER_DEBUG=true
SCRAPER_TIMEOUT=30
```

## 📋 API Reference

### Class: `scrape_and_summarize`

#### Constructor
```python
scrape_and_summarize(serper_api_key=None, gemini_api_key=None)
```

**Parameters:**
- `serper_api_key` (str, optional): Serper API key. Uses `SERPER_API_KEY` env var if not provided
- `gemini_api_key` (str, optional): Gemini API key. Uses `GEMINI_API_KEY` env var if not provided

**Raises:**
- `ValueError`: If required API keys are missing

#### Method: `run(params)`
```python
run(params: dict) -> dict
```

**Parameters:**
- `params` (dict): Configuration dictionary with query and optional parameters

**Returns:**
- `dict`: Structured result with scraped content and summaries

**Example:**
```python
result = scraper.run({
    "query": "sustainable technology innovations",
    "max_results": 5,
    "max_urls": 8,
    "save_to_file": False
})
```

## 📤 Output Format

The library returns a structured JSON object with comprehensive results:

```json
{
  "status": "success",
  "query": "artificial intelligence in healthcare",
  "timestamp": "2025-09-25 14:30:22",
  "total_sources_found": 10,
  "successfully_scraped": 8,
  "sources": [
    {
      "url": "https://www.nature.com/articles/s41591-021-01614-0",
      "title": "Artificial intelligence in healthcare: past, present and future",
      "content_preview": "Artificial intelligence (AI) is rapidly transforming healthcare, with applications ranging from diagnostic imaging to drug discovery...",
      "individual_summary": "This Nature Medicine article provides a comprehensive overview of AI applications in healthcare, covering current implementations in medical imaging, natural language processing for clinical notes, and predictive analytics for patient outcomes.",
      "scraped": true
    },
    {
      "url": "https://www.who.int/news-room/feature-stories/detail/artificial-intelligence-in-healthcare",
      "title": "Artificial Intelligence in Healthcare - World Health Organization",
      "content_preview": "The World Health Organization recognizes the potential of artificial intelligence to strengthen health systems and improve patient care...",
      "individual_summary": "WHO's perspective on AI in healthcare emphasizes the importance of ethical implementation, regulatory frameworks, and ensuring equitable access to AI-powered healthcare solutions across different populations.",
      "scraped": true
    }
  ],
  "failed_sources": [
    {
      "url": "https://inaccessible-medical-site.com/article",
      "scraped": false
    }
  ],
  "overall_summary": "Artificial intelligence is revolutionizing healthcare through multiple applications including medical imaging, diagnostics, drug discovery, and personalized treatment plans. Current implementations show promising results in improving diagnostic accuracy, reducing medical errors, and enhancing patient outcomes. However, challenges remain regarding data privacy, regulatory approval, and ensuring equitable access across different healthcare systems. The field continues to evolve with new AI models and applications being developed for clinical decision support and population health management.",
  "metadata": {
    "google_results_count": 5,
    "duckduckgo_results_count": 5,
    "total_unique_urls": 10,
    "processing_time": "Real-time processing completed",
    "success_rate": "80%"
  }
}
```

### Output Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `status` | str | "success" or "error" |
| `query` | str | Original search query |
| `timestamp` | str | Processing timestamp |
| `total_sources_found` | int | Total URLs found across all search engines |
| `successfully_scraped` | int | Number of successfully processed URLs |
| `sources` | list | Successfully scraped and summarized sources |
| `failed_sources` | list | URLs that failed to scrape with error details |
| `overall_summary` | str | AI-generated comprehensive summary |
| `metadata` | dict | Additional processing information |

## 🚨 Error Handling

### Common Error Types

```python
from ScraperSage import scrape_and_summarize

try:
    scraper = scrape_and_summarize()
    result = scraper.run({"query": "your query"})
    
    # Success check
    if result["status"] == "success":
        print(f"✅ Success: {result['successfully_scraped']} sources")
    else:
        print(f"❌ Error: {result['message']}")
        
except ValueError as e:
    print(f"🔑 API Key Error: {e}")
except ConnectionError as e:
    print(f"🌐 Network Error: {e}")
except Exception as e:
    print(f"💥 Unexpected Error: {e}")
```

### Error Response Format

```json
{
  "status": "error",
  "message": "Detailed error description",
  "error_type": "API_KEY_ERROR",
  "timestamp": "2024-01-01 12:00:00",
  "query": "original query",
  "partial_results": null
}
```

### Built-in Recovery

The library includes several recovery mechanisms:
- **Automatic retries** for network failures (3 attempts with exponential backoff)
- **Graceful degradation** when some sources fail
- **Timeout handling** for slow websites (30-second limit)
- **Rate limiting protection** with built-in delays

## 💡 Examples

### Research Assistant

```python
from ScraperSage import scrape_and_summarize
import json

def research_topic(topic, depth="medium"):
    """Research a topic with different depth levels."""
    scraper = scrape_and_summarize()
    
    depth_configs = {
        "light": {"max_results": 3, "max_urls": 5},
        "medium": {"max_results": 5, "max_urls": 8},
        "deep": {"max_results": 10, "max_urls": 15}
    }
    
    config = depth_configs.get(depth, depth_configs["medium"])
    config["query"] = topic
    config["save_to_file"] = True
    
    result = scraper.run(config)
    return result

# Usage
result = research_topic("quantum computing applications", depth="deep")
print(f"Research complete: {result['successfully_scraped']} sources analyzed")
```

### News Monitoring

```python
import time
from datetime import datetime

def monitor_news(keywords, interval_minutes=30):
    """Monitor news for specific keywords."""
    scraper = scrape_and_summarize()
    
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"\n📰 News check at {timestamp}")
        
        for keyword in keywords:
            query = f"{keyword} news today"
            result = scraper.run({
                "query": query,
                "max_results": 3,
                "max_urls": 5
            })
            
            if result["status"] == "success":
                print(f"  📌 {keyword}: {result['successfully_scraped']} new articles")
                print(f"  📄 Summary: {result['overall_summary'][:150]}...")
        
        time.sleep(interval_minutes * 60)

# Usage
keywords = ["artificial intelligence", "climate change", "space exploration"]
monitor_news(keywords, interval_minutes=60)
```

### Market Research

```python
def analyze_market(product, competitors=None):
    """Analyze market trends and competitor information."""
    scraper = scrape_and_summarize()
    queries = [f"{product} market trends 2024"]
    
    if competitors:
        for competitor in competitors:
            queries.append(f"{competitor} {product} strategy")
    
    results = []
    for query in queries:
        result = scraper.run({
            "query": query,
            "max_results": 5,
            "max_urls": 8,
            "save_to_file": True
        })
        results.append(result)
    
    return results

# Usage
market_analysis = analyze_market(
    product="electric vehicles",
    competitors=["Tesla", "BMW", "Mercedes"]
)
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. API Key Errors
```
ValueError: Missing required API keys
```
**Solution:** Ensure both `SERPER_API_KEY` and `GEMINI_API_KEY` are set correctly.

#### 2. Playwright Installation
```
playwright._impl._api_structures.Error: Executable doesn't exist
```
**Solution:** Install Playwright browsers:
```bash
playwright install chromium
```

#### 3. Network Timeouts
```
All sources failed to scrape
```
**Solutions:**
- Check internet connection
- Try reducing `max_urls` parameter
- Run during off-peak hours

#### 4. Rate Limiting
```
429 Too Many Requests
```
**Solutions:**
- Add delays between requests
- Reduce `max_results` parameter
- Check API quota limits

#### 5. Memory Issues
```
MemoryError during processing
```
**Solutions:**
- Reduce `max_urls` parameter
- Process queries individually
- Increase available RAM

### Debug Mode

Enable debug logging:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
scraper = scrape_and_summarize()
```

### Performance Optimization

```python
# Optimized for speed
params = {
    "query": "your query",
    "max_results": 3,     # Fewer results
    "max_urls": 5,        # Fewer URLs
    "save_to_file": False # Skip file I/O
}

# Optimized for comprehensiveness
params = {
    "query": "your query", 
    "max_results": 10,    # More results
    "max_urls": 20,       # More URLs
    "save_to_file": True  # Save for analysis
}
```

## Requirements

- Python 3.8+
- Internet connection
- Valid Serper API key
- Valid Google Gemini API key

## Dependencies

- `requests` - HTTP requests
- `duckduckgo-search` - DuckDuckGo search integration
- `playwright` - Web scraping with browser automation
- `google-generativeai` - Google Gemini AI integration
- `beautifulsoup4` - HTML parsing
- `tenacity` - Retry mechanisms

## Error Handling

The library includes comprehensive error handling:

- **API Key Validation**: Checks for required API keys on initialization
- **Network Retry Logic**: Automatic retries for failed network requests
- **Graceful Degradation**: Continues processing even if some sources fail
- **Timeout Management**: Proper timeouts for web scraping operations

## Performance Considerations

- Uses ThreadPoolExecutor for concurrent scraping
- Limits content size per URL to prevent memory issues
- Implements exponential backoff for retries
- Configurable worker limits for parallel processing

## 🛠️ Development

For detailed development documentation, see [DEVELOPMENT.md](DEVELOPMENT.md).

### Quick Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/akillabs/ScraperSage.git
   cd ScraperSage
   ```

2. Create virtual environment:
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt  # If available
   playwright install chromium
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env  # Edit with your API keys
   ```

5. Run tests:
   ```bash
   python -m pytest tests/  # If tests are available
   ```

### Project Structure

```
ScraperSage/
├── ScraperSage/
│   ├── __init__.py
│   └── scraper_sage.py      # Main library code
├── tests/                   # Test files (coming soon)
├── docs/                    # Documentation
├── examples/               # Usage examples
├── requirements.txt        # Dependencies
├── setup.py               # Package configuration
├── pyproject.toml         # Modern Python packaging
└── README.md              # This file
```

### Key Components

- **Search Integration**: Google (Serper) + DuckDuckGo
- **Web Scraping**: Playwright-based with JavaScript support
- **AI Summarization**: Google Gemini integration
- **Concurrent Processing**: ThreadPoolExecutor for parallel operations
- **Error Handling**: Comprehensive retry and fallback mechanisms

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contributing Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure all tests pass: `python -m pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings for all public functions
- Include tests for new features
- Update documentation as needed
- Use type hints where appropriate

## 📊 Requirements & Dependencies

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **Memory**: 2GB RAM minimum (4GB recommended)
- **Network**: Stable internet connection

### Core Dependencies
- `requests` - HTTP requests and API calls
- `duckduckgo-search` - DuckDuckGo search integration  
- `playwright` - Web scraping with browser automation
- `google-generativeai` - Google Gemini AI integration
- `beautifulsoup4` - HTML parsing and content extraction
- `tenacity` - Retry mechanisms and error handling

### Development Dependencies (Optional)
- `pytest` - Testing framework
- `black` - Code formatting
- `flake8` - Code linting
- `mypy` - Type checking

## 📈 Performance Notes

- **Concurrent Processing**: Uses ThreadPoolExecutor for parallel scraping
- **Memory Management**: Limits content size per URL to prevent memory issues
- **Rate Limiting**: Implements exponential backoff for API calls
- **Timeout Handling**: 30-second timeout per URL to prevent hanging
- **Caching**: Results can be saved to JSON for repeated analysis

### Performance Tips
- Use smaller `max_results` and `max_urls` for faster processing
- Enable `save_to_file` for large datasets to avoid reprocessing
- Add delays between consecutive runs to respect API rate limits
- Monitor memory usage when processing many URLs simultaneously

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Resources

- **Documentation**: [Full documentation](docs/)
- **Examples**: [Usage examples](EXAMPLES.md)
- **API Reference**: [Detailed API docs](API_REFERENCE.md)
- **Issues**: [GitHub Issues](https://github.com/akillabs/ScraperSage/issues)
- **Discussions**: [GitHub Discussions](https://github.com/akillabs/ScraperSage/discussions)

### Getting Help

1. Check the [troubleshooting section](#troubleshooting) first
2. Search [existing issues](https://github.com/akillabs/ScraperSage/issues)
3. Create a new issue with:
   - Clear problem description
   - Code snippet that reproduces the issue
   - Error messages (if any)
   - Environment details (Python version, OS, etc.)

## 🔄 Changelog

### v1.0.0 (Current)
- ✅ Initial release
- ✅ Multi-engine search support (Google + DuckDuckGo)
- ✅ Playwright-based web scraping with JavaScript support
- ✅ Google Gemini AI summarization
- ✅ Structured JSON output format
- ✅ Comprehensive error handling and retry mechanisms
- ✅ Concurrent processing for improved performance
- ✅ Configurable parameters and environment variable support

### Coming Soon
- 🔄 Advanced filtering and content extraction options
- 🔄 Support for additional search engines
- 🔄 Batch processing capabilities
- 🔄 Enhanced output formats (CSV, XML, etc.)
- 🔄 Performance optimizations and caching
- 🔄 Comprehensive test suite

---

**Made with ❤️ by the AkilLabs team**

*Star ⭐ this repo if you find it helpful!*