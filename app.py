from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import gradio as gr
from gradio.routes import mount_gradio_app
from chat import *
from settings import *

_JS_SAVE_API_KEY = "(key) => { localStorage.setItem('lingomate_api_key', key); return [key]; }"
_JS_LOAD_API_KEY = "() => [localStorage.getItem('lingomate_api_key') || '']"

# Chat interface.
with gr.Blocks() as chat_app:
    def update_api_key_state(value):
        state = value
        set_api_key(value)
        return state

    api_key_input = gr.Textbox(
        show_label=False, 
        placeholder="OpenAI API Key (required)",
        type="password",
        value=get_api_key()
    )
    api_key_input.change(fn=update_api_key_state, inputs=api_key_input, outputs=None, js=_JS_SAVE_API_KEY)
    
    start_new_chat_btn = gr.Button("✨ Start New Chat")

    chatbot = gr.Chatbot(
        type="messages",
        label=get_current_chat_language(),
        show_copy_button=True,
        placeholder="Please provide OpenAI API Key and press ✨ Start New Chat."
    )
    
    with gr.Row(equal_height=True):
        msg = gr.Textbox(
            placeholder="Type a message...",
            show_label=False
        )
        submit_btn = gr.Button("Submit", scale=0)

    msg.submit(chat_send_user_answer, [msg, chatbot], [msg, chatbot], queue=False).then(
        chat_send_assistant_answer, chatbot, chatbot
    )

    submit_btn.click(chat_send_user_answer, [msg, chatbot], [msg, chatbot], queue=False).then(
        chat_send_assistant_answer, chatbot, chatbot
    )
    
    start_new_chat_btn.click(chat_clear_history, outputs=[chatbot], queue=False).then(
        chat_start_new, outputs=[chatbot]
    )
    
# Settings interface.
with gr.Blocks() as settings_app:
    def update_chat_length_state(choice, state):
        state = choice
        set_chat_length(choice)
        return state
    
    def update_show_en_translation_state(value, state):
        state = value
        set_show_en_translation(value)
        return state
        
    with gr.Blocks() as demo:
        chat_length_state = gr.State()
        show_en_translation_state = gr.State()
        
        with gr.Row():
            with gr.Column():
                chat_length_radio = gr.Radio(
                    [ChatLength.SHORT.value, ChatLength.MEDIUM.value, ChatLength.LONG.value],
                    show_label=False, 
                    info="Chat length",
                    value=get_chat_length()
                )
            with gr.Column():
                show_en_translation_checkbox = gr.Checkbox(
                    label="Show English translation",
                    value=get_show_en_translation()
                )

        gr.Markdown("Please start a new chat after changing any settings.")
        
        chat_length_radio.change(
            update_chat_length_state, 
            [chat_length_radio, chat_length_state], 
            chat_length_state
        )
        show_en_translation_checkbox.change(
            update_show_en_translation_state, 
            [show_en_translation_checkbox, show_en_translation_state],
            show_en_translation_state
        )

# Tabs for navigation.
with gr.Blocks(theme=gr.themes.Soft()) as gradio_app:
    with gr.Tab("Chat"):
        chat_app.render()
    with gr.Tab("Settings"):
        settings_app.render()

    def restore_api_key(stored_key):
        if stored_key:
            set_api_key(stored_key)
            return stored_key
        return gr.update()

    gradio_app.load(
        fn=restore_api_key,
        outputs=[api_key_input],
        js=_JS_LOAD_API_KEY
    )

# FastAPI app
app = FastAPI()

# Redirect from "/" to "/app"
@app.get("/", include_in_schema=False)
def redirect_to_gradio():
    return RedirectResponse(url="/app")

app = mount_gradio_app(app, gradio_app, path="/app")
