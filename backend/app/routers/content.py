"""콘텐츠 생성 API (SFR-002) — Gemini + 상권 + 관광 데이터 결합"""
import json
from fastapi import APIRouter
from pydantic import BaseModel
from google import genai

from app.config import GEMINI_API_KEY, DEFAULT_LAT, DEFAULT_LNG
from app.database import get_db
from app.services.market_api import get_nearby_stores
from app.services.tour_api import get_nearby_festivals
from app.services.filter import check_prohibited_words

router = APIRouter()
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


class ContentRequest(BaseModel):
    prompt: str
    store_id: int = 0
    store_name: str = ""
    store_category: str = ""
    store_menus: str = ""
    store_address: str = "세종시 조치원읍"
    store_lat: float = 36.604561
    store_lng: float = 127.298342
    location: str = "조치원"
    variation: int = 0


class ContentResponse(BaseModel):
    success: bool
    instagram: str = ""
    banner: str = ""
    hashtags: str = ""
    market_info: str = ""
    festival_info: str = ""
    festival_image: str = ""
    model_used: str = ""
    error: str = ""


@router.post("/generate", response_model=ContentResponse)
def generate_content(req: ContentRequest):
    """자연어 입력 → 상권+축제 데이터 결합 → LLM 마케팅 콘텐츠 생성"""
    if not req.prompt.strip():
        return ContentResponse(success=False, error="입력이 비어있습니다.")

    if not client:
        return ContentResponse(success=False, error="GEMINI_API_KEY가 설정되지 않았습니다.")

    # 1. 상권 데이터 조회
    market_data = get_nearby_stores(req.store_lat, req.store_lng, 500)
    market_summary = f"주변 상가 {market_data['total']}개"
    if market_data["stores"]:
        cafes = [s for s in market_data["stores"] if "카페" in s.get("category", "")]
        market_summary += f", 카페 {len(cafes)}개"

    # 2. 축제 데이터 조회 (TourAPI → Gemini 폴백)
    festivals = get_nearby_festivals(lat=req.store_lat, lng=req.store_lng)
    festival_image = ""
    if festivals:
        f = festivals[0]
        festival_text = f"[인근 축제] {f['title']} ({f.get('start_date', '')}~{f.get('end_date', '')}, {f.get('address', '')})"
        festival_image = f.get("image", "") or ""
    else:
        festival_text = _get_tourism_from_gemini()

    # 3. LLM 프롬프트 조립
    store_section = ""
    if req.store_name or req.store_category or req.store_menus:
        store_section = f"""
[가게 정보]
- 가게명: {req.store_name}
- 업종: {req.store_category}
- 위치: {req.store_address}
- 대표 메뉴/주력 상품: {req.store_menus}
"""

    prompt = f"""당신은 소상공인을 돕는 10년 차 전문 마케터입니다.
아래 사장님의 요청과 실제 상권·관광 데이터를 결합하여 마케팅 콘텐츠를 생성하세요.

[사장님 요청]
"{req.prompt}"
{store_section}
[상권 데이터 (조치원읍 반경 500m)]
{market_summary}

[관광/축제 데이터]
{festival_text}

[생성 규칙]
1. 인스타그램 캡션 1개 + 배너 문구 1개를 생성하세요.
2. 해시태그와 이모지를 적절히 사용하세요.
3. 허위·과장 광고 절대 금지 ("전국 1위", "최고", "최저가" 등 사용 불가)
4. 축제·관광 데이터가 있으면 자연스럽게 연계하세요.
5. 스마트폰에서 읽기 좋은 길이로 작성하세요.
6. variation={req.variation}이면 이전과 다른 톤과 표현을 사용하세요.
7. 가게의 대표 메뉴나 주력 상품을 자연스럽게 강조하세요.
8. 그 가게만의 특색(수제, 로컬, 시즌 한정 등)을 담아주세요.
9. 업종 특성에 맞는 톤을 사용하세요 (카페=감성적, 식당=푸짐한, 농산물=신선한).
10. 반드시 실제 가게명 "{req.store_name}"을 그대로 사용하세요. [가게 이름], [가게명] 같은 플레이스홀더 절대 금지.

[출력 형식]
---인스타그램 캡션---
(여기에 작성)

---배너 문구---
(여기에 작성)

---추천 해시태그---
(여기에 5개 내외)
"""

    # 4. LLM 호출 (다중 모델 폴백)
    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash-lite", "gemini-2.0-flash"]
    last_error = None

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(model=model_name, contents=prompt)
            text = check_prohibited_words(response.text)
            result = _parse_content(text)

            # DB 저장
            _save_to_db(req, result, market_summary, festival_text, model_name)

            return ContentResponse(
                success=True,
                instagram=result["instagram"],
                banner=result["banner"],
                hashtags=result["hashtags"],
                market_info=market_summary,
                festival_info=festival_text,
                festival_image=festival_image,
                model_used=model_name,
            )
        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            else:
                return ContentResponse(success=False, error=str(e))

    return ContentResponse(success=False, error=f"모든 모델 할당량 소진. ({last_error})")


@router.get("/history/{store_id}")
def get_history(store_id: int):
    """생성 기록 조회"""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM contents WHERE store_id = ? ORDER BY created_at DESC LIMIT 20",
        (store_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def _get_tourism_from_gemini() -> str:
    """TourAPI 데이터 없을 때 Gemini에게 관광 정보 조회"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="""세종시 조치원읍 근처에서 현재 시기(7월)에 열리는 축제나 행사, 
그리고 주변 관광지 정보를 간단히 알려줘. 3줄 이내로:
- 축제/행사: (축제명, 시기, 장소)
- 관광지: (관광지명, 거리)
- 특징: (마케팅에 활용할 포인트)"""
        )
        return f"[인근 관광/축제 — AI 조사] {response.text.strip()}"
    except Exception:
        return "[인근 축제] 세종시 복숭아 축제(7월 말 예정), 세종호수공원(차량 15분)"


def _parse_content(text: str) -> dict:
    """LLM 출력 파싱"""
    instagram, banner, hashtags = "", "", ""
    if "---인스타그램 캡션---" in text:
        parts = text.split("---배너 문구---")
        instagram = parts[0].replace("---인스타그램 캡션---", "").strip()
        if len(parts) > 1:
            rest = parts[1]
            if "---추천 해시태그---" in rest:
                bp = rest.split("---추천 해시태그---")
                banner = bp[0].strip()
                hashtags = bp[1].strip() if len(bp) > 1 else ""
            else:
                banner = rest.strip()
    else:
        instagram = text
    return {"instagram": instagram, "banner": banner, "hashtags": hashtags}


def _save_to_db(req, result, market_info, festival_info, model_used):
    """생성 결과를 SQLite에 저장"""
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO contents (store_id, user_input, instagram, banner, hashtags, market_info, festival_info, model_used) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (req.store_id, req.prompt, result["instagram"], result["banner"], result["hashtags"], market_info, festival_info, model_used),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass
