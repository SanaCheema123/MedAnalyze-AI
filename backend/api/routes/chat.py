from fastapi import APIRouter, HTTPException
from datetime import datetime
from api.models.schemas import ChatRequest, ChatResponse
from api.services.gemini_service import chat_response

router = APIRouter()


@router.post("/chat", response_model=ChatResponse, summary="Chat About Medical Report")
async def chat(request: ChatRequest):
    try:
        history_dicts = [m.model_dump() for m in request.chat_history]
        response_text = chat_response(
            user_message=request.user_message,
            analysis_context=request.analysis_context or "",
            chat_history=history_dicts,
        )
    except ValueError as e:
        raise HTTPException(503, str(e))
    except RuntimeError as e:
        raise HTTPException(500, str(e))
    except Exception as e:
        raise HTTPException(500, f"Unexpected error: {str(e)}")

    return ChatResponse(
        success=True,
        response=response_text,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
