"""
[프로토타입] TourAPI JSON 파싱 테스트
- 응답에서 title, overview 추출 확인용
- 실제 서비스에서는 backend/app/services/tour_api.py 사용
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

service_key = os.getenv("DATA_API_KEY", "")
content_id = "2986679"

url = "http://apis.data.go.kr/B551011/KorService2/detailCommon2"
params = {
    "serviceKey": service_key,
    "MobileOS": "ETC",
    "MobileApp": "AppTest",
    "_type": "json",
    "contentId": content_id,
}

try:
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        festival_info = data["response"]["body"]["items"]["item"][0]

        title = festival_info["title"]
        overview = festival_info["overview"]

        print("🎉 파싱 성공! 추출된 데이터입니다.\n")
        print(f"📌 축제명: {title}")
        print(f"📝 상세 소개: {overview}\n")
    else:
        print(f"❌ 에러 발생: 상태 코드 {response.status_code}")

except Exception as e:
    print(f"통신 중 오류가 발생했습니다: {e}")
