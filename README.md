# Scrape and Summarize

A comprehensive web scraping and content summarization library that combines Google/DuckDuckGo search with web scraping and AI-powered summarization using Google Gemini.

## Features

- **Multi-Engine Search**: Combines Google (via Serper API) and DuckDuckGo search results
- **Advanced Web Scraping**: Uses Playwright for robust, JavaScript-enabled web scraping
- **AI-Powered Summarization**: Leverages Google Gemini AI for intelligent content summarization
- **Parallel Processing**: Concurrent scraping and summarization for improved performance
- **Retry Mechanisms**: Built-in retry logic for reliable operations
- **Structured Output**: Clean JSON output format for easy integration
- **Error Handling**: Comprehensive error handling and graceful degradation

## Installation

### From Source (Development)

1. Clone or download this repository
2. Navigate to the project directory
3. Install the package in development mode:

```bash
pip install -e .
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright Browsers (Required)

```bash
playwright install chromium
```

## Quick Start

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

## API Keys Setup

You need two API keys to use this library:

### 1. Serper API Key (for Google Search)
- Visit [Serper.dev](https://serper.dev)
- Sign up for a free account
- Get your API key from the dashboard
- Set as environment variable: `SERPER_API_KEY`

### 2. Google Gemini API Key
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create a new API key
- Set as environment variable: `GEMINI_API_KEY`

## Usage Examples

### Basic Usage

```python
from ScraperSage import scrape_and_summarize
import os

# Initialize with API keys
scraper = scrape_and_summarize(
    serper_api_key="your_serper_key",
    gemini_api_key="your_gemini_key"
)

# Basic search
params = {
    "query": "machine learning trends 2024"
}

result = scraper.run(params)
```

### Advanced Configuration

```python
params = {
    "query": "climate change solutions",
    "max_results": 8,        # Maximum search results per engine (default: 5)
    "max_urls": 10,          # Maximum URLs to scrape (default: 8)
    "save_to_file": True     # Save results to JSON file (default: False)
}

result = scraper.run(params)
```

### Error Handling

```python
try:
    scraper = scrape_and_summarize()
    result = scraper.run({"query": "your search query"})
    
    if result["status"] == "success":
        print(f"Found {result['successfully_scraped']} sources")
        print(f"Summary: {result['overall_summary']}")
    else:
        print(f"Error: {result['message']}")
        
except ValueError as e:
    print(f"API key error: {e}")
```

## Output Format

The library returns a structured JSON object with the following format:

```json
{
  "status": "success",
  "query": "your search query",
  "timestamp": "2024-01-01 12:00:00",
  "total_sources_found": 10,
  "successfully_scraped": 8,
  "sources": [
    {
      "url": "https://example.com",
      "title": "Page Title",
      "content_preview": "First 200 characters...",
      "individual_summary": "AI-generated summary of this source",
      "scraped": true
    }
  ],
  "failed_sources": [
    {
      "url": "https://failed-example.com",
      "scraped": false
    }
  ],
  "overall_summary": "Comprehensive AI-generated summary of all sources",
  "metadata": {
    "google_results_count": 5,
    "duckduckgo_results_count": 5,
    "total_unique_urls": 10,
    "processing_time": "Real-time processing completed"
  }
}
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | str | Required | The search query to process |
| `max_results` | int | 5 | Maximum number of search results per search engine |
| `max_urls` | int | 8 | Maximum number of URLs to scrape |
| `save_to_file` | bool | False | Whether to save results to a JSON file |

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

## Development

### Project Structure

```
ScraperSage/
├── __init__.py
├── scraper_sage.py
├── setup.py
├── requirements.txt
├── README.md
└── example_usage.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please visit the project repository or contact the maintainers.

## Changelog

### v1.0.0
- Initial release
- Multi-engine search support (Google + DuckDuckGo)
- Playwright-based web scraping
- Google Gemini AI summarization
- Structured JSON output
- Comprehensive error handling