# 資料傳輸物件 (Schema / DTO) 開發指南

## 📖 一、 Schema 的功能：資料的門面

**Schema (Data Transfer Object) 負責定義 API 回傳的資料結構。**
雖然 Model 定義了資料庫的「長相」，但我們不應直接將資料庫物件丟給前端。 Schema 的存在是為了實現以下目標：

1. **安全性過濾**：隱藏如 `deleted_at` 等系統內部欄位。
2. **資料扁平化**：將複雜的 JSON 字典根據語系（Locale）轉化為前端可直接讀取的字串。
3. **效能與規範**：明確回傳欄位，減少不必要的頻寬消耗，並讓前端擁有穩定的資料結構。

---

## 🛠️ 二、 設計細節與核心原則

以下基於 `download_schema` 的設計範例，在開發其他 Schema 時可以參考：

### 1. 基礎組件化 (Component Schemas)

為了提高代碼複用率，我們會將常用的關聯資料定義為基礎組件。

```python
class CategoryPublic(BaseModel):
    """分類顯示用：將 Model 中的 names (JSON) 扁平化為單一字串"""
    slug: str
    name: str  # 在 Service 層根據 locale 轉換後的結果

class AttachmentPublic(BaseModel):
    """附件顯示用：排除邏輯刪除標記，僅回傳顯示所需欄位"""
    id: int
    type: str          # file, link
    file_format: Optional[str] = None
    path: str
    title: Optional[str] = None
    sort_order: int

```

### 2. 視圖模型 (View Schemas)

視圖模型應根據 API 的用途（列表頁 vs 詳情頁）來定義。

- **列表視圖 (ListView)**：回傳最精簡且必要的資訊，提升載入速度。
- **欄位轉換**：將 `Download` Model 中的多語系欄位（如 `title`, `department`）在 Schema 中定義為 `str`。

```python
class DownloadListView(BaseModel):
    """下載列表 DTO：包含前端篩選與顯示所需的所有扁平化欄位"""
    id: int
    type: str                    # regulation, form, other
    category: CategoryPublic     # 巢狀結構呈現關聯分類
    title: str                   # 轉換後的標題
    department: Optional[str] = None  # 轉換後的單位
    published_at: Optional[datetime] = None
    attachments: List[AttachmentPublic] = [] # 預設空串列，防止前端報錯

```

### 3. 分頁封裝 (Pagination Wrapper)

為了支援前端的分頁組件（如 Vue Pagination），回傳格式必須包含分頁功能所需的資料。

```python
class DownloadPaginationResponse(BaseModel):
    """標準化分頁回傳格式"""
    total: int    # 總筆數，讓前端計算總頁數
    page: int     # 當前頁碼
    size: int     # 每頁筆數
    items: List[DownloadListView] # 實際資料清單

```

---

## 🔗 三、 關鍵設計問答 (Q&A)

- **為什麼要設定預設值 `attachments: List[...] = []`？**
- **回答**：這是為了確保資料的一致性。如果該項目沒有附件，回傳 `[]`（空串列）比回傳 `null` 對前端更友善，能避免 `v-for` 渲染時發生崩潰。

- **Schema 中可以包含邏輯判斷嗎？**
- **回答**：不行。Schema 應該只是單純的資料容器（Data Container）。 所有的翻譯轉換、過濾、計算應留在 **Service 層** 處理，然後才填充進 Schema。

- **如何處理 Optional 欄位？**
- **回答**：對應資料庫中 `DEFAULT NULL` 的欄位（如 `department`），在 Schema 中應使用 `Optional[str] = None`。

---

## 🗑️ 四、 安全性與隱私過濾

這點極其重要：**切勿在 Schema 中包含以下欄位**，除非該 API 是專門供後台管理的：

- `deleted_at`：邏輯刪除的時間戳記不應暴露。
- `created_at` / `updated_at`：除非業務邏輯需要展示給使用者看。
- 內部的 ID 外鍵（如 `category_id`）：改用 `CategoryPublic` 這種物件結構，能讓 API 更具語意化。
