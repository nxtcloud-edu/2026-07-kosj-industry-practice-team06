import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from google import genai

# .env 파일에서 환경변수 로드
load_dotenv()

app = Flask(__name__)

# Gemini 클라이언트
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 상권 API / TourAPI 키
DATA_API_KEY = os.getenv("DATA_API_KEY", "")

# 조치원 좌표 (기본값)
DEFAULT_LAT = 36.604561
DEFAULT_LNG = 127.298342


def get_nearby_stores(lat=DEFAULT_LAT, lng=DEFAULT_LNG, radius=500):
    """상권 API: 반경 내 상가 조회"""
    url = "http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInRadius"
    params = {
        "serviceKey": DATA_API_KEY,
        "pageNo": "1",
        "numOfRows": "10",
        "radius": str(radius),
        "cx": str(lng),
        "cy": str(lat),
        "type": "json",
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            items = data.get("body", {}).get("items", [])
            total = data.get("body", {}).get("totalCount", 0)
            stores = []
            for item in items:
                stores.append({
                    "name": item.get("bizesNm", ""),
                    "category": item.get("indsSclsNm", ""),
                    "address": item.get("rdnmAdr", ""),
                })
            return {"total": total, "stores": stores}
    except Exception:
        pass
    return {"total": 0, "stores": []}


def get_nearby_festivals():
    """TourAPI: 세종시 축제 조회 (2025년 데이터 기반 시연)"""
    BASE_URL = "http://apis.data.go.kr/B551011/KorService2"
    url = (
        f"{BASE_URL}/searchFestival2"
        f"?serviceKey={DATA_API_KEY}"
        f"&MobileOS=ETC&MobileApp=AIMarketing&_type=json"
        f"&numOfRows=5&pageNo=1"
        f"&areaCode=8&eventStartDate=20250101"
    )
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            items = data.get("response", {}).get("body", {}).get("items", {})
            item_list = items.get("item", []) if isinstance(items, dict) else []
            festivals = []
            for item in item_list:
                festivals.append({
                    "title": item.get("title", ""),
                    "start": item.get("eventstartdate", ""),
                    "end": item.get("eventenddate", ""),
                    "addr": item.get("addr1", ""),
                })
            return festivals
    except Exception:
        pass
    return []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/market/report", methods=["POST"])
def api_market_report():
    """상권 분석 API (프론트엔드 리포트 탭용)"""
    data = request.get_json()
    lat = data.get("lat", DEFAULT_LAT)
    lng = data.get("lng", DEFAULT_LNG)
    radius = data.get("radius", 500)

    # 리포트용으로 더 많은 데이터 조회
    url = "http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInRadius"
    params = {
        "serviceKey": DATA_API_KEY,
        "pageNo": "1",
        "numOfRows": "1000",
        "radius": str(radius),
        "cx": str(lng),
        "cy": str(lat),
        "type": "json",
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            resp_data = r.json()
            items = resp_data.get("body", {}).get("items", [])
            total = resp_data.get("body", {}).get("totalCount", 0)
            stores = []
            for item in items:
                stores.append({
                    "name": item.get("bizesNm", ""),
                    "category": item.get("indsSclsNm", ""),
                    "category_large": item.get("indsLclsNm", ""),
                    "category_mid": item.get("indsMclsNm", ""),
                    "address": item.get("rdnmAdr", ""),
                })
            return jsonify({"success": True, "total_count": total, "stores": stores})
    except Exception:
        pass
    return jsonify({"success": False, "total_count": 0, "stores": []})


@app.route("/api/tourism/festivals", methods=["POST"])
def api_tourism_festivals():
    """관광 연계 API (프론트엔드 관광 탭용)"""
    festivals = get_nearby_festivals()
    return jsonify({
        "success": True,
        "festivals": festivals,
    })


@app.route("/generate", methods=["POST"])
def generate_marketing():
    """
    사장님 자연어 입력 → 상권+축제 데이터 결합 → LLM 마케팅 콘텐츠 생성
    """
    data = request.get_json()
    user_input = data.get("prompt", "").strip()

    if not user_input:
        return jsonify({"success": False, "error": "입력이 비어있습니다."})

    # 1. 상권 데이터 조회
    market_data = get_nearby_stores()
    market_summary = f"주변 상가 {market_data['total']}개"
    if market_data["stores"]:
        cafes = [s for s in market_data["stores"] if "카페" in s.get("category", "")]
        market_summary += f", 카페 {len(cafes)}개"

    # 2. 축제 데이터 조회
    festivals = get_nearby_festivals()
    festival_text = ""
    if festivals:
        f = festivals[0]
        festival_text = f"[인근 축제] {f['title']} ({f['start']}~{f['end']}, {f['addr']})"
    else:
        festival_text = "[인근 축제] 현재 등록된 세종시 축제 없음"

    # 3. LLM 프롬프트 조립 (RAG 방식: 실제 데이터를 근거로 주입)
    prompt = f"""당신은 소상공인을 돕는 10년 차 전문 마케터입니다.
아래 사장님의 요청과 실제 상권·관광 데이터를 결합하여 마케팅 콘텐츠를 생성하세요.

[사장님 요청]
"{user_input}"

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

[출력 형식]
---인스타그램 캡션---
(여기에 작성)

---배너 문구---
(여기에 작성)

---추천 해시태그---
(여기에 5개 내외)
"""

    # 4. LLM 호출 (할당량 소진 대비 다중 모델)
    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash-lite", "gemini-2.0-flash"]
    last_error = None

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            text = response.text

            # 5. 결과 파싱
            result = parse_generated_content(text)
            result["success"] = True
            result["model_used"] = model_name
            result["market_info"] = market_summary
            result["festival_info"] = festival_text
            return jsonify(result)

        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            else:
                return jsonify({"success": False, "error": str(e)})

    return jsonify({"success": False, "error": f"모든 모델 할당량 소진. 잠시 후 다시 시도해주세요. ({last_error})"})


def parse_generated_content(text):
    """LLM 출력을 인스타캡션 / 배너 / 해시태그로 분리"""
    instagram = ""
    banner = ""
    hashtags = ""

    if "---인스타그램 캡션---" in text:
        parts = text.split("---배너 문구---")
        instagram = parts[0].replace("---인스타그램 캡션---", "").strip()
        if len(parts) > 1:
            rest = parts[1]
            if "---추천 해시태그---" in rest:
                banner_parts = rest.split("---추천 해시태그---")
                banner = banner_parts[0].strip()
                hashtags = banner_parts[1].strip() if len(banner_parts) > 1 else ""
            else:
                banner = rest.strip()
    else:
        # 파싱 실패 시 전체 텍스트 반환
        instagram = text

    return {
        "instagram": instagram,
        "banner": banner,
        "hashtags": hashtags,
        "raw": text,
    }


if __name__ == "__main__":
    app.run(debug=True)
