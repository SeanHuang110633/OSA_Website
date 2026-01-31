<template>
  <main class="container page">
    <div class="layout">
      <aside class="side">
        <div class="sideCard">
          <div class="sideTitle">
            <span class="bar" aria-hidden="true"></span>
            <span>各單位連結</span>
          </div>

          <nav class="sideNav">
            <button
              v-for="u in units"
              :key="u.key"
              class="sideBtn"
              :class="{ on: u.key === activeUnitKey }"
              type="button"
              @click="activeUnitKey = u.key"
            >
              <span class="txt">{{ u.name }}</span>
            </button>
          </nav>
        </div>
      </aside>

      <section class="content">
        <div class="crumb">
          <RouterLink class="crumbLink" to="/">首頁</RouterLink>
          <span class="sep">/</span>
          <span class="now">關於我們</span>
        </div>

        <h1 class="h1">
          <span class="barSm" aria-hidden="true"></span>
          關於學務處
        </h1>

        <p class="desc">（待補）請放學務處簡介文字。</p>

        <h2 class="h2">
          <span class="barSm" aria-hidden="true"></span>
          {{ activeUnit.name }}
          <span class="h2Count">（{{ activeUnit.count }} 人）</span>
        </h2>

        <div class="staffList">
            <div v-if="loading" class="state">載入中…</div>
            <div v-else-if="errorMsg" class="state state--error">{{ errorMsg }}</div>
            <div v-else-if="activePeople.length === 0" class="state">目前沒有資料。</div>

            <article v-else v-for="p in activePeople" :key="p.id" class="staffCard">
                <div class="avatarWrap">
                <img class="avatar" :src="getAvatarUrl(p)" :alt="p.name || '成員頭像'" />
                </div>

                <div class="info">
                <div class="nameLine">{{ p.name }}</div>

                <div class="kv">
                    <div class="row">
                    <div class="label">職稱：</div>
                    <div class="val">{{ p.title }}</div>
                    </div>
                    <div class="row">
                    <div class="label">公務信箱：</div>
                    <div class="val link">
                        <a v-if="p.email" :href="`mailto:${p.email}`">{{ p.email }}</a>
                        <span v-else>—</span>
                    </div>
                    </div>
                    <div class="row">
                    <div class="label">分機電話：</div>
                    <div class="val">{{ p.ext || "—" }}</div>
                    </div>
                </div>

                <div class="duty">{{ p.duty }}</div>
                <div class="extra">{{ p.extra }}</div>
                </div>
            </article>
            </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
import avatarPlaceholder from "../assets/avatar_placeholder.png";
import { fetchMembers } from "../api/member"; 

const unitDefs = [
  { key: "osa", name: "學務處" },
  { key: "life", name: "生活輔導組" },
  { key: "coun", name: "諮商輔導中心" },
  { key: "club", name: "課外活動組" },
  { key: "sl", name: "服務學習發展中心" },
  { key: "dorm", name: "住宿服務組" },
  { key: "health", name: "衛生保健組" },
  { key: "career", name: "職涯發展中心" },
  { key: "indig", name: "原住民族學生資源中心" },
];

const activeUnitKey = ref("osa");
const loading = ref(false);
const errorMsg = ref("");
const members = ref([]);

