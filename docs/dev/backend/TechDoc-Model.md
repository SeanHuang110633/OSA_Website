# 資料模型 (Model) 開發指南

## 📖 一、 Model 的功能：簡單來說

**Model 是連接 Python 物件世界與 MySQL 資料庫世界的「橋樑」。**
在我們的架構中，Model 使用 `SQLModel` 撰寫，它同時具備了 Pydantic 的資料驗證能力與 SQLAlchemy 的 ORM（物件關係映射）功能。你只需要操作 Python 物件，Model 就會自動幫你轉化為對應的 SQL 指令。

---

## 🛠️ 二、 設計細節與常見問答

在開發 Model 時，我們常會遇到以下設計選擇，請遵循此規範：

- **為什麼 `id` 預設為 `None`？**
  當一個物件剛被 `new` 出來時，MySQL 尚未分配 `AUTO_INCREMENT` 的 ID 給它。設定 `default=None` 是為了符合物件在尚未存入資料庫前的狀態。
- **`sa_type=JSON` 的用意**
  `sa` 即 **SQLAlchemy**。當 Python 的欄位型別為 `Dict` 時，必須顯式傳入 `sa_type=JSON`，告訴底層引擎這是一個 JSON 欄位，負責處理 `json.dumps` (存入) 與 `json.loads` (讀取)。
- **複合索引 (Composite Index) 的處理**
  若查詢常涉及多個欄位（如：依分類與類型過濾下載），必須在 `__table_args__` 中定義 `Index`，以確保查詢效能。

```python
__table_args__ = (Index("idx_name", "col_a", "col_b"),)

```

- **為什麼有些有英文需求的欄位不用`JSON`而用`str`？**
  以download_model中的type為例，因為它是具有「程式邏輯判斷」意義的標籤(篩選資源的時候會依據type去篩)，所以應保持單一字串，用json的話還要拿出對應的value，這樣比較麻煩，這部分的中英轉換可以在前端或 Schema 處理，否則後端在進行 `WHERE` 過濾時會變得複雜且緩慢。

---

## 🔗 三、 深入解析：Relationship 的設定

`Relationship` 是 ORM 的靈魂，它讓關聯查詢變得直覺，以下說明以download_model為例。

### 1. 映射機制與「錨點」

關聯的建立依靠兩層設定：

- **資料庫錨點 (Foreign Key)**：這是物理連結。例如 `category_id` 指向 `download_categories.id`。
- **Python 隧道 (Relationship)**：這是邏輯連結。
- **`back_populates`**：這不是指向資料庫欄位，而是指向**對方類別中的變數名稱**。
- 範例：`Download` 類別中 `back_populates="downloads"`，代表對應到 `DownloadCategory` 類別裡那個名為 `downloads` 的屬性。

### 2. 如何推斷關聯數量 (1:N, M:M)？

SQLModel 會根據 **Python 型別標記 (Type Hints)** 來判斷：

- **一對多 (1:N)**：在「一」的一方使用 `List["ModelName"]`，在「多」的一方使用單一物件型別如`Optional[Download]`。
- **多對多 (M:M)**：例如雙向皆使用 `List` ，而且通常還會有一個中間表（Link Model）。
- 1對1，多對1的邏輯也是一樣的。

---

## 🗑️ 四、 邏輯刪除 (Soft Delete) 設計規範

為了保留資料行政軌跡與誤刪救援，我們採取「主動隱藏而非物理抹除」的策略。

### 1. 不同的刪除標記

- **主體資料 (Entity)**：如 `Download`，使用 `deleted_at: datetime`。這能精確記錄刪除時間，用於資源回收站機制。
- **分類 (Category)**：使用 `is_active: bool`。分類通常不建議刪除（因為舊資料仍需參考它），僅需透過開關控制前台選單是否顯示。

### 2. 附件的版本保留邏輯

針對法規等需要「版本歷史」的資料，**附件表也應具備 `deleted_at**`。當法規更新時，舊檔案設為已刪除（隱藏但留存），新檔案設為啟用，這對行政合規性與追溯性至關重要。

---

## 🌊 五、 級聯設計 (Cascade) 與資料庫約束

我們透過 ORM 與資料庫層級的雙重設定，確保資料的完整性。

### 1. ORM 層級：`cascade="all, delete-orphan"`

這是寫在 `Relationship` 中的設定。

- **作用**：當你從 Python 的清單中 `pop()` 掉一個子物件時，ORM 會自動幫你把該筆資料從資料庫 **物理刪除**。
- **原理**：它將子物件視為父物件的一部分，一旦失去依附關係（變成孤兒），就自動清理。

### 2. 資料庫層級：`ondelete` 選項

這是寫在 `ForeignKey` 中的設定，直接影響 MySQL 的行為：

- **`CASCADE` (級聯)**：父表刪除，子表跟著刪。
- **`RESTRICT` (限制)**：若子表還有資料，禁止刪除父表資料（這是 `EventCategory` 採用的策略，防止誤刪分類導致活動失效）。
- **`SET NULL`**：父表刪除，子表外鍵變為 NULL（適用於非強制依附關係）。
- **`NO ACTION`**：不採取行動，交由資料庫在交易提交時檢查（通常與 RESTRICT 類似）。

> **最佳實踐提示**：在 OSA 系統中，附件建議使用 `ondelete="CASCADE"`，而類別建議使用 `ondelete="RESTRICT"` 以確保資料結構的穩定。
