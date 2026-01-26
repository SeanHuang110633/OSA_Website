<template>
  <section id="weekly-events" class="eventWrap">
    <div class="eventCard">
      <div class="head">
        <div class="title">
          <span class="bar" aria-hidden="true"></span>
          <span class="t">活動列表</span>
        </div>

        <div class="modes" role="tablist" aria-label="顯示模式">
          <button
            class="mode"
            :class="{ on: mode === 'card' }"
            type="button"
            @click="mode = 'card'"
          >
            卡片模式
          </button>
          <button
            class="mode"
            :class="{ on: mode === 'list' }"
            type="button"
            @click="mode = 'list'"
          >
            列表模式
          </button>
        </div>
      </div>

      <div v-if="loading" class="loading-state">資料讀取中...</div>

      <div v-else-if="mode === 'card'" class="body slider-body">
        <button class="nav prev" aria-label="上一張" @click="slidePrev">
          ‹
        </button>

        <div class="slider-viewport">
          <div
            class="track"
            :style="{
              transform: `translateX(-${sliderTranslateX}%)`,
              transition: isResetting ? 'none' : 'transform 0.4s ease-in-out',
            }"
            @transitionend="handleTransitionEnd"
          >
            <article
              v-for="(e, index) in displayEvents"
              :key="`${e.id}-${index}`"
              class="card-wrapper"
            >
              <div class="card">
                <div class="thumb-img">
                  <img
                    :src="getImageUrl(e.local_img_path)"
                    :alt="e.title"
                    @error="handleImageError"
                  />
                  <span
                    class="status-badge"
                    :class="getStatusClass(e.status)"
                    >{{ e.status }}</span
                  >
                </div>

                <div class="content">
                  <div class="meta-row">
                    <span class="meta-item" title="瀏覽次數">
                      <span class="icon">👁</span>
                      <span class="label">瀏覽:</span>
                      <span class="val">{{ e.views }}</span>
                    </span>
                    <span class="meta-divider">|</span>
                    <span class="meta-item" title="報名人數">
                      <span class="icon">👤</span>
                      <span class="label">報名:</span>
                      <span class="val">{{ e.joined }}</span>
                    </span>
                  </div>

                  <div class="date">{{ formatDateShort(e.created_at) }}</div>
                  <div class="name" :title="e.title">{{ e.title }}</div>

                  <div class="tags-section">
                    <div v-if="e.target_audience.length" class="tag-group">
                      <span class="tag-label-text">對象:</span>
                      <div class="tag-list">
                        <span
                          v-for="tag in e.target_audience"
                          :key="tag"
                          class="tag target"
                          >{{ tag }}</span
                        >
                      </div>
                    </div>
                    <div v-if="e.sdg_labels.length" class="tag-group">
                      <span class="tag-label-text">SDGs:</span>
                      <div class="tag-list">
                        <span
                          v-for="tag in e.sdg_labels"
                          :key="tag"
                          class="tag sdg"
                          >{{ tag }}</span
                        >
                      </div>
                    </div>
                  </div>

                  <a
                    :href="e.link"
                    target="_blank"
                    class="more"
                    rel="noopener noreferrer"
                    >查看詳情</a
                  >
                </div>
              </div>
            </article>
          </div>
        </div>

        <button class="nav next" aria-label="下一張" @click="slideNext">
          ›
        </button>
      </div>

      <div v-else-if="mode === 'list'" class="listWrap">
        <div class="list">
          <div v-for="e in events" :key="e.id" class="row">
            <div class="rDate">
              <div class="d1">{{ formatDateShort(e.created_at) }}</div>
              <div class="status-pill" :class="getStatusClass(e.status)">
                {{ e.status }}
              </div>
            </div>

            <div class="rMain">
              <div class="rTitle">
                <a :href="e.link" target="_blank">{{ e.title }}</a>
              </div>
              <div class="rMeta">
                <div class="r-tags" v-if="e.target_audience.length">
                  <span class="r-label">對象:</span>
                  <span
                    class="tag target mini"
                    v-for="t in e.target_audience"
                    :key="t"
                    >{{ t }}</span
                  >
                </div>

                <div class="r-tags" v-if="e.sdg_labels.length">
                  <span class="r-divider">/</span>
                  <span class="r-label">SDGs:</span>
                  <span
                    class="tag sdg mini"
                    v-for="s in e.sdg_labels"
                    :key="s"
                    >{{ s }}</span
                  >
                </div>

                <span class="r-divider">/</span>
                <span class="meta-mini">瀏覽: {{ e.views }}</span>
                <span class="r-divider">/</span>
                <span class="meta-mini">報名: {{ e.joined }}</span>
              </div>
            </div>

            <div class="rAct">
              <a :href="e.link" target="_blank" class="more small">查看詳情</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, onMounted, watch } from "vue";
