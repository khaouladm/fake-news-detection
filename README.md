# 🛡️ Hybrid Multilingual Fake News Detection

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![AI Model](https://img.shields.io/badge/Model-BERT%20%2B%20XLM--RoBERTa-green)
![Status](https://img.shields.io/badge/Status-Active-success)

**Veritas AI** is an advanced, real-time fake news detection system designed to combat digital misinformation. It utilizes a **Hybrid Architecture** that decouples "Style Detection" from "Fact Verification," allowing it to identify both sophisticated disinformation (written professionally) and obvious hoaxes across **English, French, and Arabic**.

---

## 🚀 Key Features

* **🌐 Multilingual Support:** Native analysis for English, French, and Arabic.
* **🧠 Hybrid AI Engine:**
    * **Style Classifier:** Uses **BERT Embeddings + Logistic Regression** to detect deceptive writing patterns (sensationalism, urgency).
    * **Fact Checker:** Uses **Retrieval-Augmented Generation (RAG)** with **XLM-RoBERTa** to cross-reference claims against live web search results.
* **🕵️ Real-Time Web Verification:** Automatically queries DuckDuckGo to find evidence from trusted global sources (Reuters, Al Jazeera, AFP, etc.).
* **📰 Live News Monitor:** Fetches and analyzes breaking news topics in real-time.
* **⚡ CPU Optimized:** Engineered to run efficiently on standard laptops without requiring a GPU.

---

## ⚙️ System Architecture

The system processes input through two parallel pipelines:

### 1. Pipeline A: The Style Classifier (Offline)
Detects *how* the text is written.
* **Input:** User text (AR/FR/EN).
* **Translation:** Neural Machine Translation converts non-English text to English.
* **Feature Extraction:** `bert-base-uncased` extracts deep semantic embeddings (768-dim).
* **Classification:** Logistic Regression predicts "Real" or "Fake" based on style.

### 2. Pipeline B: The Fact Checker (Online)
Detects *if* the text is factually true.
* **Search:** Queries the web for the claim using region-aware settings.
* **Semantic Filter:** Uses `MiniLM` to discard irrelevant search results (noise).

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/veritas-ai.git](https://github.com/yourusername/veritas-ai.git)
cd veritas-ai
