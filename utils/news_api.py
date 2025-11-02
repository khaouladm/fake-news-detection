import requests
import json
import time
from datetime import datetime, timedelta
import streamlit as st
from config import SEARCH_QUERIES 

class NewsFetcher:
    def __init__(self):
        # Charger les clés depuis st.secrets (méthode sécurisée)
        self.newsapi_key = st.secrets.get("NEWSAPI_KEY", "")
        self.gnews_key = st.secrets.get("GNEWS_KEY", "")
    
    def fetch_from_newsapi(self, query="news", hours_back=24, lang='en'):
        """Fetch news from NewsAPI"""
        
        # Logique pour utiliser aussi la clé de la session
        if not self.newsapi_key and 'newsapi_key' in st.session_state:
             self.newsapi_key = st.session_state.newsapi_key

        if not self.newsapi_key:
            st.error("NewsAPI key not configured")
            return []
        
        try:
            from_date = (datetime.now() - timedelta(hours=hours_back)).strftime('%Y-%m-%d')
            
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'from': from_date,
                'sortBy': 'publishedAt',
                'language': lang,  # <-- MODIFICATION: Utilise le paramètre lang
                'apiKey': self.newsapi_key,
                'pageSize': 20
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                return self._process_articles(articles, 'newsapi')
            else:
                st.warning(f"NewsAPI returned status {response.status_code}")
                st.warning(f"Response: {response.text}")
                return []
                
        except Exception as e:
            st.error(f"Error fetching from NewsAPI: {e}")
            return []
    
    def fetch_from_gnews(self, query="news", lang='en'):
        """Fetch news from GNews API (free tier available)"""
        
        # Logique pour utiliser aussi la clé de la session (de la page API Settings)
        if not self.gnews_key and 'gnews_key' in st.session_state:
             self.gnews_key = st.session_state.gnews_key
        
        if not self.gnews_key:
            st.error("GNews API key not configured. Please add it in API Settings.")
            return []
        
        try:
            url = "https://gnews.io/api/v4/top-headlines"
            params = {
                'token': self.gnews_key,
                'lang': lang,  # MODIFICATION: Utilise le paramètre lang
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
                st.warning(f"Response: {response.text}")
                return []
                
        except Exception as e:
            st.error(f"Error fetching from GNews: {e}")
            return []
    
    def _process_articles(self, articles, source):
        """Process articles from different APIs to standard format"""
        processed = []
        
        for article in articles:
            processed_article = {
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'content': article.get('content', '') or article.get('description', ''),
                'url': article.get('url', ''),
                'source': article.get('source', {}).get('name', '') if isinstance(article.get('source'), dict) else str(article.get('source', '')),
                'published_at': article.get('publishedAt', '') or article.get('publishedAt', ''),
                'api_source': source
            }
            
            if processed_article['content'] and len(processed_article['content']) > 50:
                processed.append(processed_article)
        
        return processed
    
    def fetch_real_time_news(self, queries=None, lang='en'):
        """Fetch real-time news from multiple sources"""
        if queries is None:
            queries = SEARCH_QUERIES
        
        all_articles = []
        
        # MODIFICATION: Affiche la langue dans le message
        with st.spinner(f"Fetching real-time news for '{queries[0]}' in language '{lang}'..."):
            for query in queries[:3]: # Limit to 3 queries for demo
                
                # Fetch from GNews (more free-friendly)
                # MODIFICATION: Passe le paramètre 'lang'
                articles = self.fetch_from_gnews(query, lang=lang)
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