import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.model_loader import find_model_files, check_model_files

print("🔍 Checking model files...")
found_files = find_model_files()

print("\n📁 Found files:")
for file_type, path in found_files.items():
    if path:
        print(f"✅ {file_type}: {os.path.basename(path)}")
    else:
        print(f"❌ {file_type}: Not found")

print("\n📊 Model status:")
status = check_model_files()
for file_type, info in status.items():
    print(f"  {file_type}: {info['name']}")

if found_files['pipeline'] or (found_files['svm_model'] and found_files['vectorizer']):
    print("\n🎉 Your model setup looks good! Run: streamlit run app.py")
else:
    print("\n💡 Please make sure you have both model and vectorizer files in models/ folder")