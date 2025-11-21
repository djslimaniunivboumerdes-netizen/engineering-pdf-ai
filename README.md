# Engineering AI P&ID / PDF Search - Starter (Free-tier)

This repository is a minimal starter for the **AI P&ID / PDF Engineering Search Engine**:
- Frontend: Next.js (simple upload + search UI)
- Backend: FastAPI (handles multi-PDF upload, OCR with Tesseract, embeddings with SentenceTransformers, ChromaDB)
- Storage/Auth: Supabase (instructions provided); currently files are stored locally for prototyping.

## What this starter includes
- `frontend/` - Next.js app (pages/api proxy to backend)
- `backend/` - FastAPI app (`app.py`)
- `requirements.txt` - backend Python dependencies
- `package.json` - frontend dependencies
- `.env.example` - environment variable examples
- `README` with quick setup steps

## Quick local setup (prototype)
### Prereqs
- Python 3.10+
- Node.js 18+
- Tesseract OCR installed on your system (OS-specific)
    - Ubuntu/Debian: `sudo apt install tesseract-ocr poppler-utils`
    - macOS (homebrew): `brew install tesseract poppler`
- (Optional) Create a Supabase project and set credentials if you want remote storage/auth.

### Backend (local)
1. cd backend
2. python -m venv .venv && source .venv/bin/activate
3. pip install -r requirements.txt
4. Copy `.env.example` to `.env` and edit if needed.
5. Run: `uvicorn app:app --reload --port 8000`

### Frontend (local)
1. cd frontend
2. npm install
3. npm run dev
4. Open http://localhost:3000

### Notes
- For production, you should replace local storage with Supabase storage and secure authentication.
- This starter uses MiniLM embeddings and ChromaDB saved per-user in `backend/storage/`.
- The frontend currently uses a simple file-upload form and search box.

## Next steps (recommended)
- Integrate Supabase Auth & Storage (see Supabase docs)
- Add user project/folder management in backend and frontend
- Add rate limits, usage accounting, and Stripe billing for paid plans
- Add background worker (Celery/RQ) for OCR/embedding jobs for larger files

Enjoy — modify and expand for your needs.
