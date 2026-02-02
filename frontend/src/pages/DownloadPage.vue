<template>
  <!-- 主容器：與全站一致，控制內容寬度與頁面上下留白 -->
  <main class="container page">

    <!-- 麵包屑：告訴使用者目前所在位置（資訊層級/導覽回上層） -->
    <div class="crumb">
      <RouterLink class="crumbLink" to="/">首頁</RouterLink>
      <span class="sep">/</span>
      <span class="now">下載專區</span>
    </div>

    <!-- 主面板：卡片式容器（與其他頁一致的 UI 風格） -->
    <section class="panel">
      <div class="inner">

        <!-- 工具列：提供篩選與搜尋（搜尋=可達性與效率） -->
        <div class="toolbar">
          <div class="toolLeft">
            <div class="lab">搜尋資料：</div>

            <!-- 種類下拉：用 type 篩選（法規/表單/其他） -->
            <select class="sel" v-model="form.kind">
              <option value="">全部</option>
              <option v-for="k in kindOptions" :key="k" :value="k">
                {{ kindMap[k] }}
              </option>
            </select>

            <!-- 類別下拉：用 category_id 篩選 -->
            <select class="sel" v-model="form.catId">
              <option value="">不分類</option>
              <option v-for="c in categoryList" :key="c.id" :value="c.id">
                {{ c.name }}
              </option>
            </select>

            <!-- 關鍵字輸入：enter 快速搜尋（UX：減少多餘點擊） -->
            <input
              class="kw"
              v-model.trim="form.keyword"
              placeholder="輸入關鍵字..."
              @keydown.enter="applySearch"
            />

            <!-- 觸發搜尋：將 page 重置為 1 並重新抓資料 -->
            <button class="go" type="button" @click="applySearch">搜尋</button>

            <!-- 清除條件：回到初始狀態 -->
            <button class="clear" type="button" @click="reset">清除</button>
          </div>
        </div>

        <!-- 表格區：主要內容（清單閱讀） -->
        <div class="tableWrap">
          <table class="tbl">
            <thead>
              <tr>
                <th style="width: 110px">種類</th>
                <th style="width: 140px">類別</th>
                <th>標題</th>
                <th style="width: 160px">業務單位</th>
              </tr>
            </thead>

            <tbody>
              <!-- 列表渲染：allRows 由 API 回傳 items -->
              <tr v-for="r in allRows" :key="r.id">
                <!-- 種類：用 kindMap 做顯示文字轉換 -->
                <td class="tdCenter">{{ kindMap[r.type] || r.type }}</td>

                <!-- 類別：後端回傳 r.category 物件 -->
                <td class="tdCenter">{{ r.category.name }}</td>

                <!-- 標題 + 附件：附件可多個（檔案/連結） -->
                <td class="titleCell">
                  <div class="zh">
                    {{ r.title }}

                    <!-- 附件 icon：📄 file / 🔗 link -->
                    <span v-for="att in r.attachments" :key="att.id">
                      <a
                        class="mini"
                        :href="att.path"
                        target="_blank"
                        rel="noreferrer"
                        :title="att.title"
                      >
                        {{ att.type === "file" ? "📄" : "🔗" }}
                        <!-- 顯示檔案格式，例如 (pdf) -->
                        <small v-if="att.file_format">({{ att.file_format }})</small>
                      </a>
                    </span>
                  </div>

                  <!-- 英文欄位預留：如果之後做 i18n 可放在這 -->
                  <div class="en"></div>
                </td>

                <!-- 業務單位：無資料時顯示 '-' -->
                <td class="tdCenter unit">{{ r.department || "-" }}</td>
              </tr>

              <!-- 空狀態：沒有資料時，顯示提示 -->
              <tr v-if="allRows.length === 0">
                <td colspan="4" class="empty">沒有符合條件的資料</td>
              </tr>
            </tbody>
          </table>

          <!-- 分頁列：顯示總筆數 + 主要操作（First/Prev/頁碼/Next/Last） -->
          <div class="pager">
            <div class="count">{{ totalCount }} 筆</div>

            <div class="p">
              <button class="pg" :disabled="page === 1" @click="page = 1">First</button>
              <button class="pg" :disabled="page === 1" @click="page--">‹</button>

              <!-- 動態頁碼：最多 5 顆 -->
              <button
                v-for="n in pageButtons"
                :key="n"
                class="pg"
                :class="{ on: n === page }"
                @click="page = n"
              >
                {{ n }}
              </button>

              <button class="pg" :disabled="page === totalPages" @click="page++">›</button>
              <button class="pg" :disabled="page === totalPages" @click="page = totalPages">
                Last
              </button>
            </div>
          </div>
        </div>
        <!-- /tableWrap -->
      </div>
      <!-- /inner -->
    </section>
  </main>
