"""진흥원(발주기관) 성과 대시보드 API — contents+stores 집계 (제안서 6장·화면8)

팀원 스키마(contents·stores)를 그대로 읽어 관내 전체 성과를 집계한다.
효과 지표(조회·방문·쿠폰)는 스키마 변경 없이 조회 시점에 추정 계산한다(추정치).
"""
import csv
import io
from datetime import date, datetime

from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel

from app.database import get_db

router = APIRouter()

# 세종 2026 축제 (시즌·축제 캘린더). 실 서비스에선 TourAPI 연동.
FESTIVALS_2026 = [
    {"title": "조치원 복숭아 축제", "start": "2026-07-25", "end": "2026-07-27", "place": "조치원읍 문화로 일원"},
    {"title": "세종 여름 빛축제", "start": "2026-08-14", "end": "2026-08-17", "place": "세종호수공원"},
    {"title": "세종 전통시장 한마당", "start": "2026-09-19", "end": "2026-09-20", "place": "조치원 전통시장"},
    {"title": "세종 한글날 문화축제", "start": "2026-10-09", "end": "2026-10-11", "place": "세종 정부청사 일원"},
    {"title": "세종 가을 국화축제", "start": "2026-10-24", "end": "2026-11-01", "place": "세종중앙공원"},
]


@router.get("/calendar")
def calendar():
    """시즌·축제 캘린더 — 다가오는 축제 D-day (선제 지원 계획용)"""
    today = date.today()
    items = []
    for f in FESTIVALS_2026:
        start = datetime.strptime(f["start"], "%Y-%m-%d").date()
        end = datetime.strptime(f["end"], "%Y-%m-%d").date()
        dday = (start - today).days
        status = "종료" if today > end else ("진행중" if start <= today <= end else "예정")
        items.append({**f, "dday": dday, "status": status})
    items.sort(key=lambda x: x["start"])
    return {"success": True, "today": today.isoformat(), "festivals": items}


@router.get("/insights")
def insights():
    """정책 인사이트 — 업종·시즌별 수요 (다음 사업 기획 근거, 제안서 6장)"""
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT c.id, c.festival_info, c.created_at, s.category "
            "FROM contents c LEFT JOIN stores s ON c.store_id = s.id"
        ).fetchall()
    finally:
        conn.close()

    total = len(rows)
    cat, month, linked = {}, {}, 0
    for r in rows:
        ct = r["category"] or "미등록"
        cat[ct] = cat.get(ct, 0) + 1
        ym = str(r["created_at"])[:7]
        if len(ym) == 7:
            month[ym] = month.get(ym, 0) + 1
        linked += _linked(r["festival_info"])

    by_cat = sorted([{"category": k, "count": v} for k, v in cat.items()], key=lambda x: -x["count"])
    peak = max(month, key=month.get) if month else None
    top = by_cat[0]["category"] if by_cat else "-"
    rate = round(linked / total * 100) if total else 0

    findings = [
        f"수요가 가장 높은 업종은 '{top}'입니다. 다음 지원사업·교육 편성 시 우선 대상으로 검토할 수 있습니다.",
        f"전체 게시의 {rate}%가 축제와 연계되어, 축제-상권 연계 마케팅 수요가 뚜렷합니다.",
    ]
    if peak:
        findings.append(f"게시가 가장 활발한 시기는 {int(peak[5:])}월로, 해당 시즌 집중 지원이 효과적입니다.")

    return {"success": True, "total": total, "by_category": by_cat,
            "festival_link_rate": rate, "peak_month": peak, "findings": findings}


def _linked(festival_info: str) -> int:
    """축제 연계 여부 — festival_info에 실제 축제가 담겼는지."""
    if not festival_info:
        return 0
    if "없음" in festival_info:
        return 0
    return 1


def _estimate_effect(linked: int, seed: int) -> tuple[int, int, int]:
    """추정 성과(조회·쿠폰·방문). 축제 연계가 더 큰 효과를 내도록 구성.
    실측이 아니라 시연용 추정 — 실 서비스 시 SNS 인사이트·POS로 대체."""
    if linked:
        return (1200 + seed * 40, 12 + (seed % 5), 42 + (seed % 6))
    return (420 + seed * 25, 4 + (seed % 3), 15 + (seed % 4))


