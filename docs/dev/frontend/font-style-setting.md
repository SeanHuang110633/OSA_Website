# 前端字體排版規範

## 1. 核心目標

為了解決繁體中文在資訊密集系統中的閱讀體驗問題，我們將捨棄手寫像素（如 `13px`），改採用 **模組化 CSS 變數系統**。

- **提升易讀性**：內文最小不低於 `14px` (建議 `15-16px`)，解決筆畫模糊問題。
- **統一層級**：確保所有頁面的「區塊標題」、「卡片標題」視覺權重一致。
- **維護性**：透過全域變數管理，未來調整字體大小只需改一個地方。

---

## 2. 實作步驟 Step-by-Step

### Step 1: 定義全域 CSS 變數

請在專案的全域樣式檔（例如 `src/assets/main.css`）或 `App.vue` 的 `<style>` 中加入以下變數。
_(基準為 `html { font-size: 16px; }`)_

```css
:root {
  /* --- 字體大小階層 (Scale) --- */
  /* 用於：標籤、極次要註解 (慎用) */
  --text-xs: 0.75rem; /* 12px */

  /* 用於：日期、Meta資訊、頁腳 */
  --text-sm: 0.875rem; /* 14px */

  /* 用於：標準內文、新聞列表、按鈕、連結 (預設大小) */
  --text-base: 1rem; /* 16px */

  /* 用於：強調文字、大按鈕、副標題 */
  --text-lg: 1.125rem; /* 18px */

  /* 用於：卡片標題 (Card Title)、H3 */
  --text-xl: 1.25rem; /* 20px */

  /* 用於：區塊大標題 (Section Title)、H2 */
  --text-2xl: 1.5rem; /* 24px */

  /* 用於：頁面主標題 (Page Title)、H1 */
  --text-3xl: 1.875rem; /* 30px */

  /* 用於：首頁 Hero Banner 標題 */
  --text-4xl: 2.25rem; /* 36px */

  /* --- 行高 (Line Height) - 中文閱讀關鍵 --- */
  /* 用於：標題 (避免標題換行時行距過大) */
  --leading-tight: 1.3;

  /* 用於：內文 (增加呼吸感，避免筆畫沾黏) */
  --leading-normal: 1.6;
}
```

---

### Step 2: 現有組件重構指南 (Refactoring Guide)

請依照以下對照表，修改對應檔案的 `<style scoped>` 區塊。

#### 🟢 1. HeroBanner.vue (首頁輪播)

**目標**：讓主標題更有張力，副標題更易讀。

| 選擇器 (Selector) | 原本數值  | **建議修正 (使用變數)**           | 備註 |
| ----------------- | --------- | --------------------------------- | ---- |
| `.title`          | `1.55rem` | `font-size: var(--text-4xl);`<br> |

<br>`line-height: var(--leading-tight);` | 大幅提升氣勢 |
| `.desc` | `1rem` | `font-size: var(--text-lg);`<br>

<br>`line-height: var(--leading-normal);` | 字體微調大，增加行高 |
| `.cta` | `1.05rem` | `font-size: var(--text-base);` | 按鈕保持標準大小 |

#### 🟢 2. NewsAndLinks.vue (最新消息)

**目標**：**這是最優先修改項目**。目前列表字太小 (`13px`)，閱讀困難。

| 選擇器 (Selector) | 原本數值 | **建議修正 (使用變數)**            | 備註             |
| ----------------- | -------- | ---------------------------------- | ---------------- |
| `.hTitle`         | `1.5rem` | `font-size: var(--text-2xl);`      | 統一區塊標題標準 |
| `.text`           | `13px`   | `font-size: var(--text-base);`<br> |

<br>`line-height: 1.5;`<br>

<br>`font-weight: 500;` | **重點修正**：改為 16px |
| `.date` | `12px` | `font-size: var(--text-sm);` | 改為 14px |
| `.u` (連結列表) | `13px` | `font-size: var(--text-base);` | 連結需好點擊 |
| `.badge` | (繼承) | `font-size: var(--text-xs);` | 標籤可維持小字 |

#### 🟢 3. EventsRow.vue (本週活動)

**目標**：區分「區塊標題」與「卡片內容」的層級。

| 選擇器 (Selector) | 原本數值  | **建議修正 (使用變數)**          | 備註                   |
| ----------------- | --------- | -------------------------------- | ---------------------- |
| `.t` (本週活動)   | `1.5rem`  | `font-size: var(--text-2xl);`    | 確保與 News 標題一樣大 |
| `.name` (活動名)  | `1.12rem` | `font-size: var(--text-xl);`<br> |

<br>`line-height: 1.4;` | 卡片標題適中即可 |
| `.desc` | `0.95rem` | `font-size: var(--text-base);`<br>

<br>`line-height: var(--leading-normal);` | 內文標準化 |
| `.date` | `0.95rem` | `font-size: var(--text-sm);` | 輔助資訊 |

#### 🟢 4. QuickLinksGrid.vue (快速連結)

**目標**：降低卡片標題權重，避免搶過主標題。

| 選擇器 (Selector) | 原本數值  | **建議修正 (使用變數)**        | 備註                               |
| ----------------- | --------- | ------------------------------ | ---------------------------------- |
| `.title` (大標)   | `1.55rem` | `font-size: var(--text-2xl);`  | 與 News、Events 大標一致           |
| `.head h3`        | `1.5rem`  | `font-size: var(--text-xl);`   | **降級**：卡片標題不應等於區塊標題 |
| `a` (連結內文)    | `0.95rem` | `font-size: var(--text-base);` | 標準化                             |

---

## 3. 開發通用原則 (General Rules)

前端同仁在開發新頁面（如內頁、表單）時，請遵循以下原則：

1. **內文預設使用 `var(--text-base)**`：
除非是 Footer 或極次要的註解，否則不要使用小於 `1rem (16px)`的字體。繁體中文在`14px` 以下筆畫會黏在一起。
2. **標題層級對應表**：

- **H1 (頁面標題)** → `var(--text-3xl)`
- **H2 (區塊標題)** → `var(--text-2xl)`
- **H3 (卡片/內文小標)** → `var(--text-xl)`

3. **顏色區分優於大小區分**：
   如果想讓資訊看起來「不重要」，優先嘗試**改變顏色**（如使用灰色 `#6B7280`），而不是把字縮小到看不見。

- ❌ Bad: `font-size: 12px; color: black;`
- ✅ Good: `font-size: 14px; color: var(--muted);`

4. **注意行高 (Leading)**：
   只要設定了 `font-size`，請務必檢查 `line-height`。

- 內文多行文字：`line-height: 1.6` (約 26px - 30px)
- 單行標題：`line-height: 1.3`

---

## 4. 快速檢查清單 (Checklist)

提交 PR 前，請檢查：

- [ ] 所有的 `font-size` 是否都已改用 `var(--text-...)` 變數？
- [ ] 是否消滅了所有的 `13px`？
- [ ] 區塊大標題（News, Events, Links）的大小是否視覺一致？
- [ ] 內文行高是否舒適（不會擠在一起）？
