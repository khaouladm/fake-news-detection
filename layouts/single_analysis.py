import streamlit as st
from components.cards import MetricCard
from components.charts import create_confidence_gauge
from utils.translator import t
from utils.url_scraper import URLScraper

def show(analyzer):
    """Page d'analyse d'article unique avec design stylisé"""
    
    st.markdown("""
    <style>
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
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
        .section-container {
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .result-card {
            background: rgba(255,255,255,0.02);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .prediction-badge {
            padding: 1rem;
            border-radius: 12px;
            font-weight: bold;
            text-align: center;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .fake-badge {
            background: rgba(239, 68, 68, 0.2);
            border: 2px solid rgba(239, 68, 68, 0.4);
            color: #ef4444;
        }
        .real-badge {
            background: rgba(16, 185, 129, 0.2);
            border: 2px solid rgba(16, 185, 129, 0.4);
            color: #10b981;
        }
        .uncertain-badge {
            background: rgba(245, 158, 11, 0.2);
            border: 2px solid rgba(245, 158, 11, 0.4);
            color: #f59e0b;
        }
        [data-testid="stApp"] .stButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        [data-testid="stApp"] .stButton button:hover {
            transform: translateY(-1px);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h1 class='main-header'><i class='fas fa-file-alt'></i> Analyse d'Article</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <p style='font-size: 1.1rem; color: #94a3b8;'>
            Analysez un article unique à partir de texte ou d'URL
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    input_method = st.radio(
        "Choisissez votre méthode d'analyse :",
        [" Texte direct", "URL d'article"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if "URL" in input_method:
        analyze_from_url(analyzer)
    else:
        analyze_from_text(analyzer)

def analyze_from_url(analyzer):
    st.markdown("### Analyse par URL")
    
    url = st.text_input(
        "<i class='fas fa-globe'></i> URL de l'article",
        placeholder="https://example.com/article",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("Analyser l'URL", use_container_width=True):
            if url:
                perform_url_analysis(url, analyzer)
            else:
                alert_box("Veuillez entrer une URL valide", "warning")
    
    with col2:
        if st.button("Effacer", use_container_width=True):
            st.rerun()

def analyze_from_text(analyzer):
    st.markdown("### Analyse de Texte")
    
    news_text = st.text_area(
        "Contenu de l'article",
        height=200,
        placeholder="Collez le contenu complet de l'article ici...",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("Analyser le Texte", use_container_width=True):
            if news_text:
                perform_text_analysis(news_text, analyzer)
            else:
                alert_box("Veuillez entrer du texte à analyser", "warning")
    
    with col2:
        if st.button("Effacer", use_container_width=True):
            st.rerun()

def perform_url_analysis(url, analyzer):
    with st.spinner("Extraction du contenu de l'URL..."):
        scraper = URLScraper()
        scraped_data = scraper.scrape_article(url)
    
    if scraped_data['success']:
        alert_box("Contenu extrait avec succès!", "success")
        article = {
            'title': scraped_data['title'],
            'content': scraped_data['content'],
            'source': 'URL Scraping',
            'url': url
        }
        with st.expander("Aperçu du contenu extrait", expanded=True):
            st.markdown(f"**Titre:** {article['title']}")
            st.markdown(f"**Contenu (extrait):** {article['content'][:500]}...")
        perform_analysis(article, analyzer)
    else:
        alert_box(f"Erreur d'extraction: {scraped_data.get('error', 'Erreur inconnue')}", "error")

def perform_text_analysis(text, analyzer):
    article = {
        'title': 'Article fourni par l\'utilisateur',
        'content': text,
        'source': 'Input utilisateur'
    }
    perform_analysis(article, analyzer)

def perform_analysis(article, analyzer):
    with st.spinner("Analyse en cours avec l'IA..."):
        prediction, confidence = analyzer.predict_article(article)
    display_analysis_results(prediction, confidence, article, analyzer)

def display_analysis_results(prediction, confidence, article, analyzer):
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.markdown("## Résultats de l'Analyse")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if prediction == "REAL":
            badge_class = "real-badge"
            icon = "fas fa-check-circle"
            text = "INFORMATION FIABLE"
        elif prediction == "FAKE":
            badge_class = "fake-badge"
            icon = "fas fa-times-circle"
            text = "FAKE NEWS"
        else:
            badge_class = "uncertain-badge"
            icon = "fas fa-question-circle"
            text = "INFORMATION INCERTAINE"
        st.markdown(f"""
        <div class='prediction-badge {badge_class}'>
            <i class='{icon}' style='font-size:2rem; margin-bottom:0.5rem;'></i><br>
            {text}
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Méthode utilisée:** {analyzer.get_model_info()}")
    
    with col2:
        fig = create_confidence_gauge(confidence, "Niveau de Confiance")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown("### Détails de l'Analyse")
    st.markdown(f"**Titre:** {article['title']}")
    st.markdown(f"**Source:** {article['source']}")
    if 'url' in article:
        st.markdown(f"**URL:** {article['url']}")
    st.markdown(f"**Confiance:** {confidence:.2%}")
    st.markdown("**Extrait du contenu:**")
    content_preview = article['content'][:500] + "..." if len(article['content']) > 500 else article['content']
    st.markdown(f"<div style='background: rgba(255,255,255,0.02); padding:1rem; border-radius:8px; margin:0.5rem 0;'>{content_preview}</div>", unsafe_allow_html=True)
    st.markdown("</div>")
    
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown("### Explications")
    if prediction == "FAKE":
        st.markdown("""
        <div style='background: rgba(239,68,68,0.1); padding:1rem; border-radius:8px; border-left:4px solid #ef4444;'>
            <h4 style='color:#ef4444; margin-top:0;'><i class='fas fa-exclamation-triangle'></i> Indicateurs détectés:</h4>
            <ul style='color:#fca5a5;'>
                <li>Langage sensationnaliste ou exagéré</li>
                <li>Absence de sources vérifiables</li>
                <li>Affirmations sans preuves concrètes</li>
                <li>Appel émotionnel excessif</li>
                <li>Incohérences logiques</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: rgba(16,185,129,0.1); padding:1rem; border-radius:8px; border-left:4px solid #10b981;'>
            <h4 style='color:#10b981; margin-top:0;'><i class='fas fa-check-circle'></i> Indicateurs de fiabilité:</h4>
            <ul style='color:#86efac;'>
                <li>Langage mesuré et factuel</li>
                <li>Sources identifiables et crédibles</li>
                <li>Citations appropriées</li>
                <li>Ton journalistique équilibré</li>
                <li>Informations vérifiables</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>")
    st.markdown("</div>")

def alert_box(message, alert_type="success"):
    color, icon = {
        "success": ("#10b981", "fas fa-check-circle"),
        "error": ("#ef4444", "fas fa-exclamation-circle"),
        "warning": ("#f59e0b", "fas fa-exclamation-triangle"),
        "info": ("#3b82f6", "fas fa-info-circle")
    }.get(alert_type, ("#3b82f6", "fas fa-info-circle"))
    
    st.markdown(f"""
    <div style='background: rgba(59,130,246,0.1); padding:1rem; border-radius:8px; border-left:4px solid {color}; display:flex; align-items:center; gap:10px;'>
        <i class='{icon}' style='color:{color}; font-size:1.2rem;'></i>
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)