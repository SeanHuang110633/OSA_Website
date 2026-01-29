<template>
  <div
    class="border-b border-stone-200 bg-white/80 backdrop-blur-sm sticky top-0 z-50"
  >
    <div
      class="container mx-auto px-6 h-10 flex justify-between items-center text-xs tracking-widest text-stone-500"
    >
      <span class="serif-font italic">Since 1915</span>
      <div class="flex space-x-6">
        <a href="#" class="hover:text-stone-800 transition">ENGLISH</a>
        <a
          href="https://www.ncu.edu.tw"
          target="_blank"
          class="hover:text-stone-800 transition"
          >中央大學首頁</a
        >
      </div>
    </div>
  </div>

  <header class="bg-white pt-10 pb-6 relative overflow-hidden">
    <div
      class="absolute -top-20 -left-20 w-64 h-64 bg-stone-50 rounded-full blur-3xl opacity-60"
    ></div>

    <div class="container mx-auto px-6 relative z-10">
      <div
        class="flex flex-col md:flex-row justify-between items-end md:items-center mb-10"
      >
        <div class="flex items-center space-x-4">
          <!-- <img
            src="https://www.ncu.edu.tw/assets/img/logo.png"
            alt="NCU Logo"
            class="w-16 h-16 opacity-90 grayscale-[30%]"
          /> -->
          <div>
            <h1 class="text-3xl text-stone-800 tracking-widest font-medium">
              學生事務處
            </h1>
            <p class="text-xs text-stone-500 tracking-[0.2em] uppercase mt-1">
              Office of Student Affairs
            </p>
          </div>
        </div>

        <div class="flex space-x-8 mt-6 md:mt-0">
          <a
            v-for="icon in icons"
            :key="icon.text"
            href="#"
            class="group flex flex-col items-center gap-2"
          >
            <div
              class="w-10 h-10 rounded-full bg-stone-50 flex items-center justify-center text-stone-600 group-hover:bg-[#D4A373] group-hover:text-white transition duration-300"
            >
              <i :class="icon.class + ' text-sm'"></i>
            </div>
            <span
              class="text-[10px] tracking-wider text-stone-400 group-hover:text-[#D4A373] transition"
              >{{ icon.text }}</span
            >
          </a>
        </div>
      </div>

      <nav class="border-t border-stone-100 pt-4">
        <ul
          class="flex flex-wrap gap-x-8 gap-y-3 text-sm text-stone-600 font-light"
        >
          <li v-for="dept in departments" :key="dept">
            <a href="#" class="nav-item">{{ dept }}</a>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script setup>
const icons = [
  { text: "消息", class: "fas fa-bullhorn" },
  { text: "關於", class: "far fa-compass" },
  { text: "資源", class: "far fa-building" },
  { text: "下載", class: "fas fa-file-download" },
];

const departments = [
  "生活輔導組",
  "諮商輔導中心",
  "課外活動組",
  "服務學習發展中心",
  "住宿服務組",
  "衛生保健組",
  "職涯發展中心",
  "原住民族學生資源中心",
];
</script>
