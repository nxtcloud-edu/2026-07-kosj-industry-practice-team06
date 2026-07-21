"""TourAPI (한국관광공사) 연동"""
import requests
from app.config import DATA_API_KEY

BASE_URL = "http://apis.data.go.kr/B551011/KorService2"


def get_nearby_festivals() -> list:
    """세종시 축제·행사 조회"""
    url = f"{BASE_URL}/searchFestival2"
    params = {
        "serviceKey": DATA_API_KEY,
        "MobileOS": "ETC",
        "MobileApp": "AIMarketing",
        "_type": "json",
        "numOfRows": 10,
        "pageNo": 1,
        "areaCode": 8,
        "eventStartDate": "20250101",
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
                "start": item.get("eventstartdate", ""),
                "end": item.get("eventenddate", ""),
                "addr": item.get("addr1", ""),
                "image": item.get("firstimage", ""),
                "start_date": item.get("eventstartdate", ""),
                "end_date": item.get("eventenddate", ""),
                "address": item.get("addr1", ""),
            })
        return festivals
    except Exception:
        return []
