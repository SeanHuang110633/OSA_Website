# 前後端 API 串接開發流程規範

本文檔說明如何在 OSA 系統中進行前後端 API 串接的標準作業流程 (SOP)，涵蓋 API 定義、組件開發規範以及整合測試環境的設置。

## 1. 在 Frontend/API 中建立請求模組

為了統一管理後端請求，請勿直接在 Vue 組件中撰寫 `axios` 或 `fetch` 程式碼，而是將 API 請求封裝在獨立的 JS 檔案中。

### 步驟說明：

1. **確認後端規格**：
   開發前，請先啟動後端服務，並訪問 Swagger UI 文件：`http://localhost:8000/docs`。
2. **利用 AI 加速開發**：
   在 Swagger UI頁面的上方，可以找到 `/openapi.json` 的連結。

- **技巧**：點擊該連結取得完整的 JSON 定義檔，將此 JSON 提供給 AI (如 ChatGPT/Claude/Gemini)。
- **提示詞範例**：_"這是後端的 openapi.json，請幫我根據 `/api/downloads` 的路徑，撰寫對應的 frontend/api/download.js 封裝程式碼，使用我們專案現有的 request.js 攔截器。"_

3. **建立檔案**：
   在 `frontend/src/api/` 目錄下建立對應的 `.js` 檔案（例如 `download.js`）。

```javascript
// src/api/download.js 範例
import request from "./request";

export function getDownloads(params) {
  return request({
    url: "/downloads/",
    method: "get",
    params,
  });
}
```

---

## 2. Vue 組件開發與命名規範

目前專案中的組件功能已開發完成，但為了符合 Vue 3 的最佳實踐與長期的維護性，我們需要遵循嚴格的命名規範。

### 命名規範：使用多單詞 (Multi-word) 命名

- **現狀 (不推薦)**：`Downloads.vue`, `News.vue`
- **最佳實踐 (推薦)**：`DownloadPage.vue` (或 `DownloadList.vue`), `NewsList.vue`

### 理由與優勢：

1. **避免與 HTML 元素衝突 (Priority A - Essential)**：
   HTML 規範中所有的原生標籤（如 `div`, `span`, `header`）都是單個單詞。Vue 官方強烈建議組件名稱至少包含兩個單詞，以確保未來 HTML 標準推出新標籤時（例如未來瀏覽器若推出 `<downloads>` 標籤），不會與我們的組件產生解析衝突。
2. **提高語意清晰度**：

- `DownloadPage.vue`：明確表示這是一個頁面級別的組件。
- `DownloadItem.vue`：明確表示這是列表中的單個項目組件。
  這樣的命名讓專案結構在檔案總管中一目了然。

### 開發步驟：

1. 在 `src/pages/` 或 `src/components/` 建立符合規範的組件 (如 `DownloadPage.vue`)。
2. 引入步驟 1 建立的 API 函數：

```javascript
import { getDownloads } from "@/api/download";
```

3. 在 `onMounted` 生命週期中呼叫 API 並將資料綁定至響應式變數 (ref/reactive)。

---

## 3. 啟動 Docker 進行整合測試

由於前端頁面需要顯示真實的資料庫內容，開發與測試時需依賴 Docker 環境來運行後端服務與資料庫。

### 測試流程：

直接用目前的docker環境測試就可以了，但如果之前有啟動過docker環境，可以先用 docker compose down -v 把它關掉再重啟(刪除舊的 volumn 以免資料對不齊)
