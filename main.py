import io
import os
import re
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import docx

app = FastAPI(title="EduAcessível API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extrair_texto_bytes(filename: str, content: bytes) -> str:
    nome = filename.lower()
    if nome.endswith(".pdf"):
        texto = []
        with fitz.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                texto.append(page.get_text())
        return "\n".join(texto).strip()
    elif nome.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()]).strip()
    elif nome.endswith(".txt"):
        return content.decode("utf-8", errors="ignore").strip()
    else:
        raise HTTPException(status_code=400, detail="Formato não suportado. Envie PDF, DOCX ou TXT.")


def adaptar_para_surdos_l2(texto: str) -> str:
    """
    Adapta o material didático para alunos surdos (Português como L2 / estrutura visual):
    - Quebra blocos longos em frases curtas e diretas.
    - Organiza seções com marcadores visuais.
    - Extrai termos complexos para um Glossário Visual de apoio em Libras.
    """
    linhas = [l.strip() for l in texto.split("\n") if l.strip()]
    blocos_adaptados = []
    palavras_chave = set()

    for linha in linhas:
        if len(linha) < 75 and (linha.isupper() or linha.endswith(":") or linha[0].isdigit()):
            blocos_adaptados.append(f"\n📌 {linha.upper()}")
            continue

        frases = re.split(r'(?<=[.!?])\s+', linha)
        for frase in frases:
            if not frase:
                continue
            for palavra in re.findall(r'\b[A-Za-zÀ-ÿ]{9,}\b', frase):
                palavras_chave.add(palavra.lower())
            blocos_adaptados.append(f"• {frase}")

    glossario = ""
    if palavras_chave:
        termos = sorted(list(palavras_chave))[:12]
        glossario = (
            "\n\n📖 GLOSSÁRIO VISUAL (TERMOS PARA APOIO EM LIBRAS):\n"
            + "\n".join([f"🔹 {t.upper()}: [Consultar sinal em Libras / apoio visual]" for t in termos])
        )

    cabecalho = (
        "🤟 MATERIAL ADAPTADO — EDUACESSÍVEL (PORTUGUÊS L2 / VISUAL)\n"
        "Estrutura: Tópicos curtos, linguagem direta e vocabulário destacado.\n"
        + "=" * 60 + "\n"
    )
    return cabecalho + "\n".join(blocos_adaptados) + glossario


@app.get("/")
def root():
    return {"status": "online", "projeto": "EduAcessível"}


@app.post("/file/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    texto = extrair_texto_bytes(file.filename, content)
    return {
        "filename": file.filename,
        "char_count": len(texto),
        "extracted_text": texto,
    }


@app.post("/file/adaptar")
async def adaptar_material(file: UploadFile = File(...)):
    content = await file.read()
    texto_original = extrair_texto_bytes(file.filename, content)
    if not texto_original:
        raise HTTPException(status_code=400, detail="O arquivo está vazio ou não possui texto legível.")

    # Se houver chave GEMINI_API_KEY configurada no ambiente, usa LLM; caso contrário, usa o adaptador local
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    texto_adaptado = ""

    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = (
                "Você é especialista em Educação Bilíngue de Surdos (Libras L1 / Português L2). "
                "Adapte o material escolar abaixo para alunos surdos do Ensino Fundamental usando frases curtas "
                "na ordem direta (Sujeito + Verbo + Complemento), tópicos visuais com emojis e um Glossário Visual "
                "simples ao final.\n\nMATERIAL:\n" + texto_original
            )
            resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            texto_adaptado = resp.text
        except Exception:
            texto_adaptado = adaptar_para_surdos_l2(texto_original)
    else:
        texto_adaptado = adaptar_para_surdos_l2(texto_original)

    return {
        "filename": file.filename,
        "char_count_original": len(texto_original),
        "char_count_adapted": len(texto_adaptado),
        "original_text": texto_original,
        "adapted_text": texto_adaptado,
    }
