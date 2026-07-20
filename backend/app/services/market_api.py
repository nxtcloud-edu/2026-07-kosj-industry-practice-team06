"""상가정보(상권) API 연동 서비스"""
import requests

from app.config import DATA_API_KEY

BASE_URL = "https://apis.data.go.kr/B553077/api/open/sdsc2/storeListInRadius"


def get_nearby_stores(lat: float, lng: float, radius: int = 500) -> dict:
    """좌표 기반 반경 내 상가 목록을 조회합니다."""
    params = {
        "serviceKey": DATA_API_KEY,
        "pageNo": 1,
        "numOfRows": 20,
        "radius": radius,
        "cx": lng,  # 경도
        "cy": lat,  # 위도
        "type": "json",
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    body = data.get("body", {})
    items = body.get("items", [])
    total = body.get("totalCount", 0)

    stores = []
    for item in items:
        stores.append({
            "name": item.get("bizesNm", ""),
            "category_large": item.get("indsLclsNm", ""),
            "category_mid": item.get("indsMclsNm", ""),
            "category_small": item.get("indsSclsNm", ""),
            "address": item.get("rdnmAdr", ""),
            "lat": item.get("lat", ""),
            "lng": item.get("lon", ""),
        })

    return {"total": total, "stores": stores}
