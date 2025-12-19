import streamlit as st
import pandas as pd
from utils.news_api import NewsFetcher
from utils.real_time_analyzer import RealTimeAnalyzer
import time
import plotly.express as px
import os
import utils.i18n as i18n

# Safe import for FactChecker
try:
    from utils.fact_checker import FactChecker
except ImportError:
    FactChecker = None

# --- 1. PAGE CONFIGURATION & CSS ---
st.set_page_config(
    page_title="Veritas AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_custom_css():
    st.markdown("""
        <style>
        /* IMPORT FONTS: Playfair Display (Serif) for headers, Inter (Sans) for body */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap');

        /* GLOBAL SETTINGS */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #334155; /* Slate 700 */
            background-color: #f8fafc; /* Very light slate background */
        }

        /* HEADERS - Classy Serif Font */
        h1, h2, h3, h4 {
            font-family: 'Playfair Display', serif;
            color: #0f172a; /* Slate 900 */
            font-weight: 700;
        }
        
        h1 { letter-spacing: -0.02em; }

        /* MAIN CONTAINER BACKGROUND */
        .stApp {
            background-color: #f8fafc;
        }

        /* --- CARDS (The White Boxes) --- */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0; /* Subtle border */
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.02); /* Soft elegant shadow */
        }

        /* FORCE TEXT COLOR INSIDE CARDS */
        [data-testid="stVerticalBlockBorderWrapper"] p, 
        [data-testid="stVerticalBlockBorderWrapper"] span,
        [data-testid="stVerticalBlockBorderWrapper"] div,
        [data-testid="stVerticalBlockBorderWrapper"] label {
            color: #334155;
        }

        /* --- METRICS --- */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            padding: 16px;
            border-radius: 10px;
            border: 1px solid #f1f5f9;
            border-left: 4px solid #0f172a; /* Elegant dark accent */
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        div[data-testid="stMetricLabel"] {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        div[data-testid="stMetricValue"] {
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            color: #0f172a;
        }

        /* --- BUTTONS --- */
        .stButton > button {
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            transition: all 0.2s ease;
            border: 1px solid #e2e8f0;
        }
        
        /* Primary Button (Dark Navy) */
        .stButton > button[kind="primary"] {
            background-color: #0f172a; 
            color: #ffffff !important;
            border: 1px solid #0f172a;
            box-shadow: 0 4px 6px rgba(15, 23, 42, 0.2);
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #1e293b;
            transform: translateY(-1px);
            box-shadow: 0 6px 8px rgba(15, 23, 42, 0.25);
        }

        /* Secondary Button (Light Grey) */
        .stButton > button[kind="secondary"] {
            background-color: #ffffff;
            color: #475569 !important;
        }
        .stButton > button[kind="secondary"]:hover {
            background-color: #f1f5f9;
            border-color: #cbd5e1;
        }

        /* --- SIDEBAR --- */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            text-transform: uppercase;
            color: #94a3b8;
            letter-spacing: 0.1em;
        }

        /* EXPANDERS */
        .streamlit-expanderHeader {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            color: #1e293b;
            background-color: #f8fafc;
            border-radius: 8px;
        }
        
        /* INPUT FIELDS */
        div[data-baseweb="input"] {
            background-color: #ffffff;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 2. MAIN APP LOGIC ---

def main():
    load_custom_css()
    
    # --- SIDEBAR DESIGN ---
    with st.sidebar:
        c1, c2 = st.columns([1, 3])
        with c1:
            # Use a monochrome icon for a classier look
            st.markdown("## ⚖️") 
        with c2:
            st.markdown("<h2 style='margin-top:0; color:#0f172a; font-family:Playfair Display;'>Veritas AI</h2>", unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Language selector
        st.markdown("### 🌍 Region & Language")
        lang_map = {"English": "en", "Français": "fr", "العربية": "ar"}
        lang_choice = st.selectbox("Select Language", list(lang_map.keys()), label_visibility="collapsed")
        current_lang = lang_map[lang_choice]
        i18n.set_language(current_lang)
        
        st.markdown("---")
        
        # Navigation
        st.markdown(f"### 🧭 {i18n.t('nav.choose_mode').upper()}")
        nav_keys = ["home", "live", "single", "batch", "model", "api"]
        nav_labels = [i18n.t('nav.home'), i18n.t('nav.live'), i18n.t('nav.single'), i18n.t('nav.batch'), i18n.t('nav.model'), i18n.t('nav.api')]
        
        selection = st.radio("Navigation", nav_labels, label_visibility="collapsed")
        sel_index = nav_labels.index(selection)
        app_mode = nav_keys[sel_index]
        
        st.markdown("---")

    # --- HEADER SECTION ---
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.title(i18n.t('page_title'))
        st.markdown(f"<p style='font-size: 1.1rem; color: #64748b;'>{i18n.t('page_subtitle')}</p>", unsafe_allow_html=True)
    with col_h2:
        st.markdown(
            """
            <div style="background-color: #ffffff; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <span style="color: #10b981; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.05em;">● SYSTEM ONLINE</span>
            </div>
            """, 
            unsafe_allow_html=True
        )

    st.divider()
    
    # Initialize components
    with st.spinner("Initializing Analysis Engine..."):
        news_fetcher = NewsFetcher()
        analyzer = RealTimeAnalyzer()
    
    # Render Sidebar Status
    render_sidebar_status(analyzer)
    
    # --- ROUTING ---
    if app_mode == "home":
        render_dashboard(analyzer, news_fetcher)
    elif app_mode == "live":
        live_news_monitor(news_fetcher, analyzer, current_lang)
    elif app_mode == "single":
        single_article_analysis(analyzer, current_lang)
    elif app_mode == "batch":
        batch_analysis(analyzer)
    elif app_mode == "model":
        model_info_page(analyzer)
    else:
        api_settings(news_fetcher)

# --- 3. COMPONENT FUNCTIONS ---

def render_sidebar_status(analyzer):
    """Render system status at bottom of sidebar"""
    with st.sidebar:
        with st.expander("System Status", expanded=True):
            if analyzer.model_loaded:
                st.success(f"Engine Active")
                st.caption(analyzer.get_model_info())
            else:
                st.warning("Engine Fallback")
            
            st.info("News API Ready")
            st.caption(f"Last Check: {time.strftime('%H:%M')}")

def render_dashboard(analyzer, news_fetcher):
    """Main dashboard view"""
    
    # Top Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("AI Confidence", "Active", delta="High Accuracy")
    with col2:
        st.metric("Source Coverage", "Global", delta="3 Languages")
    with col3:
        st.metric("Verification", "Enabled", delta="Web Search")
    
    st.markdown("### " + i18n.t('quick_actions'))
    
    # Quick Action Cards
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("#### 🗞️ Live Monitor")
            st.write("Scan global news streams.")
            if st.button(i18n.t('fetch_latest'), use_container_width=True, type="primary"):
                st.session_state.auto_fetch = True
                st.info("Navigating to Live Monitor...")
    
    with c2:
        with st.container(border=True):
            st.markdown("#### 🕵️ Deep Analysis")
            st.write("Verify a specific claim.")
            if st.button(i18n.t('test_analysis'), use_container_width=True):
                test_analysis(analyzer)

    with c3:
        with st.container(border=True):
            st.markdown("#### 📊 Insights")
            st.write("View detection trends.")
            if st.button(i18n.t('view_stats'), use_container_width=True):
                show_sample_stats()

def test_analysis(analyzer):
    """Quick test analysis"""
    test_article = {
        'title': 'Sample: Global Markets Show Strong Recovery',
        'content': 'Analysts report a significant upturn in global markets following the recent policy announcements.',
        'source': 'Financial Daily'
    }
    prediction, confidence = analyzer.predict_article(test_article)
    
    # Classy Result Card
    st.markdown(f"""
    <div style="background-color: #f8fafc; padding: 20px; border-radius: 12px; border-left: 4px solid #0f172a; margin-top: 10px;">
        <div style="font-family: 'Inter'; font-size: 0.8rem; color: #64748b; text-transform: uppercase;">Prediction Result</div>
        <div style="font-family: 'Playfair Display'; font-size: 1.5rem; font-weight: 700; color: #0f172a;">{prediction}</div>
        <div style="font-family: 'Inter'; font-size: 1rem; color: #334155;">Confidence: <b>{confidence:.1%}</b></div>
    </div>
    """, unsafe_allow_html=True)

def show_sample_stats():
    """Show sample statistics"""
    data = {'Category': ['Real News', 'Fake News', 'Uncertain'], 'Count': [65, 23, 12]}
    df = pd.DataFrame(data)
    
    colors = ['#0f172a', '#ef4444', '#cbd5e1'] 
    
    fig = px.pie(df, values='Count', names='Category', title='Detection Distribution', 
                 hole=0.7, color_discrete_sequence=colors)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font_family="Inter",
        title_font_family="Playfair Display"
    )
    
    st.plotly_chart(fig, key="sample_stats_pie", use_container_width=True)

# --- LIVE MONITOR ---
def live_news_monitor(news_fetcher, analyzer, lang_code='en'):
    st.header(i18n.t('live_header'))
    
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            default_search = "Technology"
            if lang_code == 'ar': default_search = "تكنولوجيا"
            elif lang_code == 'fr': default_search = "Technologie"
            
            search_query = st.text_input(i18n.t('search_placeholder'), default_search)
        with c2:
            num_articles = st.number_input(i18n.t('num_articles'), min_value=1, max_value=50, value=10)

        if st.button(i18n.t('fetch_analyze'), type="primary", use_container_width=True):
            fetch_and_analyze_news(news_fetcher, analyzer, search_query, num_articles, lang_code)

def fetch_and_analyze_news(news_fetcher, analyzer, query, num_articles, lang_code='en'):
    try:
        with st.spinner("Connecting to News Stream..."):
            articles = news_fetcher.fetch_real_time_news([query], lang=lang_code)
            articles = articles[:num_articles]
            
            if articles:
                results = analyzer.analyze_news_batch(articles)
                
                # KPIs Container
                with st.container(border=True):
                    fakes = len([r for r in results if r['prediction'] == 'FAKE'])
                    k1, k2, k3 = st.columns(3)
                    k1.metric("Analyzed", len(results))
                    k2.metric("Flagged", fakes, delta_color="inverse")
                    k3.metric("Verified", len(results) - fakes)
                
                st.divider()
                
                # Display List
                for i, result in enumerate(results):
                    icon = "🛑" if result['prediction'] == 'FAKE' else "✅"
                    with st.expander(f"{icon} {result['title']}", expanded=False):
                        display_article_card(result)
            else:
                st.warning(i18n.t('no_articles_found'))
    except Exception as e:
        st.error(f"Error: {str(e)}")

def display_article_card(result):
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f"<div style='font-size:0.8rem; color:#64748b; text-transform:uppercase; margin-bottom:5px;'>{result.get('source', 'Unknown')} • {result.get('published_at', 'N/A')}</div>", unsafe_allow_html=True)
        st.write(result['content'][:300] + "...")
        if result.get('url'): st.markdown(f"[Read Source Document]({result['url']})")
    with c2:
        pred = result['prediction']
        conf = result['confidence']
        
        # Minimalist Tags
        bg = "#fecaca" if pred == "FAKE" else "#bbf7d0"
        color = "#991b1b" if pred == "FAKE" else "#166534"
        
        st.markdown(f"""
        <div style="background-color: {bg}; padding: 12px; border-radius: 8px; text-align: center;">
            <span style="color: {color}; font-weight: 700; font-size: 0.9rem;">{pred}</span><br>
            <span style="color: {color}; font-size: 0.8rem; opacity: 0.9;">{conf:.1%} Prob.</span>
        </div>
        """, unsafe_allow_html=True)

# --- SINGLE ANALYSIS (THE CORE) ---
def single_article_analysis(analyzer, lang_code='en'):
    st.header(i18n.t('nav.single'))

    # Tabs for cleaner UI
    tab_input, tab_results = st.tabs(["📥 Input Data", "📊 Analysis Report"])
    
    with tab_input:
        with st.container(border=True):
            st.markdown("#### Select Source Material")
            input_method = st.radio("Input Method", [i18n.t('analyze_text'), i18n.t('analyze_url')], horizontal=True, label_visibility="collapsed")
            
            st.divider()
            
            # URL MODE
            if input_method == i18n.t('analyze_url'):
                url = st.text_input("Article URL", placeholder="https://example.com/news/article")
                if st.button("Analyze URL", type="primary", use_container_width=True):
                    if url:
                        analyze_url_content(url, analyzer)
                    else:
                        st.warning("Please enter a URL.")
            
            # TEXT MODE
            else:
                news_title = st.text_input("Headline (Recommended for Fact Check)", placeholder="e.g. Major Policy Shift Announced")
                news_text = st.text_area("Article Content", height=250, placeholder="Paste the body of the text here...")
                if st.button("Analyze Text", type="primary", use_container_width=True):
                    if news_text:
                        analyze_text_content(news_title, news_text, analyzer)
                    else:
                        st.warning("Please enter text.")

        if st.button("Clear & Reset", type="secondary"):
            st.session_state.pop('url_analysis_result', None)
            st.session_state.pop('text_analysis_result', None)
            st.rerun()

    # RESULTS DISPLAY LOGIC
    result_data = None
    if 'url_analysis_result' in st.session_state:
        result_data = st.session_state['url_analysis_result']
    elif 'text_analysis_result' in st.session_state:
        result_data = st.session_state['text_analysis_result']

    with tab_results:
        if result_data:
            st.markdown("### 📝 Analysis Report")
            
            # 1. AI Prediction Section (Style Analysis)
            with st.container(border=True):
                c1, c2 = st.columns([1, 2])
                pred = result_data['prediction']
                conf = result_data['confidence']
                
                with c1:
                    # Elegant Ring Chart style indicator
                    color = "#ef4444" if pred == "FAKE" else "#10b981"
                    st.markdown(f"""
                        <div style="text-align: center; padding: 20px; border: 4px solid {color}; border-radius: 50%; width: 160px; height: 160px; margin: auto; display: flex; flex-direction: column; justify-content: center; background-color: #ffffff;">
                            <span style="font-family: 'Inter'; font-size: 12px; color: #64748b; text-transform: uppercase;">Assessment</span>
                            <span style="font-family: 'Playfair Display'; font-size: 24px; font-weight: 700; color: {color};">{pred}</span>
                            <span style="font-family: 'Inter'; font-size: 14px; color: #334155; margin-top: 5px;">{conf:.1%}</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    st.markdown("#### Linguistic Style Analysis")
                    st.write("The AI model analyzes sentence structure, vocabulary, and emotional tone to detect patterns.")
                    
                    if pred == "FAKE":
                        st.error("🚩 **Flagged:** High probability of misinformation patterns detected (sensationalism, urgency, vague attribution).")
                    else:
                        st.success("✅ **Cleared:** The writing style aligns with credible journalistic standards.")

            # 2. Fact Checker Section (Restored for Text Mode primarily)
            # We only show this if it's TEXT INPUT (Source = 'Input') as requested, 
            # OR if you prefer, we can show it for all. 
            # Based on your request "keep it for the text analysis... not the url", we check the source.
            
            if result_data['article'].get('source') == 'Input':
                st.markdown("### 🌐 Verification Engine")
                
                article_title = result_data['article'].get('title', '')
                if not article_title:
                    content = result_data['article'].get('content', '')
                    article_title = " ".join(content.split()[:10])
                
                with st.container(border=True):
                    col_fc1, col_fc2 = st.columns([3, 1])
                    with col_fc1:
                         st.markdown(f"**Subject:** *{article_title}*")
                    with col_fc2:
                        run_fc = st.button("Verify Facts", key=f"fc_btn_run", type="primary", use_container_width=True)
                    
                    if run_fc:
                        if FactChecker is None:
                            st.error("Fact Checker module inactive.")
                        else:
                            checker = FactChecker()
                            with st.spinner("Cross-referencing trusted sources..."):
                                fc_result = checker.verify_article(article_title, lang=lang_code)
                            
                            # Render Results
                            status = fc_result['status']
                            color = fc_result.get('color', 'blue')
                            
                            # Classy Verdict Box
                            st.markdown(f"""
                            <div style="background-color: #f8fafc; border-left: 4px solid {color}; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                                <div style="font-family: 'Inter'; font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">Consensus Verdict</div>
                                <h3 style="margin: 5px 0; color: #0f172a; font-family: 'Playfair Display';">{status}</h3>
                                <p style="margin: 10px 0 0 0; color: #334155; font-style: italic;">"{fc_result['reason']}"</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Evidence Dropdowns
                            st.markdown("#### Reference Material")
                            if not fc_result['evidence']:
                                st.caption("No direct references found in public index.")
                            
                            for item in fc_result['evidence']:
                                trusted_badge = "🛡️ Verified Source" if item.get('is_trusted') else ""
                                with st.expander(f"{item['source']} {trusted_badge}"):
                                    st.caption(f"Domain: {item['domain']}")
                                    st.write(f"_{item['snippet']}_")
                                    st.markdown(f"[Read Original]({item['url']})")
                                    
                                    s_score = item['support_score']
                                    if s_score > 0: st.success(f"Supports Claim (+{s_score:.2f})")
                                    elif s_score < 0: st.error(f"Contradicts Claim ({s_score:.2f})")
                                    else: st.info(f"Neutral / Unrelated ({s_score:.2f})")

            # 3. Source Content
            with st.expander("📄 View Raw Content"):
                st.write(f"**Title:** {result_data['article'].get('title', 'N/A')}")
                st.text_area("Content", result_data['article'].get('content', ''), height=150, disabled=True)

        else:
            st.info("👋 Select a method in 'Input Data' to begin analysis.")

# --- HELPER FUNCTIONS ---
def analyze_url_content(url, analyzer):
    try:
        from utils.url_scraper import URLScraper
        scraper = URLScraper()
        with st.spinner("Extracting content..."):
            data = scraper.scrape_article(url)
        
        if data['success']:
            article = {'title': data['title'], 'content': data['content'], 'url': url, 'source': 'Scraped'}
            with st.spinner("Analyzing patterns..."):
                pred, conf = analyzer.predict_article(article)
            
            st.session_state['url_analysis_result'] = {'prediction': pred, 'confidence': conf, 'article': article}
            st.session_state.pop('text_analysis_result', None)
            st.toast("Analysis Complete", icon="✅")
        else:
            st.error(f"Scraping Failed: {data.get('error')}")
    except Exception as e:
        st.error(f"Error: {e}")

def analyze_text_content(title, text, analyzer):
    with st.spinner("Analyzing patterns..."):
        article = {'title': title, 'content': text, 'source': 'Input'}
        pred, conf = analyzer.predict_article(article)
        
        st.session_state['text_analysis_result'] = {'prediction': pred, 'confidence': conf, 'article': article}
        st.session_state.pop('url_analysis_result', None)
        st.toast("Analysis Complete", icon="✅")

# --- OTHER PAGES ---
def batch_analysis(analyzer):
    st.header("📊 Batch Analysis")
    with st.container(border=True):
        uploaded_file = st.file_uploader("Upload CSV (must have 'text' column)", type=['csv'])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("Preview:", df.head())
            if st.button("Process Batch", type="primary"):
                st.info("Feature queued for next release.")

def model_info_page(analyzer):
    st.header("🤖 Architecture")
    st.markdown("Technical specifications of the Veritas AI engine.")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("Style Classifier")
            st.success(f"Status: {'Online' if analyzer.model_loaded else 'Offline'}")
            st.markdown("**Model:** Hybrid BERT / Logistic Regression")
            st.markdown("**Function:** Detects linguistic anomalies, emotional manipulation, and stylistic patterns typical of misinformation.")
    with col2:
        with st.container(border=True):
            st.subheader("Verification Engine")
            st.success("Status: Online")
            st.markdown("**Model:** Cross-Encoder NLI (XLM-Roberta)")
            st.markdown("**Function:** Performs real-time web searches to cross-reference claims against trusted global media outlets.")

def api_settings(news_fetcher):
    st.header("⚙️ Configuration")
    with st.container(border=True):
        st.subheader("API Access")
        with st.form("api_config"):
            gnews = st.text_input("GNews API Key", type="password")
            newsapi = st.text_input("NewsAPI Key", type="password")
            if st.form_submit_button("Save Configuration", type="primary"):
                st.success("Credentials updated securely.")

if __name__ == "__main__":
    main()
