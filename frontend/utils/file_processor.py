import io
import PyPDF2
import streamlit as st
from config.settings import MAX_FILE_SIZE, ALLOWED_TYPES


def validate_file(uploaded_file) -> bool:
    ext = uploaded_file.name.split(".")[-1].lower()
    if ext not in ALLOWED_TYPES:
        st.error(f"❌ Unsupported file type: .{ext}. Allowed: {', '.join(ALLOWED_TYPES)}")
        return False
    try:
        size = len(uploaded_file.getvalue())
    except Exception:
        size = uploaded_file.size
    if size > MAX_FILE_SIZE:
        st.error("❌ File too large. Max allowed size is 10 MB.")
        return False
    return True


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip() if text.strip() else "⚠️ No readable text found in PDF."
    except Exception as e:
        return f"❌ PDF parsing error: {str(e)}"


def extract_text_from_txt(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1", errors="replace")


def process_uploaded_file(uploaded_file) -> dict:
    try:
        file_bytes = uploaded_file.getvalue()
    except Exception:
        file_bytes = uploaded_file.read()

    ext = uploaded_file.name.split(".")[-1].lower()

    if ext == "pdf":
        return {
            "type": "text",
            "content": extract_text_from_pdf(file_bytes),
            "filename": uploaded_file.name,
        }
    elif ext == "txt":
        return {
            "type": "text",
            "content": extract_text_from_txt(file_bytes),
            "filename": uploaded_file.name,
        }
    elif ext in ["png", "jpg", "jpeg"]:
        mime_map = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}
        return {
            "type": "image",
            "content": file_bytes,
            "mime_type": mime_map[ext],
            "filename": uploaded_file.name,
        }
    else:
        return {"type": "error", "content": f"Unsupported file type: .{ext}"}
