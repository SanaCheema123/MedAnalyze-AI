import json
import io
import time
from google import genai
import PIL.Image

from config.settings import GEMINI_API_KEY, GEMINI_MODEL, ANALYSIS_SYSTEM_PROMPT, CHAT_SYSTEM_PROMPT
from api.models.schemas import AnalysisResult, AbnormalValue


def _get_client():
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise ValueError("Gemini API key not configured. Set GEMINI_API_KEY in .env")
    return genai.Client(api_key=GEMINI_API_KEY)


def _call_with_retry(client, contents, retries=3):
    for attempt in range(retries):
        try:
            return client.models.generate_content(model=GEMINI_MODEL, contents=contents)
        except Exception as e:
            err = str(e)
            if ("429" in err or "RESOURCE_EXHAUSTED" in err) and attempt < retries - 1:
                time.sleep(65)
            else:
                raise e


def _clean_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def analyze_report_text(report_text: str, extra_context: str = "") -> AnalysisResult:
    client = _get_client()
    content = report_text
    if extra_context:
        content += f"\n\nADDITIONAL PATIENT CONTEXT:\n{extra_context}"
    prompt = f"{ANALYSIS_SYSTEM_PROMPT}\n\nMEDICAL REPORT:\n{content}"
    try:
        response = _call_with_retry(client, prompt)
        return _parse_analysis(_clean_json(response.text))
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini returned invalid JSON: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Analysis failed: {str(e)}")


def analyze_report_image(image_bytes: bytes, extra_context: str = "") -> AnalysisResult:
    client = _get_client()
    try:
        image = PIL.Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        raise ValueError(f"Could not open image: {str(e)}")
    prompt = ANALYSIS_SYSTEM_PROMPT
    if extra_context:
        prompt += f"\n\nADDITIONAL PATIENT CONTEXT:\n{extra_context}"
    try:
        response = _call_with_retry(client, [prompt, image])
        return _parse_analysis(_clean_json(response.text))
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini returned invalid JSON: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Image analysis failed: {str(e)}")


def chat_response(user_message: str, analysis_context: str, chat_history: list) -> str:
    client = _get_client()
    history_text = "\n".join([
        f"{m['role'].upper()}: {m['content']}"
        for m in chat_history[-10:]
    ])
    prompt = (
        f"{CHAT_SYSTEM_PROMPT}\n\n"
        f"REPORT ANALYSIS CONTEXT:\n{analysis_context or 'No report analyzed yet.'}\n\n"
        f"CONVERSATION HISTORY:\n{history_text}\n\n"
        f"USER: {user_message}\n\nPlease respond helpfully and concisely."
    )
    try:
        response = _call_with_retry(client, prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Chat failed: {str(e)}")


def _parse_analysis(data: dict) -> AnalysisResult:
    abnormal = [
        AbnormalValue(
            name=v.get("name", ""),
            result=v.get("result", ""),
            normal_range=v.get("normal_range", ""),
            severity=v.get("severity", "low"),
        )
        for v in data.get("abnormal_values", [])
    ]
    return AnalysisResult(
        summary=data.get("summary", ""),
        key_findings=data.get("key_findings", []),
        abnormal_values=abnormal,
        what_it_means=data.get("what_it_means", ""),
        next_steps=data.get("next_steps", []),
        urgency_level=data.get("urgency_level", "routine"),
        specialist_referral=data.get("specialist_referral"),
        disclaimer=data.get("disclaimer", "Always consult a qualified healthcare professional."),
    )
