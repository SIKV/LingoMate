import gradio as gr
from chat import *
from models import *
from languages import *

theme = gr.themes.Soft(
    primary_hue=gr.themes.colors.sky,
    secondary_hue=gr.themes.colors.cyan,
    neutral_hue=gr.themes.colors.slate,
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "sans-serif"],
).set(
    button_primary_background_fill="*primary_500",
    button_primary_background_fill_hover="*primary_600",
    button_primary_text_color="white",
    button_primary_border_color="*primary_500",
    button_primary_border_color_hover="*primary_600",
)

with gr.Blocks(theme=theme, title="LingoMate") as gradio_app:
    api_key_browser_state = gr.BrowserState("")
    api_key_state = gr.State("")
    model_browser_state = gr.BrowserState(DEFAULT_MODEL)
    practice_language_browser_state = gr.BrowserState(DEFAULT_PRACTICE_LANGUAGE)
    translation_language_browser_state = gr.BrowserState(DEFAULT_TRANSLATION_LANGUAGE)

    with gr.Tab("Chat"):
        api_key_input = gr.Textbox(
            show_label=False,
            placeholder="OpenAI API Key (required)",
            type="password",
        )

        gr.Markdown("The API key is stored locally in your browser.")

        with gr.Row(equal_height=True):
            practice_language_dropdown = gr.Dropdown(
                choices=get_practice_language_choices(),
                value=DEFAULT_PRACTICE_LANGUAGE,
                label="I practice",
                filterable=True,
            )
            translation_language_dropdown = gr.Dropdown(
                choices=get_translation_language_choices(),
                value=DEFAULT_TRANSLATION_LANGUAGE,
                label="Translate to",
                filterable=True,
            )

        start_new_chat_btn = gr.Button(
            "✨ Start New Chat", 
            variant="primary", 
            interactive=False,
        )

        chatbot = gr.Chatbot(
            type="messages",
            show_copy_button=True,
            show_label=False,
            placeholder="Please provide OpenAI API Key and press ✨ Start New Chat.",
        )

        with gr.Row(equal_height=True):
            msg = gr.Textbox(placeholder="Type a message...", show_label=False)
            submit_btn = gr.Button("Submit", scale=0, variant="primary", interactive=False)

    with gr.Tab("Settings"):
        model_dropdown = gr.Dropdown(
            choices=get_model_choices(),
            value=DEFAULT_MODEL,
            label="Model",
            filterable=True,
        )

        gr.Markdown("Please start a new chat after changing any settings.")

    def restore_all(saved_key, saved_model, saved_practice_language, saved_translation_language):
        practice_language = sanitize_practice_language(saved_practice_language)
        translation_language = sanitize_translation_language(saved_translation_language)
        return (
            saved_key,
            saved_key,
            sanitize_model(saved_model),
            practice_language,
            translation_language,
            gr.update(),
        )

    def save_api_key(value):
        return value, value

    def save_model(value):
        gr.Info("Settings updated.")
        return value

    def _notify_language_change(practice_language, translation_language):
        if should_translate(practice_language, translation_language):
            gr.Info("Please start a new chat to apply the new languages.")
        elif translation_language != NO_TRANSLATION:
            gr.Warning(f"Translation is off while both languages are {translation_language}.")
        else:
            gr.Info("Translation is off. Please start a new chat to apply the new languages.")

    def save_practice_language(practice_language, translation_language):
        _notify_language_change(practice_language, translation_language)
        return practice_language, gr.update(label=get_language_label(practice_language))

    def save_translation_language(translation_language, practice_language):
        _notify_language_change(practice_language, translation_language)
        return translation_language

    def toggle_btn(str):
        return gr.Button(
            interactive=bool(str.strip()),
        )

    gradio_app.load(
        restore_all,
        inputs=[
            api_key_browser_state,
            model_browser_state,
            practice_language_browser_state,
            translation_language_browser_state,
        ],
        outputs=[
            api_key_input,
            api_key_state,
            model_dropdown,
            practice_language_dropdown,
            translation_language_dropdown,
            chatbot,
        ],
    )

    api_key_input.change(save_api_key, inputs=[api_key_input], outputs=[api_key_browser_state, api_key_state])
    api_key_input.change(toggle_btn, inputs=[api_key_input], outputs=[start_new_chat_btn])

    # .input() rather than .change() so restoring saved settings on load doesn't fire the toasts.
    model_dropdown.input(save_model, inputs=[model_dropdown], outputs=[model_browser_state])

    practice_language_dropdown.input(
        save_practice_language,
        inputs=[practice_language_dropdown, translation_language_dropdown],
        outputs=[practice_language_browser_state, chatbot],
    )

    translation_language_dropdown.input(
        save_translation_language,
        inputs=[translation_language_dropdown, practice_language_dropdown],
        outputs=[translation_language_browser_state],
    )

    msg.change(toggle_btn, inputs=[msg], outputs=[submit_btn])

    msg.submit(chat_send_user_answer, [msg, chatbot], [msg, chatbot], queue=False).then(
        chat_send_assistant_answer,
        [chatbot, api_key_state, model_dropdown, practice_language_dropdown, translation_language_dropdown],
        chatbot,
    )

    submit_btn.click(chat_send_user_answer, [msg, chatbot], [msg, chatbot], queue=False).then(
        chat_send_assistant_answer,
        [chatbot, api_key_state, model_dropdown, practice_language_dropdown, translation_language_dropdown],
        chatbot,
    )

    start_new_chat_btn.click(chat_clear_history, outputs=[chatbot], queue=False).then(
        chat_start_new,
        inputs=[api_key_state, model_dropdown, practice_language_dropdown, translation_language_dropdown],
        outputs=[chatbot],
    )
