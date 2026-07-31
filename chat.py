from openai import OpenAI
from settings import *

def _build_chat_system_message(practice_language, translation_language):
    feedback_language = translation_language if should_translate(practice_language, translation_language) else practice_language

    translation_instruction = ""

    if should_translate(practice_language, translation_language):
        translation_instruction = f"""
        ## {get_language_flag(translation_language)}
        Your next question or topic suggestion from the section above written in {translation_language}.
        """

    return f"""
    You are a friendly and patient {practice_language} language tutor.
    Your goal is to help me practice short, natural conversations in {practice_language} while
    steadily improving my correctness, vocabulary, and fluency.

    Instructions:
        1. Start by suggesting a simple, friendly conversation topic. Be creative!
        2. Ask me one short question about this topic in {practice_language}. Keep it casual and natural.
        3. After each of my replies, first give brief feedback on what I just wrote: point out any
           mistakes in grammar, vocabulary, or sentence structure and show the corrected version. If my
           reply was correct, briefly say so and, when relevant, suggest a more natural or advanced way
           to phrase it.
        4. Then continue the conversation with a new short question on the same topic.
        5. If my reply is off-topic, politely ignore it and ask your question again.
    
    Keep the conversation light, friendly, and supportive.

    Formatting template (Markdown):

    ## ℹ️
    (Skip this section if it's your first message). 
    Your feedback followed by the correction (or confirmation). Write feedback in {feedback_language}.
    
    ## {get_language_flag(practice_language)}
    Your next question or topic suggestion.

    {translation_instruction}
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

def chat_send_assistant_answer(history, api_key, model, practice_language, translation_language):
    return _get_response(
        api_key,
        model,
        _build_chat_system_message(practice_language, translation_language),
        history
    )

def chat_send_user_answer(message, history):
    return "", history + [{"role": "user", "content": message}]
