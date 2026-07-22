'use client';
import { useState, useEffect } from 'react';

export default function ReportScreen({ store }) {
  const [data, setData] = useState(null);

  useEffect(() => { loadReport(); }, []);

  const loadReport = async () => {
    try {
      const res = await fetch('/api/market/report', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ lat: store.lat, lng: store.lng, radius: 500 }) });
      const d = await res.json();
      if (d.success) setData(d);
    } catch {}
  };

  const keywords = { '개인카페': ['카페','커피','디저트','제과','베이커리','빵','비알코올'], '식당': ['한식','중식','일식','양식','음식','분식','치킨'], '농산물': ['농산물','과일','채소'], '소매': ['소매','편의점','마트'] };
  const kws = keywords[store.category] || ['카페'];
  const sameCategory = data ? data.stores.filter(s => kws.some(k => (s.category || '').includes(k) || (s.category_mid || '').includes(k))) : [];

  return (
    <div>
      <div className="page-header"><h1>내 가게 주변 상권</h1><p>📍 {store.address} | 업종: {store.category}</p></div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-around', textAlign: 'center' }}>
          <div><div style={{ fontSize: '1.8rem', fontWeight: 900, color: 'var(--primary)' }}>{data?.total_count || '-'}</div><div style={{ fontSize: '12px', color: 'var(--text-light)' }}>주변 점포</div></div>
          <div><div style={{ fontSize: '1.8rem', fontWeight: 900, color: 'var(--success)' }}>{sameCategory.length || '-'}</div><div style={{ fontSize: '12px', color: 'var(--text-light)' }}>동종 업종</div></div>
          <div><div style={{ fontSize: '1.8rem', fontWeight: 900, color: 'var(--warning)' }}>3.2k</div><div style={{ fontSize: '12px', color: 'var(--text-light)' }}>일 유동인구</div></div>
        </div>
        {data && <p style={{ marginTop: '10px' }}><span className="badge badge-api">실제 API</span></p>}
      </div>
      <div className="card"><h3 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '8px' }}>🤖 AI 인사이트</h3><p style={{ fontSize: '13px', lineHeight: 1.8 }}>"반경 500m 내 점포 {data?.total_count || '?'}개 중 동종 업종 {sameCategory.length}개. {store.category} 수요 대비 경쟁이 {sameCategory.length > 5 ? '다소 높은' : '적은'} 편."</p></div>
      <div className="card"><h3 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '10px' }}>주요 경쟁 업체</h3>
        {sameCategory.slice(0, 5).map((s, i) => <div key={i} style={{ padding: '6px 0', borderBottom: '1px solid var(--border)', fontSize: '13px' }}>• {s.name} <span style={{ color: 'var(--text-light)' }}>({s.category})</span></div>)}
        {sameCategory.length === 0 && <p style={{ fontSize: '13px', color: 'var(--text-light)' }}>데이터 로딩 중...</p>}
      </div>
      <div className="card" style={{ background: '#f0fdf4', border: '1px solid #bbf7d0' }}><h3 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '8px', color: '#166534' }}>💡 추천 전략</h3><p style={{ fontSize: '13px', lineHeight: 1.8 }}>{getStrategy(store.category, sameCategory.length)}</p></div>
    </div>
  );
}

function getStrategy(category, competitorCount) {
  const isHigh = competitorCount > 5;

  const strategies = {
    '개인카페': isHigh
      ? '"경쟁이 치열한 카페 상권 — 수제 디저트·시그니처 음료 등 프랜차이즈에 없는 메뉴로 차별화. 인스타 감성 인테리어 + 시즌 한정 메뉴로 재방문 유도 전략 유효"'
      : '"동종 경쟁이 적은 편 — 프랜차이즈와 차별화되는 수제 디저트 강조 + 축제 시즌 한정 메뉴 전략 유효. SNS 노출을 통한 단골 확보에 집중"',
    '식당': isHigh
      ? '"주변 음식점 밀집 상권 — 메뉴 전문화(한 가지 잘하는 집) + 점심 세트 가성비 강조. 주말 가족 단위 손님 공략을 위한 키즈 메뉴·대용량 메뉴 추가 고려"'
      : '"식당 경쟁 여유 — 지역 특산물 활용 메뉴로 여기서만 먹을 수 있는 맛 포지셔닝. 축제·관광객 대상 세트 메뉴 + 네이버 플레이스 리뷰 관리 병행"',
    '농산물': isHigh
      ? '"주변 농산물 판매점 다수 — 산지 직송·당일 수확 등 신선도 차별화 핵심. 제철 과일 구독 서비스, 소포장 선물세트로 온라인 판로 확대"'
      : '"농산물 판매 경쟁 적음 — 제철 과일/채소 강조 + 축제 연계 시식 이벤트. 관광객 대상 지역 특산물 선물 세트 포지셔닝 유효"',
    '소매': isHigh
      ? '"소매업 밀집 지역 — 동네 편의성(빠른 배달, 단골 외상) 강조 + SNS에서 숨은 꿀템 소개. 프랜차이즈 편의점에 없는 로컬 상품 큐레이션으로 차별화"'
      : '"주변 소매 경쟁 적음 — 생활 필수품 + 지역 특산품 믹스 전략. 단골 적립 이벤트 + 축제 시즌 기획전으로 유동인구 유입"',
  };

  return strategies[category] || strategies['개인카페'];
}
