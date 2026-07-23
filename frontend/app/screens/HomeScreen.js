'use client';
import { useState, useEffect } from 'react';

export default function HomeScreen({ store, onGenerated }) {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => { fetchSuggestions(); }, []);

  const fetchSuggestions = async () => {
    try {
      const res = await fetch('/api/suggestions/', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lat: store.lat, lng: store.lng, address: store.address, category: store.category }),
      });
      const data = await res.json();
      if (data.success && data.suggestions) setSuggestions(data.suggestions);
    } catch {
      // 폴백 제안
      setSuggestions([
        { title: '☀️ 시즌 메뉴 홍보', desc: '지금 시기에 맞는 메뉴를 홍보해보세요.', type: '시즌', prompt: '시즌 메뉴 홍보물 만들어줘' },
        { title: '📈 주말 이벤트', desc: '주말 유동인구를 활용해보세요.', type: '상권', prompt: '주말 이벤트 홍보물 만들어줘' },
      ]);
    }
  };

  const generate = async () => {
    if (!input.trim()) return;
    setLoading(true);
    try {
      const res = await fetch('/api/content/generate', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: input,
          store_name: store.name,
          store_category: store.category,
          store_menus: store.menu || '',
          store_address: store.address,
          store_lat: store.lat,
          store_lng: store.lng,
        }),
      });
      const data = await res.json();
      if (data.success) onGenerated(data, input);
      else alert('오류: ' + (data.error || ''));
    } catch { alert('서버 연결 실패'); }
    finally { setLoading(false); }
  };

  return (
    <div>
      <div className="page-header">
        <h1>마케팅AI</h1>
        <p>{store.name} 사장님, 오늘은 뭘 홍보해볼까요?</p>
      </div>
      <div className="card">
        <textarea rows={3} style={{ resize: 'none', marginBottom: '12px' }} placeholder='"복숭아 제철이고 곧 축제 열리니까, 복숭아 케이크 한정판매 홍보물 만들어줘"' value={input} onChange={e => setInput(e.target.value)} />
        <button className="btn btn-primary" onClick={generate} disabled={loading || !input.trim()}>
          {loading ? <><span className="spinner" /> 생성 중...</> : '✨ 콘텐츠 만들기'}
        </button>
      </div>
      <div style={{ padding: '0 16px' }}><h3 style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-light)', margin: '16px 0 8px' }}>추천 제안</h3></div>
      {suggestions.map((s, i) => (
        <div key={i} className="card" style={{ cursor: 'pointer', borderLeft: '3px solid var(--primary)' }} onClick={() => setInput(s.prompt)}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <div><strong style={{ fontSize: '14px' }}>{s.title}</strong><p style={{ fontSize: '12px', color: 'var(--text-light)', marginTop: '4px' }}>{s.desc}</p></div>
            <span className={`badge badge-${s.type === '축제' ? 'festival' : s.type === '시즌' ? 'season' : 'area'}`}>{s.type}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
