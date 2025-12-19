import json
import os
from typing import Dict

_translations: Dict[str, Dict[str, str]] = {}
_lang = 'en'


def _load_translations():
    global _translations
    if _translations:
        return
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    path = os.path.join(base, 'i18n', 'translations.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            _translations = json.load(f)
    except Exception:
        _translations = {"en": {}}


def set_language(lang_code: str):
    global _lang
    _load_translations()
    if lang_code in _translations:
        _lang = lang_code
    else:
        _lang = 'en'


def get_language() -> str:
    return _lang


def t(key: str, **kwargs) -> str:
    """Translate a key using the loaded translations. If key missing, return key itself.

    Example: t('sidebar_model_type', type='BERT')
    """
    _load_translations()
    lang_map = _translations.get(_lang, {})
    text = lang_map.get(key)
    if text is None:
        # fallback to English then key
        text = _translations.get('en', {}).get(key, key)
    try:
        return text.format(**kwargs)
    except Exception:
        return text


def available_languages():
    _load_translations()
    return list(_translations.keys())
