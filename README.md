# 🍑 AI 기반 소상공인 마케팅·상권분석 및 관광 연계 플랫폼

> 2026 고려대 세종캠퍼스 기업인턴십 6팀

소상공인이 **자연어 한 문장**을 입력하면, 상권·관광 공공데이터를 근거로 결합하여 **바로 게시할 수 있는 SNS 홍보 콘텐츠**를 생성하는 모바일 웹 플랫폼입니다.

## 핵심 기능

| 기능 | 설명 |
|------|------|
| 자연어 콘텐츠 생성 | "복숭아 케이크 한정판매 홍보해줘" → 인스타 캡션 + 배너 문구 자동 생성 |
| 상권 리포트 | 주소 기반 인근 업종·경쟁 현황 요약 (상가정보 API) |
| 관광 연계 | TourAPI 축제/관광지 매칭 + 추천 코스 |
| 시즌 제안 | 축제·계절 기반 마케팅 선제 제안 |

## 프로젝트 구조

```
├── docs/               ← 기획 문서 (제안서, 와이어프레임)
├── backend/            ← FastAPI 서버
│   └── app/
│       ├── main.py
│       ├── routers/    ← API 엔드포인트
│       └── services/   ← 외부 API 연동·LLM 호출
├── frontend/           ← Next.js 모바일 웹
│   └── src/app/
└── prototypes/         ← 초기 API 테스트 스크립트
```

## 기술 스택

- **Frontend**: Next.js (모바일 우선 반응형)
- **Backend**: FastAPI (Python)
- **AI**: Google Gemini API (RAG 방식 콘텐츠 생성)
- **DB**: SQLite
- **외부 API**: 상가정보 API, TourAPI, 카카오맵 API

## 실행 방법

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # .env에 실제 API 키 입력
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 환경변수

`.env.example`을 참고하여 `backend/.env` 파일을 생성하세요.

```
GEMINI_API_KEY=your_gemini_api_key
DATA_API_KEY=your_public_data_api_key
KAKAO_API_KEY=your_kakao_api_key
```

> ⚠️ API 키는 절대 커밋하지 마세요!

## 팀 역할

| 역할 | 담당 |
|------|------|
| 프론트엔드 | 모바일 웹 UI, 사용자 흐름 |
| 백엔드·AI | API 서버, LLM 연동, 프롬프트 설계, 검수 필터 |
| 데이터·연동 | 상가정보·TourAPI·카카오맵 연동, DB 설계 |

## 라이선스

본 프로젝트는 교육 목적의 인턴십 과제입니다.
