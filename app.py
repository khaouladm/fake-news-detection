import streamlit as st
from components.sidebar import render_sidebar
from utils.translator import set_lang, t
import sys, os

def main():
    # Configuration de la page
    st.set_page_config(
        page_title="NewsVerifi AI - Dashboard Professionnel",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    initialize_session_state()
    set_lang(st.session_state.lang)  # ✅ Activation globale de la langue ici
    load_css()
    render_sidebar()
    render_main_content()

def initialize_session_state():
    """Initialisation des variables de session Streamlit"""
    if 'lang' not in st.session_state:
        st.session_state.lang = 'fr'
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    if 'system_online' not in st.session_state:
        st.session_state.system_online = True
    if 'last_update' not in st.session_state:
        st.session_state.last_update = 'Jamais'
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = None
    if 'news_fetcher' not in st.session_state:
        st.session_state.news_fetcher = None

def load_css():
    """Charger le CSS personnalisé"""
    try:
        with open('assets/styles.css') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <style>
        .main { background: #0f172a; color: white; }
        .metric-card {
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            border: 1px solid rgba(255,255,255,0.1);
        }
        </style>
        """, unsafe_allow_html=True)

def render_main_content():
    """Afficher la page correspondant à la navigation"""
    current_page = st.session_state.current_page
    initialize_components()

    # ✅ Chaque page hérite automatiquement de la langue active
    set_lang(st.session_state.lang)

    if current_page == 'dashboard':
        from layouts.dashboard import show
        show(st.session_state.analyzer, st.session_state.news_fetcher)
    elif current_page == 'live_monitor':
        from layouts.live_monitor import show
        show(st.session_state.analyzer, st.session_state.news_fetcher)
    elif current_page == 'single_analysis':
        from layouts.single_analysis import show
        show(st.session_state.analyzer)
    elif current_page == 'batch_analysis':
        from layouts.batch_analysis import show
        show(st.session_state.analyzer)
    elif current_page == 'model_info':
        from layouts.model_info import show
        show(st.session_state.analyzer)
    elif current_page == 'settings':
        from layouts.settings import show
        show(st.session_state.news_fetcher)
    else:
        from layouts.dashboard import show
        show(st.session_state.analyzer, st.session_state.news_fetcher)

def initialize_components():
    """Initialiser les composants analyzers et news_fetcher"""
    if st.session_state.analyzer is None:
        from utils.real_time_analyzer import RealTimeAnalyzer
        st.session_state.analyzer = RealTimeAnalyzer()
    if st.session_state.news_fetcher is None:
        from utils.news_api import NewsFetcher
        st.session_state.news_fetcher = NewsFetcher()

if __name__ == "__main__":
    main()
