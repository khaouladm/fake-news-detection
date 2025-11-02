import streamlit as st
import pandas as pd
from utils.news_api import NewsFetcher
from utils.real_time_analyzer import RealTimeAnalyzer
import time
import plotly.express as px
import os
from deep_translator import GoogleTranslator 
# <-- AJOUT 1: Importer le traducteur d'interface
from utils.translator import t, set_lang 

# Page configuration
# <-- MODIFIÉ: Utilise la fonction t()
st.set_page_config(
    page_title=t("page_title"),
    page_icon="📰",
    layout="wide"
)

def main():
    # <-- AJOUT 2: Sélecteur de langue en haut de la sidebar
    st.sidebar.title(t("nav_title"))
    lang_options = {"Français": "fr", "English": "en", "العربية": "ar"}
    lang_choice = st.sidebar.selectbox(
        "Language / Langue / اللغة", 
        options=lang_options.keys(),
        # Index 0 = Français (défini dans translator.py)
        index=0 if st.session_state.lang == "fr" else 1 
    )
    # Met à jour la langue dans la session si elle change
    selected_lang_code = lang_options[lang_choice]
    if st.session_state.lang != selected_lang_code:
        set_lang(selected_lang_code)
        st.rerun() # Recharge la page pour appliquer la langue

    # <-- MODIFIÉ: Utilise t() pour les titres
    st.title(t("app_title"))
    st.markdown(f"### {t('app_subtitle')}")
    
    # Initialize components
    with st.spinner(t("loading_analyzer")):
        news_fetcher = NewsFetcher()
        analyzer = RealTimeAnalyzer()
    
    # Sidebar with model info
    render_sidebar(analyzer)
    
    # Main navigation
    # <-- MODIFIÉ: Utilise t() pour la navigation
    app_mode = st.sidebar.selectbox(
        t("nav_choose_mode"),
        [t("mode_dashboard"), t("mode_live"), t("mode_single"), 
         t("mode_batch"), t("mode_model_info"), t("mode_api_settings")]
    )
    
    # Routage basé sur le texte traduit
    if app_mode == t("mode_dashboard"):
        render_dashboard(analyzer, news_fetcher)
    elif app_mode == t("mode_live"):
        live_news_monitor(news_fetcher, analyzer)
    elif app_mode == t("mode_single"):
        single_article_analysis(analyzer)
    elif app_mode == t("mode_batch"):
        batch_analysis(analyzer)
    elif app_mode == t("mode_model_info"):
        model_info_page(analyzer)
    else:
        api_settings(news_fetcher)

def render_sidebar(analyzer):
    """Render sidebar with system status"""
    # <-- MODIFIÉ: Utilise t()
    st.sidebar.title(t("sidebar_status_title"))
    
    # Model status
    if analyzer.model_loaded:
        st.sidebar.success(t("model_active"))
        st.sidebar.info(f"{t('model_type')}: {analyzer.get_model_info()}")
    else:
        st.sidebar.warning(t("model_rule_based"))
    
    # API status
    st.sidebar.info(t("api_ready"))
    st.sidebar.metric(t("last_update"), time.strftime("%H:%M:%S"))

def render_dashboard(analyzer, news_fetcher):
    """Main dashboard view"""
    # <-- MODIFIÉ: Utilise t()
    st.header(t("mode_dashboard"))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(t("db_model_status"), "Active" if analyzer.model_loaded else "Rule-Based")
    with col2:
        st.metric(t("db_analysis_ready"), "Yes")
    with col3:
        st.metric(t("db_system"), "Online")
    
    # Quick actions
    st.subheader(t("db_quick_actions"))
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button(t("db_fetch_latest"), use_container_width=True):
            st.info(t("live_info_button"))
    
    with action_col2:
        if st.button(t("db_test_analysis"), use_container_width=True):
            test_analysis(analyzer)
    
    with action_col3:
        if st.button(t("db_view_stats"), use_container_width=True):
            show_sample_stats()
    
    # Recent activity placeholder
    st.subheader(t("db_recent_activity"))
    st.info(t("db_system_ready_info"))

