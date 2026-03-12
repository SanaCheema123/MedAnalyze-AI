from fastapi import APIRouter, HTTPException
from api.models.schemas import HistoryListResponse, HistoryDetailResponse
from api.services import history_service

router = APIRouter()


@router.get("/history", response_model=HistoryListResponse)
def get_history():
    records = history_service.get_all()
    summaries = []
    for r in records:
        raw = r["analysis"].get("summary", "")
        summaries.append({
            "id": r["id"],
            "filename": r["filename"],
            "summary": raw[:120] + ("..." if len(raw) > 120 else ""),
            "urgency_level": r["analysis"].get("urgency_level", "routine"),
            "timestamp": r["timestamp"],
        })
    return HistoryListResponse(success=True, total=len(summaries), records=summaries)


@router.get("/history/{record_id}", response_model=HistoryDetailResponse)
def get_record(record_id: int):
    record = history_service.get_by_id(record_id)
    if not record:
        raise HTTPException(404, f"Record {record_id} not found")
    return HistoryDetailResponse(success=True, record=record)


@router.delete("/history")
def clear_all():
    history_service.delete_all()
    return {"success": True, "message": "All history cleared"}


@router.delete("/history/{record_id}")
def delete_record(record_id: int):
    if not history_service.delete_by_id(record_id):
        raise HTTPException(404, f"Record {record_id} not found")
    return {"success": True, "message": f"Record {record_id} deleted"}
