"""시즌·이벤트 선제 제안 API (SFR-004) — 위치+날짜 기반"""
import json
import re
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from google import genai

from app.config import GEMINI_API_KEY
from app.services.tour_api import get_nearby_festivals

router = APIRouter()
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


class SuggestionRequest(BaseModel):
    lat: float = 36.604561
    lng: float = 127.298342
    address: str = "세종시 조치원읍"
    category: str = "개인카페"


@router.post("/")
def get_suggestions(req: SuggestionRequest):
    """위치·날짜·업종 기반 선제 제안 생성"""
    today = datetime.now()
    month = today.month
    suggestions = []

    # 1. TourAPI 축제 기반 제안
    festivals = get_nearby_festivals(lat=req.lat, lng=req.lng)
    for f in festivals[:2]:
        title = f.get("title", "")
        start = f.get("start_date", "")
        if start:
            try:
                fest_date = datetime.strptime(start, "%Y%m%d")
                d_day = (fest_date - today).days
                if d_day >= 0 and d_day <= 30:
                    suggestions.append({
                        "title": f"🎉 {title} D-{d_day}",
                        "desc": f"{title}이 {d_day}일 앞이에요. 지금 홍보물 준비하면 딱 좋아요!",
                        "type": "축제",
                        "prompt": f"{title} 관련 홍보물 만들어줘",
                    })
            except ValueError:
                pass

    # 2. 축제 정보 없으면 Gemini로 조회
    if not suggestions and client:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"""오늘은 {today.strftime('%Y년 %m월 %d일')}입니다.
{req.address} 근처에서 앞으로 2주 이내에 열리는 축제나 행사가 있으면 알려줘.
없으면 이 지역에서 이 시기에 할 만한 마케팅 아이디어를 1개 제안해줘.
JSON 형식으로: {{"title": "제목", "desc": "설명", "prompt": "홍보물 프롬프트"}}
JSON만 출력해."""
            )
            text = response.text.strip()
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                item = json.loads(match.group(0))
                suggestions.append({**item, "type": "축제"})
        except Exception:
            pass

    # 3. 계절 기반 제안
    season_suggestions = _get_season_suggestions(month, req.category)
    suggestions.extend(season_suggestions)

    # 4. 상권 기반 제안 (주말)
    weekday = today.weekday()
    if weekday >= 3:  # 목~일
        suggestions.append({
            "title": "📈 주말 유동인구 증가",
            "desc": "이번 주말 주변 유동인구가 평일 대비 높을 것으로 보여요.",
            "type": "상권",
            "prompt": "주말 이벤트 홍보물 만들어줘",
        })

    return {"success": True, "suggestions": suggestions[:5]}


def _get_season_suggestions(month: int, category: str) -> list:
    """월별·업종별 시즌 제안"""
    suggestions = []

    season_map = {
        (12, 1, 2): {"keyword": "겨울", "cafe": "따뜻한 음료·크리스마스 한정 메뉴", "food": "뜨끈한 국물 요리·연말 모임", "farm": "겨울 제철 채소·김장"},
        (3, 4, 5): {"keyword": "봄", "cafe": "벚꽃 시즌·봄 한정 음료", "food": "봄나물 메뉴·야외 테라스", "farm": "봄 딸기·새싹 채소"},
        (6, 7, 8): {"keyword": "여름", "cafe": "시원한 빙수·여름 음료", "food": "보양식·시원한 면 요리", "farm": "복숭아·수박·여름 과일"},
        (9, 10, 11): {"keyword": "가을", "cafe": "단풍 시즌·가을 디저트", "food": "가을 제철 음식·버섯 요리", "farm": "사과·배·단감"},
    }

    for months, data in season_map.items():
        if month in months:
            keyword = data["keyword"]
            if category == "개인카페":
                desc = data["cafe"]
            elif category == "식당":
                desc = data["food"]
            elif category == "농산물":
                desc = data["farm"]
            else:
                desc = f"{keyword} 시즌 프로모션"

            suggestions.append({
                "title": f"☀️ {keyword} 시즌 메뉴",
                "desc": f"{desc} 홍보는 어떨까요?",
                "type": "시즌",
                "prompt": f"{keyword} 시즌 {desc} 홍보물 만들어줘",
            })
            break

    return suggestions
