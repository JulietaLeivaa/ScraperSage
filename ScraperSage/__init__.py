"""
ScraperSage - A comprehensive web scraping and content summarization library with AI-powered features.

Supports multiple AI providers: Gemini, OpenAI, OpenRouter, and DeepSeek.
"""

from .scraper_sage import scrape_and_summarize
from .ai_providers import create_ai_provider, get_supported_providers, get_available_models

__version__ = "1.2.2"
__all__ = ["scrape_and_summarize", "create_ai_provider", "get_supported_providers", "get_available_models"]