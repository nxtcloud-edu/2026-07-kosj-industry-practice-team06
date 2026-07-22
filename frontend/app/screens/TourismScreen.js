'use client';
import { useState, useEffect } from 'react';

const courseTemplates = [
  { name: '축제 → 내 가게 → 관광지', steps: (f, s, sp) => [{ n: f, t: '출발', h: false }, { n: `☕ ${s}`, t: '도보 5분', h: true }, { n: sp, t: '차량 15분', h: false }] },
  { name: '관광지 → 내 가게 → 축제', steps: (f, s, sp) => [{ n: sp, t: '출발', h: false }, { n: `☕ ${s}`, t: '차량 15분', h: true }, { n: f, t: '도보 5분', h: false }] },
  { name: '내 가게 중심 코스', steps: (f, s, sp) => [{ n: `☕ ${s}`, t: '출발', h: true }, { n: f, t: '도보 5분', h: false }, { n: sp, t: '차량 10분', h: false }, { n: `☕ ${s} (복귀)`, t: '도보 10분', h: true }] },
];

export default function TourismScreen({ store }) {
  const [spots, setSpots] = useState([]);
  const [festivals, setFestivals] = useState([]);
  const [courseIdx, setCourseIdx] = useState(0);
  const [source, setSource] = useState('');

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const res = await fetch('/api/tourism/data', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ lat: store.lat, lng: store.lng }) });
      const d = await res.json();
      if (d.success) {
        setSpots(d.spots || []);
        setFestivals(d.festivals || []);
        setSource(d.festivals_source || '');
      }
    } catch {
      setSpots([{ title: '세종호수공원', address: '세종시 연기면', type: '관광지' }]);
      setFestivals([{ title: '조치원 복숭아 축제', start_date: '20250725', end_date: '20250727', address: '세종시 조치원읍', type: '축제' }]);
    }
  };

  const fName = festivals[0]?.title || '축제장';
  const spName = spots[0]?.title || '세종호수공원';
  const course = courseTemplates[courseIdx % courseTemplates.length];
  const steps = course.steps(fName, store.name, spName);

  return (
    <div>
      <div className="page-header"><h1>관광 연계</h1><p>내 가게 주변 관광지·축제</p></div>

      {/* 축제 */}
      {festivals.length > 0 && (
        <div style={{ padding: '0 16px' }}><h3 style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-light)', margin: '12px 0 4px' }}>🎉 축제·행사 {source && <span className={`badge ${source === 'TourAPI' ? 'badge-api' : 'badge-sample'}`} style={{ marginLeft: '6px' }}>{source}</span>}</h3></div>
      )}
      {festivals.map((f, i) => (
        <div key={i} className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <div><h3 style={{ fontSize: '14px', fontWeight: 700 }}>🎉 {f.title}</h3><p style={{ fontSize: '12px', color: 'var(--text-light)', marginTop: '4px' }}>{f.start_date || ''}~{f.end_date || ''} | {f.address || ''}</p></div>
            <span className="badge badge-festival">축제</span>
          </div>
        </div>
      ))}

      {/* 관광지 */}
      {spots.length > 0 && (
        <div style={{ padding: '0 16px' }}><h3 style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-light)', margin: '16px 0 4px' }}>🏞️ 주변 관광지</h3></div>
      )}
      {spots.map((s, i) => (
        <div key={i} className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <div><h3 style={{ fontSize: '14px', fontWeight: 700 }}>🏞️ {s.title}</h3><p style={{ fontSize: '12px', color: 'var(--text-light)', marginTop: '4px' }}>{s.address || ''}</p></div>
            <span className="badge badge-season">관광지</span>
          </div>
        </div>
      ))}

      {/* 추천 코스 */}
      <div style={{ padding: '16px 16px 4px' }}><h3 style={{ fontSize: '14px', fontWeight: 700 }}>추천 코스</h3></div>
      <div className="card">
        <p style={{ fontSize: '11px', color: 'var(--text-light)', marginBottom: '12px' }}>코스 {courseIdx % courseTemplates.length + 1}/{courseTemplates.length}: {course.name}</p>
        {steps.map((s, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: i < steps.length - 1 ? '14px' : 0 }}>
            <div style={{ width: '28px', height: '28px', borderRadius: '50%', background: s.h ? 'var(--primary)' : 'var(--border)', color: s.h ? 'white' : 'var(--text)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '12px', fontWeight: 700 }}>{i + 1}</div>
            <div><p style={{ fontSize: '13px', fontWeight: 600 }}>{s.n}</p><p style={{ fontSize: '11px', color: 'var(--text-light)' }}>{s.t}</p></div>
          </div>
        ))}
      </div>
      <div style={{ padding: '0 16px 8px' }}><button className="btn-outline" style={{ width: '100%' }} onClick={() => setCourseIdx(courseIdx + 1)}>🔄 다른 코스 보기</button></div>
      <div style={{ padding: '0 16px 24px' }}><button className="btn btn-primary">🎨 이 코스로 홍보물 만들기</button></div>
    </div>
  );
}
