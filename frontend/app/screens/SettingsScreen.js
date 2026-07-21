'use client';

export default function SettingsScreen({ store, onReset }) {
  return (
    <div>
      <div className="page-header"><h1>설정</h1><p>가게 정보 관리</p></div>
      <div className="card">
        <h3 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '14px' }}>내 가게 정보</h3>
        <div style={{ fontSize: '13px', lineHeight: 2.2 }}>
          <p><strong>가게 이름:</strong> {store.name}</p>
          <p><strong>위치:</strong> 📍 {store.address}</p>
          <p><strong>업종:</strong> {store.category}</p>
          <p><strong>대표 메뉴:</strong> {store.menu || '등록된 메뉴 없음'}</p>
        </div>
      </div>
      <div className="card">
        <h3 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '10px' }}>서비스 정보</h3>
        <div style={{ fontSize: '13px', color: 'var(--text-light)', lineHeight: 2 }}>
          <p>버전: 1.0.0 (MVP)</p>
          <p>백엔드: FastAPI + SQLite</p>
          <p>AI: Google Gemini API</p>
          <p>데이터: 상권정보API, TourAPI 4.0</p>
          <p>프론트엔드: Next.js</p>
          <p>제안사: 2026_고대세종_기업인턴십_6팀</p>
        </div>
      </div>
      <div style={{ padding: '0 16px' }}>
        <button className="btn" style={{ background: '#fef2f2', color: '#dc2626', border: '1px solid #fecaca' }} onClick={() => { if (confirm('가게 정보를 초기화하시겠습니까?')) onReset(); }}>
          가게 정보 초기화
        </button>
      </div>
    </div>
  );
}