import { getActivities } from "../api/activity";

const mode = ref("card");
const events = ref([]);
const loading = ref(false);

// ----------------------------------------------------------------
// 輪播 Slider 核心變數
// ----------------------------------------------------------------
const currentIndex = ref(0);
const isResetting = ref(false); // 控制是否關閉 transition 以進行瞬間重置
const itemsPerView = ref(4); // 預設桌面版顯示 4 個

// 響應式偵測 (簡單版：視窗大小改變時更新 itemsPerView)
function updateItemsPerView() {
  const w = window.innerWidth;
  if (w <= 640) itemsPerView.value = 1;
  else if (w <= 1100) itemsPerView.value = 2;
  else itemsPerView.value = 4;
}

// ----------------------------------------------------------------
// 資料載入與處理
// ----------------------------------------------------------------
onMounted(async () => {
  updateItemsPerView();
  window.addEventListener("resize", updateItemsPerView);

  loading.value = true;
  try {
    const data = await getActivities();
    events.value = data;
  } catch (error) {
    console.error("Failed to fetch activities", error);
  } finally {
    loading.value = false;
  }
});

// ----------------------------------------------------------------
// 無限輪播邏輯
// ----------------------------------------------------------------

// 顯示用的列表：原始列表 + 複製開頭的 N 個項目 (為了無縫滑動到尾端)
const displayEvents = computed(() => {
  if (events.value.length === 0) return [];
  // 複製的數量只要足夠填滿一個畫面即可
  const clones = events.value.slice(0, itemsPerView.value);
  return [...events.value, ...clones];
});

// 計算 CSS translateX 的百分比
// 例如：目前 index=1, 每個 item 佔 25% (100/4), 則移動 -25%
const sliderTranslateX = computed(() => {
  const percentPerItem = 100 / itemsPerView.value;
  return currentIndex.value * percentPerItem;
});

// 下一張 (一次滑一個)
function slideNext() {
  if (isResetting.value) return; // 防止快速點擊造成的閃爍

  // 正常滑動
  currentIndex.value++;
}

// 上一張
function slidePrev() {
  if (isResetting.value) return;

  if (currentIndex.value === 0) {
    // 特殊情況：如果在起點按上一張
    // 1. 先瞬間跳到最後一個「真實」項目的對應複製位置 (模擬循環)
    //    其實是跳到資料尾端的邏輯位置： events.length
    isResetting.value = true;
    currentIndex.value = events.value.length;

    // 2. 下一幀再滑動到 events.length - 1
    // 使用 setTimeout 讓 Vue 渲染完「瞬間跳轉」後再執行滑動動畫
    setTimeout(() => {
      isResetting.value = false;
      currentIndex.value--;
    }, 20);
  } else {
    currentIndex.value--;
  }
}

// 監聽 Transition End：處理「滑到複製區」後的瞬間歸零
function handleTransitionEnd() {
  // 如果滑到了「複製區」的第一個 (也就是總長度的 index = events.length)
  // 代表使用者剛看完最後一個真實項目，滑到了「假的第一個」
  if (currentIndex.value >= events.value.length) {
    // 瞬間 (無動畫) 跳回真正的 index 0
    isResetting.value = true;
    currentIndex.value = currentIndex.value % events.value.length;

    // 強制重繪後恢復動畫開關 (通常 Vue 的 reactivity 夠快，不需要 extra timeout，但保險起見)
    setTimeout(() => {
      isResetting.value = false;
    }, 20);
  }
}

