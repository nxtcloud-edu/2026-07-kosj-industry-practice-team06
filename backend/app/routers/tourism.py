"""관광 연계 API (SFR-003) — TourAPI + Gemini 폴백"""
import json
import re
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from google import genai

from app.config import GEMINI_API_KEY
from app.services.tour_api import get_nearby_festivals, get_nearby_spots

router = APIRouter()
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


class TourismRequest(BaseModel):
    lat: float = 36.604561
    lng: float = 127.298342
    radius: int = 2000


@router.post("/data")
def tourism_data(req: TourismRequest):
    """관광지 + 축제 통합 조회 (프론트엔드 관광 탭용)"""
    # 1. 관광지 조회
    spots = get_nearby_spots(lat=req.lat, lng=req.lng)
    spots_source = "TourAPI" if spots else "sample"
    if not spots:
        spots = [
            {"title": "세종호수공원", "address": "세종시 연기면", "type": "관광지"},
            {"title": "조치원역 근대문화거리", "address": "세종시 조치원읍", "type": "관광지"},
            {"title": "베어트리파크", "address": "세종시 전동면", "type": "관광지"},
        ]

    # 2. 축제 조회 (현재 날짜 이후)
    festivals = get_nearby_festivals(lat=req.lat, lng=req.lng)
    festivals_source = "TourAPI"

    # 3. 축제 없으면 Gemini로 향후 축제 검색
    if not festivals and client:
        festivals = _get_future_festivals_from_gemini()
        festivals_source = "AI" if festivals else "sample"

    # 4. Gemini도 실패하면 샘플
    if not festivals:
        festivals = [
            {"title": "조치원 복숭아 축제", "start_date": "20250725", "end_date": "20250727", "address": "세종시 조치원읍", "type": "축제"},
            {"title": "세종 한글술술 축제", "start_date": "20250913", "end_date": "20250913", "address": "세종시 조치원읍", "type": "축제"},
        ]
        festivals_source = "sample"

    return {
        "success": True,
        "spots": spots,
        "spots_source": spots_source,
        "festivals": festivals,
        "festivals_source": festivals_source,
    }


@router.post("/festivals")
def nearby_festivals(req: TourismRequest):
    """축제만 조회 (레거시 호환)"""
    festivals = get_nearby_festivals(lat=req.lat, lng=req.lng)

    if festivals:
        return {"success": True, "festivals": festivals, "source": "TourAPI"}

    if client:
        festivals = _get_future_festivals_from_gemini()
        if festivals:
            return {"success": True, "festivals": festivals, "source": "AI"}

    return {
        "success": True,
        "festivals": [
            {"title": "조치원 복숭아 축제", "start_date": "20250725", "end_date": "20250727", "address": "세종시 조치원읍", "type": "축제"},
            {"title": "세종 한글술술 축제", "start_date": "20250913", "end_date": "20250913", "address": "세종시 조치원읍", "type": "축제"},
        ],
        "source": "sample",
    }


def _get_future_festivals_from_gemini() -> list:
    """Gemini에게 현재 날짜 이후 세종시 축제 검색"""
    today = datetime.now().strftime("%Y년 %m월 %d일")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""오늘은 {today}입니다.
세종시(특히 조치원읍 근처)에서 오늘 이후에 열리는 축제나 행사를 JSON 배열로 알려줘.
각 항목: {{"title": "축제명", "start_date": "YYYYMMDD", "end_date": "YYYYMMDD", "address": "장소", "type": "축제"}}
실제 매년 열리는 축제 위주로 3~5개만. JSON 배열만 출력해."""
        )
        text = response.text.strip()
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass
    return []
