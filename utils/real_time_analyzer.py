import pandas as pd
import streamlit as st
import time
import numpy as np
import re

try:
    from utils.bert_predictor import BERTPredictor
except ImportError as e:
    st.error(f"Import error: {e}")

class RealTimeAnalyzer:
    def __init__(self):
        self.bert_predictor = None
        self.model_loaded = False
        self.load_models()
    
    def load_models(self):
        """Load BERT-based models"""
        try:
            self.bert_predictor = BERTPredictor()
            self.model_loaded = self.bert_predictor.load_models()
            
            if self.model_loaded:
                st.success("🚀 BERT Model Ready - High Accuracy Expected!")
            else:
                st.warning("⚠️ Using rule-based analyzer as fallback")
                self.model_loaded = False
                
        except Exception as e:
            st.warning(f"⚠️ Using fallback analyzer: {str(e)}")
            self.model_loaded = False
    
    def enhanced_pre_detection(self, text):
        """Enhanced rule-based detection for obvious fake news"""
        text_lower = text.lower()
        
        # OBVIOUS FAKE NEWS PATTERNS
        obvious_fake_patterns = [
            r'vampire', r'werewolf', r'zombie', r'alien.*abduction', r'bigfoot',
            r'loch ness', r'ghost.*killed', r'supernatural.*kill',
            r'miracle.*cure', r'instant.*weight loss', r'one weird trick',
            r'doctors hate', r'secret.*government', r'202[5-9].*killed'
        ]
        
        # Check for obvious fake patterns
        fake_matches = 0
        for pattern in obvious_fake_patterns:
            if re.search(pattern, text_lower):
                fake_matches += 1
        
        if fake_matches >= 1:
            return True, 0.95
        
        return None, None
    
    def predict_with_bert(self, text):
        """Predict using BERT model"""
        try:
            # First, check with enhanced pre-detection
            pre_detection, pre_confidence = self.enhanced_pre_detection(text)
            if pre_detection is not None:
                if pre_detection:
                    return "FAKE", pre_confidence
                else:
                    return "REAL", pre_confidence
            
            # Use BERT model
            if self.model_loaded and self.bert_predictor:
                return self.bert_predictor.predict(text)
            else:
                return self.rule_based_analysis(text)
                
        except Exception as e:
            st.error(f"❌ BERT prediction error: {str(e)}")
            return self.rule_based_analysis(text)
    
    def predict_article(self, article):
        """Predict if an article is fake news"""
        text = f"{article['title']} {article['content']}"
        
        if self.model_loaded:
            return self.predict_with_bert(text)
        else:
            return self.rule_based_analysis(text)
    
    def rule_based_analysis(self, text):
        """Rule-based fake news detection as fallback"""
        text_lower = text.lower()
        
        fake_indicators = [
            'breaking', 'shocking', 'secret', 'hidden', 'they don\'t want you to know',
            'miracle', 'instant', 'urgent', 'warning', 'alert', 'fake', 'hoax',
            'vampire', 'werewolf', 'zombie', 'alien', 'bigfoot', 'ghost'
        ]
        
        reliability_indicators = [
            'according to study', 'research shows', 'official report',
            'experts say', 'peer-reviewed', 'journal', 'university', 'study'
        ]
        
        fake_score = sum(2 for word in fake_indicators if word in text_lower)
        reliability_score = sum(1 for word in reliability_indicators if word in text_lower)
        
        total_score = reliability_score - fake_score
        
        if total_score >= 2:
            return "RELIABLE", 0.8
        elif total_score <= -1:
            return "FAKE", 0.9
        else:
            return "UNCERTAIN", 0.5
    
    def analyze_news_batch(self, articles):
        """Analyze a batch of articles in real-time"""
        results = []
        
        if not articles:
            return results
            
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        if self.model_loaded:
            method = "BERT Model + Enhanced Detection"
        else:
            method = "Rule-Based"
            
        status_text.text(f"🔄 Analyzing with {method}...")
        
        for i, article in enumerate(articles):
            prediction, confidence = self.predict_article(article)
            
            result = {
                **article,
                'prediction': prediction,
                'confidence': confidence,
                'analysis_time': time.time(),
                'method': method
            }
            results.append(result)
            
            progress_bar.progress((i + 1) / len(articles))
        
        status_text.text("✅ Analysis complete!")
        return results
    
    def get_model_info(self):
        """Get information about the loaded model"""
        if not self.model_loaded:
            return "Rule-Based Analysis"
        return "BERT Model + Enhanced Detection"