import streamlit as st
import os
from config import APP_CONFIG
from utils.translator import t, set_lang

class SidebarRenderer:
    """Classe pour gérer le rendu de la sidebar avec un design épuré et professionnel."""
    
    def __init__(self):
        self.apply_styles()
    
    def render(self):
        """Point d'entrée principal pour le rendu de la sidebar"""
        with st.sidebar:
            self.render_sidebar_header()
            self.render_language_selector()
            self.render_navigation()
            self.render_system_status()
            self.render_quick_actions()
    
    # -------------------------- HEADER --------------------------
    def render_sidebar_header(self):
        """Affiche l'en-tête de la sidebar avec le logo et info de l'app"""     
        st.markdown(f"""
        <div class="sidebar-header">
            <div class="app-info">
                <h2 class="app-title">NewsVerifi AI</h2>
                <p class="app-subtitle">Détection Intelligente</p>
            </div>
        </div>
        <hr class='divider'>
        """, unsafe_allow_html=True)
    
    # -------------------------- LANGUE --------------------------
    def render_language_selector(self):
        """Affiche le sélecteur de langue"""
        st.markdown("<h4 class='sidebar-section-title'>Langue</h4>", unsafe_allow_html=True)
        current_lang = st.session_state.get('lang', 'fr')
        lang_options = list(APP_CONFIG['SUPPORTED_LANGUAGES'].keys())
        current_index = next(
            (i for i, (name, code) in enumerate(APP_CONFIG['SUPPORTED_LANGUAGES'].items()) 
             if code == current_lang), 0
        )
        selected_lang = st.selectbox(
            "Sélectionner une langue",
            options=lang_options,
            index=current_index,
            label_visibility="collapsed"
        )
        new_lang_code = APP_CONFIG['SUPPORTED_LANGUAGES'][selected_lang]
        if new_lang_code != current_lang:
            set_lang(new_lang_code)
            st.rerun()
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    
    # -------------------------- NAVIGATION --------------------------
    def render_navigation(self):
        """Affiche la navigation principale"""
        st.markdown("<h4 class='sidebar-section-title'>Navigation</h4>", unsafe_allow_html=True)
        nav_items = [
            {"id": "dashboard", "label": t('mode_dashboard')},
            {"id": "live_monitor", "label": t('mode_live')},
            {"id": "single_analysis", "label": t('mode_single')},
            {"id": "batch_analysis", "label": t('mode_batch')},
            {"id": "model_info", "label": t('mode_model_info')},
            {"id": "settings", "label": t('mode_api_settings')}
        ]
        current_page = st.session_state.get("current_page", "dashboard")
        for item in nav_items:
            self.render_navigation_item(item, current_page)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    
    def render_navigation_item(self, item, current_page):
        """Affiche un élément de navigation individuel avec style actif"""
        is_active = item["id"] == current_page
        style = f"""
        <style>
        div[data-testid="stButton"] > button[key="nav_{item['id']}"] {{
            background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if is_active else 'rgba(255,255,255,0.04)'} !important;
            color: {'white' if is_active else '#C8D1E0'} !important;
            border: 1px solid {'rgba(102,126,234,0.5)' if is_active else 'rgba(255,255,255,0.1)'} !important;
            font-weight: {'600' if is_active else '500'} !important;
        }}
        </style>
        """
        st.markdown(style, unsafe_allow_html=True)
        if st.button(item["label"], key=f"nav_{item['id']}", use_container_width=True):
            st.session_state.current_page = item["id"]
            st.rerun()
    
    # -------------------------- STATUT --------------------------
    def render_system_status(self):
        """Affiche le statut du système"""
        st.markdown("<h4 class='sidebar-section-title'>Statut du système</h4>", unsafe_allow_html=True)
        self.render_analyzer_status()
        st.markdown("""
        <div class='status-box status-success'>
            <span class='status-text'><strong>Services API:</strong> En ligne</span>
        </div>
        """, unsafe_allow_html=True)
        last_update = st.session_state.get('last_update', 'Jamais')
        st.caption(f"Dernière MAJ: {last_update}")
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    
    def render_analyzer_status(self):
        """Affiche le statut de l'analyseur IA"""
        try:
            status_class = 'status-success' if st.session_state.analyzer.model_loaded else 'status-error'
            status_text = 'Actif' if st.session_state.analyzer.model_loaded else 'Inactif'
        except Exception:
            status_class = 'status-warning'
            status_text = 'Indisponible'
        st.markdown(f"""
        <div class='status-box {status_class}'>
            <span class='status-text'><strong>Modèle IA:</strong> {status_text}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # -------------------------- ACTIONS RAPIDES --------------------------
    def render_quick_actions(self):
        """Affiche les actions rapides"""
        st.markdown("<h4 class='sidebar-section-title'>Actions rapides</h4>", unsafe_allow_html=True)
        if st.button("Actualiser les données", key="quick_refresh", use_container_width=True, help="Actualiser toutes les données du système"):
            self.handle_refresh()
    
    def handle_refresh(self):
        """Actualise les données et notifie l'utilisateur"""
        st.session_state.last_update = "À l'instant"
        st.toast("Données actualisées !")
        st.rerun()
    
    # -------------------------- STYLES --------------------------
    def apply_styles(self):
        """Applique les styles CSS épurés et compacts pour la sidebar"""
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0A0F24 0%, #101935 100%);
            color: #EEE;
            padding: 1rem 0.75rem;
            border-right: 1px solid rgba(255,255,255,0.1);
            height: 100vh;
            overflow-y: auto;
        }

        /* Header */
        .sidebar-header { display: flex; align-items: center; gap: 0.2rem; margin-bottom: 0.3rem; padding: 0.3rem 0; }
        .app-title { font-size:1.3rem;font-weight:700;margin:0;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent; }
        .app-subtitle { font-size:0.8rem;color:#94a3b8;margin:0;font-weight:500; }

        /* Titres de sections */
        .sidebar-section-title {
            font-size:0.95rem !important;
            color:#C8D1E0;
            margin:0.4rem 0 0.6rem 0 !important;
            font-weight:600;
        }

        /* Séparateur allégé */
        .divider {
            border:none;
            height:1px;
            background:linear-gradient(90deg,transparent 0%,rgba(255,255,255,0.1) 50%,transparent 100%);
            margin:0.8rem 0;
        }

        /* Boutons plus rapprochés */
        [data-testid="stSidebar"] .stButton button {
            text-align: left !important;
            border-radius: 10px !important;
            padding: 0.75rem 1rem !important;
            margin: 0.25rem 0 !important;   /* espacement vertical réduit */
            font-size: 0.95rem !important;
            height: 45px !important;
            transition: all 0.3s ease !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
        }

        [data-testid="stSidebar"] .stButton button:hover {
            transform: translateX(5px) !important;
            background: rgba(255,255,255,0.1) !important;
            color:white !important;
        }

        /* Boîtes de statut rapprochées */
        .status-box {
            background:rgba(255,255,255,0.05);
            border-radius:10px;
            padding:0.6rem 0.9rem;
            margin-bottom:0.4rem;   /* réduit */
            border-left:4px solid;
            transition: all 0.2s ease;
        }
        .status-box:hover { background: rgba(255,255,255,0.08); transform: translateX(2px); }
        .status-success { border-color:#10b981;color:white; }
        .status-error { border-color:#ef4444;color:white; }
        .status-warning { border-color:#f59e0b;color:white; }
        .status-text { font-size:0.85rem;font-weight:500; }

        /* Caption dernière MAJ */
        [data-testid="stSidebar"] .stCaption {
            color:#94a3b8 !important;
            font-size:0.75rem !important;
            text-align:center !important;
            margin-top:0.3rem !important;
        }

        /* Scrollbar */
        [data-testid="stSidebar"]::-webkit-scrollbar { width:5px; }
        [data-testid="stSidebar"]::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); border-radius:3px;}
        [data-testid="stSidebar"]::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius:3px; }
        [data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.3); }
        </style>
        """, unsafe_allow_html=True)


# -------------------------- INTERFACE PRINCIPALE --------------------------
def render_sidebar():
    """Affiche la sidebar complète"""
    sidebar = SidebarRenderer()
    sidebar.render()
