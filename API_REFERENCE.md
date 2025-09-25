# API Reference

This document provides comprehensive API documentation for ScraperSage, including all classes, methods, parameters, and return values.

## 📋 Table of Contents

- [Overview](#overview)
- [Main Class](#main-class)
- [Methods](#methods)
- [Parameters](#parameters)
- [Return Values](#return-values)
- [Error Handling](#error-handling)
- [Type Definitions](#type-definitions)
- [Examples](#examples)

## 🔍 Overview

ScraperSage provides a single main class `scrape_and_summarize` that orchestrates web searching, scraping, and AI summarization. The library is designed with a simple, intuitive API that handles complex operations internally.

### Architecture
```
User Input → scrape_and_summarize.run() → Structured JSON Output
    ↓
[Search] → [Scrape] → [Summarize] → [Format] → [Save (optional)]
```

## 🏛️ Main Class

### `scrape_and_summarize`

The main orchestrator class that coordinates search, scraping, and summarization operations.

#### Class Definition
```python
class scrape_and_summarize:
    """
    A comprehensive web scraping and content summarization class that combines
    Google/DuckDuckGo search with web scraping and AI-powered summarization.
    """
```

#### Constructor

```python
def __init__(
    self, 
    serper_api_key: Optional[str] = None, 
    gemini_api_key: Optional[str] = None
) -> None
```

**Description:** Initialize the scraper with API credentials.

**Parameters:**
- `serper_api_key` (Optional[str]): API key for Serper (Google Search)
  - **Default:** Uses `SERPER_API_KEY` environment variable
  - **Required:** Yes (either via parameter or environment variable)
  - **Format:** String API key from [serper.dev](https://serper.dev)

- `gemini_api_key` (Optional[str]): API key for Google Gemini AI
  - **Default:** Uses `GEMINI_API_KEY` environment variable  
  - **Required:** Yes (either via parameter or environment variable)
  - **Format:** String API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

**Raises:**
- `ValueError`: If either required API key is missing

**Example:**
```python
# Using environment variables
scraper = scrape_and_summarize()

# Using explicit API keys
scraper = scrape_and_summarize(
    serper_api_key="your_serper_key",
    gemini_api_key="your_gemini_key"
)
```

---

## 📚 Methods

### Primary Method: `run`

```python
def run(self, params: Dict[str, Any]) -> Dict[str, Any]
```

**Description:** Main execution method that orchestrates the entire scraping and summarization pipeline.

**Parameters:**
- `params` (Dict[str, Any]): Configuration dictionary with the following keys:

| Key | Type | Default | Required | Range | Description |
|-----|------|---------|----------|-------|-------------|
| `query` | str | N/A | ✅ Yes | 1-500 chars | Search query string |
| `max_results` | int | 5 | ❌ No | 1-20 | Max results per search engine |
| `max_urls` | int | 8 | ❌ No | 1-50 | Max URLs to scrape and summarize |
| `save_to_file` | bool | False | ❌ No | True/False | Save results to JSON file |

**Returns:** `Dict[str, Any]` - Structured result object (see [Return Values](#return-values))

**Raises:**
- `ValueError`: If `query` parameter is missing or invalid
- `ConnectionError`: If all search engines and scraping attempts fail
- `KeyboardInterrupt`: If operation is cancelled by user

**Processing Flow:**
1. **Input Validation**: Validates parameters and extracts configuration
2. **Multi-Engine Search**: Searches Google (Serper) and DuckDuckGo in parallel
3. **URL Deduplication**: Removes duplicate URLs from search results
4. **Concurrent Scraping**: Scrapes multiple URLs in parallel using Playwright
5. **Individual Summarization**: Generates AI summaries for each scraped source
6. **Overall Summarization**: Creates comprehensive summary from all sources
7. **Result Formatting**: Structures output in standardized JSON format
8. **Optional File Save**: Saves results to timestamped JSON file if requested

**Example:**
```python
result = scraper.run({
    "query": "artificial intelligence trends 2024",
    "max_results": 8,
    "max_urls": 12,
    "save_to_file": True
})

if result["status"] == "success":
    print(f"Successfully processed {result['successfully_scraped']} sources")
```

---

### Private Methods

> **Note:** These methods are internal implementation details and should not be called directly. They are documented for development and debugging purposes.

#### `_search_google`

```python
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def _search_google(self, query: str, max_results: int = 5) -> List[str]
```

**Description:** Search Google using Serper API with automatic retry mechanism.

**Features:**
- Exponential backoff retry (up to 3 attempts)
- Rate limiting protection
- Error handling for API failures
- Result filtering and validation

#### `_search_duckduckgo`

```python
def _search_duckduckgo(self, query: str, max_results: int = 5) -> List[str]
```

**Description:** Search DuckDuckGo using the ddgs library.

**Features:**
- Anonymous searching (no API key required)
- Built-in rate limiting
- Automatic retry on failures
- Clean URL extraction

#### `_scrape_with_playwright`

```python
def _scrape_with_playwright(self, url: str) -> Optional[Dict[str, str]]
```

**Description:** Scrape a single URL using Playwright browser automation.

**Returns:** Dictionary with keys: `url`, `title`, `content` or `None` if failed

**Features:**
- JavaScript execution support
- Mobile and desktop user agents
- Content sanitization
- Timeout handling (30 seconds)
- Memory-efficient processing

#### `_scrape_multiple_urls`

```python
def _scrape_multiple_urls(self, urls: List[str], max_urls: int = 8) -> List[Dict[str, str]]
```

**Description:** Scrape multiple URLs concurrently using ThreadPoolExecutor.

**Configuration:**
- **Max Workers:** 4 concurrent threads
- **Resource Management:** Automatic cleanup of browser instances
- **Error Isolation:** Individual failures don't stop overall processing

#### `_summarize_with_gemini`

```python
@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=4, max=10))
def _summarize_with_gemini(
    self, 
    content: str, 
    is_individual: bool = False, 
    source_title: str = ""
) -> str
```

**Description:** Generate AI summary using Google Gemini with retry mechanism.

**Parameters:**
- `content` (str): Text content to summarize
- `is_individual` (bool): Whether this is an individual source summary
- `source_title` (str): Title of the source (for context)

**Model Configuration:**
- **Model:** `gemini-2.0-flash`
- **Content Limit:** 4,000 characters per request
- **Error Handling:** Quota limit detection and graceful degradation

#### `_generate_individual_summaries`

```python
def _generate_individual_summaries(self, scraped_results: List[Dict[str, str]]) -> List[Dict[str, str]]
```

**Description:** Generate individual AI summaries for each scraped source concurrently.

**Configuration:**
- **Max Workers:** 3 concurrent summarization threads
- **Processing:** Parallel AI summarization for improved performance

#### `_save_json_output`

```python
def _save_json_output(self, data: dict, query: str) -> str
```

**Description:** Save JSON output to a timestamped file.

**File Naming Convention:** `search_results_{clean_query}_{timestamp}.json`

**Returns:** Filename if successful, empty string if failed

---

## 📋 Parameters

### Input Parameters (for `run` method)

#### `query` (Required)
- **Type:** `str`
- **Validation:** Must be non-empty string
- **Length:** 1-500 characters recommended
- **Description:** The search query to process
- **Examples:**
  ```python
  "artificial intelligence in healthcare"
  "climate change solutions 2024"
  "python web scraping best practices"
  ```

#### `max_results` (Optional)
- **Type:** `int`
- **Default:** `5`
- **Range:** 1-20 (recommended)
- **Description:** Maximum number of search results to retrieve per search engine
- **Impact:** Higher values = more comprehensive results but slower processing
- **Examples:**
  ```python
  3   # Quick search
  5   # Balanced (default)
  10  # Comprehensive search
  ```

#### `max_urls` (Optional)
- **Type:** `int`
- **Default:** `8`
- **Range:** 1-50 (recommended)
- **Description:** Maximum number of URLs to scrape and summarize
- **Impact:** Higher values = more detailed analysis but increased processing time and memory usage
- **Examples:**
  ```python
  5   # Light processing
  8   # Balanced (default)
  15  # Deep analysis
  ```

#### `save_to_file` (Optional)
- **Type:** `bool`
- **Default:** `False`
- **Description:** Whether to save results to a JSON file
- **File Location:** Current working directory
- **File Format:** UTF-8 encoded JSON with indentation
- **Examples:**
  ```python
  False  # Return results only (default)
  True   # Save to file + return results
  ```

---

## 📤 Return Values

### Success Response Structure

```python
{
    "status": "success",
    "query": str,
    "timestamp": str,
    "total_sources_found": int,
    "successfully_scraped": int,
    "sources": List[Dict],
    "failed_sources": List[Dict],
    "overall_summary": str,
    "metadata": Dict,
    "saved_file": str  # Optional, only if save_to_file=True
}
```

#### Field Descriptions

##### `status` (str)
- **Values:** `"success"`, `"error"`, `"cancelled"`
- **Description:** Overall operation status

##### `query` (str)
- **Description:** Original search query as provided

##### `timestamp` (str)
- **Format:** `"YYYY-MM-DD HH:MM:SS"`
- **Timezone:** Local system timezone
- **Example:** `"2024-01-15 14:30:22"`

##### `total_sources_found` (int)
- **Description:** Total number of unique URLs found across all search engines
- **Range:** 0-40 (typically, depending on max_results)

##### `successfully_scraped` (int)
- **Description:** Number of URLs successfully scraped and processed
- **Range:** 0 to `total_sources_found`

##### `sources` (List[Dict])
Successfully processed sources with structure:
```python
{
    "url": str,                    # Source URL
    "title": str,                  # Page title
    "content_preview": str,        # First 200 characters + "..."
    "individual_summary": str,     # AI-generated summary
    "scraped": bool               # Always True for this list
}
```

##### `failed_sources` (List[Dict])
URLs that could not be processed with structure:
```python
{
    "url": str,          # Failed URL
    "scraped": bool,     # Always False for this list
    "error": str         # Error description (optional)
}
```

##### `overall_summary` (str)
- **Description:** Comprehensive AI-generated summary combining all sources
- **Length:** Typically 500-800 words
- **Content:** Structured overview with key themes and insights

##### `metadata` (Dict)
Processing metadata with structure:
```python
{
    "google_results_count": int,        # Results from Google search
    "duckduckgo_results_count": int,    # Results from DuckDuckGo search
    "total_unique_urls": int,           # Same as total_sources_found
    "processing_time": str,             # Human-readable processing info
    "success_rate": str,                # Percentage of successful scrapes
    "file_saved": str                   # Filename if saved (optional)
}
```

##### `saved_file` (str, optional)
- **Present:** Only when `save_to_file=True` and save operation succeeds
- **Format:** Filename including extension
- **Example:** `"search_results_ai_healthcare_20240115_143022.json"`

### Error Response Structure

```python
{
    "status": "error",
    "message": str,
    "error_type": str,        # Optional
    "timestamp": str,
    "query": str,             # If available
    "partial_results": Dict   # Optional, if some processing completed
}
```

#### Common Error Types

##### API Key Errors
```python
{
    "status": "error",
    "message": "Missing required API keys. Please provide SERPER_API_KEY and GEMINI_API_KEY.",
    "error_type": "API_KEY_ERROR",
    "timestamp": "2024-01-15 14:30:22"
}
```

##### Search Failures
```python
{
    "status": "error", 
    "message": "No search results found",
    "query": "your search query",
    "timestamp": "2024-01-15 14:30:22",
    "sources": [],
    "summary": ""
}
```

##### Complete Scraping Failure
```python
{
    "status": "error",
    "message": "Failed to scrape content from any of the URLs",
    "query": "your search query",
    "timestamp": "2024-01-15 14:30:22",
    "sources": [{"url": "...", "scraped": False, "error": "Failed to scrape"}],
    "summary": ""
}
```

##### User Cancellation
```python
{
    "status": "cancelled",
    "message": "Operation cancelled by user", 
    "timestamp": "2024-01-15 14:30:22"
}
```

---

## 🚨 Error Handling

### Exception Types

#### `ValueError`
**Raised when:**
- Missing or invalid `query` parameter
- Invalid parameter types or values
- Missing required API keys

**Example:**
```python
try:
    scraper = scrape_and_summarize()
except ValueError as e:
    print(f"Configuration error: {e}")
```

#### `ConnectionError` 
**Raised when:**
- Network connectivity issues
- All search engines fail
- All scraping attempts fail

**Example:**
```python
try:
    result = scraper.run({"query": "test"})
except ConnectionError as e:
    print(f"Network error: {e}")
```

#### `KeyboardInterrupt`
**Raised when:**
- User cancels operation (Ctrl+C)
- Process termination signal received

**Handling:**
```python
try:
    result = scraper.run(params)
except KeyboardInterrupt:
    print("Operation cancelled by user")
```

### Graceful Error Recovery

The library implements several error recovery strategies:

1. **Retry Mechanisms**: Automatic retries with exponential backoff for network operations
2. **Partial Success**: Returns available results even if some sources fail
3. **Alternative Sources**: Continues processing remaining URLs if some fail
4. **Fallback Responses**: Provides meaningful error messages instead of crashes

### Error Response Patterns

```python
# Always check status before processing
result = scraper.run(params)

if result["status"] == "success":
    # Process successful results
    print(f"Found {result['successfully_scraped']} sources")
    print(f"Summary: {result['overall_summary']}")
    
elif result["status"] == "error":
    # Handle errors gracefully
    print(f"Error: {result['message']}")
    
    # Check for partial results
    if result.get("partial_results"):
        print("Some results were available:")
        # Process partial results
        
elif result["status"] == "cancelled":
    print("Operation was cancelled")
```

---

## 🔧 Type Definitions

### Custom Types

```python
from typing import Dict, List, Optional, Any

# Input parameters type
ParamsType = Dict[str, Any]

# Search results type  
SearchResults = List[str]

# Scraped content type
ScrapedContent = Dict[str, str]

# Source information type
SourceInfo = Dict[str, Any]

# API response type
ApiResponse = Dict[str, Any]
```

### Parameter Validation

```python
def validate_params(params: ParamsType) -> ParamsType:
    """
    Validate and normalize input parameters.
    
    Args:
        params: Raw parameter dictionary
        
    Returns:
        Validated and normalized parameters
        
    Raises:
        ValueError: If validation fails
    """
    if not isinstance(params, dict):
        raise ValueError("Parameters must be a dictionary")
    
    if "query" not in params or not params["query"]:
        raise ValueError("Query parameter is required and cannot be empty")
    
    # Normalize and validate optional parameters
    validated = {
        "query": str(params["query"]).strip(),
        "max_results": min(max(int(params.get("max_results", 5)), 1), 20),
        "max_urls": min(max(int(params.get("max_urls", 8)), 1), 50),
        "save_to_file": bool(params.get("save_to_file", False))
    }
    
    return validated
```

---

## 💡 Examples

### Basic Usage

```python
from ScraperSage import scrape_and_summarize

# Initialize with environment variables
scraper = scrape_and_summarize()

# Simple search
result = scraper.run({"query": "machine learning trends"})

# Process results
if result["status"] == "success":
    print(f"✅ Success: {result['successfully_scraped']} sources")
    print(f"📄 Summary: {result['overall_summary'][:200]}...")
```

### Advanced Configuration

```python
# Comprehensive search with file saving
params = {
    "query": "renewable energy innovations 2024",
    "max_results": 10,      # More search results
    "max_urls": 15,         # More sources to analyze
    "save_to_file": True    # Save results to file
}

result = scraper.run(params)

# Access detailed information
print(f"Search engines found {result['total_sources_found']} total sources")
print(f"Successfully processed {result['successfully_scraped']} sources")
print(f"Success rate: {result['successfully_scraped']/result['total_sources_found']*100:.1f}%")

# Access individual source summaries
for source in result['sources']:
    print(f"\n📌 {source['title']}")
    print(f"🔗 {source['url']}")
    print(f"📝 {source['individual_summary'][:150]}...")
```

### Error Handling Patterns

```python
def robust_search(query: str, retries: int = 3) -> Dict[str, Any]:
    """Implement custom retry logic with error handling."""
    
    scraper = scrape_and_summarize()
    
    for attempt in range(retries):
        try:
            result = scraper.run({
                "query": query,
                "max_results": 5 if attempt == 0 else 3,  # Reduce load on retries
                "max_urls": 8 if attempt == 0 else 5
            })
            
            if result["status"] == "success":
                return result
            elif result["status"] == "error":
                print(f"Attempt {attempt + 1} failed: {result['message']}")
                if attempt == retries - 1:
                    return result  # Return final error
            
        except Exception as e:
            print(f"Attempt {attempt + 1} exception: {e}")
            if attempt == retries - 1:
                raise
                
        time.sleep(2 ** attempt)  # Exponential backoff
    
    return {"status": "error", "message": "Max retries exceeded"}

# Usage
result = robust_search("artificial intelligence applications")
```

### Batch Processing

```python
def process_multiple_queries(queries: List[str]) -> List[Dict[str, Any]]:
    """Process multiple queries with rate limiting."""
    
    scraper = scrape_and_summarize()
    results = []
    
    for i, query in enumerate(queries):
        print(f"Processing query {i+1}/{len(queries)}: {query}")
        
        try:
            result = scraper.run({
                "query": query,
                "max_results": 3,        # Reduced for batch processing
                "max_urls": 5,           # Reduced for batch processing  
                "save_to_file": True     # Save each result
            })
            
            results.append(result)
            
            # Rate limiting between requests
            if i < len(queries) - 1:  # Don't sleep after last query
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("Batch processing cancelled")
            break
        except Exception as e:
            print(f"Error processing '{query}': {e}")
            results.append({
                "status": "error",
                "query": query,
                "message": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
    
    return results

# Usage
queries = [
    "sustainable agriculture techniques",
    "quantum computing applications",
    "space exploration technologies"
]

batch_results = process_multiple_queries(queries)
```

### Integration with Data Analysis

```python
import pandas as pd
from datetime import datetime

def create_analysis_dataframe(result: Dict[str, Any]) -> pd.DataFrame:
    """Convert ScraperSage results to pandas DataFrame for analysis."""
    
    if result["status"] != "success":
        return pd.DataFrame()
    
    # Extract source data
    sources_data = []
    for source in result["sources"]:
        sources_data.append({
            "url": source["url"],
            "title": source["title"],
            "content_length": len(source.get("content_preview", "")),
            "summary_length": len(source["individual_summary"]),
            "domain": source["url"].split("/")[2] if "/" in source["url"] else "",
            "scraped_successfully": True
        })
    
    # Add failed sources
    for failed in result.get("failed_sources", []):
        sources_data.append({
            "url": failed["url"],
            "title": "Failed to scrape",
            "content_length": 0,
            "summary_length": 0,
            "domain": failed["url"].split("/")[2] if "/" in failed["url"] else "",
            "scraped_successfully": False
        })
    
    df = pd.DataFrame(sources_data)
    
    # Add metadata
    df["query"] = result["query"]
    df["timestamp"] = pd.to_datetime(result["timestamp"])
    df["total_sources"] = result["total_sources_found"]
    df["success_rate"] = result["successfully_scraped"] / result["total_sources_found"]
    
    return df

# Usage
result = scraper.run({"query": "data science trends", "max_urls": 10})
df = create_analysis_dataframe(result)

# Analyze results
print("Domain distribution:")
print(df["domain"].value_counts())

print("\nSuccess rate by domain:")
success_by_domain = df.groupby("domain")["scraped_successfully"].agg(["count", "sum", "mean"])
print(success_by_domain)
```

---

This API reference provides complete documentation for all public interfaces and common usage patterns. For implementation details and development information, see [DEVELOPMENT.md](DEVELOPMENT.md).