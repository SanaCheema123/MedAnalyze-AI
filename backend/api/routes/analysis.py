from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime
from api.models.schemas import AnalysisResponse
from api.services.file_service import validate_and_read
from api.services.gemini_service import analyze_report_text, analyze_report_image
from api.services.history_service import save_record

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse, summary="Analyze Medical Report")
async def analyze_report(
    file: UploadFile = File(...),
    extra_context: str = Form(""),
):
    file_data = await validate_and_read(file)
    try:
        if file_data["type"] == "text":
            analysis = analyze_report_text(file_data["content"], extra_context)
        else:
            analysis = analyze_report_image(file_data["content"], extra_context)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except RuntimeError as e:
        raise HTTPException(500, str(e))
    except Exception as e:
        raise HTTPException(500, f"Unexpected error: {str(e)}")

    analysis_dict = analysis.model_dump()
    record_id = save_record(file_data["filename"], analysis_dict)

    return AnalysisResponse(
        success=True,
        filename=file_data["filename"],
        analysis=analysis,
        analysis_id=record_id,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
