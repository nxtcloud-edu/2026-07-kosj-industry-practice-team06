"""상권정보(소상공인시장진흥공단) API 연동"""
import requests
from app.config import DATA_API_KEY

BASE_URL = "https://apis.data.go.kr/B553077/api/open/sdsc2/storeListInRadius"


def get_nearby_stores(lat: float, lng: float, radius: int = 500, num_rows: int = 1000) -> dict:
    """좌표 기반 반경 내 상가 목록 조회"""
    params = {
        "serviceKey": DATA_API_KEY,
        "pageNo": 1,
        "numOfRows": num_rows,
        "radius": radius,
        "cx": lng,
        "cy": lat,
        "type": "json",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        body = data.get("body", {})
        items = body.get("items", [])
        total = body.get("totalCount", 0)

        stores = []
        for item in items:
            stores.append({
                "name": item.get("bizesNm", ""),
                "category": item.get("indsSclsNm", ""),
                "category_large": item.get("indsLclsNm", ""),
                "category_mid": item.get("indsMclsNm", ""),
                "address": item.get("rdnmAdr", ""),
                "lat": item.get("lat", ""),
                "lng": item.get("lon", ""),
            })
        return {"total": total, "stores": stores}
    except Exception:
        return {"total": 0, "stores": []}
