"""FastAPI 메인 앱 — AI 기반 소상공인 마케팅·상권분석 및 관광 연계 플랫폼"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import init_db
from app.routers import content, market, tourism, stores

app = FastAPI(
    title="AI 소상공인 마케팅 플랫폼",
    description="자연어 입력 → 상권·관광 데이터 기반 마케팅 콘텐츠 생성",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(stores.router, prefix="/api/stores", tags=["가게 관리"])
app.include_router(content.router, prefix="/api/content", tags=["콘텐츠 생성"])
app.include_router(market.router, prefix="/api/market", tags=["상권 분석"])
app.include_router(tourism.router, prefix="/api/tourism", tags=["관광 연계"])

# 프론트엔드 HTML 서빙 (templates/index.html)
TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"


@app.get("/")
def serve_frontend():
    return FileResponse(TEMPLATE_DIR / "index.html")


@app.on_event("startup")
def startup():
    init_db()
