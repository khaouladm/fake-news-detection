import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.real_time_analyzer import RealTimeAnalyzer
from utils.news_api import NewsFetcher
import streamlit as st

def test_complete_system():
    print("🧪 Testing Complete Fake News Detection System")
    print("=" * 50)
    
    # Test 1: Model Loading
    print("\n1. Testing Model Loading...")
    analyzer = RealTimeAnalyzer()
    
    if analyzer.model_loaded:
        print("✅ SVM Model loaded successfully!")
        print(f"   Model Info: {analyzer.get_model_info()}")
    else:
        print("⚠️ Using rule-based analyzer")
    
    # Test 2: Prediction Function
    print("\n2. Testing Predictions...")
    test_articles = [
        {
            'title': 'Scientific study confirms climate change is real',
            'content': 'A peer-reviewed study published in Nature journal shows conclusive evidence of climate change based on 50 years of data from multiple research institutions.',
            'source': 'Science Daily'
        },
        {
            'title': 'BREAKING: Secret miracle cure they dont want you to know!',
            'content': 'Doctors are shocked by this one simple trick that cures all diseases instantly. Big pharma is hiding this from you!',
            'source': 'Unknown Blog'
        },
        {
            'title': 'Government releases economic growth report',
            'content': 'The official economic report indicates stable market growth and positive indicators for the upcoming quarter according to financial experts.',
            'source': 'Reuters'
        }
    ]
    
    for i, article in enumerate(test_articles, 1):
        prediction, confidence = analyzer.predict_article(article)
        print(f"   Article {i}: {prediction} ({confidence:.2f} confidence)")
        print(f"   Title: {article['title'][:60]}...")
        print()
    
    # Test 3: News API (if keys are configured)
    print("\n3. Testing News API Connectivity...")
    news_fetcher = NewsFetcher()
    
    # Test with a simple query
    try:
        # This will show API status without making actual calls
        if hasattr(news_fetcher, 'gnews_key') and news_fetcher.gnews_key:
            print("✅ GNews API configured")
        else:
            print("⚠️ GNews API not configured - using demo mode")
            
        if hasattr(news_fetcher, 'newsapi_key') and news_fetcher.newsapi_key:
            print("✅ NewsAPI configured")
        else:
            print("⚠️ NewsAPI not configured - using demo mode")
            
    except Exception as e:
        print(f"❌ API test error: {e}")
    
    print("\n🎯 System Test Complete!")
    print("Next: Run 'streamlit run app.py' to start the web application")

if __name__ == "__main__":
    test_complete_system()