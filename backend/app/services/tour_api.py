"""TourAPI (한국관광공사) 연동"""
import requests
from datetime import datetime
from app.config import DATA_API_KEY

BASE_URL = "http://apis.data.go.kr/B551011/KorService2"


def get_nearby_festivals(lat: float = 36.604561, lng: float = 127.298342) -> list:
    """좌표 기반 축제·행사 조회 (현재 날짜 이후만)"""
    today = datetime.now().strftime("%Y%m%d")
    url = f"{BASE_URL}/searchFestival2"
    params = {
        "serviceKey": DATA_API_KEY,
        "MobileOS": "ETC",
        "MobileApp": "AIMarketing",
        "_type": "json",
        "numOfRows": 10,
        "pageNo": 1,
        "mapX": lng,
        "mapY": lat,
        "radius": 20000,
        "eventStartDate": today,
    }

    try:
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
                "type": "축제",
            })
        return festivals
    except Exception:
        return []


def get_nearby_spots(lat: float = 36.604561, lng: float = 127.298342) -> list:
    """좌표 기반 관광지 조회 (contentTypeId=12)"""
    url = f"{BASE_URL}/locationBasedList2"
    params = {
        "serviceKey": DATA_API_KEY,
        "MobileOS": "ETC",
        "MobileApp": "AIMarketing",
        "_type": "json",
        "numOfRows": 10,
        "pageNo": 1,
        "mapX": lng,
        "mapY": lat,
        "radius": 20000,
        "contentTypeId": 12,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        items_wrapper = data.get("response", {}).get("body", {}).get("items", {})
        items = items_wrapper.get("item", []) if items_wrapper else []

        spots = []
        for item in items:
            spots.append({
                "title": item.get("title", ""),
                "address": item.get("addr1", ""),
                "image": item.get("firstimage", ""),
                "type": "관광지",
            })
        return spots
    except Exception:
        return []

