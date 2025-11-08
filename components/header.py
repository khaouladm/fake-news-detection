import streamlit as st
from utils.translator import t

def render_header():
    """En-tête moderne avec métriques principales"""
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="main-header">
            <h1>📰 {t('app_title')}</h1>
            <p class="app-subtitle">{t('app_subtitle')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Articles Analysés</div>
            <div class="metric-value">1,247</div>
            <div class="metric-trend positive">↑ 12%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Taux de Précision</div>
            <div class="metric-value">94.2%</div>
            <div class="metric-trend positive">↑ 2.1%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        status_color = "#10b981" if st.session_state.system_online else "#ef4444"
        status_text = "En Ligne" if st.session_state.system_online else "Hors Ligne"
        
        st.markdown(f"""
        <div class="status-indicator">
            <div class="status-dot" style="background-color: {status_color}"></div>
            <div class="status-text">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='header-divider'></div>", unsafe_allow_html=True)