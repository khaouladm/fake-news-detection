import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.real_time_analyzer import RealTimeAnalyzer

def test_bert_system():
    print("🧪 Testing BERT-Based Fake News Detection")
    print("=" * 50)
    
    analyzer = RealTimeAnalyzer()
    
    test_cases = [
        {
            "title": "Vampire Attack in 2025",
            "content": "A woman was reportedly killed by a vampire in mysterious circumstances.",
            "expected": "FAKE"
        },
        {
            "title": "New Study Links Coffee to Cancer Risk", 
            "content": "A recent study suggests that drinking coffee may increase cancer risk.",
            "expected": "FAKE"
        },
        {
            "title": "Federal Reserve Raises Interest Rates",
            "content": "The Federal Reserve raised interest rates to combat inflation.",
            "expected": "REAL"
        }
    ]
    
    print("\n📊 BERT Model Test Results:")
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
    test_bert_system()