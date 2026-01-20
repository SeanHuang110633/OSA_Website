# 本地啟動專案指南

**Version** : v1
**Release Date** : 2026-01-19
**Author** : Sean

---

### 1. 準備工具 (Prerequisites)

在開始之前，請確保電腦已安裝：

- **Git**：用於拉取程式碼。
- **Docker Desktop**：確保啟動並顯示綠燈。
- **VS Code**：推薦的開發工具。

---

### 2. 第一步：複製專案與切換分支

打開終端機（PowerShell 或 Terminal），執行以下指令：

```powershell
# 1. 複製專案
git clone <你的專案倉庫網址>
cd OSA_Website

# 2. 切換至開發主分支
git checkout develop

```

---

### 3. 第二步：設定環境變數 (.env)

由於 `.env` 包含敏感資訊且被 Git 排除，每位組員必須手動建立一份本地版本。

- 在 `backend/` 資料夾下建立一個 **`.env`** 檔案。
- 貼入以下開發專用設定（確保連線指向 Docker 內部的 `db`）：

```env
# Docker 內部開發連線字串
DATABASE_URL="mysql+pymysql://root:root@db:3306/osa_newdb_test"

# CORS 允許來源
ALLOWED_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"

```

---

### 4. 第三步：啟動 Docker 容器

在專案根目錄（包含 `docker-compose.yml` 的地方）執行：

```powershell
docker-compose up -d --build
```

- **`--build`**：確保 Docker 會根據最新的 `requirements.txt` 和前端設定重新構建。
- **等待時間**：第一次啟動會自動執行 `pnpm install` 與 Python 套件安裝，請耐心等待直到終端機完成任務。

---

### 5. 第五步：驗證結果

現在可以打開瀏覽器檢查各項服務是否正常：

- **前端介面**：[http://localhost:5173](https://www.google.com/search?q=http://localhost:5173)（應該能看到活動列表資料）。
- **後端 API 文件**：[http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)（可以測試 API 呼叫）。
- **靜態檔案測試**：若 `uploads/` 有測試圖，可存取 `http://localhost:8000/uploads/<檔名>`。

---

### 💡 小提醒

> **關於改 Code：**
> 你們可以直接在 VS Code 修改 `frontend/` 或 `backend/` 下的程式碼。
>
> - **前端**：Vite 會自動熱更新 (HMR)，網頁會即時變動。
> - **後端**：Uvicorn 會偵測變動並自動重載，不需重啟 Docker。
> - **例外**：只有在修改了 `requirements.txt` 或 `package.json`（新增套件）時，才需要重新執行 `docker-compose up --build`。
