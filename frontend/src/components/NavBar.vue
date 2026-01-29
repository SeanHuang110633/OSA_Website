<template>
  <header class="header">
    <!-- 中間：Logo + 標題 + 搜尋 -->
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

    <!-- 下方：導覽列 -->
    <div class="navStrip">
      <div class="container navInner">
        <nav class="menu" aria-label="主選單">
          <RouterLink class="item" to="/about">關於本處</RouterLink>
          <span class="vline"></span>

          <!-- ✅ 各單位連結：點擊開關（不閃退） -->
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

            <div v-show="open" class="ddMenu" role="menu" aria-label="各單位連結">
              <a class="ddItem" :href="links.life" target="_blank" rel="noreferrer">生活輔導組</a>
              <a class="ddItem" :href="links.consult" target="_blank" rel="noreferrer">諮商輔導中心</a>
              <a class="ddItem" :href="links.activity" target="_blank" rel="noreferrer">課外活動組</a>
              <a class="ddItem" :href="links.service" target="_blank" rel="noreferrer">服務學習發展中心</a>
              <a class="ddItem" :href="links.dorm" target="_blank" rel="noreferrer">住宿服務組</a>
              <a class="ddItem" :href="links.health" target="_blank" rel="noreferrer">衛生保健組</a>
              <a class="ddItem" :href="links.career" target="_blank" rel="noreferrer">職涯發展中心</a>
              <a class="ddItem" :href="links.indigenous" target="_blank" rel="noreferrer">原住民族學生資源中心</a>
            </div>
          </div>

          <span class="vline"></span>
          <RouterLink class="item" to="/news">最新消息</RouterLink>
          <span class="vline"></span>
          <RouterLink class="item" to="/resources">服務資源</RouterLink>
          <span class="vline"></span>
          <a class="item" href="#">募款專區</a>
          <span class="vline"></span>
          <RouterLink class="item" to="/downloads">下載專區</RouterLink>
          <span class="vline"></span>
          <RouterLink class="item" :to="{ path: '/', hash: '#weekly-events' }">本週活動</RouterLink>
          <span class="vline"></span>
          <RouterLink class="item" :to="{ path: '/', hash: '#quick-links' }">快速連結</RouterLink>
          <span class="vline"></span>
          <RouterLink class="item" :to="{ path: '/', hash: '#location-map' }">位置資訊</RouterLink>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import school from "../assets/school.png";

/* 下拉開關 */
const open = ref(false);
const ddRef = ref(null);

function toggle() {
  open.value = !open.value;
}
function close() {
  open.value = false;
}

/* ✅ 點外面關閉 + ESC 關閉（避免閃退、也不會一直黏住） */
function onDocPointerDown(e) {
  if (!open.value) return;
  const el = ddRef.value;
  if (!el) return;
  if (!el.contains(e.target)) close();
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

/* 各處室連結（先保底；你之後換成每個單位的正式網址） */
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
.header{ background:#fff; }

/* 中間那塊淺藍背景 */
.mid{
  background: #eaf4ff;
  border-bottom: 1px solid rgba(21,58,99,.22);
}
.midInner{
  height: 92px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 16px;
}

/* Logo / 標題 */
.brand{ display:flex; align-items:center; gap: 14px; }
.logo{ height: 44px; width: auto; }
.brandText .zh{
  font-weight: 900;
  font-size: 22px;
  letter-spacing: .5px;
  line-height: 1.1;
}
.brandText .en{
  margin-top: 4px;
  font-size: 16px;
  color:#1f2f3d;
  letter-spacing: .3px;
}

/* 搜尋 */
.search{ display:flex; align-items:center; gap:10px; }
.input{
  width: 320px;
  height: 44px;
  border-radius: 999px;
  border: 1px solid rgba(16,24,40,.18);
  padding: 0 18px;
  background:#fff;
  font-size: 16px;
}
.btn{
  width: 44px;
  height: 44px;
  border-radius: 999px;
  border: 1px solid rgba(16,24,40,.18);
  background:#fff;
  cursor:pointer;
  font-size: 18px;
}

/* 導覽列 */
.navStrip{
  background: #eaf4ff;
  border-bottom: 1px solid rgba(21,58,99,.18);
}
.navInner{
  height: 56px;
  display:flex;
  align-items:center;
  justify-content:center;
}
.menu{
  display:flex;
  align-items:center;
  justify-content:center;
  gap: 18px;
  flex-wrap: nowrap;
}
.item{
  font-weight: 900;
  font-size: 18px;
  color:#111827;
  white-space: nowrap;
  text-decoration: none;
}
.item:hover{ text-decoration: underline; }

.vline{
  width: 1px;
  height: 26px;
  background: rgba(16,24,40,.20);
}

/* ===== 下拉：容器 ===== */
.dd{ position: relative; display:flex; align-items:center; }

/* ✅ 移除醜框框：button 跟一般 nav item 一致 */
.item.has{
  background: transparent !important;
  border: 0 !important;
  border-radius: 0 !important;
  padding: 0;
  box-shadow: none !important;
  cursor: pointer;
}
.item.has:hover{
  background: transparent;
  text-decoration: underline;
}

/* caret */
.caret{
  font-size: 12px;
  margin-left: 6px;
  position: relative;
  top: -1px;
  transition: transform .18s ease;
}
.caret.up{ transform: rotate(180deg); }

/* ===== 下拉選單（小一點寬度 + 水藍色） ===== */
.ddMenu{
  position: absolute;
  top: 44px;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  background: #f0f7ff;
  border-radius: 10px;
  border: 1px solid rgba(15,58,99,.22);
  box-shadow: 0 12px 22px rgba(15,58,99,.18);
  padding: 6px 0;
  z-index: 50;
}

.ddItem{
  display: block;
  text-align: center;
  padding: 10px 12px;
  font-size: 16px;
  font-weight: 700;
  color: #0f3a63;
  text-decoration: none;
  line-height: 1.4;
}
.ddItem + .ddItem{
  border-top: 1px solid rgba(15,58,99,.18);
}
.ddItem:hover{
  background: rgba(15,58,99,.08);
}

/* RWD */
@media (max-width: 980px){
  .input{ width: 220px; }
  .brandText .zh{ font-size: 18px; }
  .brandText .en{ font-size: 13px; }
  .item{ font-size: 15px; }
  .menu{ gap: 12px; overflow-x:auto; }
}
</style>