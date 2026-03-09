# Backend Service

This directory contains the FastAPI backend for the Weather Analytics platform.

---

## Technology

- FastAPI
- SQLModel
- PostgreSQL
- Alembic

The application uses PostgreSQL to store location and weather observation data.
Database schema migrations are managed using Alembic.


## Run the Backend

```bash
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

uvicorn src.main:app --reload
```



API documentation: `http://localhost:8000/docs`

Interactive API documentation is available at: `http://localhost:8000/docs`

