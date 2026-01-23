# 資料存取層 (Repository) 開發指南

## 📖 一、 Repository 的功能：資料的守門員

**Repository 專門負責「如何從資料庫拿資料」**。
它的核心任務是將 SQL 查詢語法與過濾邏輯封裝起來。這樣做的好處是 Service 層（大腦）不需要知道資料庫的欄位細節，只需要下達「我要拿分頁資料」或「我要依關鍵字搜尋」的指令即可。

---

## 🛠️ 二、 設計細節與常見問題 (Q&A)

- **`self.session` 是從哪裡來的？**
  透過 FastAPI 的依賴注入機制，在 `dependencies.py` 中會先呼叫 `get_session()` 取得連線，再透過建構子傳遞給 Repository。這確保了整個請求週期（Request Lifecycle）內使用的是同一個資料庫交易。(這個部份會寫在其他文件)
- **`__init__` 的作用是什麼？**
  它是 Python 的**建構子 (Constructor)**。當類別被實例化時，會先執行此方法。我們在此處將傳入的 `session` 儲存在 `self.session` 中，供類別內的所有方法（如 `get_list`）共享連線。
- **`subquery()` 是什麼時候使用的？**
  當我們需要精確計算符合條件的「總筆數」時使用。將帶有 `JOIN` 與 `WHERE` 的查詢語句先封裝成一個虛擬的「暫存表（子查詢）」，再對其進行 `COUNT(*)`，能避免因關聯表導致的計數錯誤。

---

## 🔍 三、 動態查詢與過濾設計

以download_repository為例，在處理複雜的搜尋需求時，我們採取 **「固定條件」與「動態條件(type、category、key word)」分離** 的策略：

### 1. 為什麼要分開寫？

如果將所有 `.where()` 串聯在一起，當前端沒有傳入某個參數（如 `category_id` 為空）時，SQL 會強行搜尋 `id = NULL`，導致查無資料。

- **固定條件**：如 `deleted_at == None`（軟刪除）或 `is_active == True`（分類啟用），直接寫在 `statement` 初始化處。
- **動態條件**：如關鍵字、分類 ID，使用 `if` 判斷式，只有當參數存在時才追加過濾。

```python
######## 固定 #######
# 1. 建立基礎查詢
        # selectinload: 預先載入關聯，解決 N+1 問題
        statement = (
            select(Download)
            .where(Download.deleted_at == None) # 排除軟刪除項目
            .join(Download.category).where(DownloadCategory.is_active == True) # 只取啟用的分類(如果有分類被停用，則該分類下的下載項目也不顯示)
            .options(
                selectinload(Download.category), # 為了回傳資料時有分類資訊
                selectinload(Download.attachments) # 為了回傳資料時有附件
            )
        )
###### 動態 ######
        # 2. 條件過濾(type, category)，與上面分開寫可以增加可讀性、方便後續擴充，且避免沒有傳入參數時搜尋出錯誤資料
        if dl_type:
            statement = statement.where(Download.type == dl_type)

        if category_id:
            statement = statement.where(Download.category_id == category_id)

        # 3. 模糊搜尋 (針對 JSON 欄位中的標題內容)
        if search_query:
            # 注意：這邊使用了 MySQL 的 JSON 函數來搜尋多語系欄位中的內容
            # 這邊先暫時只搜尋 zh-TW 和 en-US 兩種語言的標題
            statement = statement.where(
                or_(
                    func.json_unquote(func.json_extract(Download.title, '$."zh-TW"')).like(f"%{search_query}%"),
                    func.json_unquote(func.json_extract(Download.title, '$."en-US"')).like(f"%{search_query}%")
                )
            )
```

### 2. JSON 欄位的模糊搜尋

針對多語系標題（JSON 格式），我們使用以下技巧實現中英文同時匹配：

```python
# 將 JSON 欄位轉為字串後進行 LIKE 比對
statement = statement.where(Download.title.cast(String).like(f"%{search_query}%"))

```

---

## 🔗 四、 跨表過濾與關聯預載入

這是開發中最容易混淆的部分，請務必區分 **`JOIN`** 與 **`selectinload`** 的職責：

- **`JOIN` (過濾用)**：
  如果你要根據「關聯表」的狀態（例如：分類必須是啟用中）來決定「主表」資料是否顯示，就**必須**使用 `.join()`。
- **`selectinload` (讀取用)**：
  這僅是用於效能優化。它負責「預先抓取」關聯表的內容（如附件清單），讓你可以在一兩次 SQL 內拿完所有資料。它**無法**用來過濾主表的數量。(主要解決N+1問題，另以文件說明)

---

## 🚀 五、 分頁查詢作業的具體執行流程

以download_repository的get_list_with_total為例，這是一個標準的分頁查詢作業流程：

1. **初始化**：建立 `select(Download)` 並加上 `JOIN`（跨表過濾）與 `options`（預載入）。
2. **固定過濾**：加上軟刪除過濾 (`deleted_at IS NULL`)。
3. **動態過濾**：依據傳入參數，動態追加 `WHERE` 條件。
4. **計數 (Count)**：將上述語句包成 `subquery()`，執行一次 SQL 取得 `total`。
5. **分頁與排序**：在原語句加上 `order_by`、`offset` 與 `limit`。
6. **執行 (Data)**：執行第二次 SQL 取得真正的資料清單，最後回傳 `(items, total)`。

---

## ⚡ 六、 關於 N+1 效能問題

本系統嚴禁在 Service 層的迴圈中觸發延遲載入（Lazy Loading）。

- 所有 Schema 中需要的關聯資料（如 `attachments`），必須在 Repository 層透過 `.options(selectinload(...))` 一次性預載入。
- _詳細的 N+1 原理與計算請參閱《N+1 查詢優化說明文件》。_
