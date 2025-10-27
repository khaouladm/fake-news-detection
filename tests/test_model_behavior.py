# test_model_behavior.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.real_time_analyzer import RealTimeAnalyzer

def test_various_articles():
    print("🧪 Testing Model with Various Articles")
    print("=" * 50)
    
    analyzer = RealTimeAnalyzer()
    
    test_cases = [
        {
            "title": "Vampire Attack in 2025",
            "content": "A woman was reportedly killed by a vampire in mysterious circumstances. Witnesses claim to have seen supernatural activities.",
            "expected": "FAKE"
        },
        {
            "title": "New Climate Study Shows Alarming Results",
            "content": "According to a peer-reviewed study published in Nature, climate change is accelerating faster than previous models predicted.",
            "expected": "REAL"
        },
        {
            "title": "BREAKING: One Weird Trick Cures All Diseases",
            "content": "Doctors are shocked by this simple remedy that big pharma doesn't want you to know about!",
            "expected": "FAKE"
        },
        {
            "title": "Economic Growth Exceeds Expectations",
            "content": "Official government reports indicate that economic growth has surpassed analyst predictions for the third consecutive quarter.",
            "expected": "REAL"
        },
        {
            "title": "Alien Abduction Coverup Revealed",
            "content": "Secret documents show that governments have been hiding alien abduction cases for decades.",
            "expected": "FAKE"
        }
    ]
    
    print("\n📊 Test Results:")
    for i, test in enumerate(test_cases, 1):
        article = {
            'title': test['title'],
            'content': test['content'],
            'source': 'Test'
        }
        
        prediction, confidence = analyzer.predict_article(article)
        status = "✅ CORRECT" if prediction == test['expected'] else "❌ WRONG"
        
        print(f"\n{i}. {test['title']}")
        print(f"   Prediction: {prediction} ({confidence:.1%})")
        print(f"   Expected: {test['expected']} - {status}")

if __name__ == "__main__":
    test_various_articles()