// ----------------------------------------------------------------
// 工具函式
// ----------------------------------------------------------------

function getImageUrl(path) {
  if (!path) return "https://placehold.co/400x200?text=No+Image";
  if (path.startsWith("http")) return path;
  return `/${path}`;
}

function handleImageError(e) {
  e.target.src = "https://placehold.co/400x200?text=Activity";
}

function getStatusClass(status) {
  if (!status) return "";
  if (status.includes("報名中")) return "st-active";
  if (
    status.includes("截止") ||
    status.includes("結束") ||
    status.includes("額滿")
  )
    return "st-ended";
  if (status.includes("未開放")) return "st-future";
  return "";
}

function formatDateShort(dateStr) {
  if (!dateStr) return "";
  const d = new Date(dateStr);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
</script>

<style scoped>
/* ================= 全局容器 ================= */
#weekly-events {
  scroll-margin-top: 90px;
}
.eventWrap {
  margin-top: 18px;
}
.eventCard {
  background: #fff;
  border-radius: 26px;
  box-shadow: 0 10px 28px rgba(16, 24, 40, 0.1);
  border: 1px solid rgba(16, 24, 40, 0.08);
  padding: 34px 34px 28px;
}

/* ================= 標題區 ================= */
.head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 26px;
}
.title {
  display: flex;
  align-items: center;
  gap: 14px;
}
.bar {
  width: 10px;
  height: 32px;
  background: #f2cf57;
  border-radius: 2px;
}
.t {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: 0.2px;
}

.modes {
  display: flex;
  align-items: center;
  gap: 10px;
}
.mode {
  height: 42px;
  padding: 0 18px;
  border-radius: 6px;
  border: 1px solid rgba(16, 24, 40, 0.18);
  background: #fff;
  color: #6b7280;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
}
.mode.on {
  background: #0f3a63;
  color: #fff;
  border-color: rgba(15, 58, 99, 0.35);
}

.body {
  position: relative;
  padding: 0 58px;
}
.loading-state {
  text-align: center;
  padding: 40px;
  color: #6b7280;
  font-weight: 600;
}

/* ================= 輪播 (Slider) 核心樣式 ================= */
.slider-body {
  overflow: hidden; /* 隱藏超出的部分 */
}

.slider-viewport {
  overflow: hidden;
  width: 100%;
  /* 為了讓陰影不被裁切，上下留點空間 (視需要調整) */
  padding: 10px 0 20px 0;
  margin: -10px 0 -20px 0;
}

/* 軌道：Flex 排列，透過 JS 控制 transform */
.track {
  display: flex;
  width: 100%;
  will-change: transform; /* 效能優化 */
}

/* 卡片外層容器：負責寬度與間距 */
.card-wrapper {
  /* 預設桌面版：顯示 4 個 => 25% */
  flex: 0 0 25%;
  max-width: 25%;
  /* 使用 padding 來製造卡片間的 gap，這樣算 % 比較準 */
  padding: 0 11px;
  box-sizing: border-box;
}

/* 導航按鈕 */
.nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;

  /* 去掉白圈與陰影 */
  background: transparent;
  box-shadow: none;
  border: 0;
  background: #fff;
  box-shadow: 0 10px 24px rgba(16, 24, 40, 0.14);
  cursor: pointer;
  font-size: 34px;
  color: #0f172a;
  display: grid;
  place-items: center;
  z-index: 2;
  transition: filter 0.2s;
}
.nav:hover {
  filter: brightness(0.95);
}
.prev {
  left: -6px;
}
.next {
  right: -6px;
}

/* ================= 卡片本體樣式 ================= */
.card {
  background: #fff;
  border-radius: 18px;
  border: 1px solid rgba(16, 24, 40, 0.1);
  box-shadow: 0 8px 18px rgba(16, 24, 40, 0.06);
  overflow: hidden;
  height: 100%; /* 撐滿 wrapper */
  min-height: 420px;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(16, 24, 40, 0.12);
}

