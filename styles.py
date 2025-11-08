# styles.py - Styles CSS unifiés pour toutes les pages
UNIFIED_STYLES = """
<style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Header principal unifié */
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
    
    /* Conteneurs unifiés */
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
    
    /* Cartes de métriques */
    .metric-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(102,126,234,0.2);
        transition: transform 0.2s ease;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(102,126,234,0.4);
    }
    
    /* Badges de prédiction */
    .prediction-badge {
        padding: 1rem;
        border-radius: 12px;
        font-weight: bold;
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .fake-badge {
        background: rgba(239, 68, 68, 0.2);
        border: 2px solid rgba(239, 68, 68, 0.4);
        color: #ef4444;
    }
    .real-badge {
        background: rgba(16, 185, 129, 0.2);
        border: 2px solid rgba(16, 185, 129, 0.4);
        color: #10b981;
    }
    
    /* Boutons unifiés */
    [data-testid="stApp"] .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
    }
    [data-testid="stApp"] .stButton button:hover {
        transform: translateY(-1px);
    }
</style>
"""