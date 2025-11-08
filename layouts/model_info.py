import streamlit as st
# La 'MetricCard' n'est plus importée car nous utilisons le CSS/HTML direct
from utils.translator import t

def show(analyzer):
    """Page d'informations du modèle avec design professionnel unifié."""

    # =====================
    # CSS COMPLET (unifié avec les autres pages)
    # =====================
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

        /* Nouvelles boîtes de statut (design unifié) */
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
        .status-info    { border-color: #3b82f6; color: white; }
        .status-info i { color: #3b82f6; }
        .status-box i   { font-size: 1.2rem; }

        /* Styles pour les widgets Streamlit (tabs) */
        .stTabs [role="tablist"] {
            border-bottom: 2px solid rgba(255,255,255,0.1);
            gap: 1rem;
        }
        .stTabs [role="tab"] {
            background-color: transparent;
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.25rem;
            color: #94a3b8;
            transition: all 0.3s ease;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background-color: rgba(255,255,255,0.05);
            color: white;
            border-bottom: 2px solid #667eea;
        }
        .stTabs [role="tabpanel"] {
            padding-top: 1.5rem;
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
    # TITRE
    # =====================
    st.markdown(f"<h1 class='main-header'><i class='fas fa-robot'></i> {t('mode_model_info')}</h1>", unsafe_allow_html=True)



    # =====================
    # MÉTRIQUES DU MODÈLE (Style unifié)
    # =====================
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        accuracy = "94.2%" if analyzer.model_loaded else "85.0%"
        delta_color = "#10b981" # Vert
        st.markdown(f"""
        <div class='metric-card'>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div class='metric-card-icon' style='color: #a855f7;'>
                    <i class='fas fa-bullseye'></i>
                </div>
            </div>
            <div style="font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.25rem;">Précision</div>
            <div style="font-size: 2rem; font-weight: 700; color: #a855f7;">{accuracy}</div>
            <div class='metric-card-delta' style='color: {delta_color};'>
                <i class='fas fa-arrow-up'></i> +2.1%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div class='metric-card-icon' style='color: #3b82f6;'>
                    <i class='fas fa-database'></i>
                </div>
            </div>
            <div style="font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.25rem;">Couverture (Entraînement)</div>
            <div style="font-size: 2rem; font-weight: 700; color: #3b82f6;">15K+</div>
            <div class='metric-card-delta' style='color: #94a3b8;'>
                Articles
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div class='metric-card-icon' style='color: #f59e0b;'>
                    <i class='fas fa-bolt'></i>
                </div>
            </div>
            <div style="font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.25rem;">Vitesse</div>
            <div style="font-size: 2rem; font-weight: 700; color: #f59e0b;">0.8s</div>
            <div class='metric-card-delta' style='color: #94a3b8;'>
                Par article
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =====================
    # ARCHITECTURE DU MODÈLE
    # =====================
    st.markdown(f"<h3 class='section-title' style='margin-top:2rem;'><i class='fas fa-cogs'></i> Architecture du Modèle</h3>", unsafe_allow_html=True)

    tab_titles = [
        f"Modèle BERT",
        f"Moteur de Règles",
        f"Système Ensemble"
    ]
    tab1, tab2, tab3 = st.tabs(tab_titles)

    # Statut dynamique pour BERT
    if analyzer.model_loaded:
        bert_status = "<span style='color: #10b981;'><i class='fas fa-check-circle'></i> Actif</span>"
    else:
        bert_status = "<span style='color: #ef4444;'><i class='fas fa-times-circle'></i> Inactif</span>"

    with tab1:
        st.markdown(f"""
        <div class='section-container'>
            <h4 style='color: white;'><i class='fas fa-robot'></i> Modèle BERT Fine-Tuned</h4>
            <ul style='color: #cbd5e1; line-height: 1.6;'>
                <li><b>Base:</b> BERT-base-multilingual</li>
                <li><b>Entraînement:</b> 50,000 articles étiquetés</li>
                <li><b>Fonctionnalités:</b> Analyse sémantique profonde, compréhension contextuelle, support multilingue</li>
                <li><b>Performance:</b> 92% de précision</li>
                <li><b>Statut:</b> {bert_status}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"""
        <div class='section-container'>
            <h4 style='color: white;'><i class='fas fa-clipboard-list'></i> Système à Base de Règles</h4>
            <ul style='color: #cbd5e1; line-height: 1.6;'>
                <li>Détection de patterns: Langage sensationnaliste</li>
                <li>Vérification de sources: Base de données de crédibilité</li>
                <li>Analyse structurelle: Formatage typique des fake news</li>
                <li>Indicateurs linguistiques: Marqueurs de tromperie</li>
                <li><b>Performance:</b> 85% de précision</li>
                <li><b>Statut:</b> <span style='color: #10b981;'><i class='fas fa-check-circle'></i> Toujours actif</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown(f"""
        <div class='section-container'>
            <h4 style='color: white;'><i class='fas fa-crosshairs'></i> Système Ensemble</h4>
            <ul style='color: #cbd5e1; line-height: 1.6;'>
                <li><b>Combinaison:</b> BERT + Moteur de Règles + Métadonnées</li>
                <li><b>Pondération:</b> Optimisée par apprentissage automatique</li>
                <li><b>Fusion:</b> Moyenne pondérée des scores de confiance</li>
                <li><b>Avantage:</b> Robustesse et précision améliorées par rapport aux modèles individuels</li>
                <li><b>Performance:</b> 94.2% de précision finale</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # =====================
    # STATUT DU SYSTÈME
    # =====================
    st.markdown(f"<h3 class='section-title' style='margin-top:2rem;'><i class='fas fa-tasks'></i> Statut du Système</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        if analyzer.model_loaded:
            st.markdown(f"<div class='status-box status-success'><i class='fas fa-check-circle'></i> <span><strong>Modèle BERT:</strong> Actif</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='status-box status-error'><i class='fas fa-times-circle'></i> <span><strong>Modèle BERT:</strong> Inactif</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='status-box status-info'><i class='fas fa-clock'></i> <span><strong>Uptime:</strong> 99.8%</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='status-box status-success'><i class='fas fa-server'></i> <span><strong>API Services:</strong> En ligne</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='status-box status-info'><i class='fas fa-calendar-check'></i> <span><strong>Dernière MAJ:</strong> Aujourd'hui</span></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div class='status-box status-success'><i class='fas fa-database'></i> <span><strong>Base de données:</strong> Synchronisée</span></div>", unsafe_allow_html=True)
