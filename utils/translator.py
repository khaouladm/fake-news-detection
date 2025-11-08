import streamlit as st

# Dictionnaires de traduction
TRANSLATIONS = {
    'fr': {
        'app_title': 'NewsVerifi AI',
        'app_subtitle': 'Plateforme Professionnelle de Détection de Fake News',
        'language': 'Langue',
        'select_language': 'Choisir la langue',
        'navigation': 'Navigation',
        'system_status': 'Statut du Système',
        'quick_actions': 'Actions Rapides',
        'status_analyzer': 'Analyseur',
        'status_api': 'Statut API',
        'last_update': 'Dernière MAJ',
        'action_refresh': 'Actualiser les Données',
        'action_view_stats': 'Voir les Statistiques',
        'action_quick_scan': 'Analyse Rapide',
        'mode_dashboard': 'Tableau de Bord',
        'mode_live': 'Monitoring Temps Réel',
        'mode_single': 'Analyse d\'Article',
        'mode_batch': 'Analyse par Lot',
        'mode_model_info': 'Info Modèle',
        'mode_api_settings': 'Paramètres',
        'metric_articles_analyzed': 'Articles Analysés',
        'metric_accuracy': 'Taux de Précision',
        'metric_fake_detected': 'Fake News Détectées',
        'metric_avg_confidence': 'Confiance Moyenne',
        'analysis_overview': 'Aperçu de l\'Analyse',
        'content_distribution': 'Distribution du Contenu',
        'weekly_trends': 'Tendances Hebdomadaires',
        'recent_activity': 'Activité Récente',
        'quick_analysis': 'Analyse Rapide',
        'test_analyzer': 'Tester l\'Analyseur'
    },
    'en': {
        'app_title': 'NewsVerifi AI',
        'app_subtitle': 'Professional Fake News Detection Platform',
        'language': 'Language',
        'select_language': 'Select language',
        'navigation': 'Navigation',
        'system_status': 'System Status',
        'quick_actions': 'Quick Actions',
        'status_analyzer': 'Analyzer',
        'status_api': 'API Status',
        'last_update': 'Last Update',
        'action_refresh': 'Refresh Data',
        'action_view_stats': 'View Statistics',
        'action_quick_scan': 'Quick Scan',
        'mode_dashboard': 'Dashboard',
        'mode_live': 'Live Monitor',
        'mode_single': 'Single Analysis',
        'mode_batch': 'Batch Analysis',
        'mode_model_info': 'Model Info',
        'mode_api_settings': 'Settings',
        'metric_articles_analyzed': 'Articles Analyzed',
        'metric_accuracy': 'Accuracy Rate',
        'metric_fake_detected': 'Fake News Detected',
        'metric_avg_confidence': 'Avg Confidence',
        'analysis_overview': 'Analysis Overview',
        'content_distribution': 'Content Distribution',
        'weekly_trends': 'Weekly Trends',
        'recent_activity': 'Recent Activity',
        'quick_analysis': 'Quick Analysis',
        'test_analyzer': 'Test Analyzer'
    },
    'ar': {
        'app_title': 'نيوزفيريفاي AI',
        'app_subtitle': 'منصة احترافية للكشف عن الأخبار المزيفة',
        'language': 'اللغة',
        'select_language': 'اختر اللغة',
        'navigation': 'التنقل',
        'system_status': 'حالة النظام',
        'quick_actions': 'إجراءات سريعة',
        'status_analyzer': 'المحلل',
        'status_api': 'حالة API',
        'last_update': 'آخر تحديث',
        'action_refresh': 'تحديث البيانات',
        'action_view_stats': 'عرض الإحصائيات',
        'action_quick_scan': 'مسح سريع',
        'mode_dashboard': 'لوحة التحكم',
        'mode_live': 'المراقبة المباشرة',
        'mode_single': 'تحليل مقال',
        'mode_batch': 'تحليل جماعي',
        'mode_model_info': 'معلومات النموذج',
        'mode_api_settings': 'الإعدادات',
        'metric_articles_analyzed': 'المقالات التي تم تحليلها',
        'metric_accuracy': 'معدل الدقة',
        'metric_fake_detected': 'الأخبار المزيفة المكتشفة',
        'metric_avg_confidence': 'متوسط الثقة',
        'analysis_overview': 'نظرة عامة على التحليل',
        'content_distribution': 'توزيع المحتوى',
        'weekly_trends': 'الاتجاهات الأسبوعية',
        'recent_activity': 'النشاط الأخير',
        'quick_analysis': 'تحليل سريع',
        'test_analyzer': 'اختبار المحلل'
    }
}

def t(key):
    """Traduire une clé dans la langue courante"""
    lang = st.session_state.get('lang', 'fr')
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['fr'].get(key, key))

def set_lang(language_code):
    """Définir la langue de l'application"""
    st.session_state.lang = language_code