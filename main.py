import io
import fitz  # PyMuPDF
from docx import Document
from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI(title="Módulo de Upload e Extração de Texto")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "\n".join(page.get_text() for page in doc).strip()

def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

@app.post("/file/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    ext = filename.split(".")[-1].lower() if "." in filename else ""

    if ext not in {"pdf", "docx", "doc", "txt"}:
        raise HTTPException(
            status_code=400,
            detail="Formato não suportado. Envie um ficheiro PDF, DOCX ou TXT.",
        )

    file_bytes = await file.read()

    if ext == "pdf":
        extracted_text = extract_text_from_pdf(file_bytes)
    elif ext in ["docx", "doc"]:
        extracted_text = extract_text_from_docx(file_bytes)
    else:
        extracted_text = file_bytes.decode("utf-8")

    return {
        "filename": filename,
        "char_count": len(extracted_text),
        "extracted_text": extracted_text,
    }