.thumb-img {
  height: 180px;
  background: #eef1f4;
  position: relative;
  overflow: hidden;
}
.thumb-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  color: #fff;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  z-index: 1;
}

.content {
  padding: 16px 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.meta-row {
  display: flex;
  align-items: center;
  font-size: 0.8rem;
  color: #6b7280;
  background: #f8fafc;
  padding: 6px 10px;
  border-radius: 6px;
  margin-bottom: 4px;
}
.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}
.meta-item .label {
  font-weight: 500;
}
.meta-item .val {
  font-weight: 700;
  color: #0f3a63;
}
.meta-divider {
  margin: 0 8px;
  color: #cbd5e1;
}

.date {
  font-size: 0.9rem;
  color: #3b82f6;
  font-weight: 700;
}

.name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
  line-height: 1.4;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 3.2em;
}

.tags-section {
  margin-bottom: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.tag-group {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  font-size: 0.8rem;
}
.tag-label-text {
  color: #9ca3af;
  font-weight: 600;
  white-space: nowrap;
  margin-top: 2px;
}
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.tag {
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
}
.tag.target {
  background: #f3f4f6;
  color: #4b5563;
}
.tag.sdg {
  background: #e0f2fe;
  color: #0284c7;
}

.more {
  align-self: flex-start;
  margin-top: 14px;
  width: 100%;
  height: 40px;
  border-radius: 8px;
  border: 0;
  background: #f2cf57;
  color: #111827;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  display: grid;
  place-items: center;
  text-decoration: none;
  transition: filter 0.2s;
}
.more:hover {
  filter: brightness(0.95);
}
.more.small {
  width: 120px;
  height: 36px;
  border-radius: 999px;
}

/* ================= 列表模式 (List Mode) ================= */
.listWrap {
  padding: 0 6px;
}
.list {
  border: 1px solid rgba(16, 24, 40, 0.1);
  border-radius: 16px;
  overflow: hidden;
}
.row {
  display: grid;
  grid-template-columns: 140px 1fr 140px;
  gap: 16px;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(16, 24, 40, 0.1);
  background: #fff;
}
.row:last-child {
  border-bottom: 0;
}

.rDate .d1 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #0f3a63;
  margin-bottom: 8px;
}
.status-pill {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 99px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #fff;
  text-align: center;
  min-width: 80px;
  background: #64748b;
}

.st-active {
  background-color: #10b981 !important;
}
.st-ended {
  background-color: #94a3b8 !important;
}
.st-future {
  background-color: #f59e0b !important;
}

.rTitle a {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
  text-decoration: none;
  transition: color 0.2s;
}
.rTitle a:hover {
  color: #3b82f6;
}

.rMeta {
  margin-top: 8px;
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  font-size: 0.85rem;
  color: #6b7280;
}
.r-tags {
  display: flex;
  align-items: center;
  gap: 6px;
}
.r-label {
  font-weight: 600;
  color: #9ca3af;
}
.tag.mini {
  font-size: 0.75rem;
  padding: 1px 6px;
}
.r-divider {
  color: #e2e8f0;
}
.meta-mini {
  font-weight: 500;
}

.rAct {
  display: flex;
  justify-content: flex-end;
}

/* ================= RWD ================= */
@media (max-width: 1100px) {
  /* 平板模式：2欄 */
  .card-wrapper {
    flex: 0 0 50%;
    max-width: 50%;
  }

  /* 列表 RWD */
  .row {
    grid-template-columns: 120px 1fr 120px;
  }
}

@media (max-width: 640px) {
  /* 手機模式：1欄 */
  .card-wrapper {
    flex: 0 0 100%;
    max-width: 100%;
  }

  .eventCard {
    padding: 22px 18px 18px;
    border-radius: 20px;
  }
  .head {
    flex-direction: column;
    align-items: flex-start;
  }
  .body {
    padding: 0;
  }
  .nav {
    display: none;
  } /* 手機版通常隱藏箭頭，改用手指滑動(這邊暫時隱藏) */

  .row {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  .rDate {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
  }
  .rAct {
    justify-content: flex-start;
    margin-top: 4px;
  }
}
</style>
