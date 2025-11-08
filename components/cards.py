import streamlit as st

class MetricCard:
    """Carte de métrique moderne"""
    
    def __init__(self, title, value, trend=None, icon="📊", trend_type="positive"):
        self.title = title
        self.value = value
        self.trend = trend
        self.icon = icon
        self.trend_type = trend_type
    
    def render(self):
        """Rendre la carte de métrique"""
        trend_color = "#10b981" if self.trend_type == "positive" else "#ef4444"
        trend_icon = "↗️" if self.trend_type == "positive" else "↘️"
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-icon">{self.icon}</span>
                <span class="metric-title">{self.title}</span>
            </div>
            <div class="metric-value">{self.value}</div>
            <div class="metric-trend" style="color: {trend_color}">
                {trend_icon} {self.trend if self.trend else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

class AnalysisCard:
    """Carte d'analyse d'article"""
    
    def __init__(self, article_data):
        self.article = article_data
    
    def render(self):
        """Rendre la carte d'analyse"""
        prediction = self.article.get('prediction', 'UNKNOWN')
        confidence = self.article.get('confidence', 0)
        
        # Déterminer le style basé sur la prédiction
        if prediction == "REAL":
            border_color = "#10b981"
            status_icon = "✅"
        elif prediction == "FAKE":
            border_color = "#ef4444"
            status_icon = "❌"
        else:
            border_color = "#f59e0b"
            status_icon = "⚠️"
        
        st.markdown(f"""
        <div class="analysis-card" style="border-left: 4px solid {border_color}">
            <div class="article-header">
                <h4>{status_icon} {self.article.get('title', 'Sans titre')}</h4>
                <span class="confidence-badge">{confidence:.1%}</span>
            </div>
            <div class="article-meta">
                <span>Source: {self.article.get('source', 'Inconnue')}</span>
                <span>•</span>
                <span>{self.article.get('published_at', 'Date inconnue')}</span>
            </div>
            <p class="article-preview">{self.article.get('content', '')[:150]}...</p>
        </div>
        """, unsafe_allow_html=True)