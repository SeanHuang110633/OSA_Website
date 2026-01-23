# 路由層 (Router) 開發指南

## 📖 一、 Router 的功能：API 的總機

**Router 的核心職責是管理 API 的入口點 (Endpoints)**。
它不處理資料庫邏輯，也不處理複雜的計算，它只負責：

- **路由分流**：根據 URL 將請求導向正確的業務邏輯處。
- **輸入校驗**：確保前端傳來的參數格式、型別正確。
- **合約執行**：透過 `response_model` 確保回傳給前端的資料結構符合規範。
- **依賴串接**：透過「依賴注入」取得所需的 Service 實例。

---

## 🛠️ 二、 FastAPI 參數定義規範

在定義 API 函式時，我們主要使用以下兩種參數類型來接收前端資料：

### 1. 路徑參數 (Path Parameters)

- **使用時機**：用於定位「特定資源」，通常是 ID。
- **定義方式**：在 URL 中使用 `{}` 包圍，並在函式參數中使用 `Path(...)`。
- **必填標記**：使用 `...` (Ellipsis) 代表該參數是強制性的。
- **範例**：

```python
@router.get("/{download_id}")
def read_detail(download_id: int = Path(..., description="資源 ID")): ...

```

### 2. 查詢參數 (Query Parameters)

- **使用時機**：用於「過濾、排序、分頁」等非唯一性定位的參數。
- **定義方式**：直接定義在函式參數中，或使用 `Query()` 增加額外限制（如 `ge` 最小、`le` 最大）。
- **範例**：

```python
@router.get("/")
def read_list(
    page: int = Query(1, ge=1),      # 預設第 1 頁，必須 >= 1
    size: int = Query(10, le=100)    # 預設 10 筆，最大 100 筆
): ...

```

---

## 🔗 三、 依賴注入 (Dependency Injection) 與 Service 取得

我們嚴禁在 Router 中直接實例化 (new) 任何 Service 或 Repository。一律透過 `app/dependencies.py` 統一管理。

### 0. 解釋 dependencies.py

```python
# app/dependencies.py
# 統一處理依賴注入的工廠函式

from fastapi import Depends
from backend.app.repositories.download_repository import DownloadRepository
from sqlmodel import Session
from app.core.database import get_session
from app.repositories.event_repository import EventRepository
from app.services.event_service import EventService
from app.services.download_service import DownloadService

# event_service 依賴注入工廠
def get_event_service(session: Session = Depends(get_session)) -> EventService:
    # 建立順序：Session -> Repository -> Service
    return EventService(EventRepository(session))

# download_service 依賴注入工廠
def get_download_service(session: Session = Depends(get_session)) -> DownloadService:
    # 建立順序：Session -> Repository -> Service
    return DownloadService(DownloadRepository(session))
```

`app/dependencies.py` 的程式碼是系統的 **「組裝廠」**。它的核心用意是利用 FastAPI 的 **依賴注入 (Dependency Injection)** 機制，自動化地完成物件的建立與掛載。具體來說，這段代碼解決了「誰來負責開資料庫連線、誰來把連線交給 Repository、誰再把 Repository 交給 Service」的繁瑣過程。

這段程式碼主要實現了以下三層物件的 **「自動組裝鏈」**：

1. **取得資料庫會話 (Session)**
   - 透過 `Depends(get_session)`，系統會先去 `database.py` 拿一個可用的資料庫連線。
2. **實例化資料存取層 (Repository)**
   - 將拿到的 `session` 丟進 `EventRepository` 或 `DownloadRepository` 的構造函數中。
   - 這讓 Repository 具備了執行 SQL 的能力。
3. **封裝業務邏輯層 (Service)**
   - 最後將建好的 Repository 丟進 `EventService` 或 `DownloadService` 中。
   - Service 層現在可以專心處理邏輯（如多語系轉換），而不需要知道資料庫是怎麼連線的。

#### 為什麼要這樣寫？（優點分析）

- **讓 Router 層變得很乾淨**：
  在 `event_router.py` 中，你只需要寫 `service: EventService = Depends(get_event_service)`，FastAPI 就會幫你把整條組裝鏈跑完並直接把 Service 送到你手上。
- **職責分離 (Separation of Concerns)**：
  Router 只管接收 HTTP 請求，Service 只管邏輯，Repository 只管 SQL，而 `dependencies.py` 則專門管 **「如何把大家接起來」**。
- **方便測試**：
  未來如果要做單元測試，你可以輕鬆地在 `dependencies.py` 裡把真實的 Repository 換成一個「假資料 (Mock)」，而不必去改動 Service 或 Router 的程式碼。

### 1. 依賴注入鏈 (DI Chain) 的運作

當你在 Router 中寫下 `Depends(get_download_service)` 時，FastAPI 會執行以下連鎖動作：

1. **取得會話**：呼叫 `get_session` 開啟資料庫連線。
2. **建立倉庫**：將 Session 傳入 `DownloadRepository`。
3. **封裝服務**：將 Repository 傳入 `DownloadService`。
4. **提供實例**：最終將組裝好的 Service 傳遞給你的 Router 函式。

### 2. 在 Router 中的實作語法

```python
from app.dependencies import get_download_service  # 引入工廠函式

@router.get("/")
def my_api(service: DownloadService = Depends(get_download_service)):
    # 直接使用傳入的 service 呼叫業務邏輯
    return service.get_downloads(...)

```

---

## ✅ 四、 Router 開發守則 (Checklist)

1. **Prefix 與 Tags**：定義 `APIRouter` 時務必加上 `prefix` 與 `tags`，以便在 Swagger UI 中自動分類。
2. **型別標註**：所有參數必須標註 Python 型別（如 `int`, `str`），這會自動觸發 FastAPI 的格式驗證。
3. **Response Model**：裝飾器必須宣告 `response_model`，這除了是合約保證，也能過濾掉敏感的資料庫欄位。
4. **不寫 Logic**：若你的 Router 程式碼超過 10 行，請檢查是否把本該放在 Service 的業務邏輯寫到 Router 裡了。
