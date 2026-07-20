"""LLM(Gemini) 호출 서비스"""
from google import genai

from app.config import GEMINI_API_KEY
from app.services.filter import check_prohibited_words


def generate_marketing_content(user_prompt: str, location: str = "조치원") -> dict:
    """사장님 입력 + 데이터 근거를 결합하여 마케팅 콘텐츠를 생성합니다."""
    client = genai.Client(api_key=GEMINI_API_KEY)

    system_prompt = f"""
당신은 소상공인을 돕는 10년 차 전문 마케터입니다.
아래 사장님의 요청을 바탕으로 인스타그램 캡션과 배너 문구를 작성하세요.

[지역] {location}

[작성 조건]
1. 해시태그와 이모지를 적절히 사용
2. 허위·과장 광고 금지 (\"전국 1위\", \"최고\", \"최저가\" 등 절대 사용 금지)
3. 스마트폰 화면에서 읽기 좋은 길이

[출력 형식]
인스타그램 캡션:
(여기에 작성)

배너 문구:
(여기에 작성)
"""

    full_prompt = f"{system_prompt}\n\n[사장님 요청]\n{user_prompt}"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=full_prompt,
    )

    text = response.text

    # 금지어 필터링
    text = check_prohibited_words(text)

    # 간단한 파싱 (인스타/배너 분리)
    instagram = ""
    banner = ""
    if "인스타그램 캡션:" in text:
        parts = text.split("배너 문구:")
        instagram = parts[0].replace("인스타그램 캡션:", "").strip()
        banner = parts[1].strip() if len(parts) > 1 else ""
    else:
        instagram = text
        banner = ""

    return {"instagram": instagram, "banner": banner}
