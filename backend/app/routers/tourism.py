"""관광 연계 API (SFR-003) — TourAPI + Gemini 폴백"""
import json
import re
from fastapi import APIRouter
from pydantic import BaseModel
from google import genai

from app.config import GEMINI_API_KEY
from app.services.tour_api import get_nearby_festivals

router = APIRouter()
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


class TourismRequest(BaseModel):
    lat: float = 36.604561
    lng: float = 127.298342
    radius: int = 5000


@router.post("/festivals")
def nearby_festivals(req: TourismRequest):
    """인근 축제·행사 정보 (TourAPI → Gemini 폴백)"""
    festivals = get_nearby_festivals()

    if festivals:
        return {"success": True, "festivals": festivals, "source": "TourAPI"}

    # TourAPI 데이터 없으면 Gemini로 조회
    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents="""세종시 조치원읍 주변의 관광지와 축제를 JSON 배열로 알려줘.
각 항목은 {"title": "이름", "start_date": "시작일(YYYYMMDD)", "end_date": "종료일", "address": "주소"} 형식이야.
실제 존재하는 것만 3~5개 알려줘. JSON 배열만 출력해."""
            )
            text = response.text.strip()
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                gemini_festivals = json.loads(match.group(0))
                return {"success": True, "festivals": gemini_festivals, "source": "AI"}
        except Exception:
            pass

    # 최종 폴백 (샘플)
    return {
        "success": True,
        "festivals": [
            {"title": "조치원 복숭아 축제", "start_date": "20250725", "end_date": "20250727", "address": "세종시 조치원읍"},
            {"title": "세종 한글술술 축제", "start_date": "20250913", "end_date": "20250913", "address": "세종시 조치원읍"},
        ],
        "source": "sample",
    }
