import streamlit as st
import pandas as pd
import plotly.express as px
from deep_translator import GoogleTranslator
from utils.translator import t
from utils.news_api import NewsFetcher
from utils.real_time_analyzer import RealTimeAnalyzer

def show(analyzer: RealTimeAnalyzer, news_fetcher: NewsFetcher = None):
    """Page Live Monitor avec design unifié."""
    
    st.markdown("""
    <style>
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
        .dashboard-container {
            background: rgba(17, 25, 40, 0.8);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.125);
            backdrop-filter: blur(16px);
        }
        .section-container {
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .article-card {
            background: rgba(255,255,255,0.02);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .prediction-badge {
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: bold;
            text-align: center;
        }
        .fake-badge {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #ef4444;
        }
        .real-badge {
            background: rgba(16, 185, 129, 0.2);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #10b981;
        }
        .uncertain-badge {
            background: rgba(245, 158, 11, 0.2);
            border: 1px solid rgba(245, 158, 11, 0.4);
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
    
    st.markdown(f"<h1 class='main-header'>📡 Live Monitor</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <p style='font-size: 1.1rem; color: #94a3b8;'>
            Surveillez l'activité et l'état du système en temps réel
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    live_news_monitor(analyzer, news_fetcher)
    st.markdown("</div>", unsafe_allow_html=True)

def live_news_monitor(analyzer: RealTimeAnalyzer, news_fetcher: NewsFetcher = None):
    """Interface unifiée pour recherche et affichage."""
    
    st.markdown("### " + t("live search topics"))
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        query = st.text_input("Sujets à rechercher", "technology news", placeholder="Entrez les mots-clés...")
    with col2:
        num_articles = st.slider("Nombre d'articles", 5, 20, 10)
    with col3:
        lang = st.selectbox("Langue", ("en", "fr", "ar"))
    
    if st.button("Récupérer les actualités", use_container_width=True):
        fetch_and_analyze_news(news_fetcher, analyzer, query, num_articles, lang)
    
    display_real_time_results()

def fetch_and_analyze_news(news_fetcher, analyzer, query, num_articles, lang='en'):
    """Récupérer et analyser les articles en temps réel."""
    
    if 'results' not in st.session_state:
        st.session_state.results = []
    
    try:
        with st.spinner(f"Recherche d'articles '{query}' en {lang}..."):
            articles = news_fetcher.fetch_real_time_news([query], lang=lang)[:num_articles]
            if articles:
                st.success(f"✅ {len(articles)} articles récupérés")
                st.session_state.results = analyzer.analyze_news_batch(articles)
            else:
                st.warning("❌ Aucun article trouvé")
                st.session_state.results = []
    except Exception as e:
        st.error(f"❌ Erreur: {e}")
        st.session_state.results = []

def display_real_time_results():
    """Affiche les résultats dans un format unifié."""
    
    results = st.session_state.get('results', [])
    if not results:
        st.info(" Aucun résultat à afficher. Lancez une recherche.")
        return
    
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.markdown("### " + t("live results title"))
    
    tab1, tab2 = st.tabs(["Liste des Articles", "Résumé de l'Analyse"])
    
    with tab1:
        for i, res in enumerate(results):
            display_article_card(res, i+1)
    
    with tab2:
        show_analysis_summary(results)
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_article_card(result, index):
    """Affiche un article sous forme de carte stylée."""
    
    st.markdown("<div class='article-card'>", unsafe_allow_html=True)
    
    col_title, col_pred = st.columns([3, 1])
    with col_title:
        st.markdown(f"#### {index}. {result['title']}")
    with col_pred:
        pred = result['prediction']
        conf = result['confidence']
        if pred=="FAKE": 
            badge="fake-badge"; emoji="❌"
        elif pred=="REAL": 
            badge="real-badge"; emoji="✅"
        else: 
            badge="uncertain-badge"; emoji="❓"
        st.markdown(f"<div class='prediction-badge {badge}'>{emoji} {pred} • {conf:.1%}</div>", unsafe_allow_html=True)
    
    col_meta1, col_meta2 = st.columns(2)
    with col_meta1:
        st.markdown(f"**Source:** {result.get('source','Unknown')}")
        st.markdown(f"**Publié:** {result.get('published at','Unknown')}")
    with col_meta2:
        st.markdown(f"**Méthode:** {result.get('method','Unknown')}")
        st.markdown(f"**Confiance:** {conf:.2%}")
    
    st.markdown("**Contenu:**")
    st.markdown(f"{result['content'][:300]}{'...' if len(result['content'])>300 else ''}")
    
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        if result.get('url'):
            st.markdown(f"[🔗 Lire l'article complet]({result['url']})")
    with col_act2:
        with st.expander("Traduire l'article"):
            target_lang = st.selectbox("Langue", ("fr","ar","en"), key=f"lang_{index}")
            if st.button("Traduire", key=f"btn_{index}"):
                try:
                    with st.spinner(f"Traduction en {target_lang}..."):
                        translator = GoogleTranslator(source='auto', target=target_lang)
                        t_title = translator.translate(result['title'])
                        t_content = translator.translate(result['content'][:300]+"...")
                        st.success(f"**Titre ({target_lang}):** {t_title}")
                        st.success(f"**Contenu ({target_lang}):** {t_content}")
                except Exception as e:
                    st.error(f"Échec de la traduction: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_analysis_summary(results):
    if not results:
        return
    df = pd.DataFrame(results)
    fake_count = len(df[df['prediction']=='FAKE'])
    real_count = len(df[df['prediction']=='REAL'])
    uncertain_count = len(df[df['prediction']=='UNCERTAIN'])
    
    st.markdown("### Statistiques Globales")
    col1,col2,col3,col4 = st.columns(4)
    col1.metric("Total Articles", len(df))
    col2.metric("✅ Fiables", real_count)
    col3.metric("❌ Fake News", fake_count)
    col4.metric("❓ Incertains", uncertain_count)
    
    fig = px.pie(df, names='prediction', color='prediction', title="Distribution des Résultats",
                 color_discrete_map={'REAL':'#10b981','FAKE':'#ef4444','UNCERTAIN':'#f59e0b'})
    fig.update_layout(title_x=0.5, showlegend=True, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Métriques Avancées")
    col_a1, col_a2, col_a3 = st.columns(3)
    avg_conf = df['confidence'].mean()
    col_a1.metric("Confiance Moyenne", f"{avg_conf:.2%}")
    col_a2.metric("Taux de Fake News", f"{fake_count/len(df):.2%}")
    col_a3.metric("Taux de Fiabilité", f"{real_count/len(df):.2%}")