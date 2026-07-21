'use client';
import { useState, useEffect } from 'react';

const courseTemplates = [
  { name: '축제 → 내 가게 → 관광지', steps: (f, s) => [{ n: f, t: '출발', h: false }, { n: `☕ ${s}`, t: '도보 5분', h: true }, { n: '세종호수공원', t: '차량 15분', h: false }] },
  { name: '관광지 → 내 가게 → 축제', steps: (f, s) => [{ n: '세종호수공원', t: '출발', h: false }, { n: `☕ ${s}`, t: '차량 15분', h: true }, { n: f, t: '도보 5분', h: false }] },
  { name: '내 가게 중심 코스', steps: (f, s) => [{ n: `☕ ${s}`, t: '출발', h: true }, { n: f, t: '도보 5분', h: false }, { n: '조치원역 근대문화거리', t: '도보 8분', h: false }, { n: `☕ ${s} (복귀)`, t: '도보 10분', h: true }] },
];

export default function TourismScreen({ store }) {
  const [festivals, setFestivals] = useState([]);
  const [courseIdx, setCourseIdx] = useState(0);

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const res = await fetch('/api/tourism/festivals', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ lat: store.lat, lng: store.lng }) });
      const d = await res.json();
      if (d.success && d.festivals.length) setFestivals(d.festivals);
      else setFestivals([{ title: '조치원 복숭아 축제', start_date: '20250725', end_date: '20250727', address: '세종시 조치원읍' }]);
    } catch { setFestivals([{ title: '조치원 복숭아 축제', start_date: '20250725', end_date: '20250727', address: '세종시 조치원읍' }]); }
  };

  const fName = festivals[0]?.title || '축제장';
  const course = courseTemplates[courseIdx % courseTemplates.length];
  const steps = course.steps(fName, store.name);

  return (
    <div>
      <div className="page-header"><h1>관광 연계</h1><p>내 가게 주변 관광지·축제</p></div>
      {festivals.map((f, i) => (
        <div key={i} className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <div><h3 style={{ fontSize: '14px', fontWeight: 700 }}>🎉 {f.title}</h3><p style={{ fontSize: '12px', color: 'var(--text-light)', marginTop: '4px' }}>{f.start_date || ''}~{f.end_date || ''} | {f.address || ''}</p></div>
            <span className="badge badge-festival">축제</span>
          </div>
        </div>
      ))}
      <div style={{ padding: '12px 16px 4px' }}><h3 style={{ fontSize: '14px', fontWeight: 700 }}>추천 코스</h3></div>
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
