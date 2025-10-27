import torch
import numpy as np
import joblib
from transformers import BertTokenizer, BertModel
import streamlit as st
import os

class BERTPredictor:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.classifier = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.load_models()
    
    def load_models(self):
        """Load BERT model, tokenizer, and classifier"""
        try:
            # Load classifier
            classifier_path = "models/fake_news_model.pkl"
            if os.path.exists(classifier_path):
                self.classifier = joblib.load(classifier_path)
                st.success("✅ Classifier model loaded")
            else:
                st.error(f"❌ Classifier not found at {classifier_path}")
                return False
            
            # Load BERT tokenizer
            tokenizer_path = "models/bert_tokenizer"
            if os.path.exists(tokenizer_path):
                self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
                st.success("✅ BERT tokenizer loaded")
            else:
                st.error(f"❌ BERT tokenizer not found at {tokenizer_path}")
                return False
            
            # Load BERT model
            bert_path = "models/bert_model"
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
            st.error(f"❌ Error loading models: {str(e)}")
            return False
    
    def preprocess_text(self, text):
        """Preprocess text similar to your training"""
        import re
        import string
        
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W", " ", text)
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text
    
    def get_bert_embedding(self, text):
        """Get BERT embedding for text (same as training)"""
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Tokenize
        inputs = self.tokenizer(
            processed_text, 
            return_tensors='pt', 
            truncation=True,
            padding=True, 
            max_length=128
        )
        
        # Move to device (GPU if available)
        inputs = {key: value.to(self.device) for key, value in inputs.items()}
        
        # Get BERT embeddings
        with torch.no_grad():
            outputs = self.bert(**inputs)
        
        # Mean pooling (same as training)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze()
        
        return embedding.cpu().numpy()
    
    def predict(self, text):
        """Predict if text is fake news"""
        try:
            if self.classifier is None or self.bert is None:
                return "UNCERTAIN", 0.5
            
            # Get BERT embedding
            embedding = self.get_bert_embedding(text)
            embedding = embedding.reshape(1, -1)
            
            # Predict with classifier
            prediction = self.classifier.predict(embedding)[0]
            
            # Get probability if available
            if hasattr(self.classifier, 'predict_proba'):
                probability = self.classifier.predict_proba(embedding)[0]
                confidence = max(probability)
            else:
                confidence = 0.8
            
            # Map prediction
            return "FAKE" if prediction == 0 else "REAL", confidence
            
        except Exception as e:
            st.error(f"❌ Prediction error: {str(e)}")
            return "ERROR", 0.0
    
    def predict_batch(self, texts):
        """Predict multiple texts"""
        results = []
        for text in texts:
            prediction, confidence = self.predict(text)
            results.append({
                'prediction': prediction,
                'confidence': confidence,
                'text': text
            })
        return results