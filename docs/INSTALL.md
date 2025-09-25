# Installation Guide for Scrape and Summarize

## Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **pip (Python package manager)**
   ```bash
   pip --version
   ```

## Step-by-Step Installation

### 1. Install the Package

From the project directory:

```bash
# Install in development mode (recommended for local development)
pip install -e .

# OR install normally
pip install .
```

### 2. Install Playwright Browsers

Scrape and Summarize uses Playwright for web scraping, which requires browser installation:

```bash
playwright install chromium
```

### 3. Set Up API Keys

You need two API keys:

#### A. Serper API Key (for Google Search)
1. Go to https://serper.dev
2. Sign up for a free account
3. Copy your API key

#### B. Google Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Create a new API key
3. Copy your API key

#### C. Set Environment Variables

**On Windows:**
```cmd
set SERPER_API_KEY=your_actual_serper_key
set GEMINI_API_KEY=your_actual_gemini_key
```

**On macOS/Linux:**
```bash
export SERPER_API_KEY="your_actual_serper_key"
export GEMINI_API_KEY="your_actual_gemini_key"
```

**Or create a .env file:**
```
SERPER_API_KEY=your_actual_serper_key
GEMINI_API_KEY=your_actual_gemini_key
```

### 4. Test the Installation

Run the example usage file:

```bash
python example_usage.py
```

Or test with a simple script:

```python
from ScraperSage import scrape_and_summarize
import os

# Test initialization
try:
    scraper = scrape_and_summarize()
    print("✅ Scrape and Summarize installed successfully!")
    
    # Quick test
    result = scraper.run({"query": "test", "max_results": 1})
    print(f"✅ Test search completed with status: {result['status']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

## Troubleshooting

### Common Issues:

1. **Import Error**: Make sure you installed the package correctly
   ```bash
   pip list | grep scrape-and-summarize
   ```

2. **API Key Error**: Ensure your environment variables are set
   ```python
   import os
   print("Serper Key:", "SET" if os.getenv("SERPER_API_KEY") else "NOT SET")
   print("Gemini Key:", "SET" if os.getenv("GEMINI_API_KEY") else "NOT SET")
   ```

3. **Playwright Error**: Install browsers
   ```bash
   playwright install chromium
   ```

4. **Permission Error**: Run with appropriate permissions or use virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

## Building for Distribution

To build the package for distribution:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# This creates dist/ directory with .whl and .tar.gz files
```

## Uninstallation

```bash
pip uninstall scrape-and-summarize
```