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
