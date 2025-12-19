

import warnings
# Suppress warnings about package renaming
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*renamed to.*ddgs.*")

import os
import re
import numpy as np
from urllib.parse import urlparse
import streamlit as st
from duckduckgo_search import DDGS
from sentence_transformers import CrossEncoder

# ---------------------------
#  Load / Download Model Locally
# ---------------------------
BASE_DIR = os.path.dirname(__file__)
# Points to the 'models' folder we created earlier
MODEL_DIR = os.path.join(BASE_DIR, "../models/factchecker_nli")

class FactChecker:
    def __init__(self):
        self.model = self._load_model()
        
        #  Trusted news outlets (EN/FR/AR)
        self.trusted_domains = [
            "reuters.com", "apnews.com", "bbc.com", "cnn.com", "afp.com",
            "bloomberg.com", "nytimes.com", "theguardian.com", "forbes.com",
            "aljazeera.net", "alarabiya.net", "skynewsarabia.com", "bbc.com/arabic",
            "hespress.com", "france24.com", "lemonde.fr", "lefigaro.fr", "wsj.com",
            "rt.com", "dw.com", "independent.co.uk", "fifa.com"
        ]

        self.translations = {
            'en': { 'verified': "VERIFIED REAL", 'fake': "DEBUNKED / FAKE", 'uncertain': "UNVERIFIED", 'no_results': "Suspicious: No coverage found.", 'score': "Credibility Score" },
            'fr': { 'verified': "VÉRIFIÉ RÉEL", 'fake': "DÉMENTI / FAUX", 'uncertain': "NON VÉRIFIÉ", 'no_results': "Suspect : Aucune couverture trouvée.", 'score': "Score de Crédibilité" },
            'ar': { 'verified': "موثوق (حقيقي)", 'fake': "تم دحضه / زائف", 'uncertain': "غير مؤكد", 'no_results': "مشبوه: لم يتم العثور على تغطية إعلامية.", 'score': "درجة المصداقية" }
        }

    @st.cache_resource
    def _load_model(_self):
        """Loads the model. Cached by Streamlit."""
        try:
            # Check standard paths
            if os.path.exists(MODEL_DIR) and len(os.listdir(MODEL_DIR)) > 0:
                return CrossEncoder(MODEL_DIR)
            
            # Fallback to the old folder name if user didn't run the migration script
            old_path = os.path.join(BASE_DIR, "../factchecker_model_multilingual")
            if os.path.exists(old_path) and len(os.listdir(old_path)) > 0:
                return CrossEncoder(old_path)
                
            else:
                # Only downloads if folder is missing/empty
                model_name = "symanto/xlm-roberta-base-snli-mnli-anli-xnli"
                model = CrossEncoder(model_name)
                # Try to save to model dir, otherwise just return
                try:
                    os.makedirs(MODEL_DIR, exist_ok=True)
                    model.save_pretrained(MODEL_DIR)
                except: pass
                return model
        except Exception as e:
            st.error(f"Error loading model: {e}")
            return None

    def _clean_query(self, query):
        """Cleans the title to make it search-friendly"""
        if not query: return ""
        # Remove source attribution at the end (e.g. "| Al Jazeera")
        query = re.split(r'\s+[|:–-]\s+', query)[0]
        # Remove quotes and extra whitespace
        query = query.replace('"', '').replace("'", "").strip()
        return query

    def search_web(self, query, max_results=10):
        """
        Smart Search Strategy:
        1. Try cleaned full title.
        2. If no results, try first 8 words (keywords).
        """
        clean_q = self._clean_query(query)
        results = []
        
        # Attempt 1: Full Cleaned Title
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(clean_q, max_results=max_results))
        except:
            pass
            
        # Attempt 2: Fallback to Keywords (if Attempt 1 failed)
        if not results:
            words = re.findall(r'\w+', clean_q)
            # Filter for significant words (len > 2)
            sig_words = [w for w in words if len(w) > 2 or w.isdigit()]
            
            if len(sig_words) > 0:
                short_q = " ".join(sig_words[:8]) # Search first 8 words
                try:
                    with DDGS() as ddgs:
                        results = list(ddgs.text(short_q, max_results=max_results))
                except:
                    pass
                    
        return results

    def get_domain(self, url):
        try:
            return urlparse(url).netloc.replace("www.", "")
        except:
            return ""

    def verify_article(self, claim, lang='en'):
        """Main verification logic"""
        if not self.model:
            return {"status": "Error", "reason": "Model not loaded", "confidence": 0, "evidence": [], "color": "red"}

        t = self.translations.get(lang, self.translations['en'])
        
        # 1. Perform Smart Search
        results = self.search_web(claim)
        
        if not results:
            return {"status": t['fake'], "reason": t['no_results'], "confidence": 0.85, "evidence": [], "color": "red"}

        total_weighted_score = 0
        total_weight = 0
        evidence_list = []

        # 2. Prepare batch for AI (Efficiency)
        snippets = [(claim, r.get("body", "")) for r in results if r.get("body", "")]
        
        if not snippets:
            return {"status": t['uncertain'], "reason": "No text to analyze", "confidence": 0, "evidence": [], "color": "orange"}

        # 3. Predict
        logits_list = self.model.predict(snippets)

        valid_idx = 0
        for res in results:
            snippet = res.get("body", "")
            if not snippet: continue
            
            title = res.get("title", "")
            link = res.get("href", "")
            domain = self.get_domain(link)
            is_trusted = any(x in domain for x in self.trusted_domains)

            logits = logits_list[valid_idx]
            valid_idx += 1
            
            # Softmax
            exp_logits = np.exp(logits)
            probs = exp_logits / np.sum(exp_logits)
            
            # Symanto Model: 0=Entailment, 1=Neutral, 2=Contradiction
            p_entail = float(probs[0])
            p_neutral = float(probs[1])
            p_contra = float(probs[2])

            # 4. Weighting Logic
            # Ignore neutral/irrelevant results
            if p_neutral > 0.75:
                weight = 0.05 # Almost ignore
                item_score = 0
            else:
                # Trust reliable sources more
                weight = 4.0 if is_trusted else 1.0
                item_score = p_entail - p_contra

            total_weighted_score += item_score * weight
            total_weight += weight

            # Only show relevant evidence in UI
            if p_neutral < 0.85:
                evidence_list.append({
                    "source": title,
                    "domain": domain,
                    "is_trusted": is_trusted,
                    "snippet": snippet,
                    "url": link,
                    "support_score": item_score
                })

        if total_weight < 0.5:
            return {"status": t['uncertain'], "reason": "Insufficient relevant evidence", "confidence": 0, "evidence": evidence_list, "color": "orange"}

        # 5. Final Calculation
        final_score = total_weighted_score / total_weight
        
        # Adjusted Thresholds
        if final_score > 0.15:
            status = t['verified']
            color = "green"
        elif final_score < -0.2: # More sensitive to fakes
            status = t['fake']
            color = "red"
        else:
            status = t['uncertain']
            color = "orange"

        return {
            "status": status,
            "reason": f"{t['score']}: {final_score:.2f}",
            "confidence": abs(final_score),
            "evidence": evidence_list,
            "color": color
        }