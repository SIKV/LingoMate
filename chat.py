import gradio as gr
from openai import OpenAI
from settings import *

_model = "o4-mini"

def _build_chat_system_message(chat_language, show_en_translation):
    return f"""
    You are a friendly and patient {chat_language} language tutor. 
    Your goal is to help me practice short, natural conversations in ${chat_language}.
    
    Instructions:
        1. Start by suggesting a simple, friendly conversation topic. Be creative!
        2. Ask me one short question about this topic in {chat_language}. Keep it casual and natural.
        3. After each of my replies, ask a new short question on the same topic. Correct any mistakes I make, clearly and kindly.
        4. If my reply is off-topic, politely ignore it and ask your question again.
        { "5. After each of your messages, include the English translation in parentheses starting with 🇬🇧 and a new line." if show_en_translation else "" }
    Keep the conversation light, friendly, and supportive.
    """

def _build_feedback_system_message(chat_language, show_en_translation):
    return f"""
    You are a friendly and patient {chat_language} language tutor. 
    Your goal is to provide a helpful feedback.
    
    Instructions:
        1. Provide detailed feedback on my replies: correctness, vocabulary, sentence length, and fluency.
        2. Give me a score from 0 to 100.
        { "3. Include the English translation in parentheses starting with 🇬🇧 and a new line." if show_en_translation else "" }
    """

def _get_response(api_key, system_message, history):
    client = OpenAI(api_key=api_key)

    system = {"role": "system", "content": system_message}
    messages = []

    if history is not None:
        messages = history
    
    response = ""
 
    try:
        completion = client.chat.completions.create(model=_model, messages=[system] + messages)
        response = completion.choices[0].message.content
    except Exception as e:
        response = "Something went wrong."

    messages.append({"role": "assistant", "content": response})
    return messages

def chat_clear_history():
    return []
    
def chat_start_new():
    api_key = get_api_key()
    chat_language = get_current_chat_language()
    show_en_translation = get_show_en_translation()

    response = _get_response(
        api_key,
        _build_chat_system_message(chat_language, show_en_translation), 
         None,
    )
    
    return response

def chat_send_assistant_answer(history):
    chat_length_reached = len([msg for msg in history if msg["role"] == "user"]) >= get_chat_length_int()

    api_key = get_api_key()
    chat_language = get_current_chat_language()
    show_en_translation = get_show_en_translation()

    response = _get_response(
        api_key,
        _build_feedback_system_message(chat_language, show_en_translation) if chat_length_reached else _build_chat_system_message(chat_language, show_en_translation), 
         history
    )
    
    return response

def chat_send_user_answer(message, history):
   return "", history + [{"role": "user", "content": message}]
