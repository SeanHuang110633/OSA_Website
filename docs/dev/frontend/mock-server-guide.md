# Mock Server 使用說明勢

**Version** : v1
**Release Date** : 2026-01-21
**Author** : Sean

---

# 🚀 使用 Mock Server 實現前後端解耦

為了加快開發進度，減少前端對後端 API 開發進度的依賴，我已經在前端專案中導入了 **Mock Server (Vite-plugin-mock)** 機制。

現在大家在開發 UI 介面與邏輯時，不需要等待後端完成 API，也不需要啟動後端容器，即可直接取得測試資料進行開發。

## 💡 核心觀念

- **前後端並行**：只要 API 契約（Contract）定義好，大家就可以直接根據 Mock 資料開發畫面，不用等後端。
- **開發零依賴**：你現在只需執行 `pnpm dev` 啟動前端，就能跑通所有的 API 請求邏輯。

---

## 🛠️ 環境配置 (重要！)

由於安全性考量，環境變數設定檔 `.env.development` 並沒有上傳到 Git。**請大家在 `frontend/` 目錄下手動建立該檔案**，並填入以下內容：

```bash
# frontend/.env.development
# 確保 API 請求會打向 Vite 自身的 Mock Server
VITE_API_BASE_URL=/api

```

> **注意**：如果沒有這個檔案，Axios 可能會因為找不到 Base URL 或指向錯誤地址而導致 CORS 錯誤。

---

## 📖 如何使用 Mock API

當你在使用 Axios 發送請求時，請確保 **URL 路徑** 與 `frontend/mock/` 資料夾中定義的 `url` 完全一致。

### 以活動模組 (event.js) 為例：

我已經定義好了活動列表與詳情的資料。

#### 1. 調用方式範例 (Vue Component)：

```javascript
import axios from "axios";

// 取得活動列表
const fetchEvents = async () => {
  const res = await axios.get("/api/events/", {
    params: { locale: "zh-TW" },
  });
  console.log(res.data); // 這裏會拿到 mock/event.js 定義的假資料
};

// 取得活動詳情 (ID 為 1)
const fetchDetail = async () => {
  const res = await axios.get("/api/events/1");
  console.log(res.data);
};
```

---

## 🔍 特殊功能說明：下載專區 (download.js)

在 `download.js` 中，我實作了簡單的 **條件查詢模擬**。前端在開發篩選器時可以進行測試：

- **支援參數**：`type` (regulation/form) 與 `category` (分類 slug)。
- **範例**：`axios.get('/api/downloads/', { params: { type: 'form' } })` 會只回傳「表單」類的資料。
- **限制**：目前 Mock 尚未支援「根據檔名/標題關鍵字」查詢的功能，後續對接真實後端時會補齊。

---

## ➕ 如何新增資料？

目前我在 `mock/` 下建立了三個檔案：`event.js`, `member.js`, `download.js`。
如果你覺得假資料不夠多，或者需要測試特定情況（如：資料為空、超長字串等）：

1. 找到對應的 `.js` 檔案。
2. 依據現有的 JSON 格式，在 Array 中添加新物件。
3. 存檔後 Vite 會自動重載，你不需要重啟伺服器。

---

## 📬 反饋與建議

這套 Mock 契約是根據我們目前的資料庫模型設計的。如果開發過程中發現問題如：

1. 資料結構不合理、欄位缺失。
2. Mock 回傳的邏輯有誤。

請直接告訴我或在群組詢問~
