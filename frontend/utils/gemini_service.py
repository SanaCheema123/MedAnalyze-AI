import time
import io
import base64
import requests
import streamlit as st
import PIL.Image

from config.settings import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT, CHAT_SYSTEM_PROMPT

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _call_openrouter(messages, retries=3):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "MedAnalyze AI"
    }
    payload = {
        "model": GEMINI_MODEL,
        "messages": messages
    }
    for attempt in range(retries):
        try:
            r = requests.post(OPENROUTER_URL, headers=headers,
                              json=payload, timeout=60)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            if r.status_code == 429 and attempt < retries - 1:
                wait = 30
                st.warning(f"⏳ Rate limit hit. Waiting {wait}s... (attempt {attempt + 1}/{retries})")
                time.sleep(wait)
            elif r.status_code == 404:
                raise Exception(f"Model not found: {GEMINI_MODEL}")
            else:
                raise e
        except Exception as e:
            if attempt < retries - 1:
                st.warning(f"⏳ Retrying... (attempt {attempt + 1}/{retries})")
                time.sleep(30)
            else:
                raise e


def analyze_medical_report(report_text: str, file_type: str = "text") -> str:
    messages = [{
        "role": "user",
        "content": f"{SYSTEM_PROMPT}\n\n---\nMEDICAL REPORT:\n{report_text}\n---\n\nPlease analyze."
    }]
    try:
        return _call_openrouter(messages)
    except Exception as e:
        return f"❌ Analysis failed: {str(e)}"


def analyze_medical_image(image_bytes: bytes, mime_type: str) -> str:
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": f"{SYSTEM_PROMPT}\n\nAnalyze this medical report image."},
            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_b64}"}}
        ]
    }]
    try:
        return _call_openrouter(messages)
    except Exception as e:
        return f"❌ Image analysis failed: {str(e)}"


def chat_with_ai(user_message: str, analysis_context: str, chat_history: list) -> str:
    history_text = "\n".join([
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in chat_history[-10:]
    ])
    messages = [{
        "role": "user",
        "content": (
            f"{CHAT_SYSTEM_PROMPT}\n\n"
            f"REPORT CONTEXT:\n{analysis_context or 'No report yet.'}\n\n"
            f"HISTORY:\n{history_text}\n\n"
            f"USER: {user_message}"
        )
    }]
    try:
        return _call_openrouter(messages)
    except Exception as e:
        return f"❌ Chat error: {str(e)}"