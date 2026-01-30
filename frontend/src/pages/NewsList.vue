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
          <button
            class="tab"
            :class="{ on: activeTab === 'all' }"
            @click="changeTab('all')"
          >
            全部
          </button>
        </div>

        <div class="list">
          <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <span>載入中...</span>
          </div>

          <div v-else-if="events.length > 0">
            <div v-for="n in events" :key="n.id" class="row">
              <div class="tag" :class="getCategoryClass(n.category?.slug)">
                {{ n.category?.name || "公告" }}
              </div>

              <RouterLink
                class="title"
                :to="{ name: 'event-detail', params: { id: n.id } }"
              >
                {{ n.title }}
              </RouterLink>

              <div class="meta">
                {{ formatOrganizer(n.organizer_info) }} /
                {{ formatDate(n.published_at) }}
              </div>
            </div>
          </div>

          <div v-else class="empty">目前沒有相關資料</div>
        </div>

        <div class="pager">
          <div class="count">第 {{ page }} 頁</div>

          <div class="p" aria-label="分頁導航">
            <a
              href="#"
              @click.prevent="changePage(1)"
              :class="{ disabled: page === 1 }"
              >First</a
            >

            <a
              href="#"
              @click.prevent="changePage(page - 1)"
              :class="{ disabled: page === 1 }"
              >‹</a
            >

            <a class="on" href="#" @click.prevent>{{ page }}</a>

            <a
              href="#"
              @click.prevent="changePage(page + 1)"
              :class="{ disabled: isLastPage }"
              >›</a
            >
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { RouterLink } from "vue-router";
import { getEvents } from "../api/event"; // 引入 API

const activeTab = ref("all");
const loading = ref(false);
const events = ref([]);

// 分頁參數
const page = ref(1);
const pageSize = 10; // 每頁顯示 10 筆
const isLastPage = ref(false);

// 1. 取得資料
const fetchEvents = async () => {
  loading.value = true;
  try {
    const res = await getEvents({
      page: page.value,
      size: pageSize,
      locale: "zh-TW",
    });

    events.value = res;

    // 判斷是否為最後一頁 (若回傳筆數 < 預期筆數，代表後面沒了)
    // 註：若剛好回傳 10 筆且後面沒了，User 點下一頁會看到空資料，這是沒有 total count 下的妥協
    isLastPage.value = res.length < pageSize;
  } catch (error) {
    console.error("Fetch error:", error);
    events.value = [];
  } finally {
    loading.value = false;
  }
};

// 2. 切換頁碼
const changePage = (newPage) => {
  if (newPage < 1 || (isLastPage.value && newPage > page.value)) return;
  page.value = newPage;
  // page 改變會觸發 watch 還是直接呼叫? 建議直接呼叫
  fetchEvents();
  // 捲動到頂部
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// 3. Tab 切換 (目前後端未支援過濾，先保留介面)
const changeTab = (tab) => {
  activeTab.value = tab;
  page.value = 1;
  fetchEvents();
};

// 4. 工具函式
const formatDate = (isoStr) => {
  if (!isoStr) return "";
  const d = new Date(isoStr);
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, "0")}.${String(d.getDate()).padStart(2, "0")}`;
};

const formatOrganizer = (info) => {
  return info && info.name ? info.name : "未知單位";
};

// 5. 樣式對應：將後端的 slug 轉為對應的 CSS class
const getCategoryClass = (slug) => {
  if (!slug) return "adm"; // 預設綠色

  // 簡單映射邏輯
  if (slug.includes("speech") || slug.includes("activity")) {
    return "act"; // 橘色 (活動)
  }
  if (slug.includes("scholarship") || slug.includes("news")) {
    return "adm"; // 綠色 (行政/公告)
  }

  return "adm"; // 預設
};

onMounted(() => {
  fetchEvents();
});
</script>

<style scoped>
/* 既有樣式保留 */
.page {
  padding: 1.2rem 0 3.2rem;
}

.crumb {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin: 0.6rem 0 1rem;
  font-size: 0.86rem;
  color: #6b7280;
}
.crumb__home {
  color: #6b7280;
}
.crumb__home:hover {
  text-decoration: underline;
}
.crumb__sep {
  opacity: 0.8;
}

.newsWrap {
  width: min(65rem, 100%);
  margin: 0 auto;
}
.board {
  background: #fff;
  border-radius: 1.35rem;
  border: 1px solid rgba(16, 24, 40, 0.1);
  box-shadow: 0 0.7rem 1.8rem rgba(16, 24, 40, 0.1);
  padding: 1.35rem;
  min-height: 400px; /* 增加最小高度 */
}

.tabs {
  display: flex;
  gap: 2.2rem;
  margin-bottom: 1.2rem;
}
.tab {
  border: 0;
  background: transparent;
  padding: 0.7rem 1.6rem;
  border-radius: 999px;
  font-size: 1rem;
  font-weight: 700;
  color: #98a2b3;
  cursor: pointer;
}
.tab.on {
  background: #f2cf57;
  color: #111827;
}

.list {
  border-top: 1px solid rgba(16, 24, 40, 0.1);
  min-height: 200px;
}
.row {
  display: grid;
  grid-template-columns: 5.6rem 1fr 16rem;
  gap: 1.1rem;
  align-items: center;
  padding: 1.1rem 0;
  border-bottom: 1px solid rgba(16, 24, 40, 0.1);
}

.tag {
  font-size: 1rem;
  font-weight: 500;
  padding: 0.45rem 1rem;
  border-radius: 0.75rem;
  text-align: center;
  white-space: nowrap; /* 防止文字換行 */
}
/* 活動類：橘色系 */
.tag.act {
  background: #f7d7b8;
  color: #7a3e10;
}
/* 行政類：綠色系 */
.tag.adm {
  background: #dff2d6;
  color: #1a5a1a;
}

.title {
  font-size: 1.5rem;
  font-weight: 400;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-decoration: none;
}
.title:hover {
  text-decoration: underline;
}

.meta {
  text-align: right;
  font-size: 1rem;
  color: #98a2b3;
  white-space: nowrap;
}

.empty {
  padding: 3rem 0;
  text-align: center;
  color: #98a2b3;
  font-weight: 500;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
  color: #6b7280;
  gap: 10px;
}
.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #eee;
  border-top-color: #f2cf57;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.pager {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
  padding-top: 1.1rem;
}
.count {
  margin-right: auto;
  font-size: 1rem;
  color: #98a2b3;
}
.p {
  display: flex;
  gap: 0.9rem;
  font-size: 1rem;
  font-weight: 500;
}
.p a {
  color: inherit;
  text-decoration: none;
  cursor: pointer;
  user-select: none;
}
.p a:hover:not(.disabled) {
  text-decoration: underline;
}
.p a.on {
  background: #f2cf57;
  padding: 0.35rem 0.75rem;
  border-radius: 0.5rem;
  text-decoration: none;
  pointer-events: none;
}
/* 禁用狀態樣式 */
.p a.disabled {
  color: #d1d5db;
  pointer-events: none;
  cursor: default;
}

/* RWD */
@media (max-width: 900px) {
  .row {
    grid-template-columns: 5.6rem 1fr;
  }
  .meta {
    text-align: left;
    font-size: 0.9rem;
    margin-top: 4px;
  }
  /* 手機版讓標題與 meta 堆疊 */
  .row {
    display: flex;
    flex-wrap: wrap;
  }
  .tag {
    flex: 0 0 auto;
  }
  .title {
    flex: 1 1 auto;
    min-width: 200px;
  }
  .meta {
    width: 100%;
    padding-left: calc(5.6rem + 1.1rem);
  }
}
</style>
