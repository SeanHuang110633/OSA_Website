<template>
  <main class="container page">
    <div class="crumb">
      <RouterLink class="crumb__home" to="/">首頁</RouterLink>
      <span class="crumb__sep">/</span>
      <b>最新消息</b>
    </div>

    <div class="newsWrap">
      <section class="board">
        <div class="tabs" role="tablist" aria-label="最新消息分類">
          <button class="tab" :class="{ on: activeTab==='all' }" @click="activeTab='all'">全部</button>
          <button class="tab" :class="{ on: activeTab==='adm' }" @click="activeTab='adm'">行政</button>
          <button class="tab" :class="{ on: activeTab==='act' }" @click="activeTab='act'">活動</button>
        </div>

        <div class="list">
          <div v-for="n in visibleFiltered" :key="n.id" class="row">
            <div class="tag" :class="n.type">{{ n.typeLabel }}</div>
            <a class="title" href="#">{{ n.title }}</a>
            <div class="meta">{{ n.unit }} / {{ n.date }}</div>
          </div>

          <div v-if="filtered.length === 0" class="empty">目前沒有符合的資料</div>

          <!-- 查看更多（同頁展開） -->
          <div v-if="canLoadMore" class="moreWrap">
            <button class="moreBtn" type="button" @click="loadMore">
              查看更多
            </button>
          </div>
        </div>

        <div class="pager">
          <!-- 顯示：目前顯示 / 總筆數 -->
          <div class="count">{{ visibleFiltered.length }} / {{ filtered.length }} 筆</div>

          <!-- 保留原本 pager 外觀（目前不做真的分頁邏輯） -->
          <div class="p" aria-label="分頁（外觀保留）">
            <a href="#" @click.prevent>First</a>
            <a href="#" @click.prevent>‹</a>
            <a class="on" href="#" @click.prevent>1</a>
            <a href="#" @click.prevent>2</a>
            <a href="#" @click.prevent>3</a>
            <a href="#" @click.prevent>4</a>
            <a href="#" @click.prevent>5</a>
            <a href="#" @click.prevent>›</a>
            <a href="#" @click.prevent>Last</a>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { RouterLink } from "vue-router";

const activeTab = ref("all");

const items = ref([
  { id: 1, type:"act", typeLabel:"活動", title:"114學年度第2學期大一週會及院週會", unit:"萬怡／學務處", date:"2025.10.28" },
  { id: 2, type:"adm", typeLabel:"行政", title:"針對近日臺北捷運隨機傷人社會案件，請本校各單位及師生加強相關作為", unit:"生輔組", date:"2025.12.26" },
  { id: 3, type:"adm", typeLabel:"行政", title:"針對近日臺北捷運隨機傷人社會案件，請本校各單位及師生加強相關作為", unit:"生輔組", date:"2025.12.26" },
  { id: 4, type:"act", typeLabel:"活動", title:"114學年度第2學期大一週會及院週會", unit:"萬怡／學務處", date:"2025.10.28" },

  // 多放幾筆測試「查看更多」效果（可刪）
  { id: 5, type:"adm", typeLabel:"行政", title:"（測試）系統維護公告：XX/XX 晚間 10 點", unit:"資管組", date:"2025.11.01" },
  { id: 6, type:"act", typeLabel:"活動", title:"（測試）校園活動：社團博覽會", unit:"課外組", date:"2025.11.05" },
  { id: 7, type:"adm", typeLabel:"行政", title:"（測試）宿舍申請時程提醒", unit:"住服組", date:"2025.11.10" },
  { id: 8, type:"act", typeLabel:"活動", title:"（測試）志工招募：迎新服務隊", unit:"服務學習", date:"2025.11.12" },
]);

const filtered = computed(() => {
  if (activeTab.value === "all") return items.value;
  return items.value.filter(x => x.type === activeTab.value);
});

