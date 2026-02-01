<template>
  <main class="container page">
    <div class="crumb">
      <RouterLink class="crumbLink" to="/">首頁</RouterLink>
      <span class="sep">/</span>
      <span class="now">服務資源</span>
    </div>

    <p v-if="loading">載入中...</p>
    <p v-else-if="error" style="color:#b91c1c;">{{ error }}</p>

    <section v-else class="grid">
      <article
        v-for="c in cards"
        :key="c.id"
        class="card"
        :class="c.frame"
      >
        <div class="head">
          <span class="ico">{{ c.icon }}</span>
          <h2 class="cardTitle">{{ c.title }}</h2>
        </div>

        <ul class="links">
          <li v-for="item in c.items" :key="item.id">
            <!-- link: 開外部新分頁 -->
            <a
              v-if="item.kind === 'link'"
              :href="item.href"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ item.text }}
            </a>

            <!-- article: 走站內 detail page（仍然是「新分頁」需求可用 target=_blank + router-link 的 href） -->
            <RouterLink
              v-else
              :to="item.to"
              class="articleLink"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ item.text }}
            </RouterLink>
          </li>
        </ul>
      </article>
    </section>
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import { getResources } from "../api/serviceResources.js"; // ✅ 依你實際路徑調整

// 你原本 8 張卡的「骨架」：用 category_id 對應
const cards = ref([
  { id: 1, frame: "f1", icon: "🎓", title: "生活輔導", items: [] },
  { id: 2, frame: "f2", icon: "🏠", title: "學生住宿", items: [] },
  { id: 3, frame: "f3", icon: "🩺", title: "衛生保健", items: [] },
  { id: 4, frame: "f4", icon: "💬", title: "諮商輔導", items: [] },
  { id: 5, frame: "f5", icon: "🎉", title: "課外活動", items: [] },
  { id: 6, frame: "f6", icon: "💼", title: "職涯輔導", items: [] },
  { id: 7, frame: "f7", icon: "🧩", title: "服務學習", items: [] },
  { id: 8, frame: "f8", icon: "🔗", title: "其他", items: [] },
]);

const loading = ref(false);
const error = ref("");

/** 如果後端回的是 JSON 多語系，這裡做 fallback */
function pickLocaleValue(val, locale) {
  if (val == null) return "";
  if (typeof val === "string") return val;
  // val 可能是 { "zh-TW": "...", "en-US": "..." }
  return val[locale] ?? val["zh-TW"] ?? val["en-US"] ?? "";
}

/** 同理：url 也可能是多語系 JSON */
function pickUrl(val, locale) {
  const u = pickLocaleValue(val, locale);
  return u || "";
}

async function fetchResources() {
  loading.value = true;
  error.value = "";
  try {
    const locale = "zh-TW"; // ✅ 之後你可以改成從 Pinia/設定拿
    const res = await getResources({ locale });

    // 依你的 request 實作，這裡可能是 res.data 或 res
    const raw = res.data ?? res;

    // 可能後端回 { items: [...] } 或直接 [...]
    const list = raw.items ?? raw.data ?? raw.results ?? raw ?? [];

    // 先清空
    for (const c of cards.value) c.items = [];

    // 分組塞回 cards
    for (const r of list) {
      const categoryId = r.category_id;
      const card = cards.value.find((c) => c.id === categoryId);
      if (!card) continue;

      const text = pickLocaleValue(r.title, locale) || "(未命名)";
      const href = pickUrl(r.url, locale);
      const content = pickLocaleValue(r.content, locale);

      // 規則：有 url → link；沒有 url 但有 content/type=article → detail
      if (href) {
        card.items.push({
          id: r.id,
          kind: "link",
          text,
          href,
          sort: r.sort_order ?? 0,
        });
      } else {
        card.items.push({
          id: r.id,
          kind: "article",
          text,
          to: `/resources/${r.id}`,
          sort: r.sort_order ?? 0,
        });
      }
    }

    // 每張卡內依 sort_order 排序（你 DB 有 sort_order）
    for (const c of cards.value) {
      c.items.sort((a, b) => (a.sort ?? 0) - (b.sort ?? 0));
    }
  } catch (e) {
    error.value = e?.message ?? "載入失敗，請稍後再試";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchResources);
</script>

<style scoped>
/* 你原本的 CSS 全部保留不動，只多補 RouterLink 顏色一致 */
.articleLink{
  font-size: 1rem;
  font-weight: 500;
  color:#111827;
  text-decoration: none;
}
.articleLink:hover{ text-decoration: underline; }

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

.grid{
  display:grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.2rem;
}


.card{
  background:#fff;
  border-radius: 1.35rem;
  border: 1px solid rgba(16,24,40,.10);
  box-shadow: 0 .6rem 1.4rem rgba(16,24,40,.10);
  padding: 1.2rem 1.2rem 1rem;
  min-height: 22rem;
  position: relative;
  overflow:hidden;
}


.head{
  display:flex;
  align-items:center;
  gap:.6rem;
  margin-bottom:.8rem;
}
.ico{
  width:1.9rem;
  height:1.9rem;
  border-radius:.6rem;
  background:#f2f4f7;
  border: 1px solid rgba(16,24,40,.10);
  display:grid;
  place-items:center;
  font-size:1rem;
}
.cardTitle{
  margin:0;
  font-size:1.5rem;
  font-weight:700;
  color:#111827;
}

.links{
  margin:0;
  padding-left:1.1rem;
  display:flex;
  flex-direction:column;
  gap:.6rem;
}
.links a{
  font-size:1rem;
  font-weight:500;
  color:#111827;
}
.links a:hover{ text-decoration: underline; }

.card::before{
  content:"";
  position:absolute;
  inset:.4rem;
  border-radius: 1.15rem;
  border: 3px solid transparent;
  pointer-events:none;
}
.f1::before{ border-color:#0f3a63; }
.f2::before{ border-color:#1f6b2a; }
.f3::before{ border-color:#6b671f; }
.f4::before{ border-color:#6b1e1e; }
.f5::before{ border-color:#4b1f6b; }
.f6::before{ border-color:#6b2a2a; }
.f7::before{ border-color:#0f3a63; }
.f8::before{ border-color:#1a6b4b; }

/* RWD */
@media (max-width: 1100px){
  .grid{ grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px){
  .grid{ grid-template-columns: 1fr; }
  .card{ min-height: auto; }
}
</style>