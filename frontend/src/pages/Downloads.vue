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
              <option v-for="k in kindOptions" :key="k" :value="k">{{ k }}</option>
            </select>

            <select class="sel" v-model="form.cat">
              <option value="">不分類</option>
              <option v-for="c in catOptions" :key="c" :value="c">{{ c }}</option>
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
                <th style="width:110px;">種類</th>
                <th style="width:140px;">類別</th>
                <th>標題</th>
                <th style="width:160px;">業務單位</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="r in pagedRows" :key="r.id">
                <td class="tdCenter">{{ r.kind }}</td>
                <td class="tdCenter">{{ r.cat }}</td>
                <td class="titleCell">
                  <div class="zh">
                    {{ r.zh }}
                    <a v-if="r.fileUrl" class="mini" :href="r.fileUrl" target="_blank" rel="noreferrer">📄</a>
                  </div>
                  <div class="en">
                    {{ r.en }}
                    <a v-if="r.linkUrl" class="mini" :href="r.linkUrl" target="_blank" rel="noreferrer">🔗</a>
                  </div>
                </td>
                <td class="tdCenter unit">{{ r.unit }}</td>
              </tr>

              <tr v-if="pagedRows.length===0">
                <td colspan="4" class="empty">沒有符合條件的資料</td>
              </tr>
            </tbody>
          </table>

          <div class="pager">
            <div class="count">{{ filteredRows.length }} 筆</div>

            <div class="p">
              <button class="pg" :disabled="page===1" @click="page=1">First</button>
              <button class="pg" :disabled="page===1" @click="page--">‹</button>

              <button
                v-for="n in pageButtons"
                :key="n"
                class="pg"
                :class="{ on: n===page }"
                @click="page=n"
              >{{ n }}</button>

              <button class="pg" :disabled="page===totalPages" @click="page++">›</button>
              <button class="pg" :disabled="page===totalPages" @click="page=totalPages">Last</button>
            </div>
          </div>
        </div>

      </div>
    </section>
  </main>
</template>

<script setup>
import { computed, reactive, ref, watch } from "vue";
import { RouterLink } from "vue-router";
const allRows = ref([
  {
    id: 1,
    kind: "法規",
    cat: "性別平等",
    zh: "國立中央大學校園性別事件防治要點(民國113年11月12日修訂)",
    en: "Regulations on the Prevention of Sexual Assault Sexual Harassment and Sexual Bullying on Campus of National Central University",
    unit: "學務處",
    fileUrl: "#",
    linkUrl: "",
  },
  {
    id: 2,
    kind: "法規",
    cat: "衛生保健",
    zh: "學校衛生法",
    en: "School Health Act",
    unit: "衛生保健組",
    fileUrl: "",
    linkUrl: "#",
  },
  { id: 3, kind: "表單", cat: "性別平等", zh: "性平事件申訴表", en: "Gender Equity Complaint Form", unit: "學務處", fileUrl:"#", linkUrl:"" },
  { id: 4, kind: "表單", cat: "住宿", zh: "宿舍申請表", en: "Dorm Application Form", unit: "住服組", fileUrl:"#", linkUrl:"" },
  { id: 5, kind: "文件", cat: "衛生保健", zh: "健康檢查說明", en: "Health Check Guide", unit: "衛生保健組", fileUrl:"", linkUrl:"#"},
]);

const form = reactive({
  kind: "",    
  cat: "",     
  keyword: "",
});

const query = reactive({
  kind: "",
  cat: "",
  keyword: "",
});

function applySearch(){
  query.kind = form.kind;
  query.cat = form.cat;
  query.keyword = form.keyword;
  page.value = 1;
}

function reset(){
  form.kind = "";
  form.cat = "";
  form.keyword = "";
  applySearch();
}

const kindOptions = computed(() => {
  return Array.from(new Set(allRows.value.map(r => r.kind)));
});

const catOptions = computed(() => {
  const rows = form.kind ? allRows.value.filter(r => r.kind === form.kind) : allRows.value;
  return Array.from(new Set(rows.map(r => r.cat)));
});

watch(() => form.kind, () => {
  if (form.cat && !catOptions.value.includes(form.cat)) form.cat = "";
});

const filteredRows = computed(() => {
  const kw = (query.keyword || "").toLowerCase();

  return allRows.value.filter(r => {
    if (query.kind && r.kind !== query.kind) return false;
    if (query.cat && r.cat !== query.cat) return false;

    if (kw){
      const hay = `${r.kind} ${r.cat} ${r.zh} ${r.en} ${r.unit}`.toLowerCase();
      if (!hay.includes(kw)) return false;
    }
    return true;
  });
});

const page = ref(1);
const pageSize = 8;

const totalPages = computed(() => Math.max(1, Math.ceil(filteredRows.value.length / pageSize)));

watch(filteredRows, () => {
  if (page.value > totalPages.value) page.value = totalPages.value;
});

