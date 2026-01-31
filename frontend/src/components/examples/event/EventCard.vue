<template>
  <div
    class="zen-card p-5 flex flex-col md:flex-row items-start md:items-center gap-4 group cursor-pointer border-l-4 border-transparent"
    :class="styleMap.hoverBorder"
    @click="$emit('click', event.id)"
  >
    <div class="flex flex-col items-center min-w-15">
      <span class="text-[10px] text-stone-400">{{ monthAbbr }}</span>
      <span
        class="text-xl serif-font text-stone-600 font-bold transition"
        :class="styleMap.hoverText"
      >
        {{ day }}
      </span>
    </div>

    <div class="grow">
      <div class="flex items-center gap-2 mb-1">
        <span
          class="text-[10px] px-2 py-0.5 rounded-full"
          :class="styleMap.class"
        >
          {{ categoryName }}
        </span>

        <span class="text-[10px] text-stone-300">
          {{ event.organizer_info?.name || "學務處" }}
        </span>

        <span
          v-if="event.is_featured"
          class="text-[10px] text-red-400 border border-red-200 px-1 rounded"
        >
          置頂
        </span>
      </div>

      <h3
        class="text-stone-700 font-medium transition duration-300"
        :class="styleMap.hoverText"
      >
        {{ event.title }}
      </h3>
    </div>

    <i
      class="fas fa-arrow-right text-stone-200 transition transform group-hover:translate-x-1"
      :class="styleMap.hoverText"
    ></i>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  event: {
    type: Object,
    required: true,
  },
});

// 定義事件 (點擊卡片時通知父組件)
defineEmits(["click"]);

// 樣式對應表
const STYLE_CONFIG = {
  speech: { class: "bg-orange-50 text-[#D4A373]", hover: "#D4A373" },
  activity: { class: "bg-red-50 text-red-400", hover: "#7D9D9C" },
  official: { class: "bg-stone-100 text-stone-500", hover: "#7D9D9C" },
  default: { class: "bg-gray-50 text-gray-500", hover: "#7D9D9C" },
};

// 計算屬性
const categorySlug = computed(() => props.event.category?.slug || "default");
const categoryName = computed(() => props.event.category?.name || "未分類");

const styleMap = computed(() => {
  const config = STYLE_CONFIG[categorySlug.value] || STYLE_CONFIG["default"];
  const isSpeech = categorySlug.value === "speech";

  return {
    class: config.class,
    hoverBorder: isSpeech ? "hover:border-[#D4A373]" : "hover:border-[#7D9D9C]",
    hoverText: isSpeech
      ? "group-hover:text-[#D4A373]"
      : "group-hover:text-[#7D9D9C]",
  };
});

const monthAbbr = computed(() => {
  if (!props.event.published_at) return "";
  return new Date(props.event.published_at)
    .toLocaleString("en-US", { month: "short" })
    .toUpperCase();
});

const day = computed(() => {
  if (!props.event.published_at) return "";
  return new Date(props.event.published_at).getDate();
});
</script>
