"""
ScraperSage - Main scraper class with explicit AI provider and model requirement.
"""

import os
import json
import time
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from ddgs import DDGS  # Changed from duckduckgo_search to ddgs
from tenacity import retry, stop_after_attempt, wait_exponential

from .ai_providers import create_ai_provider, get_supported_providers, get_available_models


class scrape_and_summarize:
    """Main scraper class with explicit AI provider and model requirement."""
    
    def __init__(self, serper_api_key: str = None, provider: str = None, 
                 model: str = None, provider_api_key: str = None):
        """
        Initialize the scraper with explicit AI provider and model.
        
        Args:
            serper_api_key: API key for Serper (Google search)
            provider: AI provider name (gemini, openai, openrouter, deepseek) - REQUIRED
            model: Specific model to use - REQUIRED
            provider_api_key: API key for the AI provider (optional, uses env vars)
        """
        # Set up search API
        self.serper_api_key = serper_api_key or os.getenv("SERPER_API_KEY")
        if not self.serper_api_key:
            raise ValueError("SERPER_API_KEY is required. Set it as environment variable or pass explicitly.")
        
        # Validate provider is specified
        if not provider:
            raise ValueError(f"Provider is required. Please specify one of: {get_supported_providers()}")
        
        # Validate model is specified
        if not model:
            raise ValueError(f"Model is required for {provider}. Please specify a model for {provider} provider.")
        
        # Validate and set up AI provider
        if provider not in get_supported_providers():
            raise ValueError(f"Unsupported provider: {provider}. Available: {get_supported_providers()}")
        
        self.provider_name = provider
        self.model_name = model
        
        # Create AI provider instance
        try:
            self.ai_provider = create_ai_provider(provider, provider_api_key, model)
            print(f"🤖 Initialized {provider} with model: {self.ai_provider.model}")
        except Exception as e:
            raise ValueError(f"Failed to initialize {provider} with model {model}: {str(e)}")
    
    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the scraping and summarization process.
        
        Args:
            params: Configuration parameters including query, max_results, etc.
            
        Returns:
            Dictionary with results and metadata
        """
        # Extract parameters
        query = params.get("query")
        if not query:
            return {"status": "error", "message": "Query is required"}
        
        max_results = params.get("max_results", 5)
        max_urls = params.get("max_urls", 8)
        save_to_file = params.get("save_to_file", False)
        
        print(f"🔍 Starting search for: '{query}'")
        print(f"🤖 Using AI Provider: {self.provider_name} ({self.ai_provider.model})")
        
        try:
            # Search for URLs
            urls = self._search_urls(query, max_results)
            
            if not urls:
                return {
                    "status": "error",
                    "message": "No search results found",
                    "query": query,
                    "provider": self.provider_name,
                    "model": self.ai_provider.model
                }
            
            # Limit URLs to scrape
            urls_to_scrape = urls[:max_urls]
            print(f"📋 Found {len(urls)} total URLs, scraping top {len(urls_to_scrape)}")
            
            # Scrape and summarize
            sources, failed_sources = self._scrape_and_summarize_urls(urls_to_scrape, query)
            
            # Generate overall summary
            if sources:
                overall_summary = self._generate_overall_summary(sources, query)
            else:
                overall_summary = "No content was successfully scraped and summarized."
            
            # Prepare result
            result = {
                "status": "success",
                "query": query,
                "provider": self.provider_name,
                "model": self.ai_provider.model,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_sources_found": len(urls),
                "successfully_scraped": len(sources),
                "sources": sources,
                "failed_sources": failed_sources,
                "overall_summary": overall_summary,
                "metadata": {
                    "provider_info": {
                        "provider": self.provider_name,
                        "model": self.ai_provider.model,
                        "provider_type": self.ai_provider.__class__.__name__.replace("Provider", "")
                    },
                    "processing_time": "Real-time processing completed",
                    "success_rate": f"{(len(sources) / len(urls_to_scrape)) * 100:.0f}%" if urls_to_scrape else "0%"
                }
            }
            
            # Save to file if requested
            if save_to_file:
                filename = self._save_results(result)
                result["metadata"]["saved_filename"] = filename
                print(f"💾 Results saved to: {filename}")
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Processing failed: {str(e)}",
                "query": query,
                "provider": self.provider_name,
                "model": self.ai_provider.model,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def _search_urls(self, query: str, max_results: int) -> List[str]:
        """Search for URLs using Google and DuckDuckGo."""
        urls = []
        
        # Google Search via Serper
        try:
            google_urls = self._google_search(query, max_results)
            urls.extend(google_urls)
            print(f"📍 Google: Found {len(google_urls)} results")
        except Exception as e:
            print()
    
        # DuckDuckGo Search
        try:
            ddg_urls = self._duckduckgo_search(query, max_results)
            urls.extend(ddg_urls)
            print(f"📍 DuckDuckGo: Found {len(ddg_urls)} results")
        except Exception as e:
            print()
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        return unique_urls
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _google_search(self, query: str, max_results: int) -> List[str]:
        """Search Google via Serper API."""
        url = "https://google.serper.dev/search"
        
        payload = json.dumps({
            "q": query,
            "num": max_results
        })
        
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        organic_results = data.get("organic", [])
        
        return [result.get("link", "") for result in organic_results if result.get("link")]
    
    def _duckduckgo_search(self, query: str, max_results: int) -> List[str]:
        """Search DuckDuckGo."""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                return [result.get("href", "") for result in results if result.get("href")]
        except Exception as e:
            print(f"DuckDuckGo search error: {str(e)}")
            return []
    
    def _scrape_and_summarize_urls(self, urls: List[str], query: str) -> tuple:
        """Scrape URLs and generate summaries concurrently."""
        sources = []
        failed_sources = []
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_url = {
                executor.submit(self._scrape_and_summarize_single, url, query): url 
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result:
                        sources.append(result)
                        print(f"✅ Scraped: {url}")
                    else:
                        failed_sources.append({"url": url, "scraped": False})
                        print(f"❌ Failed: {url}")
                except Exception as e:
                    failed_sources.append({"url": url, "scraped": False, "error": str(e)})
                    print(f"💥 Error scraping {url}: {str(e)}")
        
        return sources, failed_sources
    
    def _scrape_and_summarize_single(self, url: str, query: str) -> Optional[Dict]:
        """Scrape a single URL and generate summary."""
        try:
            # Scrape content
            content = self._scrape_url_content(url)
            if not content or len(content.strip()) < 100:
                return None
            
            # Generate summary
            summary = self.ai_provider.generate_summary(content, query)
            
            return {
                "url": url,
                "title": self._extract_title(content),
                "content_preview": content[:500] + "..." if len(content) > 500 else content,
                "individual_summary": summary,
                "scraped": True
            }
            
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return None
    
    def _scrape_url_content(self, url: str) -> str:
        """Scrape content from URL using Playwright."""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.set_default_timeout(30000)
                
                page.goto(url, wait_until='domcontentloaded')
                page.wait_for_timeout(2000)
                
                content = page.content()
                browser.close()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # Remove unwanted elements
                for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                    element.decompose()
                
                # Extract text
                text = soup.get_text()
                
                # Clean up
                lines = (line.strip() for line in text.splitlines())
                text = ' '.join(line for line in lines if line)
                
                # Limit content size
                return text[:8000] if len(text) > 8000 else text
                
        except Exception as e:
            raise Exception(f"Failed to scrape {url}: {str(e)}")
    
    def _extract_title(self, content: str) -> str:
        """Extract title from content."""
        soup = BeautifulSoup(content, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else "No title found"
    
    def _generate_overall_summary(self, sources: List[Dict], query: str) -> str:
        """Generate overall summary from all sources."""
        combined_summaries = "\n\n".join([
            f"Source {i+1}: {source['individual_summary']}" 
            for i, source in enumerate(sources)
        ])
        
        overall_prompt = f"""
        Based on the following individual summaries related to "{query}", create a comprehensive overall summary:
        
        {combined_summaries[:6000]}
        
        Provide a cohesive summary that synthesizes the main themes, key insights, and important information across all sources.
        """
        
        return self.ai_provider.generate_summary(overall_prompt, f"Overall summary for: {query}")
    
    def _save_results(self, results: Dict) -> str:
        """Save results to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_safe = "".join(c for c in results["query"] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        query_safe = query_safe.replace(' ', '_')[:50]
        
        filename = f"scraper_results_{query_safe}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about current provider and model."""
        return {
            "provider": self.provider_name,
            "model": self.ai_provider.model,
            "supported_providers": get_supported_providers()
        }