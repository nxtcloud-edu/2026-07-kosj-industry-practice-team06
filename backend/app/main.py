"""FastAPI 메인 앱"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import content, market, tourism

app = FastAPI(
    title="AI 소상공인 마케팅 플랫폼",
    description="자연어 입력 → 상권·관광 데이터 기반 마케팅 콘텐츠 생성",
    version="0.1.0",
)

# CORS 설정 (프론트엔드 연동)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(content.router, prefix="/api/content", tags=["콘텐츠 생성"])
app.include_router(market.router, prefix="/api/market", tags=["상권 분석"])
app.include_router(tourism.router, prefix="/api/tourism", tags=["관광 연계"])


@app.get("/")
def root():
    return {"message": "AI 소상공인 마케팅 플랫폼 API 서버"}
