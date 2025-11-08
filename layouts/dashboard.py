import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui import MetricCard
from components.charts import create_analysis_pie_chart, create_trend_chart
from utils.translator import t

def show(analyzer, news_fetcher):
    """Dashboard principal avec un design professionnel."""
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
        .activity-item {
            background: rgba(255,255,255,0.02);
            padding: 1rem;
            margin-bottom: 0.75rem;
            border-radius: 10px;
            border-left: 4px solid;
            transition: all 0.3s ease;
        }
        .activity-item:hover {
            background: rgba(255,255,255,0.05);
            transform: translateX(5px);
        }
        .quick-analysis {
            background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.08);
            height: fit-content;
        }
        [data-testid="stApp"] .stButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        [data-testid="stApp"] .stButton button:hover {
            transform: translateY(-1px);
        }
        .info-custom {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            color: #93c5fd;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .warning-custom {
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            color: #fcd34d;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .sections-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
            align-items: start;
        }
        .left-column {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h1 class='main-header'><i class='fas fa-chart-line'></i> {t('mode_dashboard')}</h1>", unsafe_allow_html=True)
    
    # Section 1: Métriques de Performance
    render_main_metrics(analyzer)
    
    # Sections organisées
    st.markdown("<div class='sections-grid'>", unsafe_allow_html=True)
    
    # Colonne gauche
    st.markdown("<div class='left-column'>", unsafe_allow_html=True)
    render_analysis_charts(analyzer)
    render_recent_activity()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Colonne droite
    render_quick_analysis(analyzer)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_main_metrics(analyzer):
    """Afficher les statistiques clés avec des cartes stylées."""
    st.markdown("### Métriques de Performance")
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")

    total_articles = getattr(analyzer, 'total_articles', 0)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="background: rgba(59, 130, 246, 0.2); padding: 0.5rem; border-radius: 10px; margin-right: 0.75rem;">
                    <i class='fas fa-newspaper' style='font-size: 1.3rem; color: #3b82f6;'></i>
                </div>
            </div>
            <div style="font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.25rem;">Articles analysés</div>
            <div style="font-size: 2rem; font-weight: 700; color: #3b82f6;">{total_articles}</div>
        </div>
        """, unsafe_allow_html=True)

    accuracy = f"{getattr(analyzer, 'model_accuracy', 0):.1f}%"
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="background: rgba(16, 185, 129, 0.2); padding: 0.5rem; border-radius: 10px; margin-right: 0.75rem;">
                    <i class='fas fa-bullseye' style='font-size: 1.3rem; color: #10b981;'></i>
                </div>
            </div>
            <div style="font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.25rem;">Précision modèle</div>
            <div style="font-size: 2rem; font-weight: 700; color: #10b981;">{accuracy}</div>
        </div>
        """, unsafe_allow_html=True)

    fake_count = getattr(analyzer, 'fake_count', 0)
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="background: rgba(239, 68, 68, 0.2); padding: 0.5rem; border-radius: 10px; margin-right: 0.75rem;">
                    <i class='fas fa-exclamation-triangle' style='font-size: 1.3rem; color: #ef4444;'></i>
                </div>
            </div>
            <div style="font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.25rem;">Fake News détectées</div>
            <div style="font-size: 2rem; font-weight: 700; color: #ef4444;">{fake_count}</div>
        </div>
        """, unsafe_allow_html=True)

    avg_confidence = f"{getattr(analyzer, 'avg_confidence', 0):.1f}%"
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="background: rgba(168, 85, 247, 0.2); padding: 0.5rem; border-radius: 10px; margin-right: 0.75rem;">
                    <i class='fas fa-shield-alt' style='font-size: 1.3rem; color: #a855f7;'></i>
                </div>
            </div>
            <div style="font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.25rem;">Confiance moyenne</div>
            <div style="font-size: 2rem; font-weight: 700; color: #a855f7;">{avg_confidence}</div>
        </div>
        """, unsafe_allow_html=True)

