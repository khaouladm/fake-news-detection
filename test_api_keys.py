import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
from datetime import datetime, timedelta

def test_api_keys_directly():
    """Test API keys without using Streamlit"""
    print("🔑 Testing API Keys Directly...")
    
    # Read API keys from environment or secrets file
    try:
        # Try to read from secrets.toml if it exists
        import toml
        try:
            secrets = toml.load('.streamlit/secrets.toml')
            gnews_key = secrets.get('GNEWS_KEY', '')
            newsapi_key = secrets.get('NEWSAPI_KEY', '')
        except:
            # If secrets file doesn't exist or can't be read
            gnews_key = os.environ.get('GNEWS_KEY', '')
            newsapi_key = os.environ.get('NEWSAPI_KEY', '')
    except ImportError:
        # Fallback if toml not installed
        gnews_key = os.environ.get('GNEWS_KEY', '')
        newsapi_key = os.environ.get('NEWSAPI_KEY', '')
    
    print(f"GNews Key: {gnews_key[:8]}..." if gnews_key else "❌ GNews Key: Not found")
    print(f"NewsAPI Key: {newsapi_key[:8]}..." if newsapi_key else "❌ NewsAPI Key: Not found")
    
    if not gnews_key and not newsapi_key:
        print("💡 Please add your API keys to .streamlit/secrets.toml")
        return False
    
    # Test GNews API
    if gnews_key:
        print("\n📡 Testing GNews API...")
        try:
            url = "https://gnews.io/api/v4/top-headlines"
            params = {
                'token': gnews_key,
                'lang': 'en',
                'max': 3,
                'q': 'technology'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                print(f"✅ GNews API: SUCCESS - Found {len(articles)} articles")
                for i, article in enumerate(articles, 1):
                    print(f"   {i}. {article.get('title', 'No title')[:60]}...")
                return True
            else:
                print(f"❌ GNews API: FAILED - HTTP {response.status_code}")
                if response.status_code == 401:
                    print("   Invalid API key")
                return False
                
        except Exception as e:
            print(f"❌ GNews API: ERROR - {e}")
            return False
    
    # Test NewsAPI
    elif newsapi_key:
        print("\n📡 Testing NewsAPI...")
        try:
            from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': 'technology',
                'from': from_date,
                'sortBy': 'publishedAt',
                'language': 'en',
                'apiKey': newsapi_key,
                'pageSize': 3
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                print(f"✅ NewsAPI: SUCCESS - Found {len(articles)} articles")
                for i, article in enumerate(articles, 1):
                    print(f"   {i}. {article.get('title', 'No title')[:60]}...")
                return True
            else:
                print(f"❌ NewsAPI: FAILED - HTTP {response.status_code}")
                if response.status_code == 401:
                    print("   Invalid API key")
                return False
                
        except Exception as e:
            print(f"❌ NewsAPI: ERROR - {e}")
            return False
    
    return False

if __name__ == "__main__":
    success = test_api_keys_directly()
    if success:
        print("\n🎉 API Keys are working! Your system is ready for real-time news!")
        print("🚀 Run: streamlit run app.py")
    else:
        print("\n❌ API Keys test failed.")
        print("💡 Make sure:")
        print("   1. Your API keys are valid")
        print("   2. You have internet connection")
        print("   3. The keys are in .streamlit/secrets.toml")