/* ===== 查看更多：一次多顯示幾筆 ===== */
const pageSize = 5;                 // 每次多顯示 5 筆
const visibleCount = ref(pageSize); // 目前顯示筆數上限

const visibleFiltered = computed(() => {
  return filtered.value.slice(0, visibleCount.value);
});

const canLoadMore = computed(() => {
  return filtered.value.length > visibleCount.value;
});

function loadMore() {
  visibleCount.value += pageSize;
}

// 切 tab 時重置顯示筆數
watch(activeTab, () => {
  visibleCount.value = pageSize;
});
</script>

<style scoped>
.page{ padding: 1.2rem 0 3.2rem; }

.crumb{
  display:flex;
  align-items:center;
  gap:.4rem;
  margin:.6rem 0 1rem;
  font-size:.86rem;
  color:#6b7280;
}
.crumb__home{ color:#6b7280; }
.crumb__home:hover{ text-decoration: underline; }
.crumb__sep{ opacity:.8; }

.newsWrap{
  width: min(65rem, 100%);
  margin: 0 auto;
}
.board{
  background:#fff;
  border-radius: 1.35rem;
  border: 1px solid rgba(16,24,40,.10);
  box-shadow: 0 .7rem 1.8rem rgba(16,24,40,.10);
  padding: 1.35rem;
}

.tabs{
  display:flex;
  gap: 2.2rem;
  margin-bottom: 1.2rem;
}
.tab{
  border:0;
  background:transparent;
  padding:.7rem 1.6rem;
  border-radius:999px;
  font-size:1rem;
  font-weight:700;
  color:#98a2b3;
  cursor:pointer;
}
.tab.on{
  background:#f2cf57;
  color:#111827;
}

.list{
  border-top:1px solid rgba(16,24,40,.10);
}
.row{
  display:grid;
  grid-template-columns: 5.6rem 1fr 16rem;
  gap:1.1rem;
  align-items:center;
  padding:1.1rem 0;
  border-bottom:1px solid rgba(16,24,40,.10);
}

.tag{
  font-size:1rem;
  font-weight:500;
  padding:.45rem 1rem;
  border-radius:.75rem;
  text-align:center;
}
.tag.act{ background:#f7d7b8; color:#7a3e10; }
.tag.adm{ background:#dff2d6; color:#1a5a1a; }

.title{
  font-size:1.5rem;
  font-weight:400;
  color:#111827;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.title:hover{ text-decoration: underline; }

.meta{
  text-align:right;
  font-size:1rem;
  color:#98a2b3;
  white-space:nowrap;
}

.empty{
  padding: 1.2rem 0;
  color:#98a2b3;
}

/* ===== 查看更多按鈕 ===== */
.moreWrap{
  display:flex;
  justify-content:flex-end;
  padding-top: 1.1rem;
}
.moreBtn{
  border: 0;
  cursor: pointer;
  background: #f2cf57;
  color: #111827;
  font-size: 1rem;
  font-weight: 800;
  padding: .85rem 1.6rem;
  border-radius: 999px;
  box-shadow: 0 .4rem 1rem rgba(16,24,40,.10);
}
.moreBtn:hover{
  filter: brightness(.98);
}

.pager{
  display:flex;
  justify-content:flex-end;
  align-items:center;
  gap:1rem;
  padding-top:1.1rem;
}
.count{
  margin-right:auto;
  font-size:1rem;
  color:#98a2b3;
}
.p{
  display:flex;
  gap:.9rem;
  font-size:1rem;
  font-weight:500;
}
.p a{
  color: inherit;
  text-decoration: none;
}
.p a:hover{
  text-decoration: underline;
}
.p a.on{
  background:#f2cf57;
  padding:.35rem .75rem;
  border-radius:.5rem;
  text-decoration: none;
}

/* RWD */
@media (max-width:900px){
  .row{ grid-template-columns: 5.6rem 1fr; }
  .meta{ text-align:left; }
}
</style>