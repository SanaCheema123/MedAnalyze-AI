from pydantic import BaseModel, Field
from typing import Optional, List


class AbnormalValue(BaseModel):
    name: str
    result: str
    normal_range: str
    severity: str


class AnalysisResult(BaseModel):
    summary: str
    key_findings: List[str]
    abnormal_values: List[AbnormalValue]
    what_it_means: str
    next_steps: List[str]
    urgency_level: str
    specialist_referral: Optional[str] = None
    disclaimer: str


class AnalysisResponse(BaseModel):
    success: bool
    filename: str
    analysis: AnalysisResult
    analysis_id: int
    timestamp: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    user_message: str = Field(..., min_length=1, max_length=2000)
    analysis_context: Optional[str] = None
    chat_history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    success: bool
    response: str
    timestamp: str


class HistoryRecord(BaseModel):
    id: int
    filename: str
    summary: str
    urgency_level: str
    timestamp: str


class HistoryListResponse(BaseModel):
    success: bool
    total: int
    records: List[HistoryRecord]


class HistoryDetailResponse(BaseModel):
    success: bool
    record: dict


class HealthResponse(BaseModel):
    status: str
    version: str
    gemini_connected: bool
    environment: str
