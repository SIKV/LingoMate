import gradio as gr
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

# Storage for settings.
_settings = {
    "api_key": "",
    "chat_length": ChatLength.MEDIUM,
    "show_en_translation": True
}

def show_settings_updated_alert():
    gr.Info("Settings updated.")

def set_api_key(api_key):
    _settings["api_key"] = api_key

def get_api_key():
    return _settings["api_key"]

def set_chat_length(length):
    _settings["chat_length"] = length
    show_settings_updated_alert()

def get_chat_length():
    return ChatLength(_settings["chat_length"])

def get_chat_length_int():
    return get_chat_length().to_int()

def set_show_en_translation(show):
    _settings["show_en_translation"] = show
    show_settings_updated_alert()

def get_show_en_translation():
    return _settings["show_en_translation"]

def get_current_chat_language():
    return "Spanish"
