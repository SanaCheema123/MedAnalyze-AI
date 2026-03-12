import os
from dotenv import load_dotenv

load_dotenv()

# ── Gemini ────────────────────────────────────────────────────────────────────
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL    = "gemini-1.5-flash"

# ── Server ────────────────────────────────────────────────────────────────────
API_HOST        = os.getenv("API_HOST", "0.0.0.0")
API_PORT        = int(os.getenv("API_PORT", 8000))
SECRET_KEY      = os.getenv("SECRET_KEY", "change-me")
APP_ENV         = os.getenv("APP_ENV", "development")

# ── File limits ───────────────────────────────────────────────────────────────
MAX_FILE_SIZE   = int(os.getenv("MAX_FILE_SIZE_MB", 10)) * 1024 * 1024
ALLOWED_TYPES   = {"pdf", "txt", "png", "jpg", "jpeg"}

# ── Storage ───────────────────────────────────────────────────────────────────
DATA_DIR        = "data"
HISTORY_FILE    = f"{DATA_DIR}/history.json"
UPLOADS_DIR     = f"{DATA_DIR}/uploads"

# ── Gemini Prompts ────────────────────────────────────────────────────────────
ANALYSIS_SYSTEM_PROMPT = """
You are MedAnalyze AI, an expert medical report analysis assistant.

Analyze the provided medical report and respond with this EXACT JSON structure:
{
  "summary": "2-3 sentence overview of the report",
  "key_findings": ["finding 1", "finding 2", "finding 3"],
  "abnormal_values": [
    {"name": "value name", "result": "patient result", "normal_range": "normal range", "severity": "low|medium|high"}
  ],
  "what_it_means": "plain English explanation for the patient",
  "next_steps": ["step 1", "step 2", "step 3"],
  "urgency_level": "routine|soon|urgent|emergency",
  "specialist_referral": "type of specialist if needed, or null",
  "disclaimer": "This analysis is for informational purposes only. Always consult a qualified healthcare professional."
}

Return ONLY valid JSON. No markdown, no extra text.
"""

CHAT_SYSTEM_PROMPT = """
You are MedAnalyze AI, a helpful medical assistant.
You have access to the patient's analyzed report.
Answer questions clearly, in plain English.
Always recommend consulting a doctor for personalized advice.
Keep responses concise and friendly.
"""
