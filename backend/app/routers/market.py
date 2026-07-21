"""상권 분석 API (SFR-001)"""
from fastapi import APIRouter
from pydantic import BaseModel

from app.config import DEFAULT_LAT, DEFAULT_LNG
from app.services.market_api import get_nearby_stores

router = APIRouter()


class MarketRequest(BaseModel):
    lat: float = DEFAULT_LAT
    lng: float = DEFAULT_LNG
    radius: int = 500


@router.post("/report")
def market_report(req: MarketRequest):
    """좌표 기반 반경 내 상가 정보 조회"""
    try:
        result = get_nearby_stores(req.lat, req.lng, req.radius, num_rows=1000)
        return {"success": True, "total_count": result["total"], "stores": result["stores"]}
    except Exception as e:
        return {"success": False, "total_count": 0, "stores": [], "error": str(e)}
