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
import { fetchMembers } from "../api/member"; // ✅ 新增：member API

// ✅ 這裡的 key 要跟後端回傳的 unit_key / unitKey 對得上
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

// ✅ API 狀態
const loading = ref(false);
const errorMsg = ref("");
const members = ref([]);

// ✅ 取得資料
async function loadMembers() {
  loading.value = true;
  errorMsg.value = "";
  try {
    const res = await fetchMembers({ locale: "zh-TW", page: 1, size: 200 });
    const data = res?.data;

    // 兼容：array / {items} / {data:{items}}
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

// ✅ 將 members 依 unitKey 分組（這裡假設後端給 unit_key 或 unitKey）
const membersByUnit = computed(() => {
  const map = {};
  for (const m of members.value) {
    const key = m.unit_key ?? m.unitKey ?? "osa"; // 沒有就先丟 osa（避免爆）
    (map[key] ||= []).push(m);
  }
  return map;
});

// ✅ units 用「def + count」組合，count 用資料算
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

// ✅ 頭像：如果後端有 avatar_url 就用，沒有就用 placeholder
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
  font-size: 1.5rem; 
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

  font-size: 1rem; 
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
  line-height: 1.4;
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
  font-size: 0.86rem; 
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

.h1,
.h2 {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 1.5rem; 
  font-weight: 700;
  color: #111827;
}

.h1 {
  margin: 0.75rem 0 0.75rem;
}

.h2 {
  margin: 1.3rem 0 0.9rem;
}

.h2Count {
  font-size: 0.95rem;
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
  font-size: 1rem; 
  color: #334155;
  line-height: 1.8;
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
  font-size: 1.5rem; 
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.75rem;
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
  font-size: 1rem;
  color: #0f172a;
}

.val {
  font-size: 1rem;
  color: #111827;
  line-height: 1.7;
}

.val.link {
  color: #1d4ed8;
}

.duty {
  font-size: 1rem; 
  color: #111827;
  margin-top: 0.65rem;
  line-height: 1.8;
}

.extra {
  font-size: 1rem; 
  margin-top: 0.5rem;
  color: #334155;
  line-height: 1.8;
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
}
.state {
  padding: 16px;
  border-radius: 12px;
  background: rgba(0,0,0,.04);
  color: #334155;
}
.state--error {
  background: rgba(255,0,0,.06);
  color: #991b1b;
}
</style>