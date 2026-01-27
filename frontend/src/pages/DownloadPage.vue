<template>
  <main class="container page">
    <div class="crumb">
      <RouterLink class="crumbLink" to="/">首頁</RouterLink>
      <span class="sep">/</span>
      <span class="now">下載專區</span>
    </div>

    <section class="panel">
      <div class="inner">
        <div class="toolbar">
          <div class="toolLeft">
            <div class="lab">搜尋資料：</div>

            <select class="sel" v-model="form.kind">
              <option value="">全部</option>
              <option v-for="k in kindOptions" :key="k" :value="k">
                {{ kindMap[k] }}
              </option>
            </select>

            <select class="sel" v-model="form.catId">
              <option value="">不分類</option>
              <option v-for="c in categoryList" :key="c.id" :value="c.id">
                {{ c.name }}
              </option>
            </select>

            <input
              class="kw"
              v-model.trim="form.keyword"
              placeholder="輸入關鍵字..."
              @keydown.enter="applySearch"
            />

            <button class="go" type="button" @click="applySearch">搜尋</button>
            <button class="clear" type="button" @click="reset">清除</button>
          </div>
        </div>

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
              <tr v-for="r in allRows" :key="r.id">
                <td class="tdCenter">{{ kindMap[r.type] || r.type }}</td>
                <td class="tdCenter">{{ r.category.name }}</td>
                <td class="titleCell">
                  <div class="zh">
                    {{ r.title }}
                    <span v-for="att in r.attachments" :key="att.id">
                      <a
                        class="mini"
                        :href="att.path"
                        target="_blank"
                        rel="noreferrer"
                        :title="att.title"
                      >
                        {{ att.type === "file" ? "📄" : "🔗" }}
                        <small v-if="att.file_format"
                          >({{ att.file_format }})</small
                        >
                      </a>
                    </span>
                  </div>
                  <div class="en"></div>
                </td>
                <td class="tdCenter unit">{{ r.department || "-" }}</td>
              </tr>

              <tr v-if="allRows.length === 0">
                <td colspan="4" class="empty">沒有符合條件的資料</td>
              </tr>
            </tbody>
          </table>

          <div class="pager">
            <div class="count">{{ totalCount }} 筆</div>

            <div class="p">
              <button class="pg" :disabled="page === 1" @click="page = 1">
                First
              </button>
              <button class="pg" :disabled="page === 1" @click="page--">
                ‹
              </button>

              <button
                v-for="n in pageButtons"
                :key="n"
                class="pg"
                :class="{ on: n === page }"
                @click="page = n"
              >
                {{ n }}
              </button>

              <button
                class="pg"
                :disabled="page === totalPages"
                @click="page++"
              >
                ›
              </button>
              <button
                class="pg"
                :disabled="page === totalPages"
                @click="page = totalPages"
              >
                Last
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { onMounted, reactive, ref, watch, computed } from "vue";
import { RouterLink } from "vue-router";
import { getDownloads, getCategories } from "../api/download.js";

// --- 狀態管理 ---
const allRows = ref([]); // API 回傳的列表資料
const totalCount = ref(0); // API 回傳的總筆數
const categoryList = ref([]); // API 回傳的分類清單
const page = ref(1);
const pageSize = 10; // 設定每頁顯示筆數

// --- 映射設定 ---
const kindMap = {
  regulation: "法規",
  form: "表單",
  other: "其他", // 對應 document 或其他
};
const kindOptions = Object.keys(kindMap);

// --- 搜尋表單 ---
const form = reactive({
  kind: "",
  catId: "", // 改用 ID
  keyword: "",
});

// --- API 請求 ---

// 1. 取得分類
async function fetchCategories() {
  try {
    const res = await getCategories("zh-TW");
    categoryList.value = res;
  } catch (err) {
    console.error("分類獲取失敗", err);
  }
}

// 2. 取得列表
async function fetchList() {
  try {
    const res = await getDownloads({
      locale: "zh-TW",
      page: page.value,
      size: pageSize,
      type: form.kind || null,
      category_id: form.catId || null,
      query: form.keyword || null,
    });

    allRows.value = res.items;
    totalCount.value = res.total;
  } catch (err) {
    console.error("列表獲取失敗", err);
  }
}

