<template>
  <main class="container">
    <HeroBanner class="section" />
    <NewsAndLinks class="section" />
    <EventsRow class="section" />
  </main>

  <QuickLinksGrid class="section" />
  
  <main class="container">
    <MapSection class="section" />
  </main>
</template>

<script setup>
import HeroBanner from "../components/HeroBanner.vue";
import NewsAndLinks from "../components/NewsAndLinks.vue";
import EventsRow from "../components/EventsRow.vue";
import QuickLinksGrid from "../components/QuickLinksGrid.vue";
import MapSection from "../components/MapSection.vue";
</script>

<style scoped>
/* 頁面容器與區塊間距調整 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section {
  margin-bottom: 3.5rem; /* 增加區塊間的呼吸感 */
}

/* 雖然 Home.vue 主要是結構組件，但我們確保基礎文字屬性符合規範：
  1. 預設內文不低於 16px (var(--text-base))
  2. 確保繁體中文具備 1.6 倍行高
*/
:deep(body), :deep(.container) {
  font-size: var(--text-base); /* 標準內文 16px */
  line-height: var(--leading-normal); /* 內文行高 1.6 */
  -webkit-font-smoothing: antialiased; /* 優化繁體中文筆畫渲染 */
}

/* 確保所有透過 Home 載入的組件標題層級權重一致 */
:deep(h2) {
  font-size: var(--text-2xl); /* 區塊大標題 24px */
  line-height: var(--leading-tight); /* 標題行高 1.3 */
}
</style>