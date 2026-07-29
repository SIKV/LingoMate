from openai import OpenAI
from settings import *

def _build_chat_system_message(practice_language, translation_language):
    translation_instruction = ""
    if should_translate(practice_language, translation_language):
        translation_instruction = (
            f"5. After each of your messages, include the {translation_language} translation "
            f"in parentheses starting with {get_language_flag(translation_language)} and a new line."
        )

    return f"""
    You are a friendly and patient {practice_language} language tutor.
    Your goal is to help me practice short, natural conversations in {practice_language}.

    Instructions:
        1. Start by suggesting a simple, friendly conversation topic. Be creative!
        2. Ask me one short question about this topic in {practice_language}. Keep it casual and natural.
        3. After each of my replies, ask a new short question on the same topic. Correct any mistakes I make, clearly and kindly.
        4. If my reply is off-topic, politely ignore it and ask your question again.
        { translation_instruction }
    Keep the conversation light, friendly, and supportive.
    """

def _build_feedback_system_message(practice_language, translation_language):
    translation_instruction = ""
    if should_translate(practice_language, translation_language):
        translation_instruction = (
            f"3. Include the {translation_language} translation in parentheses "
            f"starting with {get_language_flag(translation_language)} and a new line."
        )

    return f"""
    You are a friendly and patient {practice_language} language tutor.
    Your goal is to provide a helpful feedback.

    Instructions:
        1. Provide detailed feedback on my replies: correctness, vocabulary, sentence length, and fluency.
        2. Give me a score from 0 to 100.
        { translation_instruction }
    """

def _get_response(api_key, model, system_message, history):
    client = OpenAI(api_key=api_key)

    system = {"role": "system", "content": system_message}
    messages = []

    if history is not None:
        messages = history

    response = ""

    if not api_key:
        response = "Please provide OpenAI API key."
    else:
        try:
            completion = client.chat.completions.create(model=model, messages=[system] + messages)
            response = completion.choices[0].message.content
        except Exception as e:
            status_code = getattr(e, "status_code", None)
            if status_code == 401:
                response = "Invalid OpenAI API key."
            else:
                response = "Something went wrong."

    messages.append({"role": "assistant", "content": response})
    return messages

def chat_clear_history():
    return []

def chat_start_new(api_key, model, practice_language, translation_language):
    return _get_response(
        api_key,
        model,
        _build_chat_system_message(practice_language, translation_language),
        None,
    )

def chat_send_assistant_answer(history, api_key, model, chat_length_value, practice_language, translation_language):
    chat_length_reached = len([msg for msg in history if msg["role"] == "user"]) >= ChatLength(chat_length_value).to_int()
    return _get_response(
        api_key,
        model,
        _build_feedback_system_message(practice_language, translation_language) if chat_length_reached else _build_chat_system_message(practice_language, translation_language),
        history
    )

def chat_send_user_answer(message, history):
    return "", history + [{"role": "user", "content": message}]
