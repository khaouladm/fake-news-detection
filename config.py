# Configuration de l'application
APP_CONFIG = {
    'APP_NAME': 'NewsVerifi AI',
    'APP_ICON': '📰',
    'VERSION': '2.0.0',
    'SUPPORTED_LANGUAGES': {
        'Français': 'fr',
        'English': 'en', 
        'العربية': 'ar'
    },
    'DEFAULT_LANGUAGE': 'fr'
}

# Sujets de recherche
SEARCH_QUERIES = [
    "breaking news", "politics", "technology", "health", 
    "coronavirus", "elections", "climate change", "economy",
    "artificial intelligence", "science", "education", "business",
    "entertainment", "sports", "world news", "local news"
]

# Configuration de l'analyse
ANALYSIS_CONFIG = {
    'CONFIDENCE_THRESHOLDS': {
        'HIGH': 0.8,
        'MEDIUM': 0.6,
        'LOW': 0.4
    },
    'MAX_ARTICLES': 50,
    'BATCH_SIZE': 10
}

# Configuration API
API_CONFIG = {
    'NEWS_API_TIMEOUT': 30,
    'MAX_RETRIES': 3
}