</template>

<script setup>
import { onMounted, reactive, ref, watch, computed } from "vue";
import { RouterLink } from "vue-router";
import { getDownloads, getCategories } from "../api/download.js";

/** 表格資料：後端 /downloads 回傳 items */
const allRows = ref([]);

/** 總筆數：後端回傳 total */
const totalCount = ref(0);

/** 分類資料：後端 /categories 回傳 */
const categoryList = ref([]);

/** 目前頁碼（分頁控制） */
const page = ref(1);

/** 每頁筆數（前端固定 10） */
const pageSize = 10;

/** 種類顯示映射（UI 顯示中文） */
const kindMap = {
  regulation: "法規",
  form: "表單",
  other: "其他",
};
const kindOptions = Object.keys(kindMap);

/** 搜尋表單狀態（v-model 綁定） */
const form = reactive({
  kind: "",
  catId: "",
  keyword: "",
});

/** 取得分類清單（下拉選單用） */
async function fetchCategories() {
  try {
    const res = await getCategories("zh-TW");
    categoryList.value = res;
  } catch (err) {
    console.error("分類獲取失敗", err);
  }
}

/** 取得下載清單（主表格） */
async function fetchList() {
  try {
    const res = await getDownloads({
      locale: "zh-TW",
      page: page.value,
      size: pageSize,
      // API 需要 null 表示不篩選，避免傳空字串造成後端判斷困難
      type: form.kind || null,
      category_id: form.catId || null,
      query: form.keyword || null,
    });

    // 對應表格渲染
    allRows.value = res.items;
    totalCount.value = res.total;
  } catch (err) {
    console.error("列表獲取失敗", err);
  }
}

/** 搜尋：重置到第 1 頁再抓資料（避免停留在舊頁碼） */
function applySearch() {
  page.value = 1;
  fetchList();
}

/** 清除：把所有條件重置，再觸發搜尋 */
function reset() {
  form.kind = "";
  form.catId = "";
  form.keyword = "";
  applySearch();
}

/** 計算總頁數（至少要有 1 頁避免 UI 壞掉） */
const totalPages = computed(() =>
  Math.max(1, Math.ceil(totalCount.value / pageSize)),
);

/** 當 page 改變 → 自動抓新頁資料 */
watch(page, () => {
  fetchList();
});

/** 頁碼按鈕：最多顯示 5 顆，並以當前頁為中心 */
const pageButtons = computed(() => {
  const maxButtons = 5;

  let start = page.value - 2;
  if (start < 1) start = 1;

  let end = start + maxButtons - 1;
  if (end > totalPages.value) {
    end = totalPages.value;
    start = Math.max(1, end - maxButtons + 1);
  }

  const buttons = [];
  for (let i = start; i <= end; i++) buttons.push(i);
  return buttons;
});

/** 首次進入頁面：先抓分類，再抓列表 */
onMounted(() => {
  fetchCategories();
  fetchList();
});
</script>
<style scoped>
/* ===== Page spacing：頁面上下留白，與全站一致 ===== */
.page {
  padding: 18px 0 56px;
}

