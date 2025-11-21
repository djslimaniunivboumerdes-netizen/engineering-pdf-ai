import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.datastructures import UploadFile as StarletteUploadFile
from typing import List
import tempfile
from pdf2image import convert_from_path
import pytesseract
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

STORAGE_ROOT = os.environ.get('STORAGE_ROOT', './storage')
CHROMA_DIR = os.environ.get('CHROMA_DIR', './storage/chroma')

os.makedirs(STORAGE_ROOT, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# Load embedding model (MiniLM)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Initialize chroma client (filesystem)
chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=CHROMA_DIR))
# create a global collection name; in production you will create per-user collections
try:
    collection = chroma_client.create_collection(name='documents')
except Exception:
    collection = chroma_client.get_collection(name='documents')

def ocr_pdf_bytes(file_path):
    pages = convert_from_path(file_path)
    texts = []
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        texts.append((i+1, text))
    return texts

@app.post('/upload')
async def upload(pdfs: List[UploadFile] = File(...)):
    saved = []
    for pdf in pdfs:
        uid = str(uuid.uuid4())
        dest = os.path.join(STORAGE_ROOT, uid + '_' + pdf.filename)
        with open(dest, 'wb') as f:
            shutil.copyfileobj(pdf.file, f)
        # OCR and embeddings (synchronous; for large files use background tasks)
        texts = ocr_pdf_bytes(dest)
        for page, text in texts:
            chunks = [c.strip() for c in text.split('\n') if len(c.strip())>10]
            for chunk in chunks:
                emb = model.encode(chunk).tolist()
                collection.add(documents=[chunk], embeddings=[emb], metadatas=[{'page': page, 'source': pdf.filename}])
        saved.append({'filename': pdf.filename, 'id': uid})
    # persist chroma to disk
    chroma_client.persist()
    return JSONResponse({'detail':'uploaded', 'files': saved})

@app.get('/search')
async def search(q: str):
    emb = model.encode(q).tolist()
    results = collection.query(query_embeddings=[emb], n_results=10, include=['documents','metadatas','distances'])
    out = []
    for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        out.append({'text': doc, 'page': meta.get('page'), 'source': meta.get('source'), 'score': float(dist)})
    return JSONResponse({'results': out})
