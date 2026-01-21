// vite.config.js
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
import { viteMockServe } from "vite-plugin-mock";

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    viteMockServe({
      mockPath: "mock", // 指定 mock 檔案存放路徑
      localEnabled: true, // 開發環境下開啟
    }),
  ],
  server: {
    host: "0.0.0.0", // 允許外部存取容器內的 Vite 服務
    port: 5173, // 確保與 compose.yml 的 port 一致
    watch: {
      usePolling: true, // 在 Windows 或某些環境下，確保存檔後畫面會自動更新
    },
  },
});