const pagedRows = computed(() => {
  const start = (page.value - 1) * pageSize;
  return filteredRows.value.slice(start, start + pageSize);
});

const pageButtons = computed(() => {
  const max = Math.min(5, totalPages.value);
  return Array.from({ length: max }, (_, i) => i + 1);
});
</script>

<style scoped>
.page{ padding: 18px 0 56px; }

/* 修正：麵包屑改用 14px (sm)，移除 12px 硬編碼 */
.crumb{
  color:#6b7280;
  font-size: var(--text-sm);
  margin: 10px 0 18px;
  display:flex;
  align-items:center;
  gap: 8px;
}
.crumbLink{
  color:#6b7280;
  text-decoration:none;
}
.crumbLink:hover{
  text-decoration: underline;
}
.sep{ opacity:.7; }
.now{ color:#111827; }
.panel{
  background:#fff;
  border-radius: 24px;
  border: 1px solid rgba(16,24,40,.10);
  box-shadow: 0 10px 28px rgba(16,24,40,.10);
  padding: 18px;
}

.inner{
  border-radius: 16px;
  border: 2px solid rgba(47,118,168,.45);
  overflow:hidden;
}

.toolbar{
  background: #8fb6d3;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(16,24,40,.10);
}
.toolLeft{
  display:flex;
  align-items:center;
  gap: 12px;
  flex-wrap: wrap;
}
/* 修正：搜尋標籤改用 16px (base) */
.lab{ 
  font-size: var(--text-base);
  font-weight: 900; 
  color:#0f172a; 
}

/* 修正：下拉選單與輸入框改用 16px (base) */
.sel{
  height: 34px;
  border-radius: 10px;
  border: 2px solid rgba(16,24,40,.16);
  background:#fff;
  padding: 0 12px;
  font-size: var(--text-base);
  font-weight: 900;
}
.kw{
  height: 34px;
  width: 320px;
  border-radius: 999px;
  border: 2px solid rgba(16,24,40,.16);
  padding: 0 14px;
  background:#fff;
  font-size: var(--text-base);
  font-weight: 900;
  outline: none;
}
.kw:focus{ border-color: rgba(0,100,220,.85); box-shadow: 0 0 0 3px rgba(0,100,220,.12); }

/* 修正：按鈕改用 16px (base) */
.go{
  height: 32px;
  padding: 0 18px;
  border-radius: 999px;
  border: 0;
  background:#f2cf57;
  font-size: var(--text-base);
  font-weight: 900;
  cursor:pointer;
}
.go:hover{ filter: brightness(.97); }

.clear{
  height: 32px;
  padding: 0 16px;
  border-radius: 999px;
  border: 1px solid rgba(16,24,40,.18);
  background:#fff;
  font-size: var(--text-base);
  font-weight: 900;
  cursor:pointer;
}

/* 表格 */
.tableWrap{ padding: 0 8px 10px; }
.tbl{
  width:100%;
  border-collapse: collapse;
  background:#fff;
}
/* 修正：表頭改用 16px (base) */
thead th{
  padding: 18px 10px 14px;
  font-size: var(--text-base);
  font-weight: 900;
  text-align:center;
  border-bottom: 1px solid rgba(16,24,40,.55);
}
/* 修正：表格內容改用 16px (base) */
tbody td{
  padding: 18px 10px;
  border-bottom: 1px solid rgba(16,24,40,.12);
  vertical-align: middle;
  font-size: var(--text-base);
  font-weight: 400;
}
.tdCenter{ text-align:center; }

/* 修正：標題行高改用 1.6 (leading-normal) 提升繁體中文閱讀體驗 */
.titleCell .zh{
  font-weight: 400;
  line-height: var(--leading-normal);
}
.titleCell .en{
  margin-top: 10px;
  font-weight: 400;
  color:#111827;
  line-height: var(--leading-normal);
}
.mini{
  margin-left: 8px;
  text-decoration:none;
}
.unit{ color:#111827; }

/* 修正：空資料提示改用 16px (base) */
.empty{
  text-align:center;
  color:#98a2b3;
  font-size: var(--text-base);
  font-weight: 900;
  padding: 26px 0;
}

.pager{
  display:flex;
  justify-content:flex-end;
  align-items:center;
  gap: 16px;
  padding: 14px 6px 0;
}
/* 修正：筆數統計改用 14px (sm) */
.count{
  margin-right:auto;
  color:#98a2b3;
  font-size: var(--text-sm);
  font-weight: 400;
}

/* 修正：分頁按鈕改用 16px (base) */
.p{
  display:flex;
  gap: 10px;
  align-items:center;
  font-size: var(--text-base);
  font-weight: 400;
}
.pg{
  font-size: var(--text-base);
  font-weight: 400;
}
.pg.on{
  font-weight: 700; 
}
.pg:disabled{
  opacity:.35;
  cursor:not-allowed;
}

/* RWD */
@media (max-width: 900px){
  .kw{ width: 200px; }
}
</style>