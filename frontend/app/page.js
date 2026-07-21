'use client';
import { useState, useEffect } from 'react';
import RegisterScreen from './screens/RegisterScreen';
import HomeScreen from './screens/HomeScreen';
import ResultScreen from './screens/ResultScreen';
import ReportScreen from './screens/ReportScreen';
import TourismScreen from './screens/TourismScreen';
import SavedScreen from './screens/SavedScreen';
import SettingsScreen from './screens/SettingsScreen';

export default function Page() {
  const [tab, setTab] = useState('home');
  const [store, setStore] = useState(null);
  const [result, setResult] = useState(null);
  const [lastInput, setLastInput] = useState('');
  const [variation, setVariation] = useState(0);
  const [savedContents, setSavedContents] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem('store');
    if (saved) setStore(JSON.parse(saved));
    const contents = localStorage.getItem('savedContents');
    if (contents) setSavedContents(JSON.parse(contents));
  }, []);

  const handleRegistered = (data) => {
    setStore(data);
    localStorage.setItem('store', JSON.stringify(data));
    setTab('home');
  };

  const handleGenerated = (data, input) => {
    setResult(data);
    setLastInput(input);
    setVariation(0);
    setTab('result');
  };

  const handleRegenerate = async () => {
    const next = variation + 1;
    setVariation(next);
    try {
      const res = await fetch('/api/content/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: lastInput, variation: next }),
      });
      const data = await res.json();
      if (data.success) setResult(data);
    } catch {}
  };

  const handleSave = (content) => {
    const item = { ...content, id: Date.now(), savedAt: new Date().toLocaleDateString('ko-KR') };
    const updated = [item, ...savedContents];
    setSavedContents(updated);
    localStorage.setItem('savedContents', JSON.stringify(updated));
  };

  const handleDelete = (id) => {
    const updated = savedContents.filter(c => c.id !== id);
    setSavedContents(updated);
    localStorage.setItem('savedContents', JSON.stringify(updated));
  };

  const handleViewSaved = (content) => {
    setResult(content);
    setTab('result');
  };

  if (!store) return <RegisterScreen onRegistered={handleRegistered} />;

  return (
    <>
      {tab === 'home' && <HomeScreen store={store} onGenerated={handleGenerated} />}
      {tab === 'result' && <ResultScreen result={result} store={store} onBack={() => setTab('home')} onRegenerate={handleRegenerate} onUpdate={setResult} onSave={handleSave} />}
      {tab === 'saved' && <SavedScreen contents={savedContents} onDelete={handleDelete} onView={handleViewSaved} />}
      {tab === 'report' && <ReportScreen store={store} />}
      {tab === 'tourism' && <TourismScreen store={store} />}
      {tab === 'settings' && <SettingsScreen store={store} onReset={() => { localStorage.removeItem('store'); localStorage.removeItem('savedContents'); setStore(null); setSavedContents([]); }} />}

      <nav className="bottom-nav">
        {[
          { id: 'home', icon: '🏠', label: '홈' },
          { id: 'saved', icon: '📁', label: '보관함' },
          { id: 'report', icon: '📊', label: '리포트' },
          { id: 'tourism', icon: '🗺️', label: '관광' },
          { id: 'settings', icon: '⚙️', label: '설정' },
        ].map(t => (
          <button key={t.id} className={`nav-item ${tab === t.id ? 'active' : ''}`} onClick={() => setTab(t.id)}>
            <span className="icon">{t.icon}</span>{t.label}
          </button>
        ))}
      </nav>
    </>
  );
}
