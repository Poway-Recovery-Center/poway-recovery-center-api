""" Support assistant API: forwards the site chatbot conversation to Google Gemini, with xAI Grok as a backup.

The keys live only in .env (GEMINI_API_KEY, XAI_API_KEY) so they are never exposed in the GitHub Pages frontend.
"""
import json
import urllib.error
import urllib.request

from flask import Blueprint, request, current_app
from flask_restful import Api, Resource


chat_api = Blueprint('chat_api', __name__, url_prefix='/api')
api = Api(chat_api)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
XAI_URL = "https://api.x.ai/v1/chat/completions"
MAX_MESSAGES = 20
MAX_MESSAGE_CHARS = 1000

SYSTEM_PROMPT = """You are the support assistant on the Poway Recovery Center website, a compassionate,
trauma-informed peer recovery and mental-health community in Poway, California.

- Be warm, calm, non-judgmental, and brief (2-5 short sentences). Write plain text, no markdown.
- Offer practical grounding, coping, and next-step ideas, and point people to the site's pages when helpful:
  Resources (Mood Room, reflection wall, resource directory), Programs (community meetings, wellness
  workshops, care connections, meeting schedule), and About Us.
- You are not a therapist, doctor, or crisis service. Do not diagnose, and do not give medication or dosing
  advice; encourage contacting a medical professional for medical concerns such as severe withdrawal.
- If someone mentions suicide, self-harm, overdose, being in danger, or harming others, respond with care and
  clearly encourage them to call or text 988 (Suicide & Crisis Lifeline) right now, or call 911 if they are in
  immediate danger.
"""

CRISIS_REPLY = ("I want to make sure you get the right support. If you are thinking about harming yourself "
                "or are in crisis, please call or text 988 now, or call 911 if you are in immediate danger.")


class ProviderError(Exception):
    """ An AI provider could not answer; the message is safe to show the user """


def _post_json(url, payload, headers):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json", **headers},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        detail = error.read().decode('utf-8', 'replace')
        raise ProviderError(f"error {error.code}: {detail}")
    except (urllib.error.URLError, TimeoutError) as error:
        raise ProviderError(f"unreachable: {error}")


def ask_gemini(contents):
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": contents,
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 400},
    }
    url = GEMINI_URL.format(model=current_app.config['GEMINI_MODEL'])
    data = _post_json(url, payload, {"x-goog-api-key": current_app.config['GEMINI_API_KEY']})
    candidates = data.get('candidates') or []
    parts = (candidates[0].get('content') or {}).get('parts', []) if candidates else []
    # Empty when Gemini's safety filters block the reply; still point the person to real help
    return ''.join(part.get('text', '') for part in parts).strip() or CRISIS_REPLY


def ask_grok(contents):
    # Grok uses the OpenAI chat format: Gemini's "model" role is "assistant"
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for content in contents:
        role = 'assistant' if content["role"] == 'model' else 'user'
        messages.append({"role": role, "content": content["parts"][0]["text"]})
    payload = {
        "model": current_app.config['XAI_MODEL'],
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 400,
    }
    data = _post_json(XAI_URL, payload, {"Authorization": f"Bearer {current_app.config['XAI_API_KEY']}"})
    choices = data.get('choices') or []
    reply = ((choices[0].get('message') or {}).get('content') or '') if choices else ''
    return reply.strip() or CRISIS_REPLY


class _Chat(Resource):
    def post(self):
        # Gemini first, Grok as the backup; keys live only in the backend .env
        providers = [(name, ask) for name, ask, key in (
            ('Gemini', ask_gemini, 'GEMINI_API_KEY'),
            ('Grok', ask_grok, 'XAI_API_KEY'),
        ) if current_app.config[key]]
        if not providers:
            return {"message": "The support assistant is not configured: set GEMINI_API_KEY or XAI_API_KEY in .env"}, 503

        body = request.get_json(silent=True) or {}
        messages = body.get('messages')
        if not isinstance(messages, list) or not messages:
            return {"message": "messages must be a non-empty list"}, 400

        contents = []
        for message in messages[-MAX_MESSAGES:]:
            if not isinstance(message, dict):
                return {"message": "Each message needs a role and text"}, 400
            role = 'model' if message.get('role') == 'model' else 'user'
            text = str(message.get('text') or '').strip()[:MAX_MESSAGE_CHARS]
            if text:
                contents.append({"role": role, "parts": [{"text": text}]})
        # Gemini expects the conversation to start with the user
        while contents and contents[0]["role"] != 'user':
            contents.pop(0)
        if not contents:
            return {"message": "messages must include text from the user"}, 400

        for name, ask in providers:
            try:
                return {"reply": ask(contents)}
            except ProviderError as error:
                current_app.logger.error(f"{name} {error}")
        return {"message": "The support assistant is unavailable right now. Please try again soon."}, 502


api.add_resource(_Chat, '/chat')
