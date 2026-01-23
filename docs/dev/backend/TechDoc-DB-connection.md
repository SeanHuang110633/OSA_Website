# 📚 技術檔案：資料庫核心連線機制 (`database.py`)

## 一、 環境變數與安全性處理

在初始化資料庫連線前，系統必須從環境變數中讀取敏感資訊（如連線字串）。

- **`load_dotenv()` 的作用**：
  - 該函式會讀取專案根目錄下的 `.env` 檔案。
  - 它將檔案中的鍵值對（Key-Value pairs）注入到系統的環境變數中。
  - **執行後**即可使用 `os.getenv("DATABASE_URL")` 抓取設定值。
- **資安風險判斷**：
  - **本地開發**：只要確保 `.env` 已加入 `.gitignore`（不推送到 Git），風險極低。
  - **生產環境**：建議直接在作業系統或 Docker 容器層級注入環境變數，避免機密檔案留在磁碟上，進一步降低外洩風險。

---

## 二、 核心連線引擎：`create_engine`

`create_engine` 是 SQLAlchemy/SQLModel 用來與資料庫對話的「工廠」，它持有連線池管理與方言（Dialect）處理邏輯。

### 1. 以 Spring Framework 視角理解

如果你具備 Spring 開發經驗，可以將 `create_engine` 理解為 **`DataSource` Bean** 的配置（例如 HikariCP）：

- 它不代表單一連線，而是一個 **「連線池 (Connection Pool)」**。
- `DATABASE_URL` 等同於 `spring.datasource.url`。

### 2. 關鍵參數說明

- **`pool_recycle=3600`**：等同於設定連線的最大存活時間，防止 MySQL 端因為閒置過久強制斷開連線而導致「Server has gone away」錯誤。
- **`pool_pre_ping=True`**：
  - 這是一種「悲觀」連線檢查機制。
  - 在應用程式每次使用連線前，會先發送一個微小指令（如 `SELECT 1`）測試有效性。
  - 雖然不再使用 Aiven，但若資料庫與伺服器不在同一區域，保留此設定可自動處理「過時連線」問題。

---

## 三、 自動化表格建立：`create_db_and_tables`

這是 SQLModel 確保資料庫結構與 Python 代碼同步的關鍵機制。

### 1. 映射物件 (Mapping) 機制

當定義 `class Apple(SQLModel, table=True)` 時，這是一個「宣告式」動作。

- `create_all(engine)` 會掃描 Python 記憶體中所有已註冊的模型，並與實體資料庫比對。
- 如果 MySQL 中不存在對應表格，它會根據類別定義自動執行 `CREATE TABLE` 指令。

### 2. 為何必須在函式內 `import` 模型？

- **註冊機制**：只有當 Python **執行到** Model 的定義程式碼時，該模型才會被註冊到全域的 `metadata` 目錄中。
- **強迫讀取**：在 `create_db_and_tables` 內部進行 `import`（如 `from app.models.event_model import ...`），是為了確保所有表格資訊在執行 `create_all` 前都已成功登記。

---

## 四、 會話管理：`get_session` 的語法邏輯與生命週期

這段程式碼是 FastAPI 處理資料庫連線的靈魂：

Python

```
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

### 1. 語法拆解

- **`Generator[Session, None, None]`**：這是一個型別註解，代表這個函式是一個「產生器」，會產出（yield）一個 `Session` 物件。
- **`with Session(engine) as session:`**：Python 的 **上下文管理器 (Context Manager)**。當程式離開 `with` 範圍時，會自動呼叫 `session.close()`，確保連線歸還連線池，防止洩漏。
- **`yield session`**：將 `session` 交給呼叫者後，**暫停在此處**，而不是像 `return` 一樣直接結束。

### 2. 生命週期範例：一筆 API 請求的流程

1. **請求開始**：前端呼叫 API（如 `/api/events`）。
2. **依賴注入**：FastAPI 發現需要資料庫服務，呼叫 `get_session()`。
3. **借出連線**：執行到 `yield session`，連線被「借給」API 邏輯使用。
4. **執行業務**：API 進行 CRUD 資料操作。
5. **請求結束**：API 準備回傳結果給前端。
6. **回收連線**：**關鍵步驟！** API 回傳後，FastAPI 回到 `get_session` 暫停處繼續執行，離開 `with` 區塊，系統自動關閉 session 並釋放連線。

### 3. 生活化類比：圖書館借閱室

- **`with Session`**：你走進借閱室並刷卡（開啟連線）。
- **`yield session`**：管理員把書交給你，你可以拿去座位上看（執行邏輯）。
- **請求結束後**：你離開座位，管理員自動把書收回架上（關閉連線），確保資源不被浪費。

---

> **知識管理註記**：`create_all` 只會建立「不存在」的表。若未來需修改現有欄位，建議引入 **Alembic** 進行 Migration 管理。
