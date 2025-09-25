"""
scrape_and_summarize - A comprehensive web scraping and content summarization class.
"""

import os
import requests
from ddgs import DDGS
from playwright.sync_api import sync_playwright
import google.generativeai as genai
from bs4 import BeautifulSoup
from typing import List, Optional, Dict, Any
import time
import json
from tenacity import retry, stop_after_attempt, wait_exponential
from concurrent.futures import ThreadPoolExecutor, as_completed


class scrape_and_summarize:
    """
    A comprehensive web scraping and content summarization class that combines
    Google/DuckDuckGo search with web scraping and AI-powered summarization.
    """
    
    def __init__(self, serper_api_key: str = None, gemini_api_key: str = None):
        """
        Initialize scrape_and_summarize with API keys.
        
        Args:
            serper_api_key (str): API key for Serper (Google Search)
            gemini_api_key (str): API key for Google Gemini AI
        """
        self.serper_api_key = serper_api_key or os.getenv("SERPER_API_KEY")
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        
        # Validate API keys are present
        if not self.serper_api_key or not self.gemini_api_key:
            raise ValueError("Missing required API keys. Please provide SERPER_API_KEY and GEMINI_API_KEY.")
        
        # Configure Gemini AI
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _search_google(self, query: str, max_results: int = 5) -> List[str]:
        """Search Google using Serper API with retry mechanism."""
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": self.serper_api_key, "Content-Type": "application/json"}
        payload = {"q": query}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            results = response.json()
            return [result["link"] for result in results.get("organic", [])][:max_results]
        except requests.exceptions.RequestException as e:
            return []

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _search_duckduckgo(self, query: str, max_results: int = 5) -> List[str]:
        """Search DuckDuckGo with retry mechanism."""
        try:
            with DDGS() as ddgs:
                return [result["href"] for result in ddgs.text(query, max_results=max_results)]
        except Exception as e:
            print(f"DuckDuckGo Search Error: {e}")
            return []

    def _scrape_with_playwright(self, url: str) -> Optional[Dict[str, str]]:
        """Scrape webpage content using Playwright with improved error handling."""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = context.new_page()
                
                # Set longer timeout and wait for network idle
                page.goto(url, timeout=30000, wait_until='networkidle')
                page.wait_for_load_state('load')
                
                # Wait for content to load
                page.wait_for_selector('body', timeout=10000)
                html_content = page.content()
                
                # Get page title
                title = page.title()
                
                context.close()
                browser.close()
            
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'nav', 'footer']):
                element.decompose()
                
            # Get text from multiple elements
            text_elements = []
            for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'article', 'section']):
                text = element.get_text(strip=True)
                if text and len(text) > 50:  # Filter out very short snippets
                    text_elements.append(text)
            
            content = "\n\n".join(text_elements)
            
            return {
                "url": url,
                "title": title,
                "content": content[:4000]  # Limit content per URL
            }
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            return None

    def _scrape_multiple_urls(self, urls: List[str], max_urls: int = 8) -> List[Dict[str, str]]:
        """Scrape multiple URLs in parallel."""
        scraped_data = []
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_url = {executor.submit(self._scrape_with_playwright, url): url 
                            for url in urls[:max_urls]}
            
            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    scraped_data.append(result)
        
        return scraped_data

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _summarize_with_gemini(self, content: str, is_individual: bool = False, source_title: str = "") -> str:
        """Summarize content using Gemini AI with retry mechanism."""
        if not content:
            return "No content to summarize."
        
        try:
            if is_individual:
                prompt = (
                    f"Please provide a concise and focused summary of the following content from '{source_title}'. "
                    "Extract the key points, main ideas, and important information in a clear and structured way:\n\n"
                    f"{content}"
                )
            else:
                prompt = (
                    "Please provide a comprehensive summary of the following content from multiple sources, "
                    "highlighting the main points and key information. Organize the summary in a clear structure:\n\n"
                    f"{content}"
                )
            response = self.model.generate_content(prompt)
            return response.text if response else "Failed to generate summary."
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                print(f"Gemini AI Quota Error: {e}")
                return f"Summary unavailable due to API quota limits. Original content length: {len(content)} characters."
            else:
                print(f"Gemini AI Error: {e}")
                return "Failed to generate summary due to an error."

    def _generate_individual_summaries(self, scraped_results: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Generate individual summaries for each scraped result."""
        print("Generating individual summaries for each source...")
        
        def summarize_single_source(result):
            summary = self._summarize_with_gemini(result["content"], is_individual=True, source_title=result["title"])
            return {
                **result,
                "individual_summary": summary
            }
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_result = {executor.submit(summarize_single_source, result): result 
                              for result in scraped_results}
            
            summarized_results = []
            for future in as_completed(future_to_result):
                summarized_results.append(future.result())
        
        return summarized_results

    def _save_json_output(self, data: dict, query: str) -> str:
        """Save JSON output to a file and return filename."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        # Clean query for filename
        clean_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_query = clean_query.replace(' ', '_')[:50]  # Limit filename length
        
        filename = f"search_results_{clean_query}_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return filename
        except Exception as e:
            print(f"Failed to save JSON file: {e}")
            return ""
    
    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the scraper with provided parameters.
        
        Args:
            params (Dict[str, Any]): Parameters dictionary containing:
                - query (str): Search query
                - max_results (int, optional): Maximum number of search results (default: 5)
                - max_urls (int, optional): Maximum number of URLs to scrape (default: 8)
                - save_to_file (bool, optional): Whether to save results to JSON file (default: False)
        
        Returns:
            Dict[str, Any]: Structured JSON result containing scraped data and summaries
        """
        try:
            query = params.get("query")
            if not query:
                raise ValueError("Query parameter is required")
            
            max_results = params.get("max_results", 5)
            max_urls = params.get("max_urls", 8)
            save_to_file = params.get("save_to_file", False)
            
            print(f"Searching for: {query}")
            print("Searching multiple sources...")

            # Search using both engines
            google_results = self._search_google(query, max_results)
            duckduckgo_results = self._search_duckduckgo(query, max_results)

            # Combine and deduplicate results
            all_urls = list(dict.fromkeys(google_results + duckduckgo_results))

            if not all_urls:
                return {
                    "status": "error",
                    "message": "No search results found",
                    "query": query,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "sources": [],
                    "summary": ""
                }

            print(f"Found {len(all_urls)} unique URLs. Starting content scraping...")
            scraped_results = self._scrape_multiple_urls(all_urls, max_urls)

            if not scraped_results:
                return {
                    "status": "error",
                    "message": "Failed to scrape content from any of the URLs",
                    "query": query,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "sources": [{"url": url, "scraped": False, "error": "Failed to scrape"} for url in all_urls],
                    "summary": ""
                }

            print(f"Successfully scraped {len(scraped_results)} pages")

            # Generate individual summaries for each source
            scraped_results_with_summaries = self._generate_individual_summaries(scraped_results)

            # Combine content from all sources
            combined_content = "\n\nSOURCE SEPARATION\n\n".join(
                f"From {result['title']}:\n{result['content']}"
                for result in scraped_results_with_summaries
            )

            print("Generating comprehensive summary...")
            overall_summary = self._summarize_with_gemini(combined_content)
            
            # Create structured JSON output
            structured_result = {
                "status": "success",
                "query": query,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_sources_found": len(all_urls),
                "successfully_scraped": len(scraped_results_with_summaries),
                "sources": [
                    {
                        "url": result["url"],
                        "title": result["title"],
                        "content_preview": result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"],
                        "individual_summary": result["individual_summary"],
                        "scraped": True
                    }
                    for result in scraped_results_with_summaries
                ],
                "failed_sources": [
                    {"url": url, "scraped": False}
                    for url in all_urls
                    if url not in [r["url"] for r in scraped_results_with_summaries]
                ],
                "overall_summary": overall_summary,
                "metadata": {
                    "google_results_count": len(google_results),
                    "duckduckgo_results_count": len(duckduckgo_results),
                    "total_unique_urls": len(all_urls),
                    "processing_time": "Real-time processing completed"
                }
            }
            
            # Save to file if requested
            if save_to_file:
                filename = self._save_json_output(structured_result, query)
                if filename:
                    structured_result["saved_file"] = filename
                    print(f"Results saved to: {filename}")
            
            return structured_result

        except KeyboardInterrupt:
            return {
                "status": "cancelled",
                "message": "Operation cancelled by user",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"An unexpected error occurred: {str(e)}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }