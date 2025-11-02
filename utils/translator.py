import streamlit as st

# Dictionnaire contenant toutes les traductions
translations = {
    "fr": {
        "page_title": "Détecteur de Fake News en Temps Réel",
        "app_title": "📰 Détecteur de Fake News en Temps Réel",
        "app_subtitle": "Surveillez et analysez les articles en temps réel avec l'IA",
        "loading_analyzer": "Chargement de l'analyseur IA...",
        "sidebar_status_title": "État du Système",
        "model_active": "✅ Modèle IA: Actif",
        "model_type": "Type",
        "model_rule_based": "⚠️ Modèle IA: Basé sur règles",
        "api_ready": "🌐 API News: Prête",
        "last_update": "Dernière MàJ",
        "nav_title": "Navigation",
        "nav_choose_mode": "Choisir le Mode",
        "mode_dashboard": "🏠 Tableau de bord",
        "mode_live": "🔴 Moniteur Live",
        "mode_single": "🔍 Analyse Unique",
        "mode_batch": "📊 Analyse par Lots",
        "mode_model_info": "🤖 Infos Modèle",
        "mode_api_settings": "⚙️ Paramètres API",
        
        # Tableau de bord
        "db_model_status": "Statut Modèle IA",
        "db_analysis_ready": "Analyse Prête",
        "db_system": "Système",
        "db_quick_actions": "Actions Rapides",
        "db_fetch_latest": "🔄 Récupérer Articles",
        "db_test_analysis": "🔍 Tester Analyse",
        "db_view_stats": "📈 Voir Stats",
        "db_recent_activity": "Activité Récente",
        "db_system_ready_info": """
        **Système prêt pour l'analyse en temps réel:**
        - Modèle BERT chargé et actif
        - Connectivité à l'API News établie
        - Traitement en temps réel activé
        
        **Suivant:** Allez à **Moniteur Live** pour commencer à analyser !
        """,
        "db_test_success": "Analyse Test: **{prediction}** (Confiance: {confidence:.2%})",
        "db_test_info": "Cela démontre que le système fonctionne correctement !",

        # Live Monitor
        "live_title": "🔴 Moniteur Live",
        "live_feed_subtitle": "Flux d'articles en temps réel",
        "live_search_topics": "🔍 Sujets de recherche:",
        "live_num_articles": "Nombre d'articles",
        "live_language": "Langue (Article)",
        "live_fetch_button": "🎯 Récupérer & Analyser",
        "live_stats_title": "Stats Live",
        "live_model": "Modèle",
        "live_status": "Statut",
        "live_alerts": "Alertes",
        "live_model_warn": "Utilisation de l'analyse basée sur des règles",
        "live_info_button": "Cliquez sur le bouton pour récupérer les articles",
        "live_warn_language": "⚠️ Vous récupérez des articles en '{lang}'. Le modèle IA est principalement entraîné en anglais et pourrait être moins fiable.",
        "live_spinner_fetch": "🔄 Récupération des articles '{query}' en '{lang}'...",
        "live_fetch_success": "📰 {len} articles récupérés",
        "live_fetch_error": "❌ Aucun article trouvé. Vérifiez la configuration de l'API ou essayez d'autres termes.",
        "live_fetch_info": "💡 Essayez de rechercher : 'technologie', 'politique', 'santé', 'sport'",
        "live_results_title": "📊 Résultats de l'analyse",
        "live_tab_list": "📋 Vue Liste",
        "live_tab_summary": "📈 Résumé",
        "live_tab_feed": "🔄 Flux Live (Info)",
        "live_card_source": "Source",
        "live_card_published": "Publié",
        "live_card_content": "Contenu",
        "live_card_read_full": "📖 Lire l'article complet",
        "live_card_translate_to": "Traduire",
        "live_card_translate_btn": "Traduire",
        "live_card_spinner": "Traduction vers {lang}...",
        "live_card_trans_title": "Titre ({lang})",
        "live_card_trans_content": "Contenu ({lang})",
        "live_card_trans_fail": "Traduction échouée",
        "live_card_prediction": "Prédiction",
        "live_card_confidence": "Confiance",
        "live_card_method": "Méthode",
        "live_summary_total": "Total Articles",
        "live_summary_reliable": "Fiables",
        "live_summary_fake": "Potentiel Faux",
        "live_summary_uncertain": "Incertains",
        "live_summary_pie_title": "Distribution de la fiabilité",

        # Single Check
        "single_title": "🔍 Analyser un seul article",
        "single_input_method": "Méthode d'entrée:",
        "single_method_text": "Entrer Texte",
        "single_method_url": "Entrer URL",
        "single_url_placeholder": "URL de l'article:",
        "single_url_button": "🌐 Analyser URL",
        "single_url_warn": "Veuillez entrer une URL",
        "single_clear_button": "🧹 Effacer",
        "single_text_placeholder": "Coller le texte de l'article:",
        "single_text_button": "Analyser Texte",
        "single_spinner_analyze": "🤖 Analyse du contenu...",
        "single_results_title": "🎯 Résultats de l'analyse",
        "single_expander_info": "📋 Information de l'article",
        "single_info_title": "Titre",
        "single_info_source": "Source",
        "single_info_url": "URL",
        "single_explanation_title": "💡 Explication",
        "single_exp_fake": """
        Cet article montre des caractéristiques de fausses nouvelles potentielles. Pensez à:
        - Vérifier auprès de sources fiables
        - Vérifier la date de publication
        - Chercher des preuves à l'appui
        - Être prudent avec les affirmations sensationnelles
        """,
        "single_exp_real": """
        Cet article semble crédible. Cependant, toujours:
        - Vérifier auprès de plusieurs sources
        - Vérifier la réputation de la publication
        - Chercher des preuves et des citations
        - Considérer les biais potentiels
        """,
        "single_translate_title": "🌐 Traduire l'article",
        "single_translate_to": "Traduire en:",
        "single_translate_btn": "Traduire",

        # API Settings
        "api_title": "⚙️ Configuration de l'API",
        "api_info": "Obtenez des clés API gratuites pour activer la récupération de news:",
        "api_expander_title": "📋 Comment obtenir les clés API",
        "api_expander_content": """
        **GNews API (Recommandé):**
        1. Allez sur [gnews.io](https://gnews.io)
        2. Créez un compte gratuit
        3. Obtenez votre clé API
        4. Entrez-la ci-dessous
        
        **NewsAPI (Optionnel):**
        1. Allez sur [newsapi.org](https://newsapi.org)
        2. Créez un compte développeur
        3. Obtenez votre clé API
        """,
        "api_form_input": "Clé API GNews:",
        "api_form_placeholder": "Entrez votre clé API GNews",
        "api_form_button": "Sauvegarder les clés API",
        "api_form_success": "Clé API sauvegardée pour cette session !",
        "api_form_info": "Pour la production, utilisez .streamlit/secrets.toml",
        "api_form_warn": "Veuillez entrer une clé API",
    },
    "en": {
        "page_title": "Real-Time Fake News Detector",
        "app_title": "📰 Real-Time Fake News Detector",
        "app_subtitle": "Monitor and analyze news in real-time using AI",
        "loading_analyzer": "Loading AI analyzer...",
        "sidebar_status_title": "System Status",
        "model_active": "✅ AI Model: Active",
        "model_type": "Type",
        "model_rule_based": "⚠️ AI Model: Rule-Based",
        "api_ready": "🌐 News API: Ready",
        "last_update": "Last Update",
        "nav_title": "Navigation",
        "nav_choose_mode": "Choose Mode",
        "mode_dashboard": "🏠 Dashboard",
        "mode_live": "🔴 Live News Monitor",
        "mode_single": "🔍 Single Article Check",
        "mode_batch": "📊 Batch Analysis",
        "mode_model_info": "🤖 Model Info",
        "mode_api_settings": "⚙️ API Settings",

        # Dashboard
        "db_model_status": "AI Model Status",
        "db_analysis_ready": "Analysis Ready",
        "db_system": "System",
        "db_quick_actions": "Quick Actions",
        "db_fetch_latest": "🔄 Fetch Latest News",
        "db_test_analysis": "🔍 Test Analysis",
        "db_view_stats": "📈 View Stats",
        "db_recent_activity": "Recent Activity",
        "db_system_ready_info": """
        **System Ready for Real-Time Analysis:**
        - BERT Model loaded and active
        - News API connectivity established
        - Real-time processing enabled
        
        **Next:** Go to **Live News Monitor** to start analyzing real news!
        """,
        "db_test_success": "Test Analysis: **{prediction}** (Confidence: {confidence:.2%})",
        "db_test_info": "This demonstrates the system is working correctly!",
        
        # Live Monitor
        "live_title": "🔴 Live News Monitor",
        "live_feed_subtitle": "Real-time News Feed",
        "live_search_topics": "🔍 Search topics:",
        "live_num_articles": "Number of articles",
        "live_language": "Language (Article)",
        "live_fetch_button": "🎯 Fetch & Analyze",
        "live_stats_title": "Live Stats",
        "live_model": "Model",
        "live_status": "Status",
        "live_alerts": "Alerts",
        "live_model_warn": "Using rule-based analysis",
        "live_info_button": "Click button to fetch news",
        "live_warn_language": "⚠️ You are fetching news in '{lang}'. The AI model is likely trained on English and may produce unreliable results.",
        "live_spinner_fetch": "🔄 Fetching latest '{query}' news in '{lang}'...",
        "live_fetch_success": "📰 Fetched {len} articles",
        "live_fetch_error": "❌ No articles found. Check API configuration or try different search terms.",
        "live_fetch_info": "💡 Try searching for: 'technology', 'politics', 'health', 'sports'",
        "live_results_title": "📊 Analysis Results",
        "live_tab_list": "📋 List View",
        "live_tab_summary": "📈 Summary",
        "live_tab_feed": "🔄 Live Feed (Info)",
        "live_card_source": "Source",
        "live_card_published": "Published",
        "live_card_content": "Content",
        "live_card_read_full": "📖 Read full article",
        "live_card_translate_to": "Translate",
        "live_card_translate_btn": "Translate",
        "live_card_spinner": "Translating to {lang}...",
        "live_card_trans_title": "Title ({lang})",
        "live_card_trans_content": "Content ({lang})",
        "live_card_trans_fail": "Translation failed",
        "live_card_prediction": "Prediction",
        "live_card_confidence": "Confidence",
        "live_card_method": "Method",
        "live_summary_total": "Total Articles",
        "live_summary_reliable": "Reliable",
        "live_summary_fake": "Potential Fake",
        "live_summary_uncertain": "Uncertain",
        "live_summary_pie_title": "News Reliability Distribution",

        # Single Check
        "single_title": "🔍 Analyze Single Article",
        "single_input_method": "Input method:",
        "single_method_text": "Enter Text",
        "single_method_url": "Enter URL",
        "single_url_placeholder": "News article URL:",
        "single_url_button": "🌐 Analyze URL",
        "single_url_warn": "Please enter a URL",
        "single_clear_button": "🧹 Clear",
        "single_text_placeholder": "Paste article text:",
        "single_text_button": "Analyze Text",
        "single_spinner_analyze": "🤖 Analyzing article content...",
        "single_results_title": "🎯 Analysis Results",
        "single_expander_info": "📋 Article Information",
        "single_info_title": "Title",
        "single_info_source": "Source",
        "single_info_url": "URL",
        "single_explanation_title": "💡 Explanation",
        "single_exp_fake": """
        This article shows characteristics of potentially fake news. Consider:
        - Verifying with trusted sources
        - Checking the publication date
        - Looking for supporting evidence
        - Being cautious about sensational claims
        """,
        "single_exp_real": """
        This article appears to be credible. However, always:
        - Verify with multiple sources
        - Check the publication's reputation
        - Look for evidence and citations
        - Consider potential biases
        """,
        "single_translate_title": "🌐 Translate Article",
        "single_translate_to": "Translate to:",
        "single_translate_btn": "Translate",
        
        # API Settings
        "api_title": "⚙️ API Configuration",
        "api_info": "Get free API keys to enable real-time news fetching:",
        "api_expander_title": "📋 How to get API keys",
        "api_expander_content": """
        **GNews API (Recommended):**
        1. Go to [gnews.io](https://gnews.io)
        2. Sign up for free account
        3. Get your API key
        4. Enter it below
        
        **NewsAPI (Optional):**
        1. Go to [newsapi.org](https://newsapi.org)
        2. Register for developer account
        3. Get your API key
        """,
        "api_form_input": "GNews API Key:",
        "api_form_placeholder": "Enter your GNews API key",
        "api_form_button": "Save API Keys",
        "api_form_success": "API key saved for this session!",
        "api_form_info": "For production, use .streamlit/secrets.toml",
        "api_form_warn": "Please enter an API key",
    },
    
    # <-- AJOUTÉ : Bloc de traduction arabe complet
    "ar": {
        "page_title": "كاشف الأخبار الكاذبة في الوقت الفعلي",
        "app_title": "📰 كاشف الأخبار الكاذبة في الوقت الفعلي",
        "app_subtitle": "مراقبة وتحليل الأخبار في الوقت الفعلي باستخدام الذكاء الاصطناعي",
        "loading_analyzer": "جاري تحميل محلل الذكاء الاصطناعي...",
        "sidebar_status_title": "حالة النظام",
        "model_active": "✅ نموذج الذكاء الاصطناعي: نشط",
        "model_type": "النوع",
        "model_rule_based": "⚠️ نموذج الذكاء الاصطناعي: يعتمد على القواعد",
        "api_ready": "🌐 واجهة برمجة تطبيقات الأخبار: جاهزة",
        "last_update": "آخر تحديث",
        "nav_title": "التنقل",
        "nav_choose_mode": "اختر الوضع",
        "mode_dashboard": "🏠 لوحة التحكم",
        "mode_live": "🔴 مراقبة حية",
        "mode_single": "🔍 تحليل فردي",
        "mode_batch": "📊 تحليل الدفعات",
        "mode_model_info": "🤖 معلومات النموذج",
        "mode_api_settings": "⚙️ إعدادات API",

        # Tableau de bord
        "db_model_status": "حالة نموذج الذكاء الاصطناعي",
        "db_analysis_ready": "التحليل جاهز",
        "db_system": "النظام",
        "db_quick_actions": "إجراءات سريعة",
        "db_fetch_latest": "🔄 جلب آخر الأخبار",
        "db_test_analysis": "🔍 اختبار التحليل",
        "db_view_stats": "📈 عرض الإحصائيات",
        "db_recent_activity": "النشاط الأخير",
        "db_system_ready_info": """
        **النظام جاهز للتحليل في الوقت الفعلي:**
        - تم تحميل نموذج BERT وهو نشط
        - تم إنشاء الاتصال بواجهة برمجة تطبيقات الأخبار
        - المعالجة في الوقت الفعلي مفعلة
        
        **التالي:** اذهب إلى **مراقبة حية** لبدء التحليل!
        """,
        "db_test_success": "تحليل اختباري: **{prediction}** (الثقة: {confidence:.2%})",
        "db_test_info": "هذا يوضح أن النظام يعمل بشكل صحيح!",

        # Live Monitor
        "live_title": "🔴 مراقبة حية",
        "live_feed_subtitle": "موجز الأخبار في الوقت الفعلي",
        "live_search_topics": "🔍 البحث عن مواضيع:",
        "live_num_articles": "عدد المقالات",
        "live_language": "اللغة (المقالات)",
        "live_fetch_button": "🎯 جلب وتحليل",
        "live_stats_title": "إحصائيات حية",
        "live_model": "النموذج",
        "live_status": "الحالة",
        "live_alerts": "تنبيهات",
        "live_model_warn": "يتم استخدام التحليل القائم على القواعد",
        "live_info_button": "انقر فوق الزر لجلب الأخبار",
        "live_warn_language": "⚠️ أنت تجلب أخبارًا باللغة '{lang}'. نموذج الذكاء الاصطناعي مدرب بشكل أساسي على اللغة الإنجليزية وقد تكون النتائج غير موثوقة.",
        "live_spinner_fetch": "🔄 جاري جلب آخر الأخبار لـ '{query}' باللغة '{lang}'...",
        "live_fetch_success": "📰 تم جلب {len} مقالات",
        "live_fetch_error": "❌ لم يتم العثور على مقالات. تحقق من إعدادات API أو جرب مصطلحات بحث مختلفة.",
        "live_fetch_info": "💡 حاول البحث عن: 'تكنولوجيا', 'سياسة', 'صحة', 'رياضة'",
        "live_results_title": "📊 نتائج التحليل",
        "live_tab_list": "📋 عرض القائمة",
        "live_tab_summary": "📈 ملخص",
        "live_tab_feed": "🔄 بث حي (معلومات)",
        "live_card_source": "المصدر",
        "live_card_published": "نشر في",
        "live_card_content": "المحتوى",
        "live_card_read_full": "📖 قراءة المقال كاملاً",
        "live_card_translate_to": "ترجمة",
        "live_card_translate_btn": "ترجمة",
        "live_card_spinner": "جاري الترجمة إلى {lang}...",
        "live_card_trans_title": "العنوان ({lang})",
        "live_card_trans_content": "المحتوى ({lang})",
        "live_card_trans_fail": "فشلت الترجمة",
        "live_card_prediction": "التنبؤ",
        "live_card_confidence": "الثقة",
        "live_card_method": "الطريقة",
        "live_summary_total": "إجمالي المقالات",
        "live_summary_reliable": "موثوق",
        "live_summary_fake": "محتمل زائف",
        "live_summary_uncertain": "غير مؤكد",
        "live_summary_pie_title": "توزيع موثوقية الأخبار",

        # Single Check
        "single_title": "🔍 تحليل مقال واحد",
        "single_input_method": "طريقة الإدخال:",
        "single_method_text": "إدخال نص",
        "single_method_url": "إدخال رابط",
        "single_url_placeholder": "رابط المقال:",
        "single_url_button": "🌐 تحليل الرابط",
        "single_url_warn": "الرجاء إدخال رابط",
        "single_clear_button": "🧹 مسح",
        "single_text_placeholder": "الصق نص المقال هنا:",
        "single_text_button": "تحليل النص",
        "single_spinner_analyze": "🤖 جاري تحليل المحتوى...",
        "single_results_title": "🎯 نتائج التحليل",
        "single_expander_info": "📋 معلومات المقال",
        "single_info_title": "العنوان",
        "single_info_source": "المصدر",
        "single_info_url": "الرابط",
        "single_explanation_title": "💡 توضيح",
        "single_exp_fake": """
        يظهر هذا المقال خصائص الأخبار التي يحتمل أن تكون زائفة. ننصح بـ:
        - التحقق من مصادر موثوقة
        - التحقق من تاريخ النشر
        - البحث عن أدلة داعمة
        - توخي الحذر من الادعاءات المثيرة
        """,
        "single_exp_real": """
        يبدو هذا المقال ذا مصداقية. ومع ذلك، دائماً:
        - تحقق من مصادر متعددة
        - تحقق من سمعة الناشر
        - ابحث عن أدلة ومصادر
        - ضع في اعتبارك التحيزات المحتملة
        """,
        "single_translate_title": "🌐 ترجمة المقال",
        "single_translate_to": "ترجمة إلى:",
        "single_translate_btn": "ترجمة",

        # API Settings
        "api_title": "⚙️ إعدادات واجهة برمجة التطبيقات (API)",
        "api_info": "احصل على مفاتيح API مجانية لتفعيل جلب الأخبار في الوقت الفعلي:",
        "api_expander_title": "📋 كيفية الحصول على مفاتيح API",
        "api_expander_content": """
        **GNews API (موصى به):**
        1. اذهب إلى [gnews.io](https://gnews.io)
        2. قم بإنشاء حساب مجاني
        3. احصل على مفتاح API الخاص بك
        4. أدخله أدناه
        
        **NewsAPI (اختياري):**
        1. اذهب إلى [newsapi.org](https://newsapi.org)
        2. قم بالتسجيل للحصول على حساب مطور
        3. احصل على مفتاح API الخاص بك
        """,
        "api_form_input": "مفتاح GNews API:",
        "api_form_placeholder": "أدخل مفتاح GNews API الخاص بك",
        "api_form_button": "حفظ مفاتيح API",
        "api_form_success": "تم حفظ مفتاح API لهذه الجلسة!",
        "api_form_info": "للإنتاج، استخدم .streamlit/secrets.toml",
        "api_form_warn": "الرجاء إدخال مفتاح API",
    }
}

# Initialiser l'état de la session pour la langue si elle n'existe pas
if 'lang' not in st.session_state:
    st.session_state.lang = "fr" # Défaut en français

# Fonction pour changer la langue
def set_lang(lang_code):
    st.session_state.lang = lang_code

# Fonction 't' (pour 'translate') qui récupère le texte
def t(key):
    """
    Récupère une chaîne de traduction basée sur la clé et la langue actuelle 
    stockée dans st.session_state.lang
    """
    lang = st.session_state.lang
    # Revient à l'anglais si la clé n'existe pas dans la langue sélectionnée
    return translations.get(lang, translations["en"]).get(key, f"NO_TRANSLATION_FOR_{key}")