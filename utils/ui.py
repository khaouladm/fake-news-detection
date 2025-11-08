import streamlit as st

class MetricCard:
    """Carte de métrique moderne compatible avec les thèmes clair/sombre"""

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
        <div style="
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            backdrop-filter: blur(6px);
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="font-size: 1.2rem;">{self.icon} {self.title}</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{self.value}</div>
            </div>
            <div style="color: {trend_color}; font-size: 0.9rem; margin-top: 0.2rem;">
                {trend_icon} {self.trend if self.trend else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
