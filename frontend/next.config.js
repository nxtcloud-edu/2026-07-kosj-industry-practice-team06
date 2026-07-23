/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://two026-07-kosj-industry-practice-team06.onrender.com/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
