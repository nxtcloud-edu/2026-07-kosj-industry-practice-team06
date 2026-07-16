"""
[프로토타입] Gemini 새 Client 방식 테스트 (google-genai SDK)
- 실제 서비스에서는 backend/app/services/llm.py 사용
"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))

title = "가족의 달 어린이 축제"
overview = (
    "'키즈벤처(키즈+어드벤처)'를 주제로 열리는 이번 축제는 동심 가득한 "
    "놀이공원 콘셉트로 어린이와 가족이 함께 즐길 수 있도록 기획됐다."
)

prompt = f"""
당신은 소상공인을 돕는 10년 차 전문 마케터입니다.
아래 지역 축제 정보를 바탕으로, 행사장에서 도보 5분 거리에 있는
디저트 카페의 '어린이 한정판 복숭아 케이크' 인스타그램 홍보 문구를 작성해 주세요.

[축제 정보]
- 행사명: {title}
- 행사 내용: {overview}

[작성 조건]
1. 해시태그와 이모지를 적절히 사용
2. 허위 과장 광고 절대 금지
3. 스마트폰에서 읽기 좋은 길이
"""

print("AI 마케터가 홍보 문구를 작성 중입니다...\n")

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    print("✨ [생성 완료]\n")
    print("-" * 50)
    print(response.text)
    print("-" * 50)
except Exception as e:
    print(f"통신 중 오류가 발생했습니다: {e}")
