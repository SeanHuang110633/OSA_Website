# 業務邏輯層 (Service) 開發指南

## 📖 一、 Service 的功能：系統的大腦

**Service 層負責處理核心業務邏輯與資料轉換。**
它是介於 Router（API 入口）與 Repository（資料存取）之間的橋樑。其主要職責包括：

1. **業務計算**：如分頁偏移量計算、權限檢查、複雜的演算法處理。
2. **多語系處理**：實施「降級策略 (Fallback)」，確保不同語系使用者都能看到最合適的內容。
3. **資料對應 (DTO Mapping)**：將資料庫模型 (Model) 轉換為前端所需的資料傳輸物件 (Schema/DTO)。
4. **邏輯過濾**：處理如「僅顯示未刪除附件」等細節業務規則。

---

## 🛠️ 二、 以 DownloadService 為例的實踐細節

以下透過 `download_service.py` 的實作來拆解開發重點。

### 1. 初始化與依賴注入 (Dependency Injection)

Service 不直接連接資料庫，而是透過「注入」Repository 來獲取資料，這讓程式碼更易於測試與解耦。

```python
class DownloadService:
    def __init__(self, repository: DownloadRepository):
        # 透過建構子注入 Repository
        self.repository = repository

```

### 2. 分頁邏輯與參數處理

Router 傳來的是人性化的 `page` (第幾頁)，Service 負責將其轉為資料庫能理解的 `skip` (跳過幾筆)。

- **語法邏輯**：使用公式 `(page - 1) * page_size`。
- **範例**：

```python
def get_downloads(self, locale, page=1, page_size=10, ...):
    skip = (page - 1) * page_size
    raw_items, total = self.repository.get_list_with_total(skip=skip, limit=page_size, ...)

```

### 3. 多語系降級策略 (Fallback Mechanism)

當資料庫存有多個語言版本時，必須確保在指定語言缺失時有備援方案。

- **實踐方式**：建立私有工具函式 `_get_json_text`。
- **取值順序**：`指定語言` -> `繁體中文 (zh-TW)` -> `預設字串`。

```python
def _get_json_text(self, data_dict: dict, locale: str, default: str = "Unknown") -> str:
    if not data_dict:
        return default
    # 優先回傳 locale，若無則回傳 zh-TW，皆無則回傳預設值
    return data_dict.get(locale) or data_dict.get("zh-TW") or default

```

### 4. 軟刪除與子項目過濾

即使 Repository 預載入了所有關聯資料，Service 仍須根據業務需求過濾掉已標記為刪除的子項目（如舊版本附件）。

- **實踐方式**：在轉換 DTO 時使用 Python 列表推導式進行過濾。

```python
active_attachments = [
    AttachmentPublic(...)
    for att in download.attachments
    if att.deleted_at is None  # 只顯示未被標記軟刪除的附件
]

```

### 5. 模型轉換 (Model to Schema Mapping)

為了確保 API 的安全性與效能，我們將 Model 轉換為 Schema。

- **扁平化**：將 Model 中的 `Dict` (JSON) 欄位轉為 Schema 中的 `str`。
- **封裝回傳**：將資料列表與總筆數包裝成 `PaginationResponse` 格式。

---

## 📝 三、 Service 開發核心守則

| 開發原則       | 說明                                                                              |
| -------------- | --------------------------------------------------------------------------------- |
| **不寫 SQL**   | Service 絕對不出現 `select` 或 `Session` 操作，資料讀取一律呼叫 Repository。      |
| **私有化轉換** | 建議將複雜的轉換邏輯寫在 `_transform_to_list_view` 等私有方法中，保持主方法簡潔。 |
| **防禦性編碼** | 針對 `Optional` 的 JSON 欄位（如 `department`），取值前必須先檢查是否為 `None`。  |
| **回傳 DTO**   | Service 的公開方法應回傳 `Schema` 物件，而非 `Model` 資料庫物件。                 |
