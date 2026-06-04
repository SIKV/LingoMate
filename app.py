from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import gradio as gr
from gradio.routes import mount_gradio_app
from chat import *
from settings import *

with gr.Blocks(theme=gr.themes.Soft()) as gradio_app:
    api_key_browser_state = gr.BrowserState("")
    api_key_state = gr.State("")
    chat_length_browser_state = gr.BrowserState(ChatLength.MEDIUM.value)
    # Stored as "true"/"false" string because gr.BrowserState doesn't reliably round-trip Python booleans through JSON serialization.
    show_en_translation_browser_state = gr.BrowserState("true")

    with gr.Tab("Chat"):
        api_key_input = gr.Textbox(
            show_label=False,
            placeholder="OpenAI API Key (required)",
            type="password"
        )
        gr.Markdown("The API key is stored locally in your browser.")
        start_new_chat_btn = gr.Button("✨ Start New Chat")
        chatbot = gr.Chatbot(
            type="messages",
            label=get_current_chat_language(),
            show_copy_button=True,
            placeholder="Please provide OpenAI API Key and press ✨ Start New Chat."
        )
        with gr.Row(equal_height=True):
            msg = gr.Textbox(placeholder="Type a message...", show_label=False)
            submit_btn = gr.Button("Submit", scale=0)

    with gr.Tab("Settings"):
        chat_length_radio = gr.Radio(
            [ChatLength.SHORT.value, ChatLength.MEDIUM.value, ChatLength.LONG.value],
            show_label=False,
            info="Chat length",
            value=ChatLength.MEDIUM.value
        )
        show_en_translation_checkbox = gr.Checkbox(
            label="Show English translation",
            value=True
        )
        gr.Markdown("Please start a new chat after changing any settings.")

    def restore_all(saved_key, saved_length, saved_translation):
        return saved_key, saved_key, saved_length, saved_translation == "true"

    def save_api_key(value):
        return value, value

    def save_chat_length(value):
        gr.Info("Settings updated.")
        return value

    def save_show_en_translation(value):
        gr.Info("Settings updated.")
        return "true" if value else "false"

    gradio_app.load(
        restore_all,
        inputs=[api_key_browser_state, chat_length_browser_state, show_en_translation_browser_state],
        outputs=[api_key_input, api_key_state, chat_length_radio, show_en_translation_checkbox]
    )

    api_key_input.change(save_api_key, inputs=[api_key_input], outputs=[api_key_browser_state, api_key_state])
    chat_length_radio.change(save_chat_length, inputs=[chat_length_radio], outputs=[chat_length_browser_state])
    show_en_translation_checkbox.change(save_show_en_translation, inputs=[show_en_translation_checkbox], outputs=[show_en_translation_browser_state])

    msg.submit(chat_send_user_answer, [msg, chatbot], [msg, chatbot], queue=False).then(
        chat_send_assistant_answer, [chatbot, api_key_state, chat_length_radio, show_en_translation_checkbox], chatbot
    )
    submit_btn.click(chat_send_user_answer, [msg, chatbot], [msg, chatbot], queue=False).then(
        chat_send_assistant_answer, [chatbot, api_key_state, chat_length_radio, show_en_translation_checkbox], chatbot
    )
    start_new_chat_btn.click(chat_clear_history, outputs=[chatbot], queue=False).then(
        chat_start_new, inputs=[api_key_state, show_en_translation_checkbox], outputs=[chatbot]
    )

app = FastAPI()

@app.get("/", include_in_schema=False)
def redirect_to_gradio():
    return RedirectResponse(url="/app")

app = mount_gradio_app(app, gradio_app, path="/app")
