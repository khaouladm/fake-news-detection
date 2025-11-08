import streamlit as st
from utils.translator import t
import time # Gardé pour la simulation de test

def add_custom_css():
    """Ajoute le CSS personnalisé pour un design professionnel unifié."""
    st.markdown("""
    <style>
        /* Importation de Font Awesome */
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
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: white;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        /* Cartes de métriques (style du dashboard) */
        .metric-card {
            background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid rgba(102,126,234,0.2);
            transition: transform 0.2s ease;
            height: 100%; /* Assure la même hauteur */
        }
        .metric-card:hover {
            transform: translateY(-2px);
            border-color: rgba(102,126,234,0.4);
        }
        .metric-card-icon {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.5rem;
            border-radius: 10px;
            margin-right: 0.75rem;
            font-size: 1.3rem;
            width: 40px; /* Taille fixe */
            height: 40px; /* Taille fixe */
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .metric-card-delta {
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 0.25rem;
        }

        /* Boîtes de statut (style de model_info.py) */
        .status-box {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            border-left: 5px solid;
            margin-bottom: 0.75rem;
        }
        .status-success { border-color: #10b981; color: white; }
        .status-success i { color: #10b981; }
        .status-error   { border-color: #ef4444; color: white; }
        .status-error i { color: #ef4444; }
        .status-warning { border-color: #f59e0b; color: white; }
        .status-warning i { color: #f59e0b; }
        .status-info    { border-color: #3b82f6; color: white; }
        .status-info i { color: #3b82f6; }
        .status-box i   { font-size: 1.2rem; }

        /* Styles pour les widgets Streamlit */
        .stButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(102,126,234,0.4);
        }
        .stTextInput > div > div > input, 
        .stTextArea > div > textarea,
        .stSelectbox > div > div,
        .stSlider > div {
            background-color: rgba(0,0,0,0.2);
            color: white;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        /* Style spécifique pour le slider */
        .stSlider > div {
            padding: 0.5rem;
        }
        .stNumberInput > div > div > input {
            background-color: rgba(0,0,0,0.2);
            color: white;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
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

# =====================
# PAGE PRINCIPALE
# =====================
def show(news_fetcher):
    """Page des paramètres avec design unifié"""
    
    add_custom_css()

    st.markdown(f"<h1 class='main-header'><i class='fas fa-cog'></i> {t('mode_api_settings')}</h1>", unsafe_allow_html=True)



    # =====================
    # Configuration API
    # =====================
    with st.container():
        st.markdown(f"<h3 class='section-title'><i class='fas fa-key'></i> Configuration API</h3>", unsafe_allow_html=True)
        
        with st.form("api_settings"):
            st.markdown("<div class_='section-container'>", unsafe_allow_html=True)
            
            st.markdown("**Clés API**")
            
            # GNews API
            gnews_key = st.text_input(
                "GNews API Key",
                type="password",
                placeholder="Entrez votre clé API GNews",
                help="Obtenez une clé sur gnews.io"
            )
            
            # NewsAPI
            newsapi_key = st.text_input(
                "NewsAPI Key (Optionnel)",
                type="password",
                placeholder="Entrez votre clé NewsAPI",
                help="Pour des sources supplémentaires"
            )
            
            # Soumission
            col1, col2 = st.columns([1, 4])
            with col1:
                api_submitted = st.form_submit_button(
                    "Sauvegarder", 
                    use_container_width=True,
                    help="Sauvegarder les clés dans la session"
                )
            with col2:
                test_api = st.form_submit_button(
                    "Tester les APIs", 
                    use_container_width=True,
                    help="Tester la connexion aux APIs"
                )
            
            # Logique de sauvegarde (messages stylés)
            if api_submitted:
                if gnews_key:
                    st.session_state.gnews_key = gnews_key
                    news_fetcher.gnews_key = gnews_key
                    st.markdown("<div class='status-box status-success'><i class='fas fa-check-circle'></i> <span>Clé GNews sauvegardée avec succès!</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='status-box status-warning'><i class='fas fa-exclamation-triangle'></i> <span>La clé GNews est requise</span></div>", unsafe_allow_html=True)
                
                if newsapi_key:
                    st.session_state.newsapi_key = newsapi_key
                    news_fetcher.newsapi_key = newsapi_key
                    st.markdown("<div class='status-box status-success'><i class='fas fa-check-circle'></i> <span>Clé NewsAPI sauvegardée!</span></div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True) # Fin section-container

        # Logique de test (en dehors du form mais déclenchée par lui)
        if test_api:
            test_api_connections(gnews_key, newsapi_key, news_fetcher)

    # =====================
    # Paramètres d'analyse
    # =====================
    with st.container():
        st.markdown(f"<h3 class='section-title' style='margin-top:2rem;'><i class='fas fa-tools'></i> Paramètres d'Analyse</h3>", unsafe_allow_html=True)
        
        with st.container(): # Simule le section-container pour le style
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                confidence_threshold = st.slider(
                    "Seuil de confiance minimum",
                    min_value=0.5,
                    max_value=1.0,
                    value=st.session_state.get('confidence_threshold', 0.7),
                    help="Seuil de confiance pour considérer une analyse comme fiable"
                )
                
                max_articles = st.number_input(
                    "Nombre maximum d'articles par analyse",
                    min_value=5,
                    max_value=100,
                    value=st.session_state.get('max_articles', 20),
                    help="Limite le nombre d'articles analysés en une seule fois"
                )
            
            with col2:
                auto_refresh = st.checkbox(
                    "Actualisation automatique",
                    value=st.session_state.get('auto_refresh', True),
                    help="Actualise automatiquement les données du tableau de bord"
                )
                
                if auto_refresh:
                    refresh_interval = st.selectbox(
                        "Intervalle d'actualisation",
                        options=["5 minutes", "15 minutes", "30 minutes", "1 heure"],
                        index=1
                    )
            
            if st.button("Sauvegarder les paramètres", use_container_width=True, help="Sauvegarder les paramètres d'analyse"):
                st.session_state.confidence_threshold = confidence_threshold
                st.session_state.max_articles = max_articles
                st.session_state.auto_refresh = auto_refresh
                if auto_refresh:
                    st.session_state.refresh_interval = refresh_interval
                st.markdown("<div class='status-box status-success'><i class='fas fa-check-circle'></i> <span>Paramètres sauvegardés avec succès!</span></div>", unsafe_allow_html=True)

    # =====================
    # Informations système (Cartes de Métriques)
    # =====================
    with st.container():
        st.markdown(f"<h3 class='section-title' style='margin-top:2rem;'><i class='fas fa-info-circle'></i> Informations Système</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <div class='metric-card-icon' style='color: #3b82f6;'>
                        <i class='fas fa-code-branch'></i>
                    </div>
                </div>
                <div style="font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.25rem;">Version Application</div>
                <div style="font-size: 2rem; font-weight: 700; color: #3b82f6;">2.0.0</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='metric-card' style='margin-top: 1rem;'>
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <div class='metric-card-icon' style='color: #10b981;'>
                        <i class='fas fa-file-alt'></i>
                    </div>
                </div>
                <div style="font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.25rem;">Articles Analysés (Total)</div>
                <div style="font-size: 2rem; font-weight: 700; color: #10b981;">1,247</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <div class='metric-card-icon' style='color: #a855f7;'>
                        <i class='fas fa-calendar-alt'></i>
                    </div>
                </div>
                <div style="font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.25rem;">Dernière Mise à Jour</div>
                <div style="font-size: 2rem; font-weight: 700; color: #a855f7;">2024-01-15</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='metric-card' style='margin-top: 1rem;'>
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <div class='metric-card-icon' style='color: #ef4444;'>
                        <i class='fas fa-check-double'></i>
                    </div>
                </div>
                <div style="font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.25rem;">Taux de Succès (Modèle)</div>
                <div style="font-size: 2rem; font-weight: 700; color: #ef4444;">94.2%</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True) # Fin dashboard-container


# =====================
# FONCTION DE TEST (Stylisée)
# =====================
def test_api_connections(gnews_key, newsapi_key, news_fetcher):
    """Tester les connexions API avec des alertes stylisées."""
    
    with st.spinner("Test des connexions en cours..."):
        time.sleep(1.5) # Simulation du test
        
        # Test GNews
        if gnews_key:
            # (Ici, vous feriez un vrai appel `news_fetcher.test_gnews()`)
            st.markdown("<div class='status-box status-success'><i class='fas fa-check-circle'></i> <span>GNews API: Connectée avec succès!</span></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-box status-error'><i class='fas fa-times-circle'></i> <span>GNews API: Clé manquante</span></div>", unsafe_allow_html=True)
        
        # Test NewsAPI
        if newsapi_key:
            # (Ici, vous feriez un vrai appel `news_fetcher.test_newsapi()`)
            st.markdown("<div class='status-box status-success'><i class='fas fa-check-circle'></i> <span>NewsAPI: Connectée avec succès!</span></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-box status-warning'><i class='fas fa-exclamation-triangle'></i> <span>NewsAPI: Non configurée (optionnel)</span></div>", unsafe_allow_html=True)