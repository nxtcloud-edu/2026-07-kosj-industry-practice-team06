# 🍑 AI 기반 소상공인 마케팅·상권분석 및 관광 연계 플랫폼

> **공고번호** 2026-세종-0004 | **제안사** 2026_고대세종_기업인턴십_6팀

## 서비스 한 줄 요약

> "사장님이 이미 아는 현장 맥락을 자연어 한 문장으로 입력하면, 상권·관광 데이터와 결합해 바로 쓸 수 있는 SNS 콘텐츠가 나오는 서비스."

소상공인이 **"복숭아 제철이니 복숭아 케이크 홍보물 만들어줘"** 라고 입력하면, 상권 공공데이터(주변 업종·경쟁 현황)와 관광 데이터(축제·관광지 일정)를 자동으로 결합해 **근거 있는 홍보 콘텐츠**를 생성하는 모바일 웹 플랫폼입니다.

## 차별점

| # | 기존 서비스 | 본 서비스 |
|---|------------|-----------|
| 1 | 복잡한 메뉴 선택 | 자연어 한 문장으로 시작 |
| 2 | 상권 데이터만 분석 | 상권 + 관광 데이터 결합 (축제·관광객 활용) |
| 3 | 분석 리포트에서 끝 | 바로 게시할 수 있는 콘텐츠까지 생성 |

## 서비스 흐름

```
💬 자연어 입력 → 🗂️ 데이터 결합 → 🤖 AI 생성+검수 → 📱 바로 게시
                  (상권 API·TourAPI)  (금지어 점검·근거 표시)  (캡션·배너)
```

## 핵심 기능

| ID | 기능 | 설명 |
|----|------|------|
| SFR-002 | 자연어 → 콘텐츠 생성 | 한 문장 입력 → LLM이 인스타 캡션·배너 문구 생성 |
| SFR-001 | 상권 리포트 | 주소 기반 반경 내 업종·경쟁 현황 + AI 자연어 인사이트 |
| SFR-003 | 관광 연계 추천 | 반경 내 관광지·축제 자동 매칭 + 방문 코스 구성 |
| SFR-004 | 시즌·이벤트 선제 제안 | 축제 일정 기반 "D-7, 지금 준비하세요" 카드 |
| COR-001 | 게시 전 검수 | 금지어 자동 필터링 + 생성 근거 데이터 표시 |

## 기술 스택

| 영역 | 기술 | 선정 이유 |
|------|------|-----------|
| 프론트엔드 | Next.js (React) | 모바일 우선 반응형, Vercel 무료 배포 |
| 백엔드 | FastAPI (Python) | AI/데이터 처리 최적, Gemini SDK 연동 |
| AI | Google Gemini API | 무료 티어, 카드 등록 불필요 |
| DB | SQLite | 설치 불필요, 가게·콘텐츠 이력 저장 |
| 외부 API | 상권정보 API, TourAPI 4.0 | 무료 공공데이터 |

## 프로젝트 구조

```
├── backend/                    ← FastAPI 서버 (메인)
│   ├── app/
│   │   ├── main.py             ← FastAPI 앱 + HTML 서빙
│   │   ├── config.py           ← 환경변수·좌표·DB경로
│   │   ├── database.py         ← SQLite 초기화·연결
│   │   ├── routers/
│   │   │   ├── content.py      ← 콘텐츠 생성 API (SFR-002)
│   │   │   ├── market.py       ← 상권 분석 API (SFR-001)
│   │   │   ├── tourism.py      ← 관광 연계 API (SFR-003)
│   │   │   └── stores.py       ← 가게 관리 API (DAR-003)
│   │   └── services/
│   │       ├── llm.py          ← Gemini 호출 (레거시)
│   │       ├── filter.py       ← 금지어 필터링 (COR-001)
│   │       ├── market_api.py   ← 상권정보 API 연동
│   │       └── tour_api.py     ← TourAPI 연동
│   ├── requirements.txt
│   ├── store.db                ← SQLite DB (자동 생성)
│   └── .env.example
├── templates/
│   └── index.html              ← 프론트엔드 SPA (모바일 웹앱)
├── frontend/                   ← Next.js 프론트엔드 (React)
│   ├── app/
│   │   ├── layout.js           ← 루트 레이아웃
│   │   ├── page.js             ← 메인 페이지 (탭 전환)
│   │   ├── globals.css         ← 전역 스타일
│   │   └── screens/            ← 화면 컴포넌트
│   │       ├── RegisterScreen.js
│   │       ├── HomeScreen.js
│   │       ├── ResultScreen.js
│   │       ├── ReportScreen.js
│   │       ├── TourismScreen.js
│   │       └── SettingsScreen.js
│   ├── next.config.js          ← API 프록시 설정
│   └── package.json
├── app.py                      ← Flask 프로토타입 (레거시)
├── .env                        ← API 키 (gitignore 대상)
├── .gitignore
└── README.md
```

## 실행 방법

### Backend (FastAPI + SQLite)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 http://localhost:3000 접속 (모바일 뷰 권장)

> FastAPI(8000)와 Next.js(3000)를 동시에 실행해야 합니다. Next.js가 `/api/*` 요청을 FastAPI로 프록시합니다.

## 환경변수

`backend/.env.example`을 참고하여 프로젝트 루트에 `.env` 파일을 생성하세요.

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATA_API_KEY=your_public_data_api_key_here
```

| 키 | 용도 | 발급처 |
|----|------|--------|
| GEMINI_API_KEY | AI 콘텐츠 생성 | [Google AI Studio](https://aistudio.google.com/) |
| DATA_API_KEY | 상권정보 + TourAPI | [data.go.kr](https://www.data.go.kr/) |

> ⚠️ **API 키는 절대 커밋하지 마세요!** `.gitignore`에 `.env`가 포함되어 있습니다.

## 팀 역할

| 역할 | 담당 범위 |
|------|-----------|
| A: 프론트엔드 | 모바일 웹 UI, 사용자 플로우, 시연 자료 |
| B: 백엔드 + AI | API 서버, LLM 연동, 프롬프트 설계, 금지어 검수 |
| C: 데이터 + 연동 | 상권 API·TourAPI 연동, DB 설계 |

## 라이선스

본 프로젝트는 2026년 고려대학교 세종캠퍼스 기업인턴십 교육 과제입니다.
