"""가게 관리 API (DAR-003)"""
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_db

router = APIRouter()


class StoreCreate(BaseModel):
    name: str
    address: str = "세종시 조치원읍"
    lat: float = 36.604561
    lng: float = 127.298342
    category: str = "개인카페"
    menus: list = []


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
