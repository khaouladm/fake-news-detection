import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.preprocess import preprocess_text
    print("✅ preprocess_text imported successfully!")
    
    # Test the function
    test_text = "This is a test article about breaking news."
    result = preprocess_text(test_text)
    print(f"✅ Preprocessing test: '{test_text}' -> '{result}'")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    
try:
    from utils.real_time_analyzer import RealTimeAnalyzer
    print("✅ RealTimeAnalyzer imported successfully!")
except ImportError as e:
    print(f"❌ Import failed: {e}")