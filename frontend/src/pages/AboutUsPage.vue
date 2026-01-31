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
          <article v-for="p in activePeople" :key="p.id" class="staffCard">
            <div class="avatarWrap">
              <img class="avatar" :src="avatarPlaceholder" alt="匿名頭像" />
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
                  <div class="val link">{{ p.email }}</div>
                </div>
                <div class="row">
                  <div class="label">分機電話：</div>
                  <div class="val">{{ p.ext }}</div>
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
import { computed, ref } from "vue";
import { RouterLink } from "vue-router";
import avatarPlaceholder from "../assets/avatar_placeholder.png";

const units = [
  { key: "osa", name: "學務處", count: 7 },
  { key: "life", name: "生活輔導組", count: 15 },
  { key: "coun", name: "諮商輔導中心", count: 18 },
  { key: "club", name: "課外活動組", count: 7 },
  { key: "sl", name: "服務學習發展中心", count: 4 },
  { key: "dorm", name: "住宿服務組", count: 22 },
  { key: "health", name: "衛生保健組", count: 9 },
  { key: "career", name: "職涯發展中心", count: 7 },
  { key: "indig", name: "原住民族學生資源中心", count: 1 },
];

const activeUnitKey = ref("osa");

const activeUnit = computed(
  () => units.find((u) => u.key === activeUnitKey.value) || units[0]
);

function makePeople(unitKey, unitName, count) {
  return Array.from({ length: count }, (_, i) => {
    const idx = String(i + 1).padStart(2, "0");
    return {
      id: `${unitKey}-${idx}`,
      name: `${unitName} 第${idx}人`,
      title: "職稱待補",
      email: "xxx@ncu.edu.tw",
      ext: "分機待補",
      duty: "（待補）協助本處/本組相關業務（可多行）。",
      extra: "（待補）可放第二段介紹或職務重點。",
    };
  });
}

const peopleByUnit = {
  osa: makePeople("osa", "學務處", 7),
  life: makePeople("life", "生活輔導組", 15),
  coun: makePeople("coun", "諮商輔導中心", 18),
  club: makePeople("club", "課外活動組", 7),
  sl: makePeople("sl", "服務學習發展中心", 4),
  dorm: makePeople("dorm", "住宿服務組", 22),
  health: makePeople("health", "衛生保健組", 9),
  career: makePeople("career", "職涯發展中心", 7),
  indig: makePeople("indig", "原住民族學生資源中心", 1),
};

const activePeople = computed(() => peopleByUnit[activeUnitKey.value] || []);
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
</style>