async function loadMembers() {
  loading.value = true;
  errorMsg.value = "";
  try {
    const res = await fetchMembers({ locale: "zh-TW", page: 1, size: 200 });
    const data = res?.data;
    const items = data?.items ?? data?.data?.items ?? data?.data ?? data ?? [];
    members.value = Array.isArray(items) ? items : [];
  } catch (e) {
    console.error(e);
    errorMsg.value = "成員資料載入失敗，請稍後再試。";
    members.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(loadMembers);

const membersByUnit = computed(() => {
  const map = {};
  for (const m of members.value) {
    const key = m.unit_key ?? m.unitKey ?? "osa"; 
    (map[key] ||= []).push(m);
  }
  return map;
});

const units = computed(() =>
  unitDefs.map((u) => ({
    ...u,
    count: (membersByUnit.value[u.key] || []).length,
  }))
);

const activeUnit = computed(
  () => units.value.find((u) => u.key === activeUnitKey.value) || units.value[0]
);

const activePeople = computed(() => membersByUnit.value[activeUnitKey.value] || []);

function getAvatarUrl(p) {
  return p.avatar_url || p.avatarUrl || avatarPlaceholder;
}
</script>

<style scoped>
.page {
  padding: 1.7rem 0 3.6rem;
}

.layout {
  display: grid;
  grid-template-columns: 22.5rem 1fr; 
  gap: 1.6rem;
  align-items: start;
}

.sideCard {
  background: #fff;
  border-radius: 1.35rem;
  box-shadow: 0 0.7rem 1.6rem rgba(16, 24, 40, 0.1);
  border: 1px solid rgba(16, 24, 40, 0.1);
  padding: 1.25rem 1.1rem 1.1rem;
}

.sideTitle {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  /* 修正：側欄標題統一為 20px */
  font-size: var(--text-xl); 
  font-weight: 700;
  color: #111827;
  margin-bottom: 1rem;
}

.bar {
  width: 0.5rem;
  height: 1.4rem;
  background: #f2cf57;
  border-radius: 0.2rem;
}

.sideNav {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.sideBtn {
  display: flex;
  align-items: center;
  width: 100%;
  border: 0;
  background: transparent;
  padding: 0.7rem 1rem;
  border-radius: 999px;
  cursor: pointer;
  /* 修正：側欄選單標準化 16px */
  font-size: var(--text-base); 
  font-weight: 400;
  color: #111827;
  text-align: left;
}

.sideBtn:hover {
  background: rgba(15, 23, 42, 0.04);
}

.sideBtn.on {
  background: #fff6dc;
  box-shadow: inset 0 0 0 1px rgba(242, 207, 87, 0.55);
}

.sideBtn .txt {
  letter-spacing: 0.02em;
  line-height: var(--leading-tight);
}

.content {
  background: #fff;
  border-radius: 1.35rem;
  box-shadow: 0 0.7rem 1.6rem rgba(16, 24, 40, 0.1);
  border: 1px solid rgba(16, 24, 40, 0.1);
  padding: 1.35rem 1.5rem 1.6rem;
}

.crumb {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  /* 修正：Meta 資訊標準 14px */
  font-size: var(--text-sm); 
  color: #6b7280;
  margin-bottom: 0.6rem;
}
.crumbLink {
  color: inherit;
  text-decoration: none;
}
.crumbLink:hover {
  text-decoration: underline;
}
.sep {
  opacity: 0.8;
}
.now {
  color: #6b7280;
}

.h1 {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  /* 修正：H1 頁面標題 30px */
  font-size: var(--text-3xl); 
  font-weight: 700;
  color: #111827;
  margin: 0.75rem 0 0.75rem;
  line-height: var(--leading-tight);
}

.h2 {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  /* 修正：H2 區塊標題 24px */
  font-size: var(--text-2xl); 
  font-weight: 700;
  color: #111827;
  margin: 1.3rem 0 0.9rem;
  line-height: var(--leading-tight);
}

.h2Count {
  /* 修正：輔助資訊標準 14px */
  font-size: var(--text-sm);
  color: #64748b;
  font-weight: 400;
}

.barSm {
  width: 0.6rem;
  height: 1.35rem;
  background: #f2cf57;
  border-radius: 0.2rem;
}

.desc {
  /* 修正：內文標準 16px 與行高 1.6 */
  font-size: var(--text-base); 
  line-height: var(--leading-normal);
  color: #334155;
}

.staffList {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.staffCard {
  display: grid;
  grid-template-columns: 16.25rem 1fr; 
  gap: 1.35rem;
  background: #f4f6ff;
  border: 1px solid rgba(16, 24, 40, 0.1);
  border-radius: 1.1rem;
  padding: 1.1rem;
}

.avatarWrap {
  background: #eef2ff;
  border-radius: 1rem;
  border: 1px solid rgba(16, 24, 40, 0.1);
  display: grid;
  place-items: center;
  padding: 0.75rem;
}

.avatar {
  width: 12.5rem;  
  height: 12.5rem;
  object-fit: cover;
  border-radius: 1rem;
  background: #fff;
}

.info {
  padding-top: 0.35rem;
}

.nameLine {
  /* 修正：卡片標題使用 20px */
  font-size: var(--text-xl); 
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.75rem;
  line-height: var(--leading-tight);
}

.kv {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  margin-bottom: 0.9rem;
}

.row {
  display: grid;
  grid-template-columns: 6.2rem 1fr;
  gap: 0.65rem;
  align-items: start;
}

.label {
  /* 修正：欄位標籤 16px */
  font-size: var(--text-base);
  color: #0f172a;
}

.val {
  /* 修正：欄位內容 16px 與行高 1.6 */
  font-size: var(--text-base);
  color: #111827;
  line-height: var(--leading-normal);
}

.val.link {
  color: #1d4ed8;
}

.duty {
  /* 修正：內文標準化 16px */
  font-size: var(--text-base); 
  color: #111827;
  margin-top: 0.65rem;
  line-height: var(--leading-normal);
}

.extra {
  /* 修正：內文標準化 16px */
  font-size: var(--text-base); 
  margin-top: 0.5rem;
  color: #334155;
  line-height: var(--leading-normal);
}

/* RWD */
@media (max-width: 1100px) {
  .layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  .staffCard {
    grid-template-columns: 1fr;
  }
  .avatar {
    width: 10rem;
    height: 10rem;
  }
  .h1 { font-size: var(--text-2xl); } /* 手機版降級為 24px */
}

.state {
  padding: 16px;
  border-radius: 12px;
  background: rgba(0,0,0,.04);
  /* 修正：狀態提示 16px */
  font-size: var(--text-base);
  color: #334155;
}
.state--error {
  background: rgba(255,0,0,.06);
  color: #991b1b;
}
</style>