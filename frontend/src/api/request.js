// src/api/request.js
import axios from "axios";

const service = axios.create({
  // 改用 localhost 確保與您手動測試的環境一致
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  timeout: 15000, // 稍微調長一點點
});
// 可以在這裡加入 Request 攔截器 (例如自動帶入 Token)
service.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response 攔截器 (簡化錯誤處理)
service.interceptors.response.use(
  (response) => {
    // 如果後端回傳 2xx，直接回傳 data 部分
    return response.data;
  },
  (error) => {
    console.error("API Error:", error);
    return Promise.reject(error);
  },
);

export default service;