/* ===== Breadcrumb：meta 資訊（輕量） ===== */
.crumb {
  color: #6b7280;
  /* 統一 meta 文字尺寸：14px（避免 12px 太小） */
  font-size: var(--text-sm);
  margin: 10px 0 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.crumbLink {
  color: #6b7280;
  text-decoration: none;
}
.crumbLink:hover {
  text-decoration: underline;
}
.sep { opacity: 0.7; }
.now { color: #111827; }

/* ===== Panel：卡片式外框（陰影 + 邊框 + 圓角） ===== */
.panel {
  background: #fff;
  border-radius: 24px;
  border: 1px solid rgba(16, 24, 40, 0.1);
  box-shadow: 0 10px 28px rgba(16, 24, 40, 0.1);
  padding: 18px;
}

/* 內框：藍色邊框提示，讓內容區有「被框住」的感覺 */
.inner {
  border-radius: 16px;
  border: 2px solid rgba(47, 118, 168, 0.45);
  overflow: hidden;
}

/* ===== Toolbar：搜尋工具列（高對比背景，凸顯操作區） ===== */
.toolbar {
  background: #8fb6d3;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(16, 24, 40, 0.1);
}
.toolLeft {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap; /* 小螢幕自動換行 */
}
.lab {
  /* 操作標籤：16px + 粗體，提升可掃描性 */
  font-size: var(--text-base);
  font-weight: 900;
  color: #0f172a;
}

/* ===== Select：篩選下拉 ===== */
.sel {
  height: 34px;
  border-radius: 10px;
  border: 2px solid rgba(16, 24, 40, 0.16);
  background: #fff;
  padding: 0 12px;
  font-size: var(--text-base);
  font-weight: 900;
}

/* ===== Keyword input：搜尋框 ===== */
.kw {
  height: 34px;
  width: 320px;
  border-radius: 999px; /* pill 形狀：更像「搜尋」 */
  border: 2px solid rgba(16, 24, 40, 0.16);
  padding: 0 14px;
  background: #fff;
  font-size: var(--text-base);
  font-weight: 900;
  outline: none;
}
/* Focus：提供清楚 focus ring，提升可用性 */
.kw:focus {
  border-color: rgba(0, 100, 220, 0.85);
  box-shadow: 0 0 0 3px rgba(0, 100, 220, 0.12);
}

/* ===== Primary button：搜尋（高注意力） ===== */
.go {
  height: 32px;
  padding: 0 18px;
  border-radius: 999px;
  border: 0;
  background: #f2cf57;
  font-size: var(--text-base);
  font-weight: 900;
  cursor: pointer;
}
.go:hover {
  filter: brightness(0.97);
}

/* ===== Secondary button：清除（低注意力） ===== */
.clear {
  height: 32px;
  padding: 0 16px;
  border-radius: 999px;
  border: 1px solid rgba(16, 24, 40, 0.18);
  background: #fff;
  font-size: var(--text-base);
  font-weight: 900;
  cursor: pointer;
}

/* ===== Table：主要閱讀區 ===== */
.tableWrap {
  padding: 0 8px 10px;
}
.tbl {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}
thead th {
  padding: 18px 10px 14px;
  /* 表頭：16px + 粗體，強化欄位層級 */
  font-size: var(--text-base);
  font-weight: 900;
  text-align: center;
  border-bottom: 1px solid rgba(16, 24, 40, 0.55);
}
tbody td {
  padding: 18px 10px;
  border-bottom: 1px solid rgba(16, 24, 40, 0.12);
  vertical-align: middle;
  /* 內文：16px + 正常字重（可讀性） */
  font-size: var(--text-base);
  font-weight: 400;
}
.tdCenter { text-align: center; }

/* 標題欄：標題 + 附件 icon，採用正常字重與舒適行高 */
.titleCell .zh {
  font-weight: 400;
  line-height: var(--leading-normal);
}
.titleCell .en {
  margin-top: 10px;
  font-weight: 400;
  color: #111827;
  line-height: var(--leading-normal);
}

/* 附件 link：用小 icon 降低干擾但仍可操作 */
.mini {
  margin-left: 8px;
  text-decoration: none;
}
.mini small {
  /* 檔案格式標註：更小字級（12px） */
  font-size: var(--text-xs);
}
.unit { color: #111827; }

/* Empty state：空資料提示（置中 + 高辨識） */
.empty {
  text-align: center;
  color: #98a2b3;
  font-size: var(--text-base);
  font-weight: 900;
  padding: 26px 0;
}

/* ===== Pager：分頁區（右側對齊，維持操作一致性） ===== */
.pager {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16px;
  padding: 14px 6px 0;
}
.count {
  margin-right: auto; /* 讓筆數靠左，控制靠右 */
  color: #98a2b3;
  font-size: var(--text-sm);
  font-weight: 400;
}
.p {
  display: flex;
  gap: 10px;
  align-items: center;
  font-size: var(--text-base);
  font-weight: 400;
}
.pg {
  font-weight: 400;
  /* 直接繼承父層字級，確保全站一致 */
  font-size: inherit;
}
.pg.on {
  font-weight: 700; /* 當前頁加粗，視覺提示 */
}
.pg:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

/* ===== RWD：縮小搜尋框寬度，避免擠爆工具列 ===== */
@media (max-width: 900px) {
  .kw {
    width: 200px;
  }
}
</style>