<template>
  <main class="container page">
    <div class="crumb">
      <RouterLink class="crumbLink" to="/">首頁</RouterLink>
      <span class="sep">/</span>
      <RouterLink class="crumbLink" to="/service-resources">服務資源</RouterLink>
      <span class="sep">/</span>
      <span class="now">{{ title || "資源內容" }}</span>
    </div>

    <p v-if="loading">載入中...</p>
    <p v-else-if="error" style="color:#b91c1c;">{{ error }}</p>

    <section v-else>
      <h1 style="font-size:1.6rem;font-weight:700;margin:.6rem 0 1rem;">
        {{ title }}
      </h1>

      <!-- 先原樣顯示 content（markdown 不轉換） -->
      <div class="contentBox">
        {{ content }}
      </div>
    </section>
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute, RouterLink } from "vue-router";
import { getResourceDetail } from "../api/serviceResources.js";

const route = useRoute();

const loading = ref(false);
const error = ref("");
const title = ref("");
const content = ref("");

function pickLocaleValue(val, locale) {
  if (val == null) return "";
  if (typeof val === "string") return val;
  return val[locale] ?? val["zh-TW"] ?? val["en-US"] ?? "";
}

async function fetchDetail() {
  loading.value = true;
  error.value = "";
  try {
    const locale = "zh-TW";
    const id = route.params.id;

    const res = await getResourceDetail(id, locale);
    const raw = res.data ?? res;

    title.value = pickLocaleValue(raw.title, locale) || "(未命名)";
    content.value = pickLocaleValue(raw.content, locale) || "(無內容)";
  } catch (e) {
    error.value = e?.message ?? "載入失敗";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchDetail);
</script>

<style scoped>
.page{
  padding: 1.2rem 0 3.2rem;
}
.crumb{
  display:flex;
  align-items:center;
  gap:.5rem;
  margin:.6rem 0 1.2rem;
  font-size:.86rem;
  color:#6b7280;
}
.crumbLink{ color:#6b7280; }
.crumbLink:hover{ text-decoration: underline; }
.sep{ opacity:.7; }
.now{ color:#111827; }

.contentBox{
  white-space: pre-wrap; /* 保留換行 */
  line-height: 1.9;
  color:#111827;
  background:#fff;
  border: 1px solid rgba(16,24,40,.10);
  border-radius: 1rem;
  padding: 1.1rem 1.2rem;
}
</style>
