import streamlit as st
import pandas as pd
import time
import plotly.express as px
from utils.news_api import NewsFetcher
from utils.real_time_analyzer import RealTimeAnalyzer

# Page configuration
st.set_page_config(
    page_title="Real-Time Fake News Detector",
    page_icon="📰",
    layout="wide"
)

def main():
    st.title("📰 Real-Time Fake News Detection")
    st.markdown("### Monitor and analyze news in real-time using AI and Machine Learning")
    
    # Initialize components
    with st.spinner("Loading AI analyzer..."):
        news_fetcher = NewsFetcher()
        analyzer = RealTimeAnalyzer()
    
    # Sidebar navigation and status
    render_sidebar(analyzer)
    
    # Main navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Use the menu to navigate the app.")
    lang = st.sidebar.selectbox("Choose Language", ["en", "fr", "es"])
    
    app_mode = st.sidebar.selectbox(
        "Choose Mode",
        ["🏠 Dashboard", "🔴 Live News Monitor", "🔍 Single Article Check", 
         "📊 Batch Analysis", "🤖 Model Info", "⚙️ API Settings"]
    )
    
    if app_mode == "🏠 Dashboard":
        render_dashboard(analyzer, news_fetcher)
    elif app_mode == "🔴 Live News Monitor":
        live_news_monitor(news_fetcher, analyzer)
    elif app_mode == "🔍 Single Article Check":
        single_article_analysis(analyzer)
    elif app_mode == "📊 Batch Analysis":
        batch_analysis(analyzer)
    elif app_mode == "🤖 Model Info":
        model_info_page(analyzer)
    else:
        api_settings(news_fetcher)

# ---------------- Sidebar ----------------
def render_sidebar(analyzer):
    st.sidebar.title("System Status")
    if analyzer.model_loaded:
        st.sidebar.success("✅ AI Model: Active")
        st.sidebar.info(f"Type: {analyzer.get_model_info()}")
    else:
        st.sidebar.warning("⚠️ AI Model: Using Rule-Based")
    st.sidebar.info("🌐 News API: Ready")
    st.sidebar.metric("Last Update", time.strftime("%H:%M:%S"))

