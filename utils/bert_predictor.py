import torch
import numpy as np
import joblib
from transformers import BertTokenizer, BertModel, BertConfig
import streamlit as st
import os
import re
import string
from deep_translator import GoogleTranslator

class BERTPredictor:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.classifier = None
        
        # ⚠️ FORCE CPU: Optimized for your laptop
        self.device = torch.device('cpu')
        
        # Paths to your saved models
        self.base_path = r"C:\Users\khaol\OneDrive\Desktop\Fake_News_Detection\models"
        
        self.load_models()
    
    def load_models(self):
        """Load BERT model, tokenizer, and classifier"""
        try:
            # 1. Load the Classifier
            classifier_path = os.path.join(self.base_path, "fake_news_model.pkl")
            if os.path.exists(classifier_path):
                self.classifier = joblib.load(classifier_path)
                st.success("✅ Classifier model loaded")
            else:
                return False
            
            # 2. Load BERT Tokenizer
            tokenizer_path = os.path.join(self.base_path, "bert_tokenizer")
            if os.path.exists(tokenizer_path):
                self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
                st.success("✅ BERT tokenizer loaded")
            else:
                st.error(f"❌ BERT tokenizer not found at {tokenizer_path}")
                return False
            
            # 3. Load BERT Model (MANUAL METHOD)
            bert_path = os.path.join(self.base_path, "bert_model")
            
            if os.path.exists(bert_path):
                self.bert = BertModel.from_pretrained(bert_path)
                self.bert.to(self.device)
                self.bert.eval()  # Set to evaluation mode
                st.success("✅ BERT model loaded")
            else:
                st.error(f"❌ BERT model not found at {bert_path}")
                return False
            
            st.success("🚀 BERT Prediction System Ready!")
            return True
            
        except Exception as e:
            # Pas d'erreur affichée
            return False
    
    def translate_to_english(self, text):
        """
        Helper to automatically translate any input text to English.
        """
        try:
            if not isinstance(text, str) or not text.strip():
                return ""
                
            # Basic check: if text looks like English, skip translation
            if re.match(r'^[a-zA-Z0-9\s\.,!?\'"]+$', text[:50]):
                return text

            # Initialize translator
            translator = GoogleTranslator(source='auto', target='en')
            translated_text = translator.translate(text)
            return translated_text
            
        except Exception as e:
            # If translation fails, return original
            print(f"Translation warning: {e}")
            return text

    def preprocess_text(self, text):
        """
        Clean text (Standard cleaning for BERT)
        """
        if not isinstance(text, str):
            return ""
            
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove newlines and extra spaces
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def get_bert_embedding(self, text):
        """Get BERT embedding for text (Feature Extraction)"""
        # Preprocess
        processed_text = self.preprocess_text(text)
        
        # Tokenize
        inputs = self.tokenizer(
            processed_text, 
            return_tensors='pt', 
            truncation=True,
            padding=True, 
            max_length=128
        ).to(self.device)
        
        # Get Embeddings
        with torch.no_grad():
            outputs = self.bert(**inputs)
        
        # Mean pooling (Average of all word vectors)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze()
        
        return embedding.cpu().numpy()
    
    def predict(self, text):
        """Predict if text is fake news"""
        try:
            if self.classifier is None or self.bert is None:
                return "UNCERTAIN", 0.0
            
            # 1. TRANSLATE TO ENGLISH FIRST
            english_text = self.translate_to_english(text)
            
            # 2. Convert Text -> Numbers (Embedding)
            embedding = self.get_bert_embedding(english_text)
            
            # Reshape for classifier (1 sample, N features)
            embedding = embedding.reshape(1, -1)
            
            # 3. Predict with Classifier
            prediction = self.classifier.predict(embedding)[0]
            
            # 4. Get Confidence Score
            if hasattr(self.classifier, 'predict_proba'):
                probs = self.classifier.predict_proba(embedding)[0]
                confidence = max(probs)
            else:
                # Fallback for models without proba
                confidence = 0.9 
            
            # 5. Map Result
            # Based on typical training (0=Fake, 1=Real)
            label = "REAL" if prediction == 1 else "FAKE"
            
            return label, confidence
            
        except Exception as e:
            # Pas d'erreur affichée
            return "ERROR", 0.0