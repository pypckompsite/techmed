// next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: '/auth/register/',
        destination: 'http://127.0.0.1:8000/auth/register/', // dokładny adres FastAPI
      },
      {
        source: '/auth/login',
        destination: 'http://127.0.0.1:8000/auth/login', // dokładny adres FastAPI
      },
    ];
  },
};
