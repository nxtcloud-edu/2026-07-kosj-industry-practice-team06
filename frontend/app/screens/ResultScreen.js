'use client';
import { useState } from 'react';

const templateThemes = [
  { gradient: 'linear-gradient(135deg, #667eea, #764ba2)', emoji: '☕', vibe: '따뜻한 한 잔의 여유' },
  { gradient: 'linear-gradient(135deg, #11998e, #38ef7d)', emoji: '🍑', vibe: '자연이 키운 신선함' },
  { gradient: 'linear-gradient(135deg, #ee9ca7, #ffdde1)', emoji: '🍰', vibe: '달콤한 하루의 시작' },
  { gradient: 'linear-gradient(135deg, #4facfe, #00f2fe)', emoji: '✨', vibe: '특별한 오늘' },
];

export default function ResultScreen({ result, store, onBack, onRegenerate, onUpdate }) {
  const [editing, setEditing] = useState(false);
  const [caption, setCaption] = useState(result.instagram || '');
  const [banner, setBanner] = useState(result.banner || '');
  const [tplIdx, setTplIdx] = useState(0);
  const [regenerating, setRegenerating] = useState(false);

  const theme = templateThemes[tplIdx % templateThemes.length];
  const hasProhibited = /전국 1위|최고|무조건|100%|완벽|절대/.test(result.instagram + result.banner);

  const saveEdit = () => { onUpdate({ ...result, instagram: caption, banner }); setEditing(false); };
  const doRegenerate = async () => { setRegenerating(true); await onRegenerate(); setRegenerating(false); };
  const copy = () => { navigator.clipboard.writeText(`${result.instagram}\n\n${result.banner}`); };

  // result가 바뀌면 편집 필드도 갱신
  if (result.instagram !== caption && !editing) { setCaption(result.instagram || ''); setBanner(result.banner || ''); }

  return (
    <div>
      <div className="page-header">
        <button onClick={onBack} style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.1rem' }}>← 뒤로</button>
        <h1 style={{ marginTop: '8px' }}>생성된 콘텐츠</h1>
      </div>

      {/* 템플릿 이미지 */}
      <div className="card">
        <h3 style={{ fontSize: '13px', fontWeight: 700, marginBottom: '10px' }}>🖼️ 템플릿 이미지 미리보기</h3>
        <div style={{ width: '100%', aspectRatio: '1', background: theme.gradient, borderRadius: '14px', padding: '28px 24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', position: 'relative', overflow: 'hidden' }}>
          <div style={{ position: 'absolute', top: '-30px', right: '-30px', width: '120px', height: '120px', borderRadius: '50%', background: 'rgba(255,255,255,0.12)' }} />
          <div style={{ position: 'absolute', bottom: '-40px', left: '-20px', width: '150px', height: '150px', borderRadius: '50%', background: 'rgba(255,255,255,0.1)' }} />
          <div style={{ position: 'relative', zIndex: 1 }}>
            <div style={{ display: 'inline-block', background: 'rgba(255,255,255,0.2)', padding: '4px 12px', borderRadius: '16px', fontSize: '11px', color: 'rgba(255,255,255,0.9)' }}>📍 {store.address}</div>
            <p style={{ fontSize: '13px', color: 'rgba(255,255,255,0.8)', marginTop: '6px' }}>{store.name}</p>
          </div>
          <div style={{ position: 'relative', zIndex: 1, textAlign: 'center', padding: '0 8px' }}>
            <span style={{ fontSize: '2.2rem' }}>{theme.emoji}</span>
            <h2 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'white', marginTop: '8px', lineHeight: 1.5, wordBreak: 'keep-all', overflowWrap: 'break-word', textShadow: '0 2px 8px rgba(0,0,0,0.15)' }}>{result.banner || ''}</h2>
          </div>
          <div style={{ position: 'relative', zIndex: 1, textAlign: 'center' }}>
            <p style={{ fontSize: '11px', color: 'rgba(255,255,255,0.7)', fontStyle: 'italic' }}>{theme.vibe}</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '8px', marginTop: '10px' }}>
          <button className="btn-outline" style={{ flex: 1 }} onClick={() => setTplIdx(tplIdx + 1)}>🎨 템플릿 변경</button>
        </div>
      </div>

      {/* 근거 */}
      <div className="card">
        <h3 style={{ fontSize: '13px', fontWeight: 700, marginBottom: '10px' }}>📋 이 콘텐츠의 근거</h3>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
          <span className={`badge ${result.market_info ? 'badge-api' : 'badge-sample'}`}>{result.market_info ? '실제 API' : '샘플'}</span>
          <span style={{ fontSize: '13px' }}><strong>상가정보</strong> — {result.market_info || '샘플'}</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className={`badge ${result.festival_info?.includes('AI') ? 'badge-sample' : 'badge-api'}`}>{result.festival_info?.includes('없음') || result.festival_info?.includes('AI') ? 'AI 조사' : '실제 API'}</span>
          <span style={{ fontSize: '13px' }}><strong>관광정보</strong> — {result.festival_info || '샘플'}</span>
        </div>
      </div>

      {/* 검수 */}
      <div className="card">
        <h3 style={{ fontSize: '13px', fontWeight: 700, marginBottom: '8px' }}>게시 전 검수</h3>
        <div style={{ padding: '10px', borderRadius: '10px', background: hasProhibited ? '#fef2f2' : '#f0fdf4', border: `1px solid ${hasProhibited ? '#fecaca' : '#bbf7d0'}` }}>
          <p style={{ fontSize: '13px', fontWeight: 600, color: hasProhibited ? '#dc2626' : '#166534' }}>
            {hasProhibited ? '⚠️ 금지어가 포함되어 있습니다.' : '✅ 허위·과장 표현 점검 통과'}
          </p>
          {result.instagram?.includes('한정') && <p style={{ fontSize: '12px', color: 'var(--text-light)', marginTop: '4px' }}>💡 "한정 판매"는 실제 진행 여부를 확인해 주세요.</p>}
        </div>
      </div>

      {/* 캡션 */}
      <div className="card">
        <h3 style={{ fontSize: '13px', fontWeight: 700, marginBottom: '8px' }}>📸 인스타 캡션</h3>
        {editing ? <textarea rows={5} value={caption} onChange={e => setCaption(e.target.value)} style={{ resize: 'vertical' }} />
          : <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '10px', fontSize: '14px', lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>{result.instagram}</div>}
      </div>

      {/* 배너 */}
      <div className="card">
        <h3 style={{ fontSize: '13px', fontWeight: 700, marginBottom: '8px' }}>🎨 배너 문구</h3>
        {editing ? <input value={banner} onChange={e => setBanner(e.target.value)} />
          : <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '10px', fontSize: '14px', fontWeight: 600, textAlign: 'center' }}>{result.banner}</div>}
      </div>

      {/* 해시태그 */}
      {result.hashtags && <div className="card"><h3 style={{ fontSize: '13px', fontWeight: 700, marginBottom: '8px' }}>#️⃣ 추천 해시태그</h3><p style={{ fontSize: '14px', lineHeight: 1.7 }}>{result.hashtags}</p></div>}

      {/* 액션 */}
      <div style={{ padding: '0 16px', display: 'flex', gap: '8px' }}>
        {editing
          ? <><button className="btn-outline" style={{ flex: 1 }} onClick={saveEdit}>✅ 저장</button><button className="btn-outline" style={{ flex: 1 }} onClick={() => setEditing(false)}>취소</button></>
          : <><button className="btn-outline" style={{ flex: 1 }} onClick={() => setEditing(true)}>✏️ 문구 수정</button><button className="btn-outline" style={{ flex: 1 }} onClick={doRegenerate} disabled={regenerating}>{regenerating ? '⏳ 생성 중...' : '🔄 다시 생성'}</button></>
        }
      </div>
      <div style={{ padding: '12px 16px 24px' }}><button className="btn btn-primary" onClick={copy}>📋 텍스트 복사</button></div>
    </div>
  );
}
