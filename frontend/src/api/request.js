// src/api/request.js
import axios from "axios";

// 建立 axios 實體
const service = axios.create({
  // 使用 Vite 的環境變數，注意必須以 VITE_ 開頭
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api",
  timeout: 10000,
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
