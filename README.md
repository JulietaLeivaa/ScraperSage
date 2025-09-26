# ScraperSage

A comprehensive web scraping and content summarization library that combines Google/DuckDuckGo search with web scraping and AI-powered summarization using multiple providers: **Gemini**, **OpenAI**, **OpenRouter**, and **DeepSeek**.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/ScraperSage.svg)](https://pypi.org/project/ScraperSage/)

## 🚀 Features

- **Multi-Engine Search**: Combines Google (via Serper API) and DuckDuckGo search results
- **Advanced Web Scraping**: Uses Playwright for robust, JavaScript-enabled web scraping  
- **Multiple AI Providers**: Support for Gemini, OpenAI, OpenRouter, and DeepSeek
- **Explicit Model Selection**: Must specify both provider and model - no defaults
- **Dynamic Model Support**: Use any model supported by your chosen provider
- **Parallel Processing**: Concurrent scraping and summarization for improved performance
- **Retry Mechanisms**: Built-in retry logic for reliable operations
- **Structured Output**: Clean JSON output format for easy integration
- **Error Handling**: Comprehensive error handling and graceful degradation
- **Configurable Parameters**: Flexible configuration for different use cases
- **Real-time Processing**: Live status updates during processing

## 🤖 Supported AI Providers

> **Important**: You **must** specify both provider and model - there are no default models.

### Gemini (Google)
- Any Gemini model supported by your API key

### OpenAI
- Any OpenAI model supported by your API key

### OpenRouter
- Any model available on OpenRouter

### DeepSeek
- Any DeepSeek model supported by your API key

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install ScraperSage
```

### Install Playwright Browsers (Required)

```bash
playwright install chromium
```

## 🔑 API Keys Setup

You need API keys for:
1. **Serper API** (for Google Search) - [Get it here](https://serper.dev)
2. **Your chosen AI provider**:
   - **Gemini**: [Google AI Studio](https://aistudio.google.com/app/apikey)
   - **OpenAI**: [OpenAI Platform](https://platform.openai.com/api-keys)
   - **OpenRouter**: [OpenRouter](https://openrouter.ai/keys)
   - **DeepSeek**: [DeepSeek Platform](https://platform.deepseek.com/api-keys)

### Set Environment Variables

```bash
# Required for search
export SERPER_API_KEY="your_serper_api_key"

# Choose your AI provider (set one)
export GEMINI_API_KEY="your_gemini_key"
export OPENAI_API_KEY="your_openai_key" 
export OPENROUTER_API_KEY="your_openrouter_key"
export DEEPSEEK_API_KEY="your_deepseek_key"
```

## 📚 Usage Guide

### Basic Usage - Provider and Model Required

```python
from ScraperSage import scrape_and_summarize

# ✅ CORRECT: Specify both provider and model
scraper = scrape_and_summarize(provider="gemini", model="gemini-1.5-flash")
result = scraper.run({"query": "AI trends 2024"})

# ✅ CORRECT: Using OpenAI
scraper = scrape_and_summarize(provider="openai", model="gpt-4o-mini")
result = scraper.run({"query": "AI trends 2024"})

# ❌ INCORRECT: This will raise an error
# scraper = scrape_and_summarize()  # Missing provider and model
# scraper = scrape_and_summarize(provider="openai")  # Missing model
```

### Get Supported Providers

```python
from ScraperSage import get_supported_providers

# See all supported providers
providers = get_supported_providers()
print(f"Providers: {providers}")
```

### Advanced Configuration

```python
# All parameters with explicit model
params = {
    "query": "machine learning in healthcare",
    "max_results": 8,
    "max_urls": 12,
    "save_to_file": True
}

# Try different providers/models
providers_to_try = [
    {"provider": "gemini", "model": "gemini-1.5-pro"},
    {"provider": "openai", "model": "gpt-4o"},
    {"provider": "openrouter", "model": "anthropic/claude-3.5-sonnet"},
    {"provider": "deepseek", "model": "deepseek-chat"}
]

for config in providers_to_try:
    try:
        scraper = scrape_and_summarize(**config)
        result = scraper.run(params)
        if result["status"] == "success":
            print(f"✅ {config['provider']} with {config['model']} worked!")
            break
    except Exception as e:
        print(f"❌ {config['provider']}/{config['model']} failed: {e}")
        continue
```

## ⚙️ Configuration Parameters

### Constructor Parameters (All Required)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider` | str | ✅ **YES** | AI provider: gemini, openai, openrouter, deepseek |
| `model` | str | ✅ **YES** | Specific model name supported by the provider |
| `serper_api_key` | str | Optional | Serper API key (uses env var if not provided) |
| `provider_api_key` | str | Optional | AI provider API key (uses env var if not provided) |

### Run Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | str | **Required** | The search query to process |
| `max_results` | int | 5 | Maximum search results per engine (1-20) |
| `max_urls` | int | 8 | Maximum URLs to scrape (1-50) |
| `save_to_file` | bool | False | Save results to timestamped JSON file |

## 🚨 Error Handling

### Common Errors and Solutions

```python
from ScraperSage import scrape_and_summarize

# ❌ Missing provider
try:
    scraper = scrape_and_summarize(model="gpt-4o")
except ValueError as e:
    print(f"Error: {e}")
    # Shows: Provider is required. Please specify one of: ['gemini', 'openai', 'openrouter', 'deepseek']

# ❌ Missing model
try:
    scraper = scrape_and_summarize(provider="openai")
except ValueError as e:
    print(f"Error: {e}")
    # Shows: Model is required for openai. Please specify a model for openai provider.
```

### Safe Model Selection Helper

```python
def safe_create_scraper(provider, model):
    """Create scraper with error handling."""
    try:
        scraper = scrape_and_summarize(provider=provider, model=model)
        return scraper
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return None

# Usage
scraper = safe_create_scraper("openai", "gpt-4o-mini")
if scraper:
    result = scraper.run({"query": "your search query"})
```

## 💡 Model Selection Strategy

### Recommended Approach

```python
from ScraperSage import scrape_and_summarize

def create_scraper_with_fallback(provider_configs):
    """Create scraper with provider/model fallbacks."""
    
    for provider_config in provider_configs:
        provider = provider_config["provider"]
        models = provider_config["models"]
        
        for model in models:
            try:
                scraper = scrape_and_summarize(provider=provider, model=model)
                print(f"✅ Success: {provider}/{model}")
                return scraper
            except Exception as e:
                print(f"❌ Failed: {provider}/{model} - {str(e)[:50]}...")
                continue
    
    raise ValueError("No working provider/model combinations found")

# Define your preferences (you need to know the model names)
preferences = [
    {
        "provider": "openai",
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
    },
    {
        "provider": "gemini", 
        "models": ["gemini-1.5-pro", "gemini-1.5-flash"]
    }
]

scraper = create_scraper_with_fallback(preferences)
result = scraper.run({"query": "your search query"})
```

## 📊 Benefits of Explicit Model Selection

### ✅ Advantages
- **No surprises**: You always know which model is being used
- **Cost control**: Explicitly choose cost-effective models
- **Performance predictability**: Know exactly what capabilities you're getting
- **Future-proof**: New models don't change existing behavior
- **Debugging**: Easier to identify model-specific issues
- **Transparency**: Clear model usage in logs and results

### 📈 Best Practices
1. **Always specify both provider and model**
2. **Test models with small queries first**
3. **Implement fallback strategies for reliability**
4. **Monitor costs when using premium models**
5. **Keep model preferences in configuration files**

## 🔄 Changelog

### v1.2.2 (Latest)
- ✅ **REMOVED**: Default model functions and example model listings
- ✅ **BREAKING CHANGE**: Removed `get_default_model()` and made `get_available_models()` return empty
- ✅ **ENHANCED**: Library now requires complete explicit configuration
- ✅ **UPDATED**: Documentation reflects minimal API

### v1.2.0
- ✅ Multiple AI provider support (Gemini, OpenAI, OpenRouter, DeepSeek)
- ✅ Dynamic model support
- ✅ Provider comparison capabilities

## 🤝 Contributing

Areas where you can help:
- 🔧 Add support for more AI providers
- 🎯 Improve model validation and discovery
- 📊 Add model performance benchmarking
- 🧪 Expand test coverage for various models
- 📚 Add more usage examples

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by AkilLabs**

*Now requires explicit provider and model selection with minimal API!*

**📦 Available on PyPI**: [https://pypi.org/project/ScraperSage/](https://pypi.org/project/ScraperSage/)
