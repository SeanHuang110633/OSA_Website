<template>
  <header class="header">
    <div class="mid">
      <div class="container midInner">
        <div class="brand">
          <img class="logo" :src="school" alt="國立中央大學" />
          <div class="brandText">
            <div class="zh">學生事務處</div>
            <div class="en">NCU Office of Students Affairs</div>
          </div>
        </div>

        <div class="search">
          <input class="input" placeholder="全站搜尋" />
          <button class="btn" aria-label="搜尋">🔍</button>
        </div>
      </div>
    </div>

    <div class="navStrip">
      <div class="container navInner">
        <nav class="menu" aria-label="主選單">
          <RouterLink class="item" to="/about">關於本處</RouterLink>
          <span class="vline"></span>

          <div class="dd" ref="ddRef">
            <button
              class="item has"
              type="button"
              :aria-expanded="open ? 'true' : 'false'"
              aria-haspopup="true"
              @click="toggle"
            >
              各單位連結 <span class="caret" :class="{ up: open }">▼</span>
            </button>

            <div
              v-show="open"
              class="ddMenu"
              role="menu"
              aria-label="各單位連結"
            >
              <a
                class="ddItem"
                :href="links.life"
                target="_blank"
                rel="noreferrer"
                >生活輔導組</a
              >
              <a
                class="ddItem"
                :href="links.consult"
                target="_blank"
                rel="noreferrer"
                >諮商輔導中心</a
              >
              <a
                class="ddItem"
                :href="links.activity"
                target="_blank"
                rel="noreferrer"
                >課外活動組</a
              >
              <a
                class="ddItem"
                :href="links.service"
                target="_blank"
                rel="noreferrer"
                >服務學習發展中心</a
              >
              <a
                class="ddItem"
                :href="links.dorm"
                target="_blank"
                rel="noreferrer"
                >住宿服務組</a
              >
              <a
                class="ddItem"
                :href="links.health"
                target="_blank"
                rel="noreferrer"
                >衛生保健組</a
              >
              <a
                class="ddItem"
                :href="links.career"
                target="_blank"
                rel="noreferrer"
                >職涯發展中心</a
              >
              <a
                class="ddItem"
                :href="links.indigenous"
                target="_blank"
                rel="noreferrer"
                >原住民族學生資源中心</a
              >
            </div>
          </div>

          <span class="vline"></span>
          <RouterLink class="item" to="/news">最新消息</RouterLink>
          <span class="vline"></span>
          <RouterLink class="item" to="/resources">服務資源</RouterLink>
          <span class="vline"></span>
          <RouterLink class="item" to="/donate">募款專區</RouterLink>
          <span class="vline"></span>
          <RouterLink class="item" to="/downloads">下載專區</RouterLink>
          <span class="vline"></span>
          <RouterLink class="item" :to="{ path: '/', hash: '#weekly-events' }"
            >本週活動</RouterLink
          >
          <span class="vline"></span>
          <RouterLink class="item" :to="{ path: '/', hash: '#quick-links' }"
            >快速連結</RouterLink
          >
          <span class="vline"></span>
          <RouterLink class="item" :to="{ path: '/', hash: '#location-map' }"
            >位置資訊</RouterLink
          >
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import school from "../assets/school.png";

const open = ref(false);
const ddRef = ref(null);

function toggle() { open.value = !open.value; }
function close() { open.value = false; }

function onDocPointerDown(e) {
  if (!open.value) return;
  const el = ddRef.value;
  if (!el || !el.contains(e.target)) close();
}
function onDocKeyDown(e) {
  if (e.key === "Escape") close();
}

onMounted(() => {
  document.addEventListener("pointerdown", onDocPointerDown);
  document.addEventListener("keydown", onDocKeyDown);
});
onBeforeUnmount(() => {
  document.removeEventListener("pointerdown", onDocPointerDown);
  document.removeEventListener("keydown", onDocKeyDown);
});

