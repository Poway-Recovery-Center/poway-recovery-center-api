""" Support assistant API: forwards the site chatbot conversation to Google Gemini, with Groq as a backup.

The keys live only in .env (GEMINI_API_KEY, GROQ_API_KEY) so they are never exposed in the GitHub Pages frontend.
"""
import json
import urllib.error
import urllib.request

from flask import Blueprint, request, current_app
from flask_restful import Api, Resource


chat_api = Blueprint('chat_api', __name__, url_prefix='/api')
api = Api(chat_api)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MAX_MESSAGES = 20
MAX_MESSAGE_CHARS = 1000
# Both models "think" before answering and that reasoning counts against this cap, so it must leave
# plenty of room for the reply itself; the system prompt is what keeps replies short
MAX_OUTPUT_TOKENS = 2048

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


def _post_json(url, payload, headers, timeout=30):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        # Groq's Cloudflare front rejects urllib's default User-Agent (error 1010)
        headers={"Content-Type": "application/json", "User-Agent": "poway-recovery-center-api/1.0", **headers},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
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
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": MAX_OUTPUT_TOKENS,
            "thinkingConfig": {"thinkingLevel": "low"},
        },
    }
    url = GEMINI_URL.format(model=current_app.config['GEMINI_MODEL'])
    # Short timeout so an overloaded Gemini hands off to Groq quickly
    data = _post_json(url, payload, {"x-goog-api-key": current_app.config['GEMINI_API_KEY']}, timeout=15)
    candidates = data.get('candidates') or []
    if not candidates:
        # No candidates means the prompt itself was blocked by Gemini's safety filters; still point the person to real help
        return CRISIS_REPLY
    finish = candidates[0].get('finishReason')
    if finish in ('SAFETY', 'PROHIBITED_CONTENT', 'BLOCKLIST'):
        return CRISIS_REPLY
    parts = (candidates[0].get('content') or {}).get('parts', [])
    reply = ''.join(part.get('text', '') for part in parts if not part.get('thought')).strip()
    if finish == 'MAX_TOKENS' or not reply:
        # A cut-off or empty reply would read as broken; let Groq answer instead
        raise ProviderError(f"incomplete reply (finishReason {finish})")
    return reply


def ask_groq(contents):
    # Groq uses the OpenAI chat format: Gemini's "model" role is "assistant"
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for content in contents:
        role = 'assistant' if content["role"] == 'model' else 'user'
        messages.append({"role": role, "content": content["parts"][0]["text"]})
    payload = {
        "model": current_app.config['GROQ_MODEL'],
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": MAX_OUTPUT_TOKENS,
    }
    data = _post_json(GROQ_URL, payload, {"Authorization": f"Bearer {current_app.config['GROQ_API_KEY']}"})
    choices = data.get('choices') or []
    if not choices:
        raise ProviderError("no reply")
    if choices[0].get('finish_reason') == 'content_filter':
        return CRISIS_REPLY
    reply = ((choices[0].get('message') or {}).get('content') or '').strip()
    if choices[0].get('finish_reason') == 'length' or not reply:
        raise ProviderError(f"incomplete reply (finish_reason {choices[0].get('finish_reason')})")
    return reply


class _Chat(Resource):
    def post(self):
        # Gemini first, Groq as the backup; keys live only in the backend .env
        providers = [(name, ask) for name, ask, key in (
            ('Gemini', ask_gemini, 'GEMINI_API_KEY'),
            ('Groq', ask_groq, 'GROQ_API_KEY'),
        ) if current_app.config[key]]
        if not providers:
            return {"message": "The support assistant is not configured: set GEMINI_API_KEY or GROQ_API_KEY in .env"}, 503

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
