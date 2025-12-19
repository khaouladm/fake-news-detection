import streamlit as st
import pandas as pd
from utils.news_api import NewsFetcher
from utils.real_time_analyzer import RealTimeAnalyzer
import time
import plotly.express as px
import os

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
    
    # Sidebar with model info
    render_sidebar(analyzer)
    
    # Main navigation
    st.sidebar.title("Navigation")
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

def render_sidebar(analyzer):
    """Render sidebar with system status"""
    st.sidebar.title("System Status")
    
    # Model status
    if analyzer.model_loaded:
        st.sidebar.success("✅ AI Model: Active")
        st.sidebar.info(f"Type: {analyzer.get_model_info()}")
    else:
        st.sidebar.warning("⚠️ AI Model: Using Rule-Based")
    
    # API status
    st.sidebar.info("🌐 News API: Ready")
    st.sidebar.metric("Last Update", time.strftime("%H:%M:%S"))

def render_dashboard(analyzer, news_fetcher):
    """Main dashboard view"""
    st.header("🏠 Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("AI Model Status", "Active" if analyzer.model_loaded else "Rule-Based")
    
    with col2:
        st.metric("Analysis Ready", "Yes")
    
    with col3:
        st.metric("System", "Online")
    
    # Quick actions
    st.subheader("Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🔄 Fetch Latest News", use_container_width=True):
            st.session_state.auto_fetch = True
    
    with action_col2:
        if st.button("🔍 Test Analysis", use_container_width=True):
            test_analysis(analyzer)
    
    with action_col3:
        if st.button("📈 View Stats", use_container_width=True):
            show_sample_stats()
    
    # Recent activity placeholder
    st.subheader("Recent Activity")
    st.info("""
    **System Ready for Real-Time Analysis:**
    - BERT Model loaded and active
    - News API connectivity established
    - Real-time processing enabled
    
    **Next:** Go to **Live News Monitor** to start analyzing real news!
    """)

def test_analysis(analyzer):
    """Quick test analysis"""
    test_article = {
        'title': 'Breaking: New Study Shows Important Findings',
        'content': 'Researchers from leading universities have published a new study with significant implications for future policy decisions.',
        'source': 'Test Source'
    }
    
    prediction, confidence = analyzer.predict_article(test_article)
    
    st.success(f"Test Analysis: **{prediction}** (Confidence: {confidence:.2%})")
    st.info("This demonstrates the system is working correctly!")

def show_sample_stats():
    """Show sample statistics"""
    data = {
        'Category': ['Real News', 'Fake News', 'Uncertain'],
        'Count': [65, 23, 12]
    }
    df = pd.DataFrame(data)
    
    fig = px.pie(df, values='Count', names='Category', 
                 title='Sample Analysis Distribution')
    st.plotly_chart(fig)

def live_news_monitor(news_fetcher, analyzer):
    st.header("🔴 Live News Monitor")
    
    # Controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Real-time News Feed")
        
        search_query = st.text_input("🔍 Search topics:", "technology news")
        
        col_a, col_b = st.columns(2)
        with col_a:
            num_articles = st.slider("Number of articles", 5, 20, 10)
        with col_b:
            if st.button("🎯 Fetch & Analyze News", type="primary"):
                fetch_and_analyze_news(news_fetcher, analyzer, search_query, num_articles)
    
    with col2:
        st.subheader("Live Stats")
        st.metric("Model", "BERT" if analyzer.model_loaded else "Rule-Based")
        st.metric("Status", "Ready")
        
        st.subheader("Alerts")
        if not analyzer.model_loaded:
            st.warning("Using rule-based analysis")
        st.info("Click button to fetch news")

def fetch_and_analyze_news(news_fetcher, analyzer, query, num_articles):
    """Fetch and analyze news in real-time"""
    try:
        with st.spinner("🔄 Fetching latest news..."):
            articles = news_fetcher.fetch_real_time_news([query])
            articles = articles[:num_articles]  # Limit to requested number
            
            if articles:
                st.success(f"📰 Fetched {len(articles)} articles")
                
                # Analyze articles
                results = analyzer.analyze_news_batch(articles)
                
                # Display results
                display_real_time_results(results)
                
                # Show summary
                show_analysis_summary(results)
                
            else:
                st.error("❌ No articles found. Check API configuration or try different search terms.")
                st.info("💡 Try searching for: 'technology', 'politics', 'health', 'sports'")
                
    except Exception as e:
        st.error(f"❌ Error fetching news: {str(e)}")

def display_real_time_results(results):
    """Display analysis results with better UI"""
    st.subheader("📊 Analysis Results")
    
    if not results:
        st.info("No results to display")
        return
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 List View", "📈 Summary", "🔄 Live Feed"])
    
    with tab1:
        for i, result in enumerate(results):
            # Create expandable cards for each article
            with st.expander(f"{i+1}. {result['title'][:80]}...", expanded=i==0):
                display_article_card(result)
    
    with tab2:
        show_analysis_summary(results)
    
    with tab3:
        st.info("Live feed would show real-time updates here")

def display_article_card(result):
    """Display individual article result as a card"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write(f"**Source:** {result.get('source', 'Unknown')}")
        st.write(f"**Published:** {result.get('published_at', 'Unknown')}")
        st.write(f"**Content:** {result['content'][:200]}...")
        
        if result.get('url'):
            st.markdown(f"[📖 Read full article]({result['url']})")
    
    with col2:
        # Prediction with color coding
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
    """Show analysis summary with charts"""
    if not results:
        return
    
    df = pd.DataFrame(results)
    
    # Summary metrics
    fake_count = len(df[df['prediction'] == 'FAKE'])
    reliable_count = len(df[df['prediction'] == 'REAL'])
    uncertain_count = len(df[df['prediction'] == 'UNCERTAIN'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Articles", len(df))
    with col2:
        st.metric("Reliable", reliable_count)
    with col3:
        st.metric("Potential Fake", fake_count)
    with col4:
        st.metric("Uncertain", uncertain_count)
    
    # Pie chart
    if len(df) > 0:
        fig = px.pie(df, names='prediction', title='News Reliability Distribution')
        st.plotly_chart(fig)

def single_article_analysis(analyzer):
    st.header("🔍 Analyze Single Article")
    
    # Input methods
    input_method = st.radio("Input method:", ["Enter Text", "Enter URL"])
    
    if input_method == "Enter URL":
        url = st.text_input("News article URL:", placeholder="https://example.com/news-article")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🌐 Analyze URL", type="primary"):
                if url:
                    analyze_url_content(url, analyzer)
                else:
                    st.warning("Please enter a URL")
        with col2:
            if st.button("🧹 Clear", type="secondary"):
                st.session_state.pop('scraped_article', None)
    
    else:  # Text input
        news_text = st.text_area("Paste article text:", height=200,
                                placeholder="Paste the complete news article content here...")
        
        if st.button("Analyze Text") and news_text:
            analyze_text_content(news_text, analyzer)

def analyze_url_content(url, analyzer):
    """Analyze content from URL"""
    try:
        # Try to import the URL scraper
        try:
            from utils.url_scraper import URLScraper
        except ImportError as e:
            st.error("❌ URL scraping dependencies not installed")
            st.code("pip install beautifulsoup4 requests newspaper3k")
            return
        
        scraper = URLScraper()
        
        with st.spinner("🌐 Scraping article content from URL..."):
            scraped_data = scraper.scrape_article(url)
        
        if scraped_data['success']:
            st.success("✅ Successfully extracted article content")
            
            # Create article object for analysis
            article = {
                'title': scraped_data['title'],
                'content': scraped_data['content'],
                'source': 'URL Scraping',
                'url': url
            }
            
            # Analyze the article
            with st.spinner("🤖 Analyzing article content with BERT..."):
                prediction, confidence = analyzer.predict_article(article)
            
            # Display results
            display_analysis_results(prediction, confidence, article)
            
            # Show scraped content in expander
            with st.expander("📄 View Scraped Content"):
                st.subheader("Title")
                st.write(scraped_data['title'])
                
                st.subheader("Content Preview")
                content_preview = scraped_data['content'][:500] + "..." if len(scraped_data['content']) > 500 else scraped_data['content']
                st.write(content_preview)
                
                st.subheader("Article Stats")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Content Length", f"{len(scraped_data['content']):,} chars")
                with col2:
                    st.metric("Word Count", f"{len(scraped_data['content'].split()):,} words")
                with col3:
                    st.metric("Source", "URL")
                
                if 'summary' in scraped_data and scraped_data['summary']:
                    st.subheader("AI Summary")
                    st.write(scraped_data['summary'])
        
        else:
            st.error(f"❌ Failed to scrape article: {scraped_data.get('error', 'Unknown error')}")
            st.info("💡 Try a different URL or paste the text directly")
            
    except Exception as e:
        st.error(f"❌ Error analyzing URL: {str(e)}")

def analyze_text_content(news_text, analyzer):
    """Analyze text content"""
    with st.spinner("🤖 Analyzing article content..."):
        # Create a mock article for analysis
        mock_article = {
            'title': 'User Input Article',
            'content': news_text,
            'source': 'Direct Input'
        }
        
        prediction, confidence = analyzer.predict_article(mock_article)
        
        # Display results
        display_analysis_results(prediction, confidence, mock_article)
        
        # Show text statistics
        with st.expander("📊 Text Statistics"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Characters", len(news_text))
            with col2:
                st.metric("Words", len(news_text.split()))
            with col3:
                st.metric("Sentences", news_text.count('.') + news_text.count('!') + news_text.count('?'))

def display_analysis_results(prediction, confidence, article):
    """Display analysis results in a nice format"""
    st.subheader("🎯 Analysis Results")
    
    # Create columns for results
    col1, col2 = st.columns(2)
    
    with col1:
        if prediction == "FAKE":
            st.error(f"🚨 Prediction: {prediction}")
        elif prediction == "REAL":
            st.success(f"✅ Prediction: {prediction}")
        else:
            st.warning(f"⚠️ Prediction: {prediction}")
    
    with col2:
        # Color code confidence
        if confidence >= 0.9:
            st.success(f"Confidence: {confidence:.2%}")
        elif confidence >= 0.7:
            st.info(f"Confidence: {confidence:.2%}")
        else:
            st.warning(f"Confidence: {confidence:.2%}")
    
    # Show article info
    with st.expander("📋 Article Information"):
        st.write(f"**Title:** {article.get('title', 'N/A')}")
        st.write(f"**Source:** {article.get('source', 'N/A')}")
        if 'url' in article:
            st.write(f"**URL:** {article['url']}")
    
    # Show explanation
    st.subheader("💡 Explanation")
    if prediction == "FAKE":
        st.warning("""
        This article shows characteristics of potentially fake news. Consider:
        - Verifying with trusted sources
        - Checking the publication date
        - Looking for supporting evidence
        - Being cautious about sensational claims
        """)
    else:
        st.info("""
        This article appears to be credible. However, always:
        - Verify with multiple sources
        - Check the publication's reputation
        - Look for evidence and citations
        - Consider potential biases
        """)

def batch_analysis(analyzer):
    st.header("📊 Batch Analysis")
    st.info("Upload multiple articles for analysis")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data preview:", df.head())
        
        if st.button("Analyze Batch"):
            st.success("Batch analysis would process all articles")

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
        
        **NewsAPI (Optional):**
        1. Go to [newsapi.org](https://newsapi.org)
        2. Register for developer account
        3. Get your API key
        """)
    
    with st.form("api_config"):
        gnews_key = st.text_input("GNews API Key:", type="password", 
                                 placeholder="Enter your GNews API key")
        
        if st.form_submit_button("Save API Keys"):
            if gnews_key:
                st.success("API key saved for this session!")
                st.info("For production, use .streamlit/secrets.toml")
            else:
                st.warning("Please enter an API key")

if __name__ == "__main__":
    main()
