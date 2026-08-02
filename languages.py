# Sentinel value for the translation dropdown, stored in browser state alongside real language names.
NO_TRANSLATION = "None"

DEFAULT_PRACTICE_LANGUAGE = "Spanish"
DEFAULT_TRANSLATION_LANGUAGE = NO_TRANSLATION

_LANGUAGE_FLAGS = {
    "Arabic": "🇸🇦",
    "Czech": "🇨🇿",
    "Danish": "🇩🇰",
    "Dutch": "🇳🇱",
    "English": "🇬🇧",
    "Finnish": "🇫🇮",
    "French": "🇫🇷",
    "German": "🇩🇪",
    "Greek": "🇬🇷",
    "Hungarian": "🇭🇺",
    "Italian": "🇮🇹",
    "Japanese": "🇯🇵",
    "Korean": "🇰🇷",
    "Norwegian": "🇳🇴",
    "Polish": "🇵🇱",
    "Portuguese": "🇵🇹",
    "Romanian": "🇷🇴",
    "Spanish": "🇪🇸",
    "Swedish": "🇸🇪",
    "Turkish": "🇹🇷",
    "Ukrainian": "🇺🇦",
}

def get_language_flag(language):
    return _LANGUAGE_FLAGS.get(language, "")

def get_language_label(language):
    return f"{language} {get_language_flag(language)}".strip()

def get_practice_language_choices():
    """(label, value) pairs for the practice dropdown. The value is the bare language name."""
    return [(get_language_label(name), name) for name in _LANGUAGE_FLAGS]

def get_translation_language_choices():
    return [("None (no translation)", NO_TRANSLATION)] + get_practice_language_choices()

def sanitize_practice_language(language):
    """Browser state outlives this code, so fall back when it holds a language we no longer offer."""
    return language if language in _LANGUAGE_FLAGS else DEFAULT_PRACTICE_LANGUAGE

def sanitize_translation_language(language):
    if language == NO_TRANSLATION or language in _LANGUAGE_FLAGS:
        return language
    return DEFAULT_TRANSLATION_LANGUAGE

def should_translate(practice_language, translation_language):
    """Translating a language into itself is a no-op, so treat it the same as no translation."""
    return translation_language != NO_TRANSLATION and translation_language != practice_language
