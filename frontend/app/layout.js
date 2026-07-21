import './globals.css';

export const metadata = {
  title: '마케팅AI - 소상공인 마케팅 플랫폼',
  description: 'AI 기반 소상공인 마케팅·상권분석 및 관광 연계 플랫폼',
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
