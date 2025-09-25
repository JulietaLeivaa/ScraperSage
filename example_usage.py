# Example usage of scrape_and_summarize

import os
import json
from ScraperSage import scrape_and_summarize   # your packaged library

# Set API keys (replace with your actual keys or set as environment variables)
os.environ["SERPER_API_KEY"] = "SERPER_API_KEY"
os.environ["GEMINI_API_KEY"] = "GEMINI_API_KEY"

# Initialize scrape_and_summarize
scraper = scrape_and_summarize(
    serper_api_key=os.getenv("SERPER_API_KEY"),
    gemini_api_key=os.getenv("GEMINI_API_KEY")
)

# Pass parameters as JSON/dict
params = {
    "query": "AI in healthcare",
    "max_results": 5,
    "save_to_file": False   # optional parameter if you want to save JSON
}

# Run the scraper
result_json = scraper.run(params)

# Print structured JSON output
print(json.dumps(result_json, indent=2, ensure_ascii=False))

