# test_url_scraping_simple.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.url_scraper import URLScraper

def test_scraping():
    print("🧪 Testing URL Scraping")
    print("=" * 50)
    
    scraper = URLScraper()
    
    # Test URLs (you can replace these with actual news URLs)
    test_urls = [
        "https://www.bbc.com/news/world-60525350",  # Example BBC article
        "https://www.reuters.com/business/",        # Reuters business section
        "https://apnews.com/hub/climate-and-environment"  # AP News climate section
    ]
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{i}. Testing: {url}")
        result = scraper.scrape_article(url)
        
        print(f"   Success: {result['success']}")
        if result['success']:
            print(f"   Title: {result.get('title', 'No title')[:80]}...")
            print(f"   Content length: {len(result.get('content', ''))} characters")
            if result.get('summary'):
                print(f"   Summary: {result['summary'][:100]}...")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        print("   " + "-" * 40)

if __name__ == "__main__":
    test_scraping()