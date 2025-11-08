import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_analysis_pie_chart(data, title="Distribution des Analyses"):
    """Créer un graphique circulaire d'analyse"""
    fig = px.pie(
        data, 
        values='Count', 
        names='Category',
        title=title,
        color='Category',
        color_discrete_map={
            'Réel': '#10b981',
            'Fake News': '#ef4444',
            'Incertain': '#f59e0b',
            'Satire': '#8b5cf6',
            'Biaisé': '#6366f1'
        }
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    return fig

def create_confidence_gauge(confidence_score, title="Niveau de Confiance"):
    """Créer un indicateur de confiance"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = confidence_score * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#3b82f6"},
            'steps': [
                {'range': [0, 50], 'color': "#ef4444"},
                {'range': [50, 80], 'color': "#f59e0b"},
                {'range': [80, 100], 'color': "#10b981"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    return fig

def create_trend_chart(data, title="Évolution des Analyses"):
    """Créer un graphique de tendance"""
    fig = px.line(
        data, 
        x='Date', 
        y=['Real', 'Fake', 'Uncertain'],
        title=title,
        color_discrete_map={
            'Real': '#10b981',
            'Fake': '#ef4444',
            'Uncertain': '#f59e0b'
        }
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_color='white',
        yaxis_color='white'
    )
    return fig