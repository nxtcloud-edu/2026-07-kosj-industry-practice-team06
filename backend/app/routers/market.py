"""상권 분석 API 라우터"""
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.market_api import get_nearby_stores

router = APIRouter()


class MarketRequest(BaseModel):
    lat: float  # 위도
    lng: float  # 경도
    radius: int = 500  # 반경(m)


class MarketResponse(BaseModel):
    success: bool
    total_count: int = 0
    stores: list = []
    error: str = ""


@router.post("/report", response_model=MarketResponse)
async def market_report(req: MarketRequest):
    """좌표 기반으로 반경 내 상가 정보를 조회합니다."""
    try:
        result = get_nearby_stores(req.lat, req.lng, req.radius)
        return MarketResponse(
            success=True,
            total_count=result.get("total", 0),
            stores=result.get("stores", []),
        )
    except Exception as e:
        return MarketResponse(success=False, error=str(e))