def test_analysis(analyzer):
    """Quick test analysis"""
    test_article = {
        'title': 'Breaking: New Study Shows Important Findings',
        'content': 'Researchers from leading universities have published a new study with significant implications for future policy decisions.',
        'source': 'Test Source'
    }
    
    prediction, confidence = analyzer.predict_article(test_article)
    
    # <-- MODIFIÉ: Utilise t() avec .format()
    st.success(t("db_test_success").format(prediction=prediction, confidence=confidence))
    st.info(t("db_test_info"))

def show_sample_stats():
    """Show sample statistics"""
    data = {
        'Category': ['Real News', 'Fake News', 'Uncertain'],
        'Count': [65, 23, 12]
    }
    df = pd.DataFrame(data)
    
    fig = px.pie(df, values='Count', names='Category', 
                 title=t("live_summary_pie_title"))
    st.plotly_chart(fig)

def live_news_monitor(news_fetcher, analyzer):
    # <-- MODIFIÉ: Utilise t()
    st.header(t("live_title"))
    
    # Controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(t("live_feed_subtitle"))
        
        search_query = st.text_input(t("live_search_topics"), "technology news")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            num_articles = st.slider(t("live_num_articles"), 5, 20, 10)
        with col_b:
            # Sélecteur de langue pour les articles (pas l'interface)
            lang = st.selectbox(t("live_language"), ('en', 'fr', 'ar', 'es', 'de'))
        with col_c:
            st.write("") 
            st.write("") 
            if st.button(t("live_fetch_button"), type="primary"):
                fetch_and_analyze_news(news_fetcher, analyzer, search_query, num_articles, lang)
    
    with col2:
        st.subheader(t("live_stats_title"))
        st.metric(t("live_model"), "BERT" if analyzer.model_loaded else "Rule-Based")
        st.metric(t("live_status"), "Prêt" if st.session_state.lang == "fr" else "Ready")
        
        st.subheader(t("live_alerts"))
        if not analyzer.model_loaded:
            st.warning(t("live_model_warn"))
        st.info(t("live_info_button"))

def fetch_and_analyze_news(news_fetcher, analyzer, query, num_articles, lang='en'):
    """Fetch and analyze news in real-time"""
    
    if lang != 'en':
        st.warning(t("live_warn_language").format(lang=lang))
        
    try:
        with st.spinner(t("live_spinner_fetch").format(query=query, lang=lang)):
            articles = news_fetcher.fetch_real_time_news([query], lang=lang)
            articles = articles[:num_articles]
            
            if articles:
                st.success(t("live_fetch_success").format(len=len(articles)))
                results = analyzer.analyze_news_batch(articles)
                display_real_time_results(results)
            else:
                st.error(t("live_fetch_error"))
                st.info(t("live_fetch_info"))
                
    except Exception as e:
        st.error(f"Erreur: {str(e)}")

def display_real_time_results(results):
    """Display analysis results with better UI"""
    st.subheader(t("live_results_title"))
    
    if not results:
        st.info(t("live_results_title")) # "Aucun résultat à afficher"
        return
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs([t("live_tab_list"), t("live_tab_summary"), t("live_tab_feed")])
    
    with tab1:
        for i, result in enumerate(results):
            with st.expander(f"{i+1}. {result['title'][:80]}...", expanded=i==0):
                display_article_card(result)
    
    with tab2:
        show_analysis_summary(results)
    
    with tab3:
        st.info(t("live_tab_feed")) # Message d'info pour le flux live

