<template>
  <aside>
    <div class="sticky top-24">
      <div class="zen-card p-6 bg-white/60 backdrop-blur-md">
        <h4
          class="serif-font text-lg text-stone-700 mb-6 border-b border-stone-100 pb-2"
        >
          快速連結
        </h4>

        <div class="space-y-1 max-h-[600px] overflow-y-auto no-scrollbar pr-2">
          <a v-for="link in links" :key="link" href="#" class="sidebar-link">
            {{ link }}
          </a>
        </div>
      </div>

      <div class="mt-6 text-right">
        <p class="text-[10px] tracking-widest text-stone-400 uppercase">
          VISITORS
        </p>
        <p class="serif-font text-xl text-stone-600">18,444</p>
      </div>
    </div>
  </aside>
</template>

<script setup>
const links = [
  "安心就學支持計畫",
  "新生知訊網",
  "學生意見反映",
  "大一週會",
  "性別平等教育委員會",
  "職涯諮詢預約系統",
  "校外實習網",
  "導師輔導資源系統",
  "就學補助系統",
  "獎助學金暨工讀系統",
  "學生兼任助理勞動權益保障專區",
  "兵役查詢",
  "失物招領資訊網",
  "小中大電視台",
  "防制學生藥物濫用資源網",
  "外宿資訊網",
  "臺聯大諮輔系統",
  "智慧財產權",
  "隱私權政策聲明",
];
</script>
