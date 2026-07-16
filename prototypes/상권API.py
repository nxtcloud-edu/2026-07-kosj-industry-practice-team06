"""
[프로토타입] 상가정보(상권) API 통신 테스트
- 반경 내 상가 조회 동작 확인용 스크립트
- 실제 서비스에서는 backend/app/services/market_api.py 사용
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

service_key = os.getenv("DATA_API_KEY", "")

# 예시: 서울시청 기준 반경 500m
url = f"https://apis.data.go.kr/B553077/api/open/sdsc2/storeListInRadius"
params = {
    "serviceKey": service_key,
    "pageNo": 1,
    "numOfRows": 5,
    "radius": 500,
    "cx": 126.9780,
    "cy": 37.5665,
    "type": "json",
}

print("상권 API 데이터를 요청하는 중입니다. 잠시만 기다려주세요...")

try:
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("✅ 통신 성공! 아래 상권 응답 데이터를 확인하세요:\n")
        print(response.text)
    else:
        print(f"❌ 에러 발생: 상태 코드 {response.status_code}")
        print(f"응답 내용: {response.text}")

except Exception as e:
    print(f"통신 중 오류가 발생했습니다: {e}")
