# ScraperSage Examples

This document provides comprehensive examples and real-world use cases for ScraperSage, demonstrating various configurations and integration patterns.

## 📋 Table of Contents

- [Basic Examples](#basic-examples)
- [Advanced Configurations](#advanced-configurations)
- [Real-World Use Cases](#real-world-use-cases)
- [Integration Patterns](#integration-patterns)
- [Performance Optimization](#performance-optimization)
- [Error Handling Strategies](#error-handling-strategies)
- [Automation Scripts](#automation-scripts)
- [Data Analysis Integration](#data-analysis-integration)

## 🚀 Basic Examples

### Simple Search and Summarize

```python
from ScraperSage import scrape_and_summarize
import json

# Initialize scraper
scraper = scrape_and_summarize()

# Basic search
result = scraper.run({
    "query": "Python web scraping best practices"
})

# Display results
print(f"Status: {result['status']}")
print(f"Sources found: {result['total_sources_found']}")
print(f"Successfully scraped: {result['successfully_scraped']}")
print(f"\nSummary:\n{result['overall_summary']}")
```

### Quick Research Helper

```python
def quick_research(topic: str) -> str:
    """Get a quick summary of any topic."""
    scraper = scrape_and_summarize()
    
    result = scraper.run({
        "query": topic,
        "max_results": 3,  # Quick results
        "max_urls": 5      # Light processing
    })
    
    if result["status"] == "success":
        return result["overall_summary"]
    else:
        return f"Research failed: {result['message']}"

# Usage examples
print(quick_research("blockchain technology advantages"))
print(quick_research("renewable energy statistics 2024"))
print(quick_research("machine learning career paths"))
```

### Save and Review Pattern

```python
import os
import json
from datetime import datetime

def research_and_save(query: str, filename: str = None) -> dict:
    """Research a topic and save detailed results."""
    scraper = scrape_and_summarize()
    
    # Generate filename if not provided
    if not filename:
        safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-')).strip()
        safe_query = safe_query.replace(' ', '_')[:30]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_{safe_query}_{timestamp}.json"
    
    result = scraper.run({
        "query": query,
        "max_results": 5,
        "max_urls": 8,
        "save_to_file": True
    })
    
    # Additional processing and saving
    if result["status"] == "success":
        # Create detailed report
        report = {
            "research_query": query,
            "timestamp": result["timestamp"],
            "executive_summary": result["overall_summary"][:500] + "...",
            "source_count": result["successfully_scraped"],
            "key_sources": [
                {
                    "title": source["title"],
                    "url": source["url"],
                    "summary": source["individual_summary"][:200] + "..."
                }
                for source in result["sources"][:5]  # Top 5 sources
            ],
            "full_results": result
        }
        
        # Save detailed report
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Research completed and saved to: {filename}")
        return report
    else:
        print(f"Research failed: {result['message']}")
        return result

# Usage
report = research_and_save("artificial intelligence in healthcare")
```

## ⚙️ Advanced Configurations

### High-Quality Research Mode

```python
def deep_research(query: str, save_results: bool = True) -> dict:
    """Comprehensive research with maximum quality settings."""
    scraper = scrape_and_summarize()
    
    # Maximum quality configuration
    params = {
        "query": query,
        "max_results": 15,    # Get more search results
        "max_urls": 25,       # Process more sources
        "save_to_file": save_results
    }
    
    print(f"Starting deep research on: {query}")
    print("This may take several minutes due to comprehensive analysis...")
    
    result = scraper.run(params)
    
    if result["status"] == "success":
        # Calculate quality metrics
        avg_summary_length = sum(len(s["individual_summary"]) for s in result["sources"]) / len(result["sources"])
        unique_domains = len(set(s["url"].split("/")[2] for s in result["sources"]))
        
        print(f"\n📊 Research Quality Metrics:")
        print(f"  Sources processed: {result['successfully_scraped']}")
        print(f"  Unique domains: {unique_domains}")
        print(f"  Average summary length: {avg_summary_length:.0f} characters")
        print(f"  Overall summary length: {len(result['overall_summary'])} characters")
        print(f"  Success rate: {result['successfully_scraped']/result['total_sources_found']*100:.1f}%")
    
    return result

# Usage
result = deep_research("quantum computing commercial applications")
```

### Fast Scanning Mode

```python
def quick_scan(query: str) -> dict:
    """Fast scanning for quick insights."""
    scraper = scrape_and_summarize()
    
    # Speed-optimized configuration
    params = {
        "query": query,
        "max_results": 3,     # Fewer search results
        "max_urls": 4,        # Minimal processing
        "save_to_file": False # No file I/O delay
    }
    
    import time
    start_time = time.time()
    
    result = scraper.run(params)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    if result["status"] == "success":
        print(f"⚡ Quick scan completed in {processing_time:.1f} seconds")
        print(f"📄 Key insights: {result['overall_summary'][:300]}...")
    
    return result

# Usage for rapid information gathering
queries = [
    "stock market trends today",
    "cryptocurrency news latest",
    "tech startup funding 2024"
]

for query in queries:
    print(f"\n🔍 Scanning: {query}")
    quick_scan(query)
    time.sleep(1)  # Brief pause between queries
```

### Multi-Language Research

```python
def multilang_research(base_query: str, languages: list = None) -> dict:
    """Research a topic across multiple languages."""
    if languages is None:
        languages = ["en", "es", "fr", "de", "zh"]
    
    scraper = scrape_and_summarize()
    all_results = []
    
    for lang in languages:
        # Modify query for language
        if lang == "en":
            query = base_query
        else:
            # Add language hint (this is a simple approach)
            query = f"{base_query} {lang} language"
        
        print(f"Researching in {lang.upper()}...")
        
        result = scraper.run({
            "query": query,
            "max_results": 3,
            "max_urls": 5
        })
        
        if result["status"] == "success":
            result["language"] = lang
            all_results.append(result)
        
        time.sleep(1)  # Rate limiting
    
    # Combine results
    combined_result = {
        "base_query": base_query,
        "languages_searched": len(all_results),
        "total_sources": sum(r["successfully_scraped"] for r in all_results),
        "results_by_language": all_results,
        "combined_summary": "\n\n".join(f"[{r['language'].upper()}] {r['overall_summary'][:200]}..." for r in all_results)
    }
    
    return combined_result

# Usage
multilang_results = multilang_research("renewable energy policies")
```

## 🌍 Real-World Use Cases

### Market Research Assistant

```python
class MarketResearchAssistant:
    """Professional market research using ScraperSage."""
    
    def __init__(self):
        self.scraper = scrape_and_summarize()
        self.research_history = []
    
    def analyze_market(self, product: str, competitors: list = None, market_size: bool = True) -> dict:
        """Comprehensive market analysis."""
        queries = [f"{product} market analysis 2024"]
        
        if market_size:
            queries.append(f"{product} market size trends")
        
        if competitors:
            for competitor in competitors[:3]:  # Limit to top 3
                queries.append(f"{competitor} {product} strategy")
        
        results = {}
        for i, query in enumerate(queries):
            print(f"Analyzing: {query} ({i+1}/{len(queries)})")
            
            result = self.scraper.run({
                "query": query,
                "max_results": 6,
                "max_urls": 10,
                "save_to_file": True
            })
            
            results[query] = result
            time.sleep(2)  # Respectful rate limiting
        
        # Generate market report
        report = self._generate_market_report(product, results)
        self.research_history.append(report)
        
        return report
    
    def _generate_market_report(self, product: str, results: dict) -> dict:
        """Generate structured market report."""
        successful_results = [r for r in results.values() if r["status"] == "success"]
        
        if not successful_results:
            return {"error": "No successful research results"}
        
        total_sources = sum(r["successfully_scraped"] for r in successful_results)
        
        # Extract key insights
        all_summaries = [r["overall_summary"] for r in successful_results]
        combined_insights = "\n\n---\n\n".join(all_summaries)
        
        report = {
            "product": product,
            "research_date": successful_results[0]["timestamp"],
            "sources_analyzed": total_sources,
            "research_queries": len(results),
            "executive_summary": combined_insights[:1000] + "..." if len(combined_insights) > 1000 else combined_insights,
            "detailed_results": results,
            "recommendations": self._extract_recommendations(all_summaries)
        }
        
        return report
    
    def _extract_recommendations(self, summaries: list) -> list:
        """Extract actionable recommendations from summaries."""
        # Simple keyword-based recommendation extraction
        recommendations = []
        
        for summary in summaries:
            if "recommend" in summary.lower():
                sentences = summary.split('. ')
                for sentence in sentences:
                    if "recommend" in sentence.lower():
                        recommendations.append(sentence.strip())
        
        return recommendations[:5]  # Top 5 recommendations

# Usage
assistant = MarketResearchAssistant()

report = assistant.analyze_market(
    product="electric vehicles",
    competitors=["Tesla", "BMW", "Mercedes"],
    market_size=True
)

print(f"Market Research Report for {report['product']}")
print(f"Sources analyzed: {report['sources_analyzed']}")
print(f"Executive Summary: {report['executive_summary'][:500]}...")
```

### News Monitoring System

```python
import schedule
import time
from datetime import datetime, timedelta
from collections import defaultdict

class NewsMonitor:
    """Automated news monitoring and alerting system."""
    
    def __init__(self, keywords: list, alert_threshold: int = 5):
        self.scraper = scrape_and_summarize()
        self.keywords = keywords
        self.alert_threshold = alert_threshold
        self.news_history = defaultdict(list)
        self.alerts = []
    
    def monitor_keyword(self, keyword: str) -> dict:
        """Monitor news for a specific keyword."""
        query = f"{keyword} news latest 24 hours"
        
        result = self.scraper.run({
            "query": query,
            "max_results": 5,
            "max_urls": 8,
            "save_to_file": False
        })
        
        if result["status"] == "success":
            # Store in history
            self.news_history[keyword].append({
                "timestamp": datetime.now(),
                "sources_found": result["successfully_scraped"],
                "summary": result["overall_summary"],
                "top_sources": result["sources"][:3]
            })
            
            # Check for alerts
            if result["successfully_scraped"] >= self.alert_threshold:
                alert = {
                    "keyword": keyword,
                    "timestamp": datetime.now(),
                    "source_count": result["successfully_scraped"],
                    "summary": result["overall_summary"][:300] + "...",
                    "urgency": "high" if result["successfully_scraped"] > 10 else "medium"
                }
                self.alerts.append(alert)
                self._send_alert(alert)
        
        return result
    
    def monitor_all_keywords(self):
        """Monitor all configured keywords."""
        print(f"🔍 Starting monitoring cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for keyword in self.keywords:
            print(f"  Monitoring: {keyword}")
            try:
                result = self.monitor_keyword(keyword)
                if result["status"] == "success":
                    print(f"    ✅ Found {result['successfully_scraped']} sources")
                else:
                    print(f"    ❌ {result['message']}")
            except Exception as e:
                print(f"    💥 Error: {e}")
            
            time.sleep(1)  # Rate limiting
        
        print("🏁 Monitoring cycle completed\n")
    
    def _send_alert(self, alert: dict):
        """Send alert notification (customize as needed)."""
        print(f"🚨 ALERT: High activity for '{alert['keyword']}'")
        print(f"   Sources: {alert['source_count']}")
        print(f"   Summary: {alert['summary']}")
        print(f"   Urgency: {alert['urgency']}")
        
        # Here you could integrate with:
        # - Email notifications
        # - Slack/Discord webhooks  
        # - SMS services
        # - Custom APIs
    
    def get_trend_report(self, days: int = 7) -> dict:
        """Generate trend report for the last N days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        trends = {}
        for keyword, history in self.news_history.items():
            recent_history = [
                entry for entry in history 
                if entry["timestamp"] > cutoff_date
            ]
            
            if recent_history:
                avg_sources = sum(entry["sources_found"] for entry in recent_history) / len(recent_history)
                total_mentions = len(recent_history)
                
                trends[keyword] = {
                    "mentions": total_mentions,
                    "avg_sources_per_mention": avg_sources,
                    "trend": "rising" if avg_sources > 5 else "stable",
                    "last_summary": recent_history[-1]["summary"][:200] + "..."
                }
        
        return trends

# Usage
monitor = NewsMonitor([
    "artificial intelligence breakthrough",
    "climate change policy",
    "cryptocurrency regulation",
    "space exploration news"
])

# Manual monitoring
monitor.monitor_all_keywords()

# Scheduled monitoring (uncomment to enable)
# schedule.every(30).minutes.do(monitor.monitor_all_keywords)
# 
# while True:
#     schedule.run_pending()
#     time.sleep(1)
```

### Academic Research Helper

```python
class AcademicResearcher:
    """Academic research assistant for scholarly work."""
    
    def __init__(self):
        self.scraper = scrape_and_summarize()
        self.citations = []
        self.research_papers = []
    
    def literature_review(self, topic: str, focus_areas: list = None) -> dict:
        """Conduct literature review on academic topic."""
        queries = [f"{topic} academic research recent"]
        
        if focus_areas:
            for area in focus_areas:
                queries.append(f"{topic} {area} scholarly articles")
        
        # Add methodological queries
        queries.extend([
            f"{topic} methodology approaches",
            f"{topic} research findings 2023 2024",
            f"{topic} literature review systematic"
        ])
        
        results = {}
        for query in queries:
            print(f"Searching academic sources: {query}")
            
            result = self.scraper.run({
                "query": query,
                "max_results": 8,   # Academic sources are often fewer but higher quality
                "max_urls": 12,     # Process more for comprehensive coverage
                "save_to_file": True
            })
            
            results[query] = result
            time.sleep(2)  # Respectful rate limiting
        
        # Generate literature review
        review = self._generate_literature_review(topic, results)
        return review
    
    def _generate_literature_review(self, topic: str, results: dict) -> dict:
        """Generate structured literature review."""
        successful_results = [r for r in results.values() if r["status"] == "success"]
        
        if not successful_results:
            return {"error": "No successful research results"}
        
        # Extract academic sources (filter by domain)
        academic_domains = ['.edu', '.org', 'scholar', 'researchgate', 'academia', 'pubmed']
        academic_sources = []
        
        for result in successful_results:
            for source in result["sources"]:
                if any(domain in source["url"].lower() for domain in academic_domains):
                    academic_sources.append(source)
        
        # Combine all summaries for thematic analysis
        all_summaries = [r["overall_summary"] for r in successful_results]
        
        review = {
            "topic": topic,
            "research_date": successful_results[0]["timestamp"],
            "total_sources": sum(r["successfully_scraped"] for r in successful_results),
            "academic_sources": len(academic_sources),
            "search_queries": len(results),
            "literature_overview": self._synthesize_literature(all_summaries),
            "key_themes": self._extract_themes(all_summaries),
            "academic_sources_details": academic_sources[:10],  # Top 10 academic sources
            "research_gaps": self._identify_gaps(all_summaries),
            "full_results": results
        }
        
        return review
    
    def _synthesize_literature(self, summaries: list) -> str:
        """Synthesize literature findings."""
        combined = " ".join(summaries)
        # In a real implementation, you might use the AI to further synthesize
        return combined[:2000] + "..." if len(combined) > 2000 else combined
    
    def _extract_themes(self, summaries: list) -> list:
        """Extract key research themes."""
        # Simple keyword frequency analysis
        from collections import Counter
        import re
        
        all_text = " ".join(summaries).lower()
        words = re.findall(r'\b\w+\b', all_text)
        
        # Filter academic keywords
        academic_keywords = [
            'research', 'study', 'analysis', 'findings', 'methodology',
            'approach', 'framework', 'theory', 'empirical', 'systematic'
        ]
        
        relevant_words = [w for w in words if len(w) > 4 and w not in academic_keywords]
        common_themes = Counter(relevant_words).most_common(10)
        
        return [{"theme": word, "frequency": freq} for word, freq in common_themes]
    
    def _identify_gaps(self, summaries: list) -> list:
        """Identify potential research gaps."""
        gaps = []
        gap_indicators = [
            "limited research", "further investigation", "future work",
            "gap in", "insufficient", "more research needed", "understudied"
        ]
        
        for summary in summaries:
            sentences = summary.split('. ')
            for sentence in sentences:
                if any(indicator in sentence.lower() for indicator in gap_indicators):
                    gaps.append(sentence.strip())
        
        return gaps[:5]  # Top 5 identified gaps

# Usage
researcher = AcademicResearcher()

review = researcher.literature_review(
    topic="machine learning interpretability",
    focus_areas=["explainable AI", "model transparency", "algorithmic fairness"]
)

print(f"Literature Review: {review['topic']}")
print(f"Sources analyzed: {review['total_sources']}")
print(f"Academic sources: {review['academic_sources']}")
print(f"Key themes: {[t['theme'] for t in review['key_themes'][:5]]}")
```

## 🔗 Integration Patterns

### Flask Web Application

```python
from flask import Flask, request, jsonify, render_template
from ScraperSage import scrape_and_summarize
import json
from datetime import datetime

app = Flask(__name__)
scraper = scrape_and_summarize()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/research', methods=['POST'])
def research_endpoint():
    """API endpoint for research requests."""
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        # Configure based on request parameters
        params = {
            "query": query,
            "max_results": data.get('max_results', 5),
            "max_urls": data.get('max_urls', 8),
            "save_to_file": data.get('save_to_file', False)
        }
        
        result = scraper.run(params)
        
        # Format response for web client
        if result["status"] == "success":
            response = {
                "success": True,
                "data": {
                    "summary": result["overall_summary"],
                    "sources": len(result["sources"]),
                    "timestamp": result["timestamp"],
                    "sources_detail": result["sources"]
                }
            }
        else:
            response = {
                "success": False,
                "error": result["message"]
            }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/batch-research', methods=['POST'])
def batch_research_endpoint():
    """API endpoint for batch research requests."""
    try:
        data = request.get_json()
        queries = data.get('queries', [])
        
        if not queries:
            return jsonify({"error": "Queries list is required"}), 400
        
        results = []
        for query in queries[:10]:  # Limit to 10 queries
            result = scraper.run({
                "query": query,
                "max_results": 3,  # Reduced for batch processing
                "max_urls": 5
            })
            
            results.append({
                "query": query,
                "success": result["status"] == "success",
                "summary": result.get("overall_summary", ""),
                "sources": result.get("successfully_scraped", 0)
            })
        
        return jsonify({
            "success": True,
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### Data Pipeline Integration

```python
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

class ScraperSageDataPipeline:
    """Data pipeline for storing and analyzing ScraperSage results."""
    
    def __init__(self, db_path: str = "research_data.db"):
        self.db_path = db_path
        self.scraper = scrape_and_summarize()
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create research sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                total_sources INTEGER,
                successful_sources INTEGER,
                overall_summary TEXT,
                metadata TEXT
            )
        ''')
        
        # Create sources table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                url TEXT NOT NULL,
                title TEXT,
                domain TEXT,
                summary TEXT,
                content_preview TEXT,
                scraped_successfully BOOLEAN,
                FOREIGN KEY (session_id) REFERENCES research_sessions (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def process_and_store(self, query: str, **kwargs) -> int:
        """Process query and store results in database."""
        result = self.scraper.run({"query": query, **kwargs})
        
        if result["status"] != "success":
            print(f"Research failed: {result['message']}")
            return None
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert research session
        cursor.execute('''
            INSERT INTO research_sessions 
            (query, timestamp, total_sources, successful_sources, overall_summary, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            query,
            datetime.now(),
            result["total_sources_found"],
            result["successfully_scraped"],
            result["overall_summary"],
            json.dumps(result["metadata"])
        ))
        
        session_id = cursor.lastrowid
        
        # Insert sources
        for source in result["sources"]:
            domain = source["url"].split("/")[2] if "/" in source["url"] else ""
            cursor.execute('''
                INSERT INTO sources 
                (session_id, url, title, domain, summary, content_preview, scraped_successfully)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                source["url"],
                source["title"],
                domain,
                source["individual_summary"],
                source["content_preview"],
                True
            ))
        
        # Insert failed sources
        for failed in result.get("failed_sources", []):
            domain = failed["url"].split("/")[2] if "/" in failed["url"] else ""
            cursor.execute('''
                INSERT INTO sources 
                (session_id, url, title, domain, summary, content_preview, scraped_successfully)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                failed["url"],
                "Failed to scrape",
                domain,
                "",
                "",
                False
            ))
        
        conn.commit()
        conn.close()
        
        print(f"Research session {session_id} stored successfully")
        return session_id
    
    def get_research_analytics(self, days: int = 30) -> pd.DataFrame:
        """Get analytics for recent research sessions."""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                r.query,
                r.timestamp,
                r.total_sources,
                r.successful_sources,
                r.successful_sources * 1.0 / r.total_sources as success_rate,
                COUNT(s.id) as sources_count,
                AVG(LENGTH(s.summary)) as avg_summary_length
            FROM research_sessions r
            LEFT JOIN sources s ON r.id = s.session_id
            WHERE r.timestamp > datetime('now', '-{} days')
            GROUP BY r.id, r.query, r.timestamp, r.total_sources, r.successful_sources
            ORDER BY r.timestamp DESC
        '''.format(days)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_domain_performance(self) -> pd.DataFrame:
        """Analyze performance by domain."""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                domain,
                COUNT(*) as total_attempts,
                SUM(scraped_successfully) as successful_scrapes,
                AVG(scraped_successfully) as success_rate,
                AVG(LENGTH(summary)) as avg_summary_length
            FROM sources
            WHERE domain != ''
            GROUP BY domain
            HAVING total_attempts >= 3
            ORDER BY success_rate DESC, total_attempts DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df

# Usage
pipeline = ScraperSageDataPipeline()

# Process research queries
queries = [
    "artificial intelligence ethics",
    "sustainable energy solutions",
    "remote work productivity"
]

for query in queries:
    session_id = pipeline.process_and_store(query, max_results=5, max_urls=8)
    time.sleep(2)  # Rate limiting

# Get analytics
analytics_df = pipeline.get_research_analytics(days=7)
domain_performance_df = pipeline.get_domain_performance()

print("Recent Research Analytics:")
print(analytics_df.head())

print("\nDomain Performance:")
print(domain_performance_df.head())
```

## ⚡ Performance Optimization

### Async Processing Pattern

```python
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from typing import List

class AsyncScraperSage:
    """Asynchronous wrapper for ScraperSage operations."""
    
    def __init__(self, max_workers: int = 5):
        self.scraper = scrape_and_summarize()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def research_async(self, query: str, **kwargs) -> dict:
        """Async research operation."""
        loop = asyncio.get_event_loop()
        
        # Run blocking operation in thread pool
        result = await loop.run_in_executor(
            self.executor,
            lambda: self.scraper.run({"query": query, **kwargs})
        )
        
        return result
    
    async def batch_research_async(self, queries: List[str], **kwargs) -> List[dict]:
        """Process multiple queries asynchronously."""
        tasks = [
            self.research_async(query, **kwargs)
            for query in queries
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "status": "error",
                    "query": queries[i],
                    "message": str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results

# Usage
async def main():
    async_scraper = AsyncScraperSage(max_workers=3)
    
    queries = [
        "machine learning trends",
        "blockchain applications",
        "renewable energy policy"
    ]
    
    print("Starting async batch processing...")
    start_time = asyncio.get_event_loop().time()
    
    results = await async_scraper.batch_research_async(
        queries,
        max_results=3,
        max_urls=5
    )
    
    end_time = asyncio.get_event_loop().time()
    
    print(f"Completed {len(results)} research tasks in {end_time - start_time:.2f} seconds")
    
    for result in results:
        if result["status"] == "success":
            print(f"✅ {result['query']}: {result['successfully_scraped']} sources")
        else:
            print(f"❌ {result['query']}: {result['message']}")

# Run async example
# asyncio.run(main())
```

### Caching Layer

```python
import hashlib
import pickle
import os
from datetime import datetime, timedelta

class CachedScraperSage:
    """ScraperSage with intelligent caching."""
    
    def __init__(self, cache_dir: str = "cache", cache_ttl_hours: int = 24):
        self.scraper = scrape_and_summarize()
        self.cache_dir = cache_dir
        self.cache_ttl = timedelta(hours=cache_ttl_hours)
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, query: str, **kwargs) -> str:
        """Generate cache key for query and parameters."""
        cache_data = {"query": query, **kwargs}
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Get file path for cache key."""
        return os.path.join(self.cache_dir, f"{cache_key}.pkl")
    
    def _is_cache_valid(self, cache_path: str) -> bool:
        """Check if cache file is still valid."""
        if not os.path.exists(cache_path):
            return False
        
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return datetime.now() - file_time < self.cache_ttl
    
    def research_cached(self, query: str, use_cache: bool = True, **kwargs) -> dict:
        """Research with caching support."""
        cache_key = self._get_cache_key(query, **kwargs)
        cache_path = self._get_cache_path(cache_key)
        
        # Check cache first
        if use_cache and self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    cached_result = pickle.load(f)
                
                print(f"📦 Using cached result for: {query}")
                cached_result["cached"] = True
                cached_result["cache_timestamp"] = datetime.fromtimestamp(
                    os.path.getmtime(cache_path)
                ).strftime("%Y-%m-%d %H:%M:%S")
                
                return cached_result
            except Exception as e:
                print(f"Cache read error: {e}")
        
        # Perform fresh research
        print(f"🔍 Fresh research for: {query}")
        result = self.scraper.run({"query": query, **kwargs})
        
        # Cache successful results
        if result["status"] == "success":
            try:
                with open(cache_path, 'wb') as f:
                    pickle.dump(result, f)
                print(f"💾 Result cached for future use")
            except Exception as e:
                print(f"Cache write error: {e}")
        
        result["cached"] = False
        return result
    
    def clear_cache(self, older_than_hours: int = None):
        """Clear cache files."""
        if older_than_hours:
            cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
        
        cleared_count = 0
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.pkl'):
                file_path = os.path.join(self.cache_dir, filename)
                
                if older_than_hours:
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_time > cutoff_time:
                        continue
                
                os.remove(file_path)
                cleared_count += 1
        
        print(f"🗑️ Cleared {cleared_count} cache files")

# Usage
cached_scraper = CachedScraperSage(cache_ttl_hours=6)

# First call - will perform fresh research
result1 = cached_scraper.research_cached("quantum computing applications")

# Second call - will use cached result
result2 = cached_scraper.research_cached("quantum computing applications")

print(f"First call cached: {result1.get('cached', False)}")
print(f"Second call cached: {result2.get('cached', False)}")
```

## 🚨 Error Handling Strategies

### Robust Error Recovery

```python
import logging
from typing import Optional, Callable
import functools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 2.0):
    """Decorator for retry logic with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
            
        return wrapper
    return decorator

class RobustScraperSage:
    """ScraperSage with comprehensive error handling."""
    
    def __init__(self):
        try:
            self.scraper = scrape_and_summarize()
            self.available = True
        except Exception as e:
            logger.error(f"Failed to initialize scraper: {e}")
            self.available = False
    
    @retry_with_backoff(max_retries=3)
    def safe_research(
        self, 
        query: str, 
        fallback_summary: Optional[str] = None,
        on_error: Optional[Callable] = None,
        **kwargs
    ) -> dict:
        """Research with comprehensive error handling."""
        
        if not self.available:
            return self._create_error_response("Scraper not available", query)
        
        try:
            result = self.scraper.run({"query": query, **kwargs})
            
            # Validate result
            if not self._validate_result(result):
                raise ValueError("Invalid result structure")
            
            return result
            
        except KeyboardInterrupt:
            logger.info("Research cancelled by user")
            return self._create_cancelled_response(query)
            
        except Exception as e:
            logger.error(f"Research failed for '{query}': {e}")
            
            # Call error callback if provided
            if on_error:
                try:
                    on_error(e, query)
                except Exception as callback_error:
                    logger.error(f"Error callback failed: {callback_error}")
            
            # Return fallback response
            return self._create_fallback_response(query, str(e), fallback_summary)
    
    def _validate_result(self, result: dict) -> bool:
        """Validate result structure."""
        required_fields = ["status", "query", "timestamp"]
        return all(field in result for field in required_fields)
    
    def _create_error_response(self, message: str, query: str) -> dict:
        """Create standardized error response."""
        return {
            "status": "error",
            "message": message,
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sources": [],
            "overall_summary": "",
            "error_handled": True
        }
    
    def _create_cancelled_response(self, query: str) -> dict:
        """Create cancellation response."""
        return {
            "status": "cancelled",
            "message": "Research cancelled by user",
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _create_fallback_response(self, query: str, error: str, fallback_summary: str = None) -> dict:
        """Create fallback response with optional summary."""
        return {
            "status": "error",
            "message": f"Research failed: {error}",
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sources": [],
            "overall_summary": fallback_summary or f"Unable to research '{query}' due to technical issues.",
            "error_handled": True,
            "original_error": error
        }
    
    def batch_research_safe(
        self, 
        queries: List[str],
        stop_on_error: bool = False,
        max_failures: int = None,
        **kwargs
    ) -> List[dict]:
        """Safe batch processing with failure handling."""
        results = []
        failure_count = 0
        
        for i, query in enumerate(queries):
            logger.info(f"Processing query {i+1}/{len(queries)}: {query}")
            
            try:
                result = self.safe_research(query, **kwargs)
                results.append(result)
                
                if result["status"] == "error":
                    failure_count += 1
                    
                    # Check failure limits
                    if max_failures and failure_count >= max_failures:
                        logger.warning(f"Max failures ({max_failures}) reached. Stopping batch.")
                        break
                    
                    if stop_on_error:
                        logger.warning("Stopping batch processing due to error")
                        break
                
            except Exception as e:
                logger.error(f"Unexpected error processing '{query}': {e}")
                results.append(self._create_error_response(str(e), query))
                
                if stop_on_error:
                    break
            
            # Rate limiting
            if i < len(queries) - 1:
                time.sleep(1)
        
        logger.info(f"Batch processing completed. {len(results)} queries processed, {failure_count} failures.")
        return results

# Usage with error handling
def error_callback(error: Exception, query: str):
    """Custom error handling callback."""
    print(f"🚨 Custom handler: Failed to research '{query}' - {error}")
    # Could send to monitoring system, log to file, etc.

robust_scraper = RobustScraperSage()

# Safe research with fallback
result = robust_scraper.safe_research(
    "emerging technologies 2024",
    fallback_summary="Unable to fetch latest information about emerging technologies.",
    on_error=error_callback,
    max_results=5
)

print(f"Status: {result['status']}")
print(f"Summary available: {bool(result['overall_summary'])}")

# Safe batch processing
queries = [
    "valid query example",
    "another research topic",
    "",  # This will cause an error
    "final query"
]

batch_results = robust_scraper.batch_research_safe(
    queries,
    stop_on_error=False,  # Continue despite errors
    max_failures=2,       # Stop after 2 failures
    max_results=3
)

for result in batch_results:
    status_icon = "✅" if result["status"] == "success" else "❌"
    print(f"{status_icon} {result['query']}: {result['status']}")
```

This comprehensive examples document demonstrates the versatility and power of ScraperSage across various real-world scenarios, from simple research tasks to complex academic and commercial applications.