# N+1 查詢問題

在 ORM（物件關係映射）的世界中，**N+1 查詢問題**是影響系統效能的頭號殺手。如果不謹慎處理，當資料量增加時，你的 API 回應速度將會呈線性衰減。

以下針對我們的「下載系統」案例，深入拆解 N+1 問題的成因、代價與解決方案。

---

## 🛑 一、 什麼是 N+1 問題？

**N+1 問題**是指當我們查詢一組父物件（N 筆資料），並試圖存取這些物件關聯的子物件時，ORM 為了獲取這些關聯資料，會額外發送 N 次資料庫查詢。

- **「1」次查詢**：用來獲取主資料（例如：10 筆下載項目）。
- **「N」次查詢**：針對每一筆主資料，分別發送一次 SQL 去抓取其關聯資料（例如：抓取這 10 筆項目各自的分類或附件）。

### 為什麼會發生？

預設情況下，SQLModel/SQLAlchemy 採用**「延遲載入 (Lazy Loading)」**機制。這意味著當你執行 `select(Download)` 時，它**只會**抓取下載主表的資料。直到你在程式碼中呼叫 `download.category` 或 `download.attachments` 時，ORM 才會在當下「臨時」跑去資料庫抓資料。

---

## 📊 二、 案例計算：N+1 vs 預先載入

假設前端請求**分頁大小為 10** 的下載列表，且每個項目都包含「分類」與「附件」。

### 1. 沒處理 (Lazy Loading) 的 SQL 執行狀況

當 Service 層跑迴圈將 Model 轉為 Schema 時，會發生以下行為：

1. **第 1 次 SQL**：`SELECT * FROM downloads LIMIT 10;`（抓到 10 筆下載項目）。
2. **第 2~11 次 SQL**：迴圈跑第 1 圈到第 10 圈，每次都執行 `SELECT * FROM download_categories WHERE id = ?;`（為了拿分類名稱）。
3. **第 12~21 次 SQL**：迴圈跑第 1 圈到第 10 圈，每次都執行 `SELECT * FROM download_attachments WHERE download_id = ?;`（為了拿附件清單）。

> **總計 SQL 筆數：1 + 10 + 10 = 21 次查詢**。

### 2. 使用 `selectinload` (Eager Loading) 的執行狀況

當我們在 Repository 層加上 `.options(selectinload(Download.category), selectinload(Download.attachments))` 時：

1. **第 1 次 SQL**：`SELECT * FROM downloads LIMIT 10;`。
2. **第 2 次 SQL**：`SELECT * FROM download_categories WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10);`（一次抓完所有需要的分類）。
3. **第 3 次 SQL**：`SELECT * FROM download_attachments WHERE download_id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10);`（一次抓完所有相關附件）。

> **總計 SQL 筆數：1 + 1 + 1 = 3 次查詢**。

---

## 💻 三、 效能差距對比

當資料量規模擴大時，差距會非常驚人：

| **抓取資料筆數 (N)** | **N+1 查詢次數 (1+2N)** | **selectinload 查詢次數** | **效能影響**         |
| -------------------- | ----------------------- | ------------------------- | -------------------- |
| **10 筆**            | 21 次                   | 3 次                      | 尚可忍受             |
| **50 筆**            | 101 次                  | 3 次                      | API 明顯變慢         |
| **100 筆**           | 201 次                  | 3 次                      | 資料庫連線池可能耗盡 |

---

## 🛠️ 四、 `selectinload` 的運作原理

`selectinload` 是 SQLAlchemy 針對「一對多」或「多對一」關聯推薦的優化方式。

1. **獨立查詢**：它會先執行主查詢，獲取所有父物件的 ID。
2. **IN 子句**：它會發送第二條獨立的 SQL 語句，使用 `IN` 運算子一次性載入所有相關的子物件。
3. **記憶體映射**：在 Python 記憶體中，它會自動將這些子物件分配到正確的父物件屬性上。

### 為什麼不用 `joinedload` (JOIN)？

- `joinedload` 會產生一個超大的 SQL JOIN 語句。
- 對於「一對多」關聯（例如一個下載有多個附件），JOIN 會導致主表資料重複出現（重複載入下載標題），這在資料量大或欄位多時，會造成頻寬浪費與效能下降。
- **`selectinload` 避免了資料重複，是處理集合關聯的最佳實踐。**

---

## 📝 知識管理：N+1 防治開發規範

> - **預設禁令**：除非明確知道只需讀取主表，否則嚴禁在 Service 層迴圈中觸發 Lazy Loading。
> - **Repository 職責**：所有需要回傳給 Schema 的關聯欄位，必須在 Repository 層透過 `.options(selectinload(...))` 顯式宣告載入。
> - **監控手段**：開發階段應開啟 `echo=True` (在 `database.py` 中)，觀察控制台輸出的 SQL 數量，若發現查詢次數隨分頁大小增加，即為 N+1 現象。
