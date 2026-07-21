# 진흥원 대시보드 시연용 데이터 시드 (팀원 stores/contents 스키마). contents 비어있을 때만 삽입.
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.database import get_db, init_db

STORES = [
    ("조치원 복숭아카페", "세종특별자치시 조치원읍 문화로", "카페"),
    ("세종 한우명가", "세종특별자치시 조치원읍 새내로", "식당"),
    ("조치원 로컬청과", "세종특별자치시 조치원읍 상리", "농산물"),
    ("신흥동 수제베이커리", "세종특별자치시 조치원읍 신흥리", "디저트"),
    ("조치원 알뜰문구", "세종특별자치시 조치원읍 원리", "소매"),
    ("세종 손칼국수", "세종특별자치시 조치원읍 침산리", "식당"),
]
# (store_idx, 입력, 축제연계) — 순환하며 사용
POST_TEMPLATES = [
    (0, "복숭아 축제 연계 한정판매 홍보물", True),
    (2, "제철 복숭아 직거래 홍보", True),
    (1, "복숭아 축제 방문객 대상 한우 특선", True),
    (3, "복숭아 생크림 케이크 신메뉴", True),
    (5, "축제 기간 야식 칼국수 홍보", True),
    (0, "주말 디저트 세트 할인 이벤트", False),
    (1, "여름 보양 메뉴 홍보", False),
    (2, "지역 농산물 꾸러미 소개", False),
    (3, "비 오는 날 따뜻한 스콘", False),
    (4, "신학기 문구 할인 안내", False),
    (5, "장마철 든든한 한 그릇", False),
]
# 월별 게시 건수 (성장 추이) — (연, 월, 건수). 합계 = 게시 총건수
MONTHLY_PLAN = [(2026, 2, 1), (2026, 3, 2), (2026, 4, 2), (2026, 5, 3), (2026, 6, 4), (2026, 7, 6)]

init_db()
conn = get_db()
if conn.execute("SELECT COUNT(*) FROM contents").fetchone()[0] > 0:
    print("contents already has data — skip seeding")
    conn.close()
    sys.exit(0)

ids = []
for name, addr, cat in STORES:
    cur = conn.execute(
        "INSERT INTO stores (name, address, lat, lng, category, menus) VALUES (?,?,?,?,?,?)",
        (name, addr, 36.604561, 127.298342, cat, "[]"),
    )
    ids.append(cur.lastrowid)

n = 0
t = 0  # POST_TEMPLATES 순환 인덱스
for year, month, count in MONTHLY_PLAN:
    for k in range(count):
        sidx, inp, linked = POST_TEMPLATES[t % len(POST_TEMPLATES)]
        t += 1
        day = min(3 + k * 6, 28)  # 월 안에서 날짜 분산
        ts = f"{year}-{month:02d}-{day:02d} 10:00:00"
        fest = ("[인근 축제] 조치원 복숭아 축제 (20250725~20250727, 세종 조치원읍)"
                if linked else "[인근 축제] 현재 등록된 세종시 축제 없음")
        conn.execute(
            "INSERT INTO contents (store_id, user_input, instagram, banner, hashtags, "
            "market_info, festival_info, model_used, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (ids[sidx], inp, "샘플 캡션", "샘플 배너", "#조치원 #세종",
             "주변 상가 915개", fest, "demo-seed", ts),
        )
        n += 1

conn.commit()
conn.close()
print(f"seeded: {len(STORES)} stores, {n} contents (월별 추이 반영)")
