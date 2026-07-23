"""가게 관리 API (DAR-003)"""
import json
import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google import genai

from app.config import GEMINI_API_KEY
from app.database import get_db

router = APIRouter()
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


class StoreCreate(BaseModel):
    name: str
    address: str = "세종시 조치원읍"
    lat: float = 36.604561
    lng: float = 127.298342
    category: str = "개인카페"
    menus: list = []


class GeocodeRequest(BaseModel):
    address: str


@router.post("/")
def create_store(store: StoreCreate):
    """가게 등록"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO stores (name, address, lat, lng, category, menus) VALUES (?, ?, ?, ?, ?, ?)",
        (store.name, store.address, store.lat, store.lng, store.category, json.dumps(store.menus, ensure_ascii=False)),
    )
    conn.commit()
    store_id = cursor.lastrowid
    conn.close()
    return {"id": store_id, **store.model_dump()}


@router.post("/geocode")
def geocode_address(req: GeocodeRequest):
    """주소 → 좌표 변환 (Gemini 기반)"""
    if not client:
        return {"success": False, "error": "GEMINI_API_KEY가 설정되지 않았습니다.", "lat": 36.604561, "lng": 127.298342}

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""다음 주소의 위도와 경도를 알려줘: "{req.address}"
정확한 좌표를 모르면 해당 지역의 대략적인 중심 좌표를 알려줘.
JSON 형식으로만 답해: {{"lat": 위도숫자, "lng": 경도숫자}}
JSON만 출력해. 설명 없이."""
        )
        text = response.text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            coords = json.loads(match.group(0))
            lat = float(coords.get("lat", 36.604561))
            lng = float(coords.get("lng", 127.298342))
            return {"success": True, "lat": lat, "lng": lng, "address": req.address}
    except Exception as e:
        return {"success": False, "error": str(e), "lat": 36.604561, "lng": 127.298342}

    return {"success": False, "error": "좌표를 찾을 수 없습니다.", "lat": 36.604561, "lng": 127.298342}


@router.get("/{store_id}")
def get_store(store_id: int):
    """가게 조회"""
    conn = get_db()
    row = conn.execute("SELECT * FROM stores WHERE id = ?", (store_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="가게를 찾을 수 없습니다")
    return {
        "id": row["id"],
        "name": row["name"],
        "address": row["address"],
        "lat": row["lat"],
        "lng": row["lng"],
        "category": row["category"],
        "menus": json.loads(row["menus"]),
    }


@router.get("/")
def list_stores():
    """가게 목록"""
    conn = get_db()
    rows = conn.execute("SELECT * FROM stores ORDER BY created_at DESC").fetchall()
    conn.close()
    return [
        {"id": r["id"], "name": r["name"], "address": r["address"], "category": r["category"], "menus": json.loads(r["menus"])}
        for r in rows
    ]
