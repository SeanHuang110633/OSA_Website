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
import { getEvents } from "../api/event.js"; // 請確認路徑是否正確

const router = useRouter();
const newsList = ref([]);
const loading = ref(true);

// ---------------------------------------
// 左側 Events 邏輯
// ---------------------------------------

// 1. 取得資料
const fetchNews = async () => {
  try {
    loading.value = true;
    // 呼叫 API: 預設抓第一頁，取 5 筆，繁體中文
    const res = await getEvents({ page: 1, size: 5, locale: "zh-TW" });
    newsList.value = res;
  } catch (error) {
    console.error("Failed to fetch news:", error);
  } finally {
    loading.value = false;
  }
};

// 2. 格式化日期 (YYYY.MM.DD)
const formatDate = (isoString) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}.${m}.${d}`;
};

// 3. 格式化承辦單位
const formatOrganizer = (info) => {
  // 後端回傳可能是 null 或 { name: null, ... }
  if (info && info.name) {
    return info.name;
  }
  return "沒有資訊";
};

// 4. 路由跳轉
const goToNewsList = () => {
  // 導向 /news
  router.push({ name: "news" });
};

const goToDetail = (id) => {
  // 導向詳情頁 (未來實作詳情頁時使用)
  router.push({ name: "event-detail", params: { id } });
  console.log(`Go to event detail: ${id}`);
};

// -----------------------------------------------
// 右側 各單位連結
// -----------------------------------------------
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
/* 原有樣式保持不變，新增 organizer 樣式 */

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
  font-size: 1.5rem;
  line-height: 1.2;
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
  min-height: 200px; /* 避免沒資料時高度塌陷 */
}
.item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line); /* 需確認 var(--line) 是否有定義，或改用 rgba */
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
  font-size: 13px;
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

/* 新增：承辦單位樣式 */
.organizer {
  color: #6b7280; /* 灰色 */
  font-size: 0.85em;
  margin-left: 8px;
  font-weight: normal;
}

.date {
  font-size: 12px;
  color: #6b7280;
  flex: 0 0 auto;
}

.actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 10px;
}
.pill-btn {
  /* 假設這是一個全局樣式，如果沒有定義，這裡補一個簡單的 */
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
  font-size: 13px;
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
  font-size: 13px;
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
  font-size: 13px;
}

@media (max-width: 980px) {
  .row {
    grid-template-columns: 1fr;
  }
  .text {
    max-width: 100%;
  }
}

/* Badge & Dot 樣式補強 (如果全域沒定義) */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 700;
  color: #4b5563;
  flex-shrink: 0; /* 防止擠壓 */
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
