'use client';

export default function SavedScreen({ contents, onDelete, onView }) {
  return (
    <div>
      <div className="page-header">
        <h1>📁 보관함</h1>
        <p>저장한 콘텐츠를 관리하세요</p>
      </div>

      {contents.length === 0 && (
        <div className="card" style={{ textAlign: 'center', padding: '40px 20px' }}>
          <p style={{ fontSize: '2rem', marginBottom: '12px' }}>📭</p>
          <p style={{ color: 'var(--text-light)', fontSize: '14px' }}>저장한 콘텐츠가 없습니다.</p>
          <p style={{ color: 'var(--text-light)', fontSize: '13px', marginTop: '4px' }}>콘텐츠 생성 후 "저장" 버튼을 눌러보세요.</p>
        </div>
      )}

      {contents.map((item) => (
        <div key={item.id} className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
            <span style={{ fontSize: '11px', color: 'var(--text-light)' }}>{item.savedAt}</span>
            <button
              onClick={() => { if (confirm('이 콘텐츠를 삭제하시겠습니까?')) onDelete(item.id); }}
              style={{ background: 'none', border: 'none', color: 'var(--danger)', cursor: 'pointer', fontSize: '14px' }}
            >
              🗑️
            </button>
          </div>

          {/* 배너 미리보기 */}
          <div style={{ padding: '10px 14px', background: 'linear-gradient(135deg, #667eea20, #764ba220)', borderRadius: '10px', marginBottom: '10px' }}>
            <p style={{ fontSize: '14px', fontWeight: 600, textAlign: 'center' }}>{item.banner || '(배너 없음)'}</p>
          </div>

          {/* 캡션 미리보기 (2줄 제한) */}
          <p style={{ fontSize: '13px', color: 'var(--text-light)', lineHeight: 1.6, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
            {item.instagram || ''}
          </p>

          {/* 액션 */}
          <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
            <button
              className="btn-outline"
              style={{ flex: 1 }}
              onClick={() => onView(item)}
            >
              👁️ 상세보기
            </button>
            <button
              className="btn-outline"
              style={{ flex: 1 }}
              onClick={() => {
                navigator.clipboard.writeText(`${item.instagram}\n\n${item.banner}`);
                alert('복사 완료!');
              }}
            >
              📋 복사
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
