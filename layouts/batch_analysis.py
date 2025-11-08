import streamlit as st
import pandas as pd
from components.cards import MetricCard
from components.charts import create_confidence_gauge
from utils.translator import t

def show(analyzer=None):
    """Page d'analyse par lot avec design professionnel."""
    
    # =======================
    # CSS et styles globaux
    # =======================
    st.markdown("""
    <style>
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

        /* Header */
        .main-header {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        /* Section container */
        .section-container {
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255,255,255,0.08);
        }

        /* Metric card */
        .metric-card {
            background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid rgba(102,126,234,0.2);
            transition: transform 0.2s ease;
        }
        .metric-card:hover { 
            transform: translateY(-2px); 
            border-color: rgba(102,126,234,0.4); 
        }

        [data-testid="stApp"] .stButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        [data-testid="stApp"] .stButton button:hover {
            transform: translateY(-1px);
        }

        /* Custom info box */
        .info-custom { 
            background: rgba(59, 130, 246, 0.1); 
            border-radius: 8px; 
            padding: 1rem; 
            margin: 1rem 0; 
            color: #93c5fd; 
            display:flex; 
            align-items:center; 
            gap:10px; 
        }
    </style>
    """, unsafe_allow_html=True)

    # =======================
    # Header
    # =======================
    st.markdown(f"<h1 class='main-header'><i class='fas fa-layer-group'></i> Analyse par Lot</h1><br><br>", unsafe_allow_html=True)

    # =======================
    # Upload fichier
    # =======================
    uploaded_file = st.file_uploader("Choisir un fichier CSV ou XLSX", type=['csv','xlsx'])
    if uploaded_file:
        df = load_file(uploaded_file)
        if df is not None:
            st.success(f"Fichier chargé : {len(df)} articles")
            st.dataframe(df.head(), use_container_width=True)

            # Options d'analyse
            col1, col2 = st.columns(2)
            with col1:
                analyze_content = st.checkbox("Analyser le contenu", value=True)
                detect_sources = st.checkbox("Vérifier les sources", value=True)
            with col2:
                confidence_threshold = st.slider("Seuil de confiance", 0.5, 1.0, 0.7)
                max_articles = st.number_input("Nombre max d'articles", 1, 1000, len(df))

            if st.button("Lancer l'Analyse"):
                perform_batch_analysis(df, max_articles, confidence_threshold)

# =======================
# Charger fichier CSV/XLSX
# =======================
def load_file(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        return None

# =======================
# Analyse par lot simulée
# =======================
def perform_batch_analysis(df, max_articles, confidence_threshold):
    progress_bar = st.progress(0)
    status_text = st.empty()
    results = []
    total_articles = min(len(df), max_articles)

    for i in range(total_articles):
        progress_bar.progress((i+1)/total_articles)
        status_text.text(f"Analyse {i+1}/{total_articles}...")
        results.append({
            'title': df.iloc[i]['title'] if 'title' in df.columns else f'Article {i+1}',
            'prediction': 'REAL' if i % 4 != 0 else 'FAKE',
            'confidence': 0.85 + (i * 0.01) % 0.15
        })

    display_batch_results(results, confidence_threshold)
    progress_bar.empty()
    status_text.empty()

# =======================
# Affichage des résultats
# =======================
def display_batch_results(results, confidence_threshold):
    st.success("Analyse terminée !")
    df_results = pd.DataFrame(results)

    col1, col2, col3, col4 = st.columns(4)
    with col1: MetricCard("Total", len(df_results), icon="📊").render()
    with col2: MetricCard("Réels", len(df_results[df_results['prediction']=="REAL"]), icon="✅").render()
    with col3: MetricCard("Fake", len(df_results[df_results['prediction']=="FAKE"]), icon="❌").render()
    with col4: MetricCard("Haute confiance", len(df_results[df_results['confidence']>=confidence_threshold]), icon="🎯").render()

    st.dataframe(df_results, use_container_width=True)
