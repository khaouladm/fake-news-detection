import joblib
import streamlit as st
import os
import glob
from sklearn.feature_extraction.text import TfidfVectorizer

def find_model_files():
    """
    Automatically find model and vectorizer files in the models folder
    """
    model_files = {
        'svm_model': None,
        'vectorizer': None,
        'pipeline': None
    }
    
    # Look for common model file patterns
    model_patterns = [
        'models/*model*.pkl',
        'models/*classifier*.pkl', 
        'models/*svm*.pkl',
        'models/*fake*.pkl'
    ]
    
    vectorizer_patterns = [
        'models/*vectorizer*.pkl',
        'models/*tfidf*.pkl',
        'models/*count*.pkl'
    ]
    
    # Find model files
    for pattern in model_patterns:
        files = glob.glob(pattern)
        for file in files:
            if 'vector' not in file.lower() and 'tfidf' not in file.lower():
                model_files['svm_model'] = file
                break
        if model_files['svm_model']:
            break
    
    # Find vectorizer files
    for pattern in vectorizer_patterns:
        files = glob.glob(pattern)
        if files:
            model_files['vectorizer'] = files[0]
            break
    
    # Check if it's a pipeline
    if model_files['svm_model']:
        try:
            model = joblib.load(model_files['svm_model'])
            if hasattr(model, 'steps') or hasattr(model, 'named_steps'):
                model_files['pipeline'] = model_files['svm_model']
                model_files['svm_model'] = None
        except:
            pass
    
    return model_files

@st.cache_resource
def load_model_with_vectorizer():
    """
    Smart loading that automatically detects the best model/vectorizer combination
    """
    found_files = find_model_files()
    
    st.info("🔍 Searching for model files...")
    for file_type, path in found_files.items():
        if path:
            st.success(f"✅ Found {file_type}: {os.path.basename(path)}")
        else:
            st.warning(f"⚠️ No {file_type} found")
    
    # Case 1: Pipeline found (best case)
    if found_files['pipeline']:
        try:
            pipeline = joblib.load(found_files['pipeline'])
            st.success("🎯 Loaded complete pipeline (model + preprocessing)")
            return pipeline, None, 'pipeline'
        except Exception as e:
            st.error(f"❌ Error loading pipeline: {e}")
    
    # Case 2: Separate model and vectorizer files
    if found_files['svm_model'] and found_files['vectorizer']:
        try:
            model = joblib.load(found_files['svm_model'])
            vectorizer = joblib.load(found_files['vectorizer'])
            st.success("🎯 Loaded model and vectorizer separately")
            return model, vectorizer, 'separate'
        except Exception as e:
            st.error(f"❌ Error loading separate files: {e}")
    
    # Case 3: Only model file found
    if found_files['svm_model'] and not found_files['vectorizer']:
        try:
            model = joblib.load(found_files['svm_model'])
            st.warning("⚠️ Only model found - creating compatible vectorizer")
            vectorizer = create_compatible_vectorizer()
            return model, vectorizer, 'model_only'
        except Exception as e:
            st.error(f"❌ Error loading model: {e}")
    
    # Case 4: No model found
    st.error("❌ No suitable model files found in models/ folder")
    return None, None, 'none'

def create_compatible_vectorizer():
    """
    Create a basic TF-IDF vectorizer as fallback
    """
    try:
        vectorizer = TfidfVectorizer(
            max_features=5000,
            min_df=2,
            max_df=0.8,
            stop_words='english',
            ngram_range=(1, 2)
        )
        return vectorizer
    except Exception as e:
        st.error(f"❌ Error creating vectorizer: {e}")
        return None

def check_model_files():
    """
    Check if required model files exist
    """
    found_files = find_model_files()
    
    status = {}
    for file_type, path in found_files.items():
        exists = path is not None
        status[file_type] = {
            'exists': exists, 
            'path': path if exists else f'No {file_type} found',
            'name': os.path.basename(path) if exists else 'Not found'
        }
        
    return status

@st.cache_resource
def load_vectorizer(vectorizer_path="models/vectorizer.pkl"):
    """
    Load specific vectorizer file
    """
    try:
        if not os.path.exists(vectorizer_path):
            return None
        
        vectorizer = joblib.load(vectorizer_path)
        st.success(f"✅ Vectorizer loaded from {os.path.basename(vectorizer_path)}")
        return vectorizer
    except Exception as e:
        st.error(f"❌ Error loading vectorizer: {e}")
        return None

def save_model(model, model_path="models/svm_model.pkl"):
    """
    Save a trained model
    """
    try:
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(model, model_path)
        st.success(f"✅ Model saved to {model_path}")
        return True
    except Exception as e:
        st.error(f"❌ Error saving model: {e}")
        return False