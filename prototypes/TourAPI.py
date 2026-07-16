"""
[프로토타입] TourAPI 상세 정보 조회 테스트
- 축제 contentId로 상세 정보 호출 확인용
- 실제 서비스에서는 backend/app/services/tour_api.py 사용
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

service_key = os.getenv("DATA_API_KEY", "")
content_id = "2986679"  # 예: 가족의 달 어린이 축제

url = f"http://apis.data.go.kr/B551011/KorService2/detailCommon2"
params = {
    "serviceKey": service_key,
    "MobileOS": "ETC",
    "MobileApp": "AppTest",
    "_type": "json",
    "contentId": content_id,
}

print(f"콘텐츠 ID [{content_id}]의 상세 정보를 요청하는 중입니다...")

try:
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("✅ 통신 성공! 아래 상세 응답 데이터를 확인하세요:\n")
        print(response.text)
    else:
        print(f"❌ 에러 발생: 상태 코드 {response.status_code}")

except Exception as e:
    print(f"통신 중 오류가 발생했습니다: {e}")
