# COMP3011-CW1 — Starter Template (DDD)

Template aligned with the Project Charter:
- Backend: FastAPI + SQLModel + Pydantic (DDD bounded contexts)
- Frontend: Next.js + TypeScript
- DB: PostgreSQL (local)
- Git: feature branches + PRs

## Run (Backend)
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn src.main:app --reload
```
Open: http://localhost:8000/docs

## Run (Frontend)
```bash
cd frontend
npm install
npm run dev
```
Open: http://localhost:3000

## Notes
- Don't commit `.env`, `venv/`, `node_modules/`, or PostgreSQL data directories.
