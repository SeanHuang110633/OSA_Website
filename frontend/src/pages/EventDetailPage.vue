<template>
  <div class="page-container">
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>正在載入活動資訊...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>⚠️ {{ error }}</p>
      <button class="back-btn" @click="goBack">返回列表</button>
    </div>

    <main v-else-if="event" class="content-wrapper">
      <nav class="breadcrumb">
        <span class="crumb-link" @click="goBack">最新消息</span>
        <span class="sep">/</span>
        <span class="current">活動詳情</span>
      </nav>

      <article class="event-card">
        <header class="event-header">
          <div class="meta-top">
            <span class="badge">{{ event.category?.name || "公告" }}</span>
            <span class="date">{{ formatDate(event.published_at) }}</span>
          </div>

          <h1 class="title">{{ event.title }}</h1>

          <div class="organizer-info">
            <span class="icon">🏢</span>
            <span class="label">承辦單位：</span>
            <span class="value">{{
              formatOrganizer(event.organizer_info)
            }}</span>
          </div>
        </header>

        <hr class="divider" />

        <div class="editor-content" v-html="event.content"></div>

        <section
          v-if="event.attachments && event.attachments.length > 0"
          class="attachments-section"
        >
          <h3 class="sec-title">📎 附件與相關連結</h3>
          <ul class="file-list">
            <li
              v-for="(file, index) in event.attachments"
              :key="index"
              class="file-item"
            >
              <span class="file-icon">{{ getFileIcon(file.type) }}</span>

              <a
                :href="file.path"
                target="_blank"
                rel="noopener noreferrer"
                class="file-link"
              >
                {{ file.title || "下載附件" }}
              </a>

              <span class="file-type-tag" v-if="file.type === 'link'"
                >外部連結</span
              >
            </li>
          </ul>
        </section>
      </article>

      <div class="footer-actions">
        <button class="back-btn outline" @click="goBack">‹ 返回列表</button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
// 記得確認 import 路徑是否正確
import { getEventDetail } from "../api/event.js";

const route = useRoute();
const router = useRouter();

const loading = ref(true);
const error = ref(null);
const event = ref(null);

// 初始化：取得資料
onMounted(async () => {
  const eventId = route.params.id; // 從 URL 取得 ID
  if (!eventId) {
    error.value = "無效的活動 ID";
    loading.value = false;
    return;
  }

  try {
    loading.value = true;
    // 呼叫 API
    const data = await getEventDetail(eventId, "zh-TW");
    event.value = data;
  } catch (err) {
    console.error(err);
    error.value = "找不到該活動或網路發生錯誤";
  } finally {
    loading.value = false;
  }
});

// 工具：格式化日期
const formatDate = (isoString) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
};

// 工具：格式化承辦單位
const formatOrganizer = (info) => {
  if (info && info.name) return info.name;
  return "無資訊"; // 若為 null 顯示預設文字
};

// 工具：取得附件 Icon
const getFileIcon = (type) => {
  if (type === "link") return "🔗";
  if (type === "image") return "🖼️";
  return "📄"; // 預設檔案圖示
};

// 導航
const goBack = () => {
  router.push({ name: "news" }); // 或 router.go(-1)
};
</script>

<style scoped>
/* 容器設定 */
.page-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 60vh;
}

/* 麵包屑 */
.breadcrumb {
  margin-bottom: 24px;
  font-size: 0.95rem;
  color: #666;
}
.crumb-link {
  cursor: pointer;
  color: #0f3a63; /* 主色調 */
  font-weight: 600;
}
.crumb-link:hover {
  text-decoration: underline;
}
.sep {
  margin: 0 8px;
  color: #ccc;
}
.current {
  color: #999;
}

/* 卡片主體 */
.event-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  padding: 40px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

/* Header 區域 */
.event-header {
  margin-bottom: 24px;
}
.meta-top {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
.badge {
  background: #eef6ff;
  color: #0f3a63;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 700;
}
.date {
  color: #888;
  font-size: 0.9rem;
}
.title {
  font-size: 2rem;
  font-weight: 800;
  color: #1a1a1a;
  line-height: 1.4;
  margin-bottom: 16px;
}
.organizer-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.95rem;
  color: #555;
  background: #f9f9f9;
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 8px;
}

.divider {
  border: 0;
  height: 1px;
  background: #eee;
  margin: 30px 0;
}

/* 內容編輯器樣式 (Content) */
/* 使用 :deep() 讓樣式穿透 v-html 渲染出來的內容 */
.editor-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
}
.editor-content :deep(p) {
  margin-bottom: 1.2em;
}
.editor-content :deep(a) {
  color: #2563eb;
  text-decoration: underline;
  word-break: break-all;
}
.editor-content :deep(a:hover) {
  color: #1d4ed8;
}
.editor-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 16px 0;
}
.editor-content :deep(ul),
.editor-content :deep(ol) {
  margin-bottom: 1.2em;
  padding-left: 1.5em;
}

/* 附件區域 */
.attachments-section {
  margin-top: 40px;
  padding: 24px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}
.sec-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #0f172a;
}
.file-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.file-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: #fff;
  border: 1px solid #edf2f7;
  border-radius: 8px;
  transition: all 0.2s;
}
.file-item:hover {
  border-color: #cbd5e1;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}
.file-link {
  text-decoration: none;
  color: #334155;
  font-weight: 600;
  flex: 1;
}
.file-link:hover {
  color: #0f3a63;
}
.file-type-tag {
  font-size: 0.75rem;
  color: #94a3b8;
  border: 1px solid #e2e8f0;
  padding: 2px 6px;
  border-radius: 4px;
}

/* 底部按鈕 */
.footer-actions {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
.back-btn {
  padding: 10px 24px;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}
.back-btn.outline {
  background: transparent;
  border: 1px solid #cbd5e1;
  color: #64748b;
}
.back-btn.outline:hover {
  border-color: #94a3b8;
  color: #334155;
}

/* RWD */
@media (max-width: 768px) {
  .event-card {
    padding: 24px;
  }
  .title {
    font-size: 1.6rem;
  }
}

/* Loading & Error */
.loading-state,
.error-state {
  text-align: center;
  padding: 60px 0;
  color: #666;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top-color: #0f3a63;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
