from enum import Enum

class ChatLength(Enum):
    SHORT = "Short (5 replies)"
    MEDIUM = "Medium (10 replies)"
    LONG = "Long (20 replies)"

    def to_int(self) -> int:
        return {
            ChatLength.SHORT: 5,
            ChatLength.MEDIUM: 10,
            ChatLength.LONG: 20,
        }[self]

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