@router.get("/stats")
def stats():
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT c.id, c.store_id, c.user_input, c.festival_info, c.created_at, "
            "       s.name AS store_name, s.category AS category, s.address AS address "
            "FROM contents c LEFT JOIN stores s ON c.store_id = s.id "
            "ORDER BY c.id DESC"
        ).fetchall()
        stores_total = conn.execute("SELECT COUNT(*) FROM stores").fetchone()[0]
    finally:
        conn.close()

    total = len(rows)
    active = set()
    linked_posts = 0
    tv = tc = tvis = 0
    lviews, nviews, lvis, nvis = [], [], [], []
    cat_count, store_agg, recent, month_count = {}, {}, [], {}

    for r in rows:
        lk = _linked(r["festival_info"])
        linked_posts += lk
        ym = str(r["created_at"])[:7]  # 'YYYY-MM'
        if len(ym) == 7:
            month_count[ym] = month_count.get(ym, 0) + 1
        v, c, vis = _estimate_effect(lk, r["id"])
        tv += v; tc += c; tvis += vis
        (lviews if lk else nviews).append(v)
        (lvis if lk else nvis).append(vis)
        if r["store_id"]:
            active.add(r["store_id"])
        cat = r["category"] or "미등록"
        cat_count[cat] = cat_count.get(cat, 0) + 1
        key = r["store_id"] or 0
        if key not in store_agg:
            store_agg[key] = {"name": r["store_name"] or "미등록 가게", "category": cat,
                              "address": r["address"] or "", "posts": 0, "linked": 0}
        store_agg[key]["posts"] += 1
        store_agg[key]["linked"] += lk
        if len(recent) < 10:
            recent.append({"store_name": r["store_name"] or "미등록 가게",
                           "user_input": r["user_input"], "category": cat,
                           "created_at": str(r["created_at"]), "festival_linked": lk})

    def avg(xs):
        return round(sum(xs) / len(xs), 1) if xs else 0

    linked_avg, normal_avg = avg(lviews), avg(nviews)
    uplift = round((linked_avg / normal_avg - 1) * 100) if normal_avg else 0

    return {
        "success": True,
        "total_posts": total,
        "festival_linked_posts": linked_posts,
        "stores_total": stores_total,
        "active_stores": len(active),
        "by_category": sorted([{"category": k, "count": v} for k, v in cat_count.items()],
                              key=lambda x: -x["count"]),
        "by_store": sorted([dict(s) for s in store_agg.values()], key=lambda x: -x["posts"]),
        "trend": [{"ym": k, "count": month_count[k]} for k in sorted(month_count)],
        "recent": recent,
        "effect": {
            "total_views": tv, "total_coupons": tc, "total_visits": tvis,
            "linked": {"avg_views": linked_avg, "avg_visits": avg(lvis), "count": len(lviews)},
            "normal": {"avg_views": normal_avg, "avg_visits": avg(nvis), "count": len(nviews)},
            "uplift_pct": uplift,
        },
    }


# 사업 성과지표 (관공서 KPI). 목표값(target)은 DB에 저장 — 담당자가 협약 기준으로 수정.
GOAL_META = [
    {"key": "stores", "label": "참여 소상공인", "unit": "곳", "estimate": False, "default": 15},
    {"key": "posts", "label": "생성·게시 콘텐츠", "unit": "건", "estimate": False, "default": 30},
    {"key": "linked", "label": "축제 연계 캠페인", "unit": "건", "estimate": False, "default": 15},
    {"key": "reach", "label": "추정 도달 (누적)", "unit": "회", "estimate": True, "default": 40000},
]


def _get_targets(conn) -> dict:
    """목표값을 DB에서 로드 (없으면 기본값 시드)."""
    conn.execute("CREATE TABLE IF NOT EXISTS goal_targets (key TEXT PRIMARY KEY, target INTEGER)")
    for m in GOAL_META:
        conn.execute("INSERT OR IGNORE INTO goal_targets (key, target) VALUES (?,?)",
                     (m["key"], m["default"]))
    conn.commit()
    return {r["key"]: r["target"] for r in conn.execute("SELECT key, target FROM goal_targets").fetchall()}


