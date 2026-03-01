# backend/src/main.py



import os
from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response

from src.api.router import api_router
from src.shared.db.session import init_db

from src.contexts.locations.app.seed import seed_locations_if_missing


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup 영역
    if os.getenv("DATABASE_URL"):
        init_db()

        # ✅ 추가: 자동 seed (도시별로 있으면 skip, 없으면 insert)
        # 로컬/개발에서만 돌리고 싶으면 AUTO_SEED=true 환경변수로 제어
        if os.getenv("AUTO_SEED", "true").lower() == "true":
            seed_locations_if_missing()

    yield

    # shutdown 영역 (필요하면 여기에 추가)


def create_app() -> FastAPI:
    app = FastAPI(
        title="COMP3011-CW1 API",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
    @app.get("/", include_in_schema=False)
    def root() -> HTMLResponse:
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        html = f"""
        <html>
          <head><title>COMP3011-CW1 API</title></head>
          <body style="font-family: sans-serif; padding: 24px;">
            <h2>COMP3011-CW1 API Server</h2>
            <p>This server provides REST APIs for the Weather service.</p>
            <ul>
              <li><a href="/docs">Swagger UI (/docs)</a></li>
              <li>Frontend: <a href="{frontend_url}">{frontend_url}</a></li>
            </ul>
          </body>
        </html>
        """
        return HTMLResponse(content=html)


    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        return Response(status_code=204)
    


    app.include_router(api_router)
    return app


app = create_app()
