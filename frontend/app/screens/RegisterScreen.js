'use client';
import { useState } from 'react';

// 조치원읍 내 주요 위치 좌표 매핑
const locationPresets = {
  '세종시 조치원읍 (조치원역 근처)': { lat: 36.604561, lng: 127.298342 },
  '세종시 조치원읍 (조치원읍사무소 근처)': { lat: 36.601, lng: 127.297 },
  '세종시 조치원읍 (고려대 세종캠퍼스 근처)': { lat: 36.617, lng: 127.286 },
  '직접 입력': { lat: 36.604561, lng: 127.298342 },
};

export default function RegisterScreen({ onRegistered }) {
  const [name, setName] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('세종시 조치원읍 (조치원역 근처)');
  const [customAddress, setCustomAddress] = useState('');
  const [category, setCategory] = useState('개인카페');
  const [menuName, setMenuName] = useState('');
  const [menuPrice, setMenuPrice] = useState('');
  const [menus, setMenus] = useState([]);

  const addMenu = () => {
    if (!menuName) return;
    setMenus([...menus, { name: menuName, price: menuPrice }]);
    setMenuName(''); setMenuPrice('');
  };

  const removeMenu = (i) => setMenus(menus.filter((_, idx) => idx !== i));

  const save = async () => {
    if (!name) { alert('가게 이름을 입력해주세요'); return; }
    const address = selectedLocation === '직접 입력' ? customAddress : selectedLocation;
    let coords = locationPresets[selectedLocation] || locationPresets['세종시 조치원읍'];

    // 직접 입력 시 Gemini로 좌표 조회
    if (selectedLocation === '직접 입력' && customAddress) {
      try {
        const res = await fetch('/api/stores/geocode', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ address: customAddress }),
        });
        const data = await res.json();
        if (data.success) {
          coords = { lat: data.lat, lng: data.lng };
        }
      } catch {}
    }

    onRegistered({
      name,
      address,
      category,
      menus,
      menu: menus.map(m => `${m.name} ${m.price ? m.price + '원' : ''}`).join(' · '),
      lat: coords.lat,
      lng: coords.lng,
    });
  };

  return (
    <div style={{ padding: '40px 16px' }}>
      <div style={{ textAlign: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 800 }}>마케팅AI</h1>
        <p style={{ color: 'var(--text-light)', marginTop: '8px' }}>처음 오셨네요! 가게 정보를 알려주세요.</p>
      </div>
      <div className="card">
        <h2 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '16px' }}>내 가게 정보</h2>
        <div style={{ marginBottom: '14px' }}><label>가게 이름</label><input value={name} onChange={e => setName(e.target.value)} placeholder="예: 조치원 ○○카페" /></div>
        <div style={{ marginBottom: '14px' }}>
          <label>위치 (지역 선택)</label>
          <select value={selectedLocation} onChange={e => setSelectedLocation(e.target.value)}>
            {Object.keys(locationPresets).map(loc => (
              <option key={loc} value={loc}>{loc}</option>
            ))}
          </select>
          {selectedLocation === '직접 입력' && (
            <input style={{ marginTop: '8px' }} value={customAddress} onChange={e => setCustomAddress(e.target.value)} placeholder="주소를 입력하세요" />
          )}
        </div>
        <div style={{ marginBottom: '14px' }}><label>업종 선택</label>
          <select value={category} onChange={e => setCategory(e.target.value)}>
            <option value="개인카페">☕ 개인카페</option>
            <option value="농산물">🍎 농산물</option>
            <option value="식당">🍚 식당</option>
            <option value="소매">🛍️ 소매</option>
          </select>
        </div>
        <div style={{ marginBottom: '14px' }}><label>대표 메뉴 (선택)</label>
          <div style={{ display: 'flex', gap: '6px', marginBottom: '8px' }}>
            <input style={{ flex: 2 }} value={menuName} onChange={e => setMenuName(e.target.value)} placeholder="메뉴명" />
            <input style={{ flex: 1 }} value={menuPrice} onChange={e => setMenuPrice(e.target.value)} placeholder="가격" />
            <button onClick={addMenu} style={{ padding: '10px 14px', borderRadius: '10px', border: '1.5px solid var(--border)', background: 'white', cursor: 'pointer' }}>+</button>
          </div>
          {menus.map((m, i) => (
            <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid var(--border)', fontSize: '13px' }}>
              <span>{m.name}{m.price ? ` ${Number(m.price).toLocaleString()}원` : ''}</span>
              <button onClick={() => removeMenu(i)} style={{ background: 'none', border: 'none', color: 'var(--danger)', cursor: 'pointer' }}>✕</button>
            </div>
          ))}
        </div>
        <button className="btn btn-primary" onClick={save}>저장하고 시작하기</button>
      </div>
    </div>
  );
}
