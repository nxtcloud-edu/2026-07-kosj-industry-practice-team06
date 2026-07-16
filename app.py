import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from google import genai

# .env 파일에서 환경변수 로드
load_dotenv()

app = Flask(__name__)

# 환경변수에서 API 키를 읽어옴 (하드코딩 금지!)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_marketing_text():
    """공공데이터 기반 축제 정보 + LLM으로 마케팅 문구 생성"""

    # TourAPI에서 파싱한 축제 정보 (프로토타입: 하드코딩 → 추후 API 연동)
    title = "가족의 달 어린이 축제"
    overview = (
        "'키즈벤처(키즈+어드벤처)'를 주제로 열리는 이번 축제는 동심 가득한 "
        "놀이공원 콘셉트로 어린이와 가족이 함께 즐길 수 있도록 기획됐다. "
        "무대에서는 서커스 공연을 비롯해 애니메이션 OST 음악회, 버블쇼, "
        "마술쇼 등 어린이 눈높이에 맞춘 다채로운 공연이 펼쳐질 예정이다."
    )

    prompt = f"""
당신은 소상공인을 돕는 10년 차 전문 마케터입니다.
아래 지역 축제 정보를 바탕으로, 행사장에서 도보 5분 거리에 있는
디저트 카페의 '어린이 한정판 복숭아 케이크' 인스타그램 홍보 문구를 작성해 주세요.

[축제 정보]
- 행사명: {title}
- 행사 내용: {overview}

[작성 조건]
1. 해시태그와 이모지를 적절히 사용할 것
2. 행사 내용 중 아이들이 좋아하는 키워드를 자연스럽게 녹일 것
3. 허위 과장 광고 방지: '전국 1위', '최고' 등 절대 사용 금지
4. 스마트폰 화면에서 읽기 좋은 길이로 작성할 것
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return jsonify({'success': True, 'text': response.text})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