// --- 操作行為 ---

function applySearch() {
  page.value = 1; // 搜尋時重置頁碼
  fetchList();
}

function reset() {
  form.kind = "";
  form.catId = "";
  form.keyword = "";
  applySearch();
}

// --- 分頁邏輯 ---

// 計算總頁數 (依賴 API 回傳的 totalCount)
const totalPages = computed(() =>
  Math.max(1, Math.ceil(totalCount.value / pageSize)),
);

// 監聽頁碼變動，自動發送請求
watch(page, () => {
  fetchList();
});

// 計算分頁按鈕顯示範圍
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
  for (let i = start; i <= end; i++) {
    buttons.push(i);
  }
  return buttons;
});

// --- 初始化 ---
onMounted(() => {
  fetchCategories();
  fetchList();
});
</script>

<style scoped>
.page {
  padding: 18px 0 56px;
}
.crumb {
  color: #6b7280;
  font-size: 12px;
  margin: 10px 0 18px;
}
.crumb {
  color: #6b7280;
  font-size: 12px;
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
.sep {
  opacity: 0.7;
}
.now {
  color: #111827;
}
.panel {
  background: #fff;
  border-radius: 24px;
  border: 1px solid rgba(16, 24, 40, 0.1);
  box-shadow: 0 10px 28px rgba(16, 24, 40, 0.1);
  padding: 18px;
}

.inner {
  border-radius: 16px;
  border: 2px solid rgba(47, 118, 168, 0.45);
  overflow: hidden;
}

.toolbar {
  background: #8fb6d3;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(16, 24, 40, 0.1);
}
.toolLeft {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.lab {
  font-weight: 900;
  color: #0f172a;
}

.sel {
  height: 34px;
  border-radius: 10px;
  border: 2px solid rgba(16, 24, 40, 0.16);
  background: #fff;
  padding: 0 12px;
  font-weight: 900;
}
.kw {
  height: 34px;
  width: 320px;
  border-radius: 999px;
  border: 2px solid rgba(16, 24, 40, 0.16);
  padding: 0 14px;
  background: #fff;
  font-weight: 900;
  outline: none;
}
.kw:focus {
  border-color: rgba(0, 100, 220, 0.85);
  box-shadow: 0 0 0 3px rgba(0, 100, 220, 0.12);
}

.go {
  height: 32px;
  padding: 0 18px;
  border-radius: 999px;
  border: 0;
  background: #f2cf57;
  font-weight: 900;
  cursor: pointer;
}
.go:hover {
  filter: brightness(0.97);
}

.clear {
  height: 32px;
  padding: 0 16px;
  border-radius: 999px;
  border: 1px solid rgba(16, 24, 40, 0.18);
  background: #fff;
  font-weight: 900;
  cursor: pointer;
}

/* 表格 */
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
  font-weight: 900;
  text-align: center;
  border-bottom: 1px solid rgba(16, 24, 40, 0.55);
}
tbody td {
  padding: 18px 10px;
  border-bottom: 1px solid rgba(16, 24, 40, 0.12);
  vertical-align: middle;
  font-weight: 400;
}
.tdCenter {
  text-align: center;
}

.titleCell .zh {
  font-weight: 400;
  line-height: 1.6;
}
.titleCell .en {
  margin-top: 10px;
  font-weight: 400;
  color: #111827;
  line-height: 1.6;
}
.mini {
  margin-left: 8px;
  text-decoration: none;
}
.unit {
  color: #111827;
}

.empty {
  text-align: center;
  color: #98a2b3;
  font-weight: 900;
  padding: 26px 0;
}

.pager {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16px;
  padding: 14px 6px 0;
}
.count {
  margin-right: auto;
  color: #98a2b3;
  font-weight: 400;
}

.p {
  display: flex;
  gap: 10px;
  align-items: center;
  font-weight: 400;
}
.pg {
  font-weight: 400;
}
.pg.on {
  font-weight: 700;
}
.pg:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

/* RWD */
@media (max-width: 900px) {
  .kw {
    width: 200px;
  }
}
</style>
