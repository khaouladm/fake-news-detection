import requests
import json
import time
from datetime import datetime, timedelta
import streamlit as st
from config import NEWS_API_CONFIG, SEARCH_QUERIES

class NewsFetcher:
    def __init__(self):
        self.newsapi_key = st.secrets.get("NEWSAPI_KEY", "")
        self.gnews_key = st.secrets.get("GNEWS_KEY", "")
    
    def fetch_from_newsapi(self, query="news", hours_back=24):
        """Fetch news from NewsAPI"""
        if not self.newsapi_key:
            st.error("NewsAPI key not configured")
            return []
        
        try:
            # Calculate date (newsapi requires paid plan for full access)
            from_date = (datetime.now() - timedelta(hours=hours_back)).strftime('%Y-%m-%d')
            
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'from': from_date,
                'sortBy': 'publishedAt',
                'language': 'en',
                'apiKey': self.newsapi_key,
                'pageSize': 20
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                return self._process_articles(articles, 'newsapi')
            else:
                st.warning(f"NewsAPI returned status {response.status_code}")
                return []
                
        except Exception as e:
            st.error(f"Error fetching from NewsAPI: {e}")
            return []
    
    def fetch_from_gnews(self, query="news"):
        """Fetch news from GNews API (free tier available)"""
        if not self.gnews_key:
            st.error("GNews API key not configured")
            return []
        
        try:
            url = "https://gnews.io/api/v4/top-headlines"
            params = {
                'token': self.gnews_key,
                'lang': 'en',
                'max': 20,
                'q': query
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                return self._process_articles(articles, 'gnews')
            else:
                st.warning(f"GNews returned status {response.status_code}")
                return []
                
        except Exception as e:
            st.error(f"Error fetching from GNews: {e}")
            return []
    
    def _process_articles(self, articles, source):
        """Process articles from different APIs to standard format"""
        processed = []
        
        for article in articles:
            # Standardize article format
            processed_article = {
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'content': article.get('content', '') or article.get('description', ''),
                'url': article.get('url', ''),
                'source': article.get('source', {}).get('name', '') if isinstance(article.get('source'), dict) else str(article.get('source', '')),
                'published_at': article.get('publishedAt', '') or article.get('publishedAt', ''),
                'api_source': source
            }
            
            # Only include articles with sufficient content
            if processed_article['content'] and len(processed_article['content']) > 50:
                processed.append(processed_article)
        
        return processed
    
    def fetch_real_time_news(self, queries=None):
        """Fetch real-time news from multiple sources"""
        if queries is None:
            queries = SEARCH_QUERIES
        
        all_articles = []
        
        with st.spinner("Fetching real-time news..."):
            for query in queries[:3]:  # Limit to 3 queries for demo
                st.write(f"Searching for: {query}")
                
                # Fetch from GNews (more free-friendly)
                articles = self.fetch_from_gnews(query)
                all_articles.extend(articles)
                
                # Add small delay to avoid rate limiting
                time.sleep(1)
        
        # Remove duplicates based on title
        unique_articles = []
        seen_titles = set()
        
        for article in all_articles:
            title = article['title'].lower().strip()
            if title not in seen_titles and len(title) > 10:
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles