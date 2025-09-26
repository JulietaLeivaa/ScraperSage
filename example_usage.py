import os
from ScraperSage import scrape_and_summarize

# ✅ Set your API keys
os.environ["SERPER_API_KEY"] = "SERPER_API_KEY"
os.environ["GEMINI_API_KEY"] = "GEMINI_API_KEY"

# ✅ Initialize scraper with Gemini
scraper = scrape_and_summarize(provider="gemini", model="gemini-2.0-flash")

# 🔍 Run a search and summarization
result = scraper.run({
    "query": "latest developments in artificial intelligence 2024",
    "max_results": 5,
    "max_urls": 8,
    "save_to_file": True
})

# ✅ Just print the overall summary
print("\n📄 OVERALL SUMMARY:\n")
print(result["overall_summary"])