const links = {
  life: "https://www.ncu.edu.tw/tw/unit?id=student_affairs",
  consult: "https://www.ncu.edu.tw/tw/unit?id=student_affairs",
  activity: "https://www.ncu.edu.tw/tw/unit?id=student_affairs",
  service: "https://www.ncu.edu.tw/tw/unit?id=student_affairs",
  dorm: "https://www.ncu.edu.tw/tw/unit?id=student_affairs",
  health: "https://www.ncu.edu.tw/tw/unit?id=student_affairs",
  career: "https://www.ncu.edu.tw/tw/unit?id=student_affairs",
  indigenous: "https://www.ncu.edu.tw/tw/unit?id=student_affairs",
};
</script>

<style scoped>
.header {
  background: #fff;
}

.mid{
  background: #eaf4ff;
  border-bottom: 1px solid rgba(21, 58, 99, 0.22);
}
.midInner {
  height: 92px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.brand{ display:flex; align-items:center; gap: 14px; }
.logo{ height: 44px; width: auto; }
.brandText .zh{
  font-weight: 900;
  /* 修正：單位名稱標題統一為 24px */
  font-size: var(--text-2xl);
  letter-spacing: .5px;
  line-height: var(--leading-tight);
}
.brandText .en {
  margin-top: 4px;
  /* 修正：副標題標準化為 16px */
  font-size: var(--text-base);
  color:#1f2f3d;
  letter-spacing: .3px;
}

.search{ display:flex; align-items:center; gap:10px; }
.input{
  width: 320px;
  height: 44px;
  border-radius: 999px;
  border: 1px solid rgba(16, 24, 40, 0.18);
  padding: 0 18px;
  background:#fff;
  /* 修正：輸入框文字標準化 16px */
  font-size: var(--text-base);
}
.btn {
  width: 44px;
  height: 44px;
  border-radius: 999px;
  border: 1px solid rgba(16,24,40,.18);
  background:#fff;
  cursor:pointer;
  /* 修正：圖示按鈕文字標準化 18px */
  font-size: var(--text-lg);
}

.navStrip{
  background: #eaf4ff;
  border-bottom: 1px solid rgba(21, 58, 99, 0.18);
}
.navInner {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.menu {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
  flex-wrap: nowrap;
}
.item {
  font-weight: 900;
  /* 修正：主要導覽列文字統一為 18px (lg) */
  font-size: var(--text-lg);
  color:#111827;
  white-space: nowrap;
  text-decoration: none;
}
.item:hover {
  text-decoration: underline;
}

.vline {
  width: 1px;
  height: 26px;
  background: rgba(16, 24, 40, 0.2);
}

.dd{ position: relative; display:flex; align-items:center; }
.item.has{
  background: transparent !important;
  border: 0 !important;
  border-radius: 0 !important;
  padding: 0;
  box-shadow: none !important;
  cursor: pointer;
}
.item.has:hover {
  background: transparent;
  text-decoration: underline;
}

.caret{
  /* 修正：小圖示使用極小字 12px */
  font-size: var(--text-xs);
  margin-left: 6px;
  position: relative;
  top: -1px;
  transition: transform 0.18s ease;
}
.caret.up {
  transform: rotate(180deg);
}

.ddMenu{
  position: absolute;
  top: 44px;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  background: #f0f7ff;
  border-radius: 10px;
  border: 1px solid rgba(15, 58, 99, 0.22);
  box-shadow: 0 12px 22px rgba(15, 58, 99, 0.18);
  padding: 6px 0;
  z-index: 50;
}

.ddItem {
  display: block;
  text-align: center;
  padding: 10px 12px;
  /* 修正：下拉選單項目標準化 16px */
  font-size: var(--text-base);
  font-weight: 700;
  color: #0f3a63;
  text-decoration: none;
  line-height: var(--leading-tight);
}
.ddItem + .ddItem {
  border-top: 1px solid rgba(15, 58, 99, 0.18);
}
.ddItem:hover {
  background: rgba(15, 58, 99, 0.08);
}

/* RWD */
@media (max-width: 980px){
  .input{ width: 220px; }
  /* 修正：手機版標題降級為 18px */
  .brandText .zh{ font-size: var(--text-lg); }
  /* 修正：手機版輔助文字 14px */
  .brandText .en{ font-size: var(--text-sm); }
  /* 修正：手機版選單維持 16px */
  .item{ font-size: var(--text-base); }
  .menu{ gap: 12px; overflow-x:auto; }
}
</style>
