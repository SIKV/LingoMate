DEFAULT_MODEL = "gpt-5-mini"

# (value, label) pairs. The value is the OpenAI model id sent to the API;
# the label is the description shown in the dropdown.
_MODELS = [
    ("gpt-5.5", "GPT-5.5 • Excellent • $$$"),
    ("gpt-5-mini", "GPT-5 mini • Recommended • $$"),
    ("gpt-5-nano", "GPT-5 nano • Good • $"),
]

def get_model_choices():
    """(label, value) pairs for the settings dropdown. The value is the OpenAI model id."""
    return [(label, value) for value, label in _MODELS]

def sanitize_model(model):
    """Browser state outlives this code, so fall back when it holds a model we no longer offer."""
    return model if model in {value for value, _ in _MODELS} else DEFAULT_MODEL

# Sentinel value for the translation dropdown, stored in browser state alongside real language names.
NO_TRANSLATION = "None"

DEFAULT_PRACTICE_LANGUAGE = "Spanish"
DEFAULT_TRANSLATION_LANGUAGE = NO_TRANSLATION

_LANGUAGE_FLAGS = {
    "English": "🇬🇧",
    "Spanish": "🇪🇸",
    "French": "🇫🇷",
    "German": "🇩🇪",
    "Italian": "🇮🇹",
    "Portuguese": "🇵🇹",
    "Dutch": "🇳🇱",
    "Swedish": "🇸🇪",
    "Polish": "🇵🇱",
    "Ukrainian": "🇺🇦",
    "Turkish": "🇹🇷",
    "Arabic": "🇸🇦",
    "Hindi": "🇮🇳",
    "Chinese (Mandarin)": "🇨🇳",
    "Japanese": "🇯🇵",
    "Korean": "🇰🇷",
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
