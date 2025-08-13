import axios from 'axios';
import router from '../router/index.js';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // Django API 位址
  withCredentials: true // 如果要傳 JWT 或 Cookie
});


//請求攔截器:每支request出去前header加access token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});


// 回應攔截器：自動 refresh token
api.interceptors.response.use(
  response => response, //正常直接返回
  async error => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const res = await axios.post(
          'http://127.0.0.1:8000/api/token/refresh',
          {},
          { withCredentials: true }
        );
        localStorage.setItem('access_token', res.data.access);
        originalRequest.headers['Authorization'] = `Bearer ${res.data.access}`;
        return api(originalRequest);
      } catch (err) {
        console.error('Refresh token 過期，需要重新登入');
        router.push('/login')
      }
    }
    return Promise.reject(error);
  }
);

export default api;