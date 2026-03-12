import gradio as gr
import json
import os
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

_SETTINGS_FILE = os.path.expanduser("~/.lingomate_settings.json")

_DEFAULTS = {
    "api_key": "",
    "chat_length": ChatLength.MEDIUM.value,
    "show_en_translation": True
}

# Storage for settings.
_settings = dict(_DEFAULTS)

def _load_settings():
    if os.path.exists(_SETTINGS_FILE):
        try:
            with open(_SETTINGS_FILE, "r") as f:
                saved = json.load(f)
            for key in _DEFAULTS:
                if key in saved:
                    _settings[key] = saved[key]
        except (json.JSONDecodeError, IOError, OSError):
            pass

def _save_settings():
    try:
        serializable = dict(_settings)
        if isinstance(serializable.get("chat_length"), ChatLength):
            serializable["chat_length"] = serializable["chat_length"].value
        with open(_SETTINGS_FILE, "w") as f:
            json.dump(serializable, f)
    except (IOError, OSError):
        pass

_load_settings()

def show_settings_updated_alert():
    gr.Info("Settings updated.")

def set_api_key(api_key):
    _settings["api_key"] = api_key
    _save_settings()

def get_api_key():
    return _settings["api_key"]

def set_chat_length(length):
    _settings["chat_length"] = length
    _save_settings()
    show_settings_updated_alert()

def get_chat_length():
    return ChatLength(_settings["chat_length"])

def get_chat_length_int():
    return get_chat_length().to_int()

def set_show_en_translation(show):
    _settings["show_en_translation"] = show
    _save_settings()
    show_settings_updated_alert()

def get_show_en_translation():
    return _settings["show_en_translation"]

def get_current_chat_language():
    return "Spanish"
