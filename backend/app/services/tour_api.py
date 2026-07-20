"""TourAPI (한국관광공사) 연동 서비스"""
import requests

from app.config import DATA_API_KEY

BASE_URL = "http://apis.data.go.kr/B551011/KorService2"


def get_nearby_festivals(lat: float, lng: float, radius: int = 5000) -> list:
    """좌표 기반 반경 내 축제·행사 정보를 조회합니다."""
    url = f"{BASE_URL}/searchFestival2"
    params = {
        "serviceKey": DATA_API_KEY,
        "MobileOS": "ETC",
        "MobileApp": "AIMarketing",
        "_type": "json",
        "numOfRows": 10,
        "mapX": lng,
        "mapY": lat,
        "radius": radius,
        "contentTypeId": 15,  # 15 = 축제/공연/행사
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    items_wrapper = data.get("response", {}).get("body", {}).get("items", {})
    items = items_wrapper.get("item", []) if items_wrapper else []

    festivals = []
    for item in items:
        festivals.append({
            "title": item.get("title", ""),
            "start_date": item.get("eventstartdate", ""),
            "end_date": item.get("eventenddate", ""),
            "address": item.get("addr1", ""),
            "image": item.get("firstimage", ""),
            "lat": item.get("mapy", ""),
            "lng": item.get("mapx", ""),
        })

    return festivals


def get_festival_detail(content_id: str) -> dict:
    """축제 상세 정보(overview 포함)를 조회합니다."""
    url = f"{BASE_URL}/detailCommon2"
    params = {
        "serviceKey": DATA_API_KEY,
        "MobileOS": "ETC",
        "MobileApp": "AIMarketing",
        "_type": "json",
        "contentId": content_id,
        "overviewYN": "Y",
        "defaultYN": "Y",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

    if items:
        item = items[0]
        return {
            "title": item.get("title", ""),
            "overview": item.get("overview", ""),
            "address": item.get("addr1", ""),
            "image": item.get("firstimage", ""),
        }
    return {}