def render_analysis_charts(analyzer):
    """Graphiques d'analyse dans une boîte stylée"""
    st.markdown("### Analyse des Résultats")
    
    if not hasattr(analyzer, 'results') or len(analyzer.results) == 0:
        st.markdown("""
        <div class='info-custom'>
            <i class='fas fa-database' style='color:#3b82f6; font-size:1.2rem;'></i>
            <span>Aucune donnée à afficher pour le moment. Analysez des articles pour voir les résultats.</span>
        </div>
        """, unsafe_allow_html=True)
        return

    df = pd.DataFrame(analyzer.results)

    tab1, tab2 = st.tabs(["Distribution", "Tendance Temporelle"])
    
    with tab1:
        fig_pie = create_analysis_pie_chart(df, "Distribution des Résultats d'Analyse")
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        if 'date' in df.columns:
            trend_data = df.groupby('date').sum().reset_index()
            fig_trend = create_trend_chart(trend_data, "Évolution des Détections sur la Période")
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.markdown("""
            <div class='info-custom'>
                <i class='fas fa-calendar' style='color:#3b82f6; font-size:1.2rem;'></i>
                <span>Pas de données temporelles disponibles pour l'analyse de tendance.</span>
            </div>
            """, unsafe_allow_html=True)

def render_recent_activity():
    """Activité récente dans une boîte stylée"""
    st.markdown("### Activité Récente")
    
    activities = [
        {"time": "Il y a 2 min", "action": "Article analysé - 'Élections 2024'", "status": "REEL", "confidence": "92%", "icon": "fas fa-file-alt"},
        {"time": "Il y a 5 min", "action": "Lot de 15 articles traités", "status": "TERMINÉ", "confidence": "88%", "icon": "fas fa-layer-group"},
        {"time": "Il y a 12 min", "action": "Fake news détectée - 'Scandale politique'", "status": "FAKE", "confidence": "96%", "icon": "fas fa-ban"},
        {"time": "Il y a 1 h", "action": "Mise à jour du modèle IA", "status": "SYSTÈME", "confidence": "100%", "icon": "fas fa-robot"},
        {"time": "Il y a 2 h", "action": "Analyse de source - CNN International", "status": "FIABLE", "confidence": "94%", "icon": "fas fa-search"}
    ]

    for act in activities:
        if act['status'] == 'REEL':
            color = "#10b981"
            badge_color = "rgba(16, 185, 129, 0.2)"
        elif act['status'] == 'FAKE':
            color = "#ef4444"
            badge_color = "rgba(239, 68, 68, 0.2)"
        elif act['status'] == 'TERMINÉ':
            color = "#3b82f6"
            badge_color = "rgba(59, 130, 246, 0.2)"
        elif act['status'] == 'FIABLE':
            color = "#8b5cf6"
            badge_color = "rgba(139, 92, 246, 0.2)"
        else:
            color = "#f59e0b"
            badge_color = "rgba(245, 158, 11, 0.2)"
        
        st.markdown(f"""
        <div class='activity-item' style='border-left-color: {color};'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                <div style='display: flex; align-items: flex-start; gap: 12px;'>
                    <div style='background: {badge_color}; padding: 8px; border-radius: 8px; color: {color};'>
                        <i class='{act['icon']}' style='font-size: 1.1rem;'></i>
                    </div>
                    <div>
                        <strong style='font-size: 14px; color: white;'>{act['action']}</strong><br>
                        <span style='color: #94a3b8; font-size: 12px;'>{act['time']}</span>
                    </div>
                </div>
                <div style='text-align: right;'>
                    <div style='font-weight: bold; color: {color}; font-size: 13px; background: {badge_color}; padding: 4px 8px; border-radius: 6px;'>
                        {act['status']}
                    </div>
                    <div style='color: #cbd5e1; font-size: 12px; margin-top: 4px;'>
                        {act['confidence']} confiance
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_quick_analysis(analyzer):
    """Analyse rapide dans une boîte stylée"""
    st.markdown("### Analyse Rapide")
    
    with st.expander("🔍 Tester un Article", expanded=True):
        test_text = st.text_area(
            "Contenu à analyser",
            height=150,
            placeholder="Collez le texte d'un article ici pour une analyse rapide...",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns(2, gap="small")
        with col1:
            analyze_btn = st.button("Lancer l'analyse", use_container_width=True, type="primary")
        with col2:
            clear_btn = st.button("Effacer", use_container_width=True)
            
        if analyze_btn and test_text.strip():
            with st.spinner("Analyse en cours..."):
                test_article = {'title': 'Article Test', 'content': test_text, 'source': 'Input Utilisateur'}
                prediction, confidence = analyzer.predict_article(test_article)
                
                if prediction == "FAKE":
                    st.error(f"### Résultat: FAKE NEWS\n**Niveau de confiance:** {confidence:.1%}")
                else:
                    st.success(f"### Résultat: INFORMATION FIABLE\n**Niveau de confiance:** {confidence:.1%}")
        elif analyze_btn:
            st.warning("Veuillez entrer du texte à analyser")