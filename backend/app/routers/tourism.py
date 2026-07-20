"""관광 연계 API 라우터"""
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.tour_api import get_nearby_festivals

router = APIRouter()


class TourismRequest(BaseModel):
    lat: float
    lng: float
    radius: int = 5000  # 반경(m)


class TourismResponse(BaseModel):
    success: bool
    festivals: list = []
    error: str = ""


@router.post("/festivals", response_model=TourismResponse)
async def nearby_festivals(req: TourismRequest):
    """좌표 기반으로 인근 축제·행사 정보를 조회합니다."""
    try:
        festivals = get_nearby_festivals(req.lat, req.lng, req.radius)
        return TourismResponse(success=True, festivals=festivals)
    except Exception as e:
        return TourismResponse(success=False, error=str(e))
