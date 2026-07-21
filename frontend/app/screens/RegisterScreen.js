'use client';
import { useState } from 'react';

export default function RegisterScreen({ onRegistered }) {
  const [name, setName] = useState('');
  const [address, setAddress] = useState('세종시 조치원읍');
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

  const save = () => {
    if (!name) { alert('가게 이름을 입력해주세요'); return; }
    onRegistered({ name, address, category, menus, menu: menus.map(m => `${m.name} ${m.price ? m.price + '원' : ''}`).join(' · '), lat: 36.604561, lng: 127.298342 });
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
        <div style={{ marginBottom: '14px' }}><label>위치</label><input value={address} onChange={e => setAddress(e.target.value)} /></div>
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
