"""FastAPI 메인 앱 — AI 기반 소상공인 마케팅·상권분석 및 관광 연계 플랫폼"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.database import init_db
from app.routers import content, market, tourism, stores, admin

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
app.include_router(admin.router, prefix="/api/admin", tags=["진흥원 대시보드"])

# 프론트엔드 HTML 서빙 (templates/index.html)
TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"
# 진흥원 대시보드 화면
WEB_DIR = Path(__file__).parent.parent / "web"


NO_CACHE = {"Cache-Control": "no-store, no-cache, must-revalidate", "Pragma": "no-cache"}


@app.get("/")
def landing():
    """메인 진입 — 소상공인 앱 / 진흥원 대시보드 선택"""
    return FileResponse(WEB_DIR / "landing.html", headers=NO_CACHE)


@app.get("/app")
def serve_frontend():
    """고객A: 소상공인 앱 (팀원 templates)"""
    return FileResponse(TEMPLATE_DIR / "index.html", headers=NO_CACHE)


@app.get("/admin")
def admin_dashboard():
    """세종경제관광진흥원 성과 대시보드"""
    return FileResponse(WEB_DIR / "admin.html", headers=NO_CACHE)


@app.get("/admin/report")
def admin_report():
    """진흥원 담당자용 성과 보고서 (인쇄·PDF·CSV)"""
    return FileResponse(WEB_DIR / "report.html", headers=NO_CACHE)


@app.get("/admin/stores")
def admin_stores():
    """관내 참여 가게 목록"""
    return FileResponse(WEB_DIR / "stores.html", headers=NO_CACHE)


@app.get("/admin/insights")
def admin_insights():
    """정책 인사이트 (업종·시즌 수요)"""
    return FileResponse(WEB_DIR / "insights.html", headers=NO_CACHE)


@app.get("/admin/calendar")
def admin_calendar():
    """시즌·축제 캘린더"""
    return FileResponse(WEB_DIR / "calendar.html", headers=NO_CACHE)


@app.on_event("startup")
def startup():
    init_db()
