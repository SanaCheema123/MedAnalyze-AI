import io
import PyPDF2
from fastapi import UploadFile, HTTPException
from config.settings import MAX_FILE_SIZE, ALLOWED_TYPES


async def validate_and_read(file: UploadFile) -> dict:
    if not file.filename:
        raise HTTPException(400, "No filename provided")
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_TYPES:
        raise HTTPException(400, f"Unsupported file type: .{ext}. Allowed: {sorted(ALLOWED_TYPES)}")
    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(400, "Uploaded file is empty")
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large. Max allowed: 10 MB")
    if ext == "pdf":
        return {"type": "text", "content": _extract_pdf(file_bytes), "filename": file.filename}
    elif ext == "txt":
        try:
            content = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            content = file_bytes.decode("latin-1", errors="replace")
        return {"type": "text", "content": content, "filename": file.filename}
    elif ext in {"png", "jpg", "jpeg"}:
        return {"type": "image", "content": file_bytes, "filename": file.filename}
    else:
        raise HTTPException(400, f"Unsupported file type: .{ext}")


def _extract_pdf(file_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip() or "No readable text found in PDF."
    except Exception as e:
        raise HTTPException(422, f"PDF parsing failed: {str(e)}")