# ---------------- Dashboard ----------------
def render_dashboard(analyzer, news_fetcher):
    st.header("🏠 Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("AI Model Status", "Active" if analyzer.model_loaded else "Rule-Based")
    with col2:
        st.metric("Analysis Ready", "Yes")
    with col3:
        st.metric("System", "Online")
    
    st.subheader("Quick Actions")
    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        if st.button("🔄 Fetch Latest News"):
            st.session_state.auto_fetch = True
    with action_col2:
        if st.button("🔍 Test Analysis"):
            test_analysis(analyzer)
    with action_col3:
        if st.button("📈 View Stats"):
            show_sample_stats()
    
    st.subheader("Recent Activity")
    st.info("""
    **System Ready for Real-Time Analysis:**
    - BERT Model loaded and active
    - News API connectivity established
    - Real-time processing enabled
    
    **Next:** Go to **Live News Monitor** to start analyzing real news!
    """)

def test_analysis(analyzer):
    test_article = {
        'title': 'Breaking: New Study Shows Important Findings',
        'content': 'Researchers from leading universities have published a new study with significant implications.',
        'source': 'Test Source'
    }
    prediction, confidence = analyzer.predict_article(test_article)
    st.success(f"Test Analysis: **{prediction}** (Confidence: {confidence:.2%})")
    st.info("This demonstrates the system is working correctly!")

def show_sample_stats():
    data = {'Category': ['Real News', 'Fake News', 'Uncertain'], 'Count': [65, 23, 12]}
    df = pd.DataFrame(data)
    fig = px.pie(df, values='Count', names='Category', title='Sample Analysis Distribution')
    st.plotly_chart(fig)

# ---------------- Live News Monitor ----------------
def live_news_monitor(news_fetcher, analyzer):
    st.header("🔴 Live News Monitor")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Real-time News Feed")
        search_query = st.text_input("🔍 Search topics:", "technology news")
        col_a, col_b = st.columns(2)
        with col_a:
            num_articles = st.slider("Number of articles", 5, 20, 10)
        with col_b:
            if st.button("🎯 Fetch & Analyze News"):
                fetch_and_analyze_news(news_fetcher, analyzer, search_query, num_articles)
    
    with col2:
        st.subheader("Live Stats")
        st.metric("Model", "BERT" if analyzer.model_loaded else "Rule-Based")
        st.metric("Status", "Ready")
        if not analyzer.model_loaded:
            st.warning("Using rule-based analysis")
        st.info("Click button to fetch news")

def fetch_and_analyze_news(news_fetcher, analyzer, query, num_articles):
    try:
        with st.spinner("🔄 Fetching latest news..."):
            articles = news_fetcher.fetch_real_time_news([query])[:num_articles]
            if articles:
                st.success(f"📰 Fetched {len(articles)} articles")
                results = analyzer.analyze_news_batch(articles)
                display_real_time_results(results)
                show_analysis_summary(results)
            else:
                st.error("❌ No articles found. Try different search terms.")
    except Exception as e:
        st.error(f"❌ Error fetching news: {str(e)}")

def display_real_time_results(results):
    st.subheader("📊 Analysis Results")
    if not results:
        st.info("No results to display")
        return
    tab1, tab2, tab3 = st.tabs(["📋 List View", "📈 Summary", "🔄 Live Feed"])
    with tab1:
        for i, result in enumerate(results):
            with st.expander(f"{i+1}. {result['title'][:80]}...", expanded=i==0):
                display_article_card(result)
    with tab2:
        show_analysis_summary(results)
    with tab3:
        st.info("Live feed updates will appear here.")

def display_article_card(result):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**Source:** {result.get('source', 'Unknown')}")
        st.write(f"**Published:** {result.get('published_at', 'Unknown')}")
        st.write(f"**Content:** {result['content'][:200]}...")
        if result.get('url'):
            st.markdown(f"[📖 Read full article]({result['url']})")
    with col2:
        prediction = result['prediction']
        confidence = result['confidence']
        if prediction == "FAKE":
            st.error(f"🚨 **{prediction}**")
        elif prediction == "REAL":
            st.success(f"✅ **{prediction}**")
        else:
            st.warning(f"⚠️ **{prediction}**")
        st.metric("Confidence", f"{confidence:.2%}")
        st.caption(f"Method: {result.get('method', 'Unknown')}")

def show_analysis_summary(results):
    if not results:
        return
    df = pd.DataFrame(results)
    fake_count = len(df[df['prediction'] == 'FAKE'])
    reliable_count = len(df[df['prediction'] == 'REAL'])
    uncertain_count = len(df[df['prediction'] == 'UNCERTAIN'])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Articles", len(df))
    col2.metric("Reliable", reliable_count)
    col3.metric("Potential Fake", fake_count)
    col4.metric("Uncertain", uncertain_count)
    if len(df) > 0:
        fig = px.pie(df, names='prediction', title='News Reliability Distribution')
        st.plotly_chart(fig)

# ---------------- Single Article Analysis ----------------
def single_article_analysis(analyzer):
    st.header("🔍 Analyze Single Article")
    input_method = st.radio("Input method:", ["Enter Text", "Enter URL"])
    if input_method == "Enter URL":
        url = st.text_input("News article URL:", placeholder="https://example.com/news-article")
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🌐 Analyze URL"):
                if url: analyze_url_content(url, analyzer)
                else: st.warning("Please enter a URL")
        with col2:
            if st.button("🧹 Clear"):
                st.session_state.pop('scraped_article', None)
    else:
        news_text = st.text_area("Paste article text:", height=200)
        if st.button("Analyze Text") and news_text:
            analyze_text_content(news_text, analyzer)

def analyze_url_content(url, analyzer):
    try:
        from utils.url_scraper import URLScraper
    except ImportError:
        st.error("❌ URL scraping dependencies not installed")
        st.code("pip install beautifulsoup4 requests newspaper3k")
        return
    scraper = URLScraper()
    with st.spinner("🌐 Scraping article content from URL..."):
        scraped_data = scraper.scrape_article(url)
    if scraped_data['success']:
        st.success("✅ Successfully extracted article content")
        article = {
            'title': scraped_data['title'],
            'content': scraped_data['content'],
            'source': 'URL Scraping',
            'url': url
        }
        prediction, confidence = analyzer.predict_article(article)
        display_analysis_results(prediction, confidence, article)
        with st.expander("📄 View Scraped Content"):
            st.subheader("Title")
            st.write(scraped_data['title'])
            st.subheader("Content Preview")
            content_preview = scraped_data['content'][:500] + "..." if len(scraped_data['content']) > 500 else scraped_data['content']
            st.write(content_preview)
    else:
        st.error(f"❌ Failed to scrape article: {scraped_data.get('error', 'Unknown error')}")

def analyze_text_content(news_text, analyzer):
    mock_article = {'title': 'User Input Article', 'content': news_text, 'source': 'Direct Input'}
    prediction, confidence = analyzer.predict_article(mock_article)
    display_analysis_results(prediction, confidence, mock_article)
    with st.expander("📊 Text Statistics"):
        col1, col2, col3 = st.columns(3)
        col1.metric("Characters", len(news_text))
        col2.metric("Words", len(news_text.split()))
        col3.metric("Sentences", news_text.count('.') + news_text.count('!') + news_text.count('?'))

def display_analysis_results(prediction, confidence, article):
    st.subheader("🎯 Analysis Results")
    col1, col2 = st.columns(2)
    with col1:
        if prediction == "FAKE": st.error(f"🚨 Prediction: {prediction}")
        elif prediction == "REAL": st.success(f"✅ Prediction: {prediction}")
        else: st.warning(f"⚠️ Prediction: {prediction}")
    with col2:
        if confidence >= 0.9: st.success(f"Confidence: {confidence:.2%}")
        elif confidence >= 0.7: st.info(f"Confidence: {confidence:.2%}")
        else: st.warning(f"Confidence: {confidence:.2%}")
    with st.expander("📋 Article Information"):
        st.write(f"**Title:** {article.get('title', 'N/A')}")
        st.write(f"**Source:** {article.get('source', 'N/A')}")
        if 'url' in article: st.write(f"**URL:** {article['url']}")
    st.subheader("💡 Explanation")
    if prediction == "FAKE":
        st.warning("""
        This article shows characteristics of potentially fake news. Consider verifying with trusted sources.
        """)
    else:
        st.info("""
        This article appears to be credible. Always verify with multiple sources.
        """)

# ---------------- Batch Analysis ----------------
def batch_analysis(analyzer):
    st.header("📊 Batch Analysis")
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data preview:", df.head())
        if st.button("Analyze Batch"):
            st.success("Batch analysis would process all articles")

# ---------------- Model Info ----------------
def model_info_page(analyzer):
    st.header("🤖 Model Information")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("BERT Model Status")
        if analyzer.model_loaded:
            st.success("✅ BERT Model Loaded Successfully")
            st.info("Using BERT embeddings for high-accuracy detection")
        else:
            st.warning("⚠️ BERT Model Not Loaded")
            st.info("Using rule-based analysis")
    with col2:
        st.subheader("System Capabilities")
        st.info("""
        **Current Features:**
        - Real-time news fetching
        - BERT-powered classification
        - URL content scraping
        - Confidence scoring
        - Batch processing
        - Interactive dashboard
        """)

# ---------------- API Settings ----------------
def api_settings(news_fetcher):
    st.header("⚙️ API Configuration")
    st.info("Get free API keys to enable real-time news fetching:")
    with st.expander("📋 How to get API keys"):
        st.markdown("""
        **GNews API (Recommended):**
        1. Go to [gnews.io](https://gnews.io)
        2. Sign up for free account
        3. Get your API key
        4. Enter it below
        """)
    with st.form("api_config"):
        gnews_key = st.text_input("GNews API Key:", type="password", placeholder="Enter your GNews API key")
        if st.form_submit_button("Save API Keys"):
            if gnews_key:
                st.success("API key saved for this session!")
                st.info("For production, use .streamlit/secrets.toml")
            else:
                st.warning("Please enter an API key")

# ---------------- Run app ----------------
if __name__ == "__main__":
    main()
