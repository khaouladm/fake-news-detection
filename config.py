# News API Configuration
NEWS_API_CONFIG = {
    'newsapi': {
        'url': 'https://newsapi.org/v2/everything',
        'key': '6cdd7f0d55aa49eea3ad1e2ccb2f9ef2'  # You'll get this from newsapi.org
    },
    'gnews': {
        'url': 'https://gnews.io/api/v4/top-headlines',
        'key': '8e941dbedb9447ef743bfe1b4219b5f3'  # You'll get this from gnews.io
    }
}

# Search queries for fake news detection
SEARCH_QUERIES = [
    "breaking news", "politics", "technology", "health", 
    "coronavirus", "elections", "climate change", "economy"
]