def display_article_card(result):
    """Display individual article result as a card"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write(f"**{t('live_card_source')}:** {result.get('source', 'Unknown')}")
        st.write(f"**{t('live_card_published')}:** {result.get('published_at', 'Unknown')}")
        st.write(f"**{t('live_card_content')}:** {result['content'][:200]}...")
        
        if result.get('url'):
            st.markdown(f"[{t('live_card_read_full')}]({result['url']})")
            
        st.markdown("---")
        trans_col1, trans_col2 = st.columns([1, 2])
        with trans_col1:
            target_lang = st.selectbox(
                t("live_card_translate_to"),
                ("fr", "ar", "en", "es"),
                key=f"lang_{result.get('url', result['title'])}"
            )
        with trans_col2:
            st.write("") 
            if st.button(t("live_card_translate_btn"), key=f"btn_{result.get('url', result['title'])}"):
                try:
                    with st.spinner(t("live_card_spinner").format(lang=target_lang)):
                        translator = GoogleTranslator(source='auto', target=target_lang)
                        translated_title = translator.translate(result['title'])
                        translated_content = translator.translate(result['content'][:200] + "...")
                        
                        st.info(f"**{t('live_card_trans_title').format(lang=target_lang)}:** {translated_title}")
                        st.info(f"**{t('live_card_trans_content').format(lang=target_lang)}:** {translated_content}")
                except Exception as e:
                    st.error(f"{t('live_card_trans_fail')}: {e}")
    
    with col2:
        prediction = result['prediction']
        confidence = result['confidence']
        
        if prediction == "FAKE":
            st.error(f"**{prediction}**")
        elif prediction == "REAL":
            st.success(f"**{prediction}**")
        else:
            st.warning(f"**{prediction}**")
        
        st.metric(t("live_card_confidence"), f"{confidence:.2%}")
        st.caption(f"{t('live_card_method')}: {result.get('method', 'Unknown')}")

def show_analysis_summary(results):
    """Show analysis summary with charts"""
    if not results:
        return
    
    df = pd.DataFrame(results)
    
    fake_count = len(df[df['prediction'] == 'FAKE'])
    reliable_count = len(df[df['prediction'] == 'REAL'])
    uncertain_count = len(df[df['prediction'] == 'UNCERTAIN'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(t("live_summary_total"), len(df))
    with col2:
        st.metric(t("live_summary_reliable"), reliable_count)
    with col3:
        st.metric(t("live_summary_fake"), fake_count)
    with col4:
        st.metric(t("live_summary_uncertain"), uncertain_count)
    
    if len(df) > 0:
        fig = px.pie(df, names='prediction', title=t("live_summary_pie_title"))
        st.plotly_chart(fig)

def single_article_analysis(analyzer):
    # <-- MODIFIÉ: Utilise t()
    st.header(t("single_title"))
    
    input_method = st.radio(t("single_input_method"), [t("single_method_text"), t("single_method_url")])
    
    if input_method == t("single_method_url"):
        url = st.text_input(t("single_url_placeholder"), placeholder="https://example.com/news-article")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(t("single_url_button"), type="primary"):
                if url:
                    analyze_url_content(url, analyzer)
                else:
                    st.warning(t("single_url_warn"))
        with col2:
            if st.button(t("single_clear_button"), type="secondary"):
                st.session_state.pop('scraped_article', None)
    
    else:
        news_text = st.text_area(t("single_text_placeholder"), height=200,
                                 placeholder=t("single_text_placeholder"))
        
        if st.button(t("single_text_button")) and news_text:
            analyze_text_content(news_text, analyzer)

def analyze_url_content(url, analyzer):
    """Analyze content from URL"""
    try:
        try:
            from utils.url_scraper import URLScraper
        except ImportError as e:
            st.error("URL scraping dependencies not installed")
            st.code("pip install beautifulsoup4 requests newspaper3k")
            return
        
        scraper = URLScraper()
        
        with st.spinner("Scraping article content from URL..."):
            scraped_data = scraper.scrape_article(url)
        
        if scraped_data['success']:
            st.success("Successfully extracted article content")
            article = {
                'title': scraped_data['title'],
                'content': scraped_data['content'],
                'source': 'URL Scraping',
                'url': url
            }
            
            with st.spinner(t("single_spinner_analyze")):
                prediction, confidence = analyzer.predict_article(article)
            
            display_analysis_results(prediction, confidence, article)
            
            with st.expander("View Scraped Content"):
                st.subheader(t("single_info_title"))
                st.write(scraped_data['title'])
                st.subheader("Content Preview")
                st.write(scraped_data['content'][:500] + "...")
   
        
        else:
            st.error(f"Failed to scrape article: {scraped_data.get('error', 'Unknown error')}")
            
    except Exception as e:
        st.error(f"Error analyzing URL: {str(e)}")

def analyze_text_content(news_text, analyzer):
    """Analyze text content"""
    with st.spinner(t("single_spinner_analyze")):
        mock_article = {
            'title': 'User Input Article',
            'content': news_text,
            'source': 'Direct Input'
        }
        prediction, confidence = analyzer.predict_article(mock_article)
        display_analysis_results(prediction, confidence, mock_article)
        


def display_analysis_results(prediction, confidence, article):
    """Display analysis results in a nice format"""

    st.subheader(t("single_results_title"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        if prediction == "FAKE":
            st.error(f"{t('live_card_prediction')}: {prediction}")
        elif prediction == "REAL":
            st.success(f"{t('live_card_prediction')}: {prediction}")
        else:
            st.warning(f"{t('live_card_prediction')}: {prediction}")
    
    with col2:
        if confidence >= 0.9:
            st.success(f"{t('live_card_confidence')}: {confidence:.2%}")
        elif confidence >= 0.7:
            st.info(f"{t('live_card_confidence')}: {confidence:.2%}")
        else:
            st.warning(f"{t('live_card_confidence')}: {confidence:.2%}")
    
    with st.expander(t("single_expander_info")):
        st.write(f"**{t('single_info_title')}:** {article.get('title', 'N/A')}")
        st.write(f"**{t('single_info_source')}:** {article.get('source', 'N/A')}")
        if 'url' in article:
            st.write(f"**{t('single_info_url')}:** {article['url']}")
    
    st.subheader(t("single_explanation_title"))
    if prediction == "FAKE":
        st.warning(t("single_exp_fake"))
    else:
        st.info(t("single_exp_real"))

    # Section de traduction
    st.subheader(t("single_translate_title"))
    
    trans_col1, trans_col2 = st.columns([1, 2])
    with trans_col1:
        target_lang = st.selectbox(
            t("single_translate_to"),
            ("fr", "ar", "en", "es"),
            key="translate_single"
        )
    
    if st.button(t("single_translate_btn"), key="btn_single"):
        try:
            translator = GoogleTranslator(source='auto', target=target_lang)
            
            with st.spinner(t("live_card_spinner").format(lang=target_lang)):
                if article['title'] == 'User Input Article':
                     translated_title = f"Article ({target_lang})"
                     translated_content = translator.translate(article['content'])
                else:
                    translated_title = translator.translate(article['title'])
                    translated_content = translator.translate(article['content'])
            
            with st.expander(f"Traduction ({target_lang})", expanded=True):
                st.subheader(translated_title)
                st.write(translated_content)
        except Exception as e:
            st.error(f"{t('live_card_trans_fail')}: {e}")

def batch_analysis(analyzer):
    st.header(t("mode_batch"))
    # ... (le reste n'a pas été traduit pour rester bref, mais vous pouvez ajouter les clés)
    st.info("Upload multiple articles for analysis")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data preview:", df.head())
        
        if st.button("Analyze Batch"):
            st.success("Batch analysis would process all articles")

def model_info_page(analyzer):
    st.header(t("mode_model_info"))
    # ... (le reste n'a pas été traduit pour rester bref)
    st.subheader("BERT Model Status")
    if analyzer.model_loaded:
        st.success(" BERT Model Loaded Successfully")
    else:
        st.warning(" BERT Model Not Loaded")
    # ...

def api_settings(news_fetcher):
    # <-- MODIFIÉ: Utilise t()
    st.header(t("api_title"))
    
    st.info(t("api_info"))
    
    with st.expander(t("api_expander_title")):
        st.markdown(t("api_expander_content"))
    
    with st.form("api_config"):
        gnews_key = st.text_input(t("api_form_input"), type="password", 
                                  placeholder=t("api_form_placeholder"),
                                  key="gnews_key_input") 
        
        if st.form_submit_button(t("api_form_button")):
            if gnews_key:
                st.session_state.gnews_key = gnews_key
                news_fetcher.gnews_key = gnews_key 
                st.success(t("api_form_success"))
                st.info(t("api_form_info"))
            else:
                st.warning(t("api_form_warn"))

if __name__ == "__main__":
    main()