class TargetUpdate(BaseModel):
    targets: dict  # {key: 목표값}


@router.get("/goals")
def goals():
    """사업 성과 목표 대비 달성률 (관공서 사업관리 KPI)"""
    conn = get_db()
    try:
        targets = _get_targets(conn)
        total = conn.execute("SELECT COUNT(*) FROM contents").fetchone()[0]
        active = conn.execute(
            "SELECT COUNT(DISTINCT store_id) FROM contents WHERE store_id IS NOT NULL").fetchone()[0]
        rows = conn.execute("SELECT id, festival_info FROM contents").fetchall()
    finally:
        conn.close()

    linked = sum(_linked(r["festival_info"]) for r in rows)
    reach = sum(_estimate_effect(_linked(r["festival_info"]), r["id"])[0] for r in rows)
    current = {"stores": active, "posts": total, "linked": linked, "reach": reach}

    goals = []
    for m in GOAL_META:
        target = targets.get(m["key"], m["default"])
        cur = current[m["key"]]
        rate = min(100, round(cur / target * 100)) if target else 0
        goals.append({**m, "target": target, "current": cur, "rate": rate})

    overall = round(sum(g["rate"] for g in goals) / len(goals)) if goals else 0
    status = ("목표 초과 달성" if overall >= 100 else "순조롭게 진행 중" if overall >= 30 else "진행 초기")
    return {
        "success": True,
        "program": "2026 소상공인 마케팅 지원사업",
        "period": "2026.01.01 ~ 2026.12.31",
        "overall": overall, "status": status, "goals": goals,
    }


@router.post("/goals/targets")
def update_targets(body: TargetUpdate):
    """목표값 수정 (담당자 설정)"""
    conn = get_db()
    try:
        _get_targets(conn)  # 테이블 보장
        for key, val in body.targets.items():
            try:
                conn.execute("UPDATE goal_targets SET target=? WHERE key=?", (int(val), key))
            except (ValueError, TypeError):
                continue
        conn.commit()
        return {"success": True}
    finally:
        conn.close()


@router.get("/stores")
def stores():
    """관내 등록·참여 가게 목록 (가게 탭). festival_linked는 festival_info로 파이썬 판정."""
    conn = get_db()
    try:
        store_rows = conn.execute(
            "SELECT id, name, category, address FROM stores ORDER BY id").fetchall()
        content_rows = conn.execute(
            "SELECT store_id, festival_info FROM contents").fetchall()
    finally:
        conn.close()

    agg = {s["id"]: {"id": s["id"], "name": s["name"], "category": s["category"],
                     "address": s["address"], "posts": 0, "linked": 0} for s in store_rows}
    for c in content_rows:
        if c["store_id"] in agg:
            agg[c["store_id"]]["posts"] += 1
            agg[c["store_id"]]["linked"] += _linked(c["festival_info"])
    result = sorted(agg.values(), key=lambda x: (-x["posts"], x["id"]))
    return {"success": True, "total": len(result), "stores": result}


@router.get("/export.csv")
def export_csv():
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT s.name AS store, s.category AS cat, s.address AS addr, "
            "       c.user_input AS inp, c.festival_info AS fest, c.created_at AS ts "
            "FROM contents c LEFT JOIN stores s ON c.store_id = s.id ORDER BY c.id DESC"
        ).fetchall()
    finally:
        conn.close()

    buf = io.StringIO()
    buf.write("﻿")  # 엑셀 한글 깨짐 방지
    w = csv.writer(buf)
    w.writerow(["가게명", "업종", "주소", "입력내용", "축제연계", "생성일시"])
    for r in rows:
        w.writerow([r["store"] or "미등록", r["cat"] or "", r["addr"] or "",
                    r["inp"], "Y" if _linked(r["fest"]) else "N", r["ts"]])
    return Response(content=buf.getvalue(), media_type="text/csv; charset=utf-8",
                    headers={"Content-Disposition": "attachment; filename=sejong_marketing_report.csv"})
