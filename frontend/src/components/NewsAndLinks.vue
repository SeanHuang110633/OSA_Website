<template>
  <section class="row">
    <div class="card news">
      <div class="head">
        <div class="hTitle">
          <span class="hIcon">📰</span>
          <span>最新消息</span>
        </div>
      </div>

      <div class="list">
        <div v-if="loading" class="loading-state">載入中...</div>

        <div v-else v-for="item in newsList" :key="item.id" class="item">
          <div class="left">
            <span class="badge">
              <span class="dot blue"></span>
              <span>{{ item.category?.name || "公告" }}</span>
            </span>

            <a class="text" href="#" @click.prevent="goToDetail(item.id)">
              {{ item.title }}

              <span class="organizer">
                (承辦單位: {{ formatOrganizer(item.organizer_info) }})
              </span>
            </a>
          </div>

          <div class="date">{{ formatDate(item.published_at) }}</div>
        </div>
      </div>

      <div class="actions">
        <button class="pill-btn small" @click="goToNewsList">查看更多</button>
      </div>
    </div>

    <div class="card links">
      <div class="head">
        <div class="hTitle">
          <span class="hIcon">🔗</span>
          <span>各單位連結</span>
        </div>
      </div>

      <div class="linkList">
        <a v-for="(l, i) in units" :key="i" class="u" href="#">{{ l }}</a>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getEvents } from "../api/event.js"; 

const router = useRouter();
const newsList = ref([]);
const loading = ref(true);

const fetchNews = async () => {
  try {
    loading.value = true;
    const res = await getEvents({ page: 1, size: 5, locale: "zh-TW" });
    newsList.value = res;
  } catch (error) {
    console.error("Failed to fetch news:", error);
  } finally {
    loading.value = false;
  }
};

const formatDate = (isoString) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}.${m}.${d}`;
};

const formatOrganizer = (info) => {
  if (info && info.name) {
    return info.name;
  }
  return "沒有資訊";
};

const goToNewsList = () => {
  router.push({ name: "news" });
};

const goToDetail = (id) => {
  router.push({ name: "event-detail", params: { id } });
};

const units = [
  "諮商輔導中心",
  "課外活動組",
  "生活輔導組",
  "服務學習中心",
  "住宿服務組",
  "衛生保健組",
  "職涯發展中心",
  "原住民族學生資源中心",
];

onMounted(() => {
  fetchNews();
});
</script>

<style scoped>
.row {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 16px;
}
.news {
  padding: 14px 14px 12px;
}
.links {
  padding: 14px;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.hTitle {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 900;
  /* 修正：區塊標題統一使用 24px */
  font-size: var(--text-2xl);
  line-height: var(--leading-tight);
}
.hIcon {
  width: 26px;
  height: 26px;
  display: grid;
  place-items: center;
}

.list {
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
  min-height: 200px; 
}
.item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-bottom: 1px solid rgba(16, 24, 40, 0.08);
}
.item:last-child {
  border-bottom: 0;
}
.left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}
.text {
  /* 重點修正：消除 13px，改為 16px 並設定行高與字重 */
  font-size: var(--text-base);
  line-height: 1.5;
  font-weight: 500;
  color: #1b2430;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 600px;
  text-decoration: none;
  cursor: pointer;
}
.text:hover {
  text-decoration: underline;
}

.organizer {
  color: #6b7280; 
  /* 修正：使用極小字變數 */
  font-size: var(--text-xs);
  margin-left: 8px;
  font-weight: normal;
}

.date {
  /* 修正：日期統一改為 14px */
  font-size: var(--text-sm);
  color: #6b7280;
  flex: 0 0 auto;
}

.actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 10px;
}
.pill-btn {
  border: 1px solid #ddd;
  background: white;
  border-radius: 20px;
  cursor: pointer;
}
.pill-btn:hover {
  background: #f9fafb;
}
.small {
  padding: 8px 14px;
  /* 修正：按鈕保持標準 16px */
  font-size: var(--text-base);
}

.linkList {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px 12px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 12px;
}
.u {
  /* 修正：連結列表標準化為 16px 確保易點擊 */
  font-size: var(--text-base);
  padding: 6px 8px;
  border-radius: 10px;
  color: #1b2430;
  text-decoration: none;
}
.u:hover {
  background: rgba(21, 58, 99, 0.06);
}

.loading-state {
  padding: 20px;
  text-align: center;
  color: #999;
  /* 修正：載入中提示改為 16px */
  font-size: var(--text-base);
}

@media (max-width: 980px) {
  .row {
    grid-template-columns: 1fr;
  }
  .text {
    max-width: 100%;
  }
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  /* 修正：標籤可維持小字 12px */
  font-size: var(--text-xs);
  font-weight: 700;
  color: #4b5563;
  flex-shrink: 0; 
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}
.dot.blue {
  background-color: #3b82f6;
}
</style>