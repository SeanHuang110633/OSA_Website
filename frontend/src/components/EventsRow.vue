<template>
  <section id="weekly-events" class="eventWrap">
    <div class="eventCard">
      <div class="head">
        <div class="title">
          <span class="bar" aria-hidden="true"></span>
          <span class="t">本週活動</span>
        </div>

        <div class="modes" role="tablist" aria-label="顯示模式">
          <button class="mode" :class="{ on: mode==='card' }" type="button" @click="mode='card'">卡片模式</button>
          <button class="mode" :class="{ on: mode==='list' }" type="button" @click="mode='list'">列表模式</button>
          <button class="mode" :class="{ on: mode==='week' }" type="button" @click="mode='week'">週曆模式</button>
        </div>
      </div>

      <div v-if="mode==='card'" class="body">
        <button class="nav prev" aria-label="上一頁" @click="prev">‹</button>

        <div class="track">
          <article v-for="e in visibleCards" :key="e.id" class="card">
            <div class="thumb">
              <div class="ico" aria-hidden="true">{{ e.icon }}</div>
            </div>

            <div class="content">
              <div class="date">{{ e.date }}</div>
              <div class="name">{{ e.title }}</div>
              <div class="desc">{{ e.desc }}</div>
              <button class="more" type="button">了解更多</button>
            </div>
          </article>
        </div>

        <button class="nav next" aria-label="下一頁" @click="next">›</button>
      </div>

      <div v-else-if="mode==='list'" class="listWrap">
        <div class="list">
          <div v-for="e in events" :key="e.id" class="row">
            <div class="rDate">
              <div class="d1">{{ e.date }}</div>
              <div class="d2">{{ e.time || '—' }}</div>
            </div>

            <div class="rMain">
              <div class="rTitle">{{ e.title }}</div>
              <div class="rDesc">{{ e.desc }}</div>
            </div>

            <div class="rAct">
              <button class="more small" type="button">了解更多</button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="weekWrap">
        <div class="weekHead">
          <button class="wkBtn" type="button" @click="shiftWeek(-7)">‹</button>
          <div class="wkTitle">{{ weekTitle }}</div>
          <button class="wkBtn" type="button" @click="shiftWeek(7)">›</button>
        </div>

        <div class="weekGrid">
          <div v-for="d in weekDays" :key="d.key" class="day">
            <div class="dayTop">
              <div class="dow">{{ d.dow }}</div>
              <div class="dnum">{{ d.mmdd }}</div>
            </div>

            <div class="dayBody">
              <div v-if="d.items.length===0" class="empty">—</div>

              <button v-for="it in d.items" :key="it.id" class="chip" type="button">
                <span class="chipTime">{{ it.time || '' }}</span>
                <span class="chipTitle">{{ it.title }}</span>
              </button>
            </div>
          </div>
        </div>

        <div class="weekHint">點選活動可再導到詳細頁（之後接路由/後端）</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from "vue";

const mode = ref("card");

const events = ref([
  { id: 1, icon: "🖼️", date: "2024-06-01 (Sat)", time: "", title: "校慶運動會報名開始", desc: "一年一度的校慶運動會即將展開，歡迎各系所組隊參加！" },
  { id: 2, icon: "🎤", date: "2024-06-05 (Wed)", time: "18:00", title: "校園歌唱大賽決賽", desc: "最強好聲音就在中央！決賽之夜。" },
  { id: 3, icon: "🌱", date: "2024-06-10 (Mon)", time: "", title: "永續校園植樹活動", desc: "為地球盡一份心力，一起種下希望的樹苗。" },
  { id: 4, icon: "📝", date: "2024-06-15 (Sat)", time: "", title: "期末舒壓講座", desc: "考試壓力大？來放鬆一下。" }
]);

const page = ref(0);
const pageSize = 4;

const visibleCards = computed(() => {
  const start = page.value * pageSize;
  return events.value.slice(start, start + pageSize);
});

function next(){
  const maxPage = Math.max(0, Math.ceil(events.value.length / pageSize) - 1);
  page.value = Math.min(maxPage, page.value + 1);
}
function prev(){
  page.value = Math.max(0, page.value - 1);
}

const weekOffsetDays = ref(0);

function parseYMD(str){
  const m = str.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if(!m) return null;
  const y = Number(m[1]), mo = Number(m[2]) - 1, d = Number(m[3]);
  return new Date(y, mo, d);
}

const baseWeekStart = computed(() => {
  const now = new Date();
  const day = (now.getDay() + 6) % 7; // Mon=0..Sun=6
  const monday = new Date(now);
  monday.setDate(now.getDate() - day + weekOffsetDays.value);
  monday.setHours(0,0,0,0);
  return monday;
});

function shiftWeek(delta){
  weekOffsetDays.value += delta;
}

const weekTitle = computed(() => {
  const s = baseWeekStart.value;
  const e = new Date(s);
  e.setDate(s.getDate() + 6);
  const fmt = (dt) => `${dt.getFullYear()}-${String(dt.getMonth()+1).padStart(2,'0')}-${String(dt.getDate()).padStart(2,'0')}`;
  return `${fmt(s)} ~ ${fmt(e)}`;
});

const weekDays = computed(() => {
  const dows = ["一","二","三","四","五","六","日"];
  const start = baseWeekStart.value;

  const map = new Map();
  for(const ev of events.value){
    const dt = parseYMD(ev.date);
    if(!dt) continue;
    const key = `${dt.getFullYear()}-${String(dt.getMonth()+1).padStart(2,'0')}-${String(dt.getDate()).padStart(2,'0')}`;
    if(!map.has(key)) map.set(key, []);
    map.get(key).push(ev);
  }

  const out = [];
  for(let i=0;i<7;i++){
    const dt = new Date(start);
    dt.setDate(start.getDate() + i);
    const key = `${dt.getFullYear()}-${String(dt.getMonth()+1).padStart(2,'0')}-${String(dt.getDate()).padStart(2,'0')}`;
    out.push({
      key,
      dow: `週${dows[i]}`,
      mmdd: `${String(dt.getMonth()+1).padStart(2,'0')}/${String(dt.getDate()).padStart(2,'0')}`,
      items: map.get(key) || []
    });
  }
  return out;
});
</script>

<style scoped>
#weekly-events{
  scroll-margin-top: 90px;
}

.eventWrap{ margin-top: 18px; }
.eventCard{
  background:#fff;
  border-radius: 26px;
  box-shadow: 0 10px 28px rgba(16,24,40,.10);
  border: 1px solid rgba(16,24,40,.08);
  padding: 34px 34px 28px;
}

.head{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap: 16px;
  margin-bottom: 26px;
}
.title{ display:flex; align-items:center; gap: 14px; }
.bar{ width: 10px; height: 32px; background:#f2cf57; border-radius:2px; }

.t{
  font-size: 1.5rem;
  font-weight: 700;
  color:#0f172a;
  letter-spacing:.2px;
}

.modes{ display:flex; align-items:center; gap: 10px; }
.mode{
  height: 42px;
  padding: 0 18px;
  border-radius: 6px;
  border: 1px solid rgba(16,24,40,.18);
  background:#fff;
  color:#6b7280;
  font-weight: 700;
  font-size: 0.95rem;
  cursor:pointer;
}
.mode.on{
  background:#0f3a63;
  color:#fff;
  border-color: rgba(15,58,99,.35);
}

.body{ position: relative; padding: 0 58px; }
.nav{
  position:absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 56px;
  height: 56px;
  border-radius: 999px;
  border: 0;
  background:#fff;
  box-shadow: 0 10px 24px rgba(16,24,40,.14);
  cursor:pointer;
  font-size: 34px;
  color:#0f172a;
  display:grid;
  place-items:center;
}
.prev{ left: -6px; }
.next{ right: -6px; }

.track{
  display:grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 22px;
  align-items: stretch;
}
.card{
  background:#fff;
  border-radius: 18px;
  border: 1px solid rgba(16,24,40,.10);
  box-shadow: 0 8px 18px rgba(16,24,40,.06);
  overflow:hidden;
  min-height: 360px;
  display:flex;
  flex-direction:column;
}
.thumb{ height: 180px; background:#eef1f4; display:grid; place-items:center; }
.ico{ font-size: 30px; opacity:.85; }

.content{ padding: 16px 16px 18px; display:flex; flex-direction:column; gap: 10px; }

.date{
  font-size: 0.95rem;
  font-weight: 700;
  color:#3b82f6;
}
.name{
  font-size: 1.12rem;
  font-weight: 700;
  color:#111827;
  line-height: 1.35;
}
.desc{
  color:#6b7280;
  font-size: 0.95rem;
  line-height: 1.65;
  flex: 1;
}

.more{
  align-self:flex-start;
  margin-top: 4px;
  width: 140px;
  height: 42px;
  border-radius: 999px;
  border: 0;
  background:#f2cf57;
  color:#111827;
  font-weight: 700;
  font-size: 1rem;
  cursor:pointer;
}
.more:hover{ filter: brightness(.97); }
.more.small{ width: 128px; height: 40px; font-size: 0.95rem; }

.listWrap{ padding: 0 6px; }
.list{
  border: 1px solid rgba(16,24,40,.10);
  border-radius: 16px;
  overflow:hidden;
}
.row{
  display:grid;
  grid-template-columns: 220px 1fr 160px;
  gap: 16px;
  align-items:center;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(16,24,40,.10);
  background:#fff;
}
.row:last-child{ border-bottom:0; }

.rDate .d1{ font-size: 0.9rem; font-weight: 700; color:#0f3a63; }
.rDate .d2{ margin-top: 6px; font-size: 0.85rem; color:#6b7280; font-weight: 600; }

.rTitle{ font-size: 1.05rem; font-weight: 700; color:#111827; }
.rDesc{ margin-top: 6px; font-size: 0.95rem; color:#6b7280; line-height: 1.65; }

.rAct{ display:flex; justify-content:flex-end; }

.weekWrap{ padding: 0 6px; }
.weekHead{
  display:flex;
  align-items:center;
  justify-content:center;
  gap: 14px;
  margin: 6px 0 14px;
}
.wkBtn{
  width: 42px; height: 42px;
  border-radius: 999px;
  border: 1px solid rgba(16,24,40,.16);
  background:#fff;
  cursor:pointer;
  font-size: 22px;
}
.wkTitle{
  font-weight: 700;
  font-size: 1.05rem;
  color:#0f172a;
}

.weekGrid{
  display:grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
}
.day{
  border: 1px solid rgba(16,24,40,.10);
  border-radius: 14px;
  overflow:hidden;
  background:#fff;
  min-height: 200px;
}
.dayTop{
  padding: 10px 10px 8px;
  background:#f3f6fb;
  border-bottom: 1px solid rgba(16,24,40,.08);
}
.dow{ font-weight: 700; color:#0f3a63; font-size: 0.8rem; }
.dnum{ margin-top: 4px; color:#111827; font-weight: 700; font-size: 0.95rem; }

.dayBody{
  padding: 10px;
  display:flex;
  flex-direction:column;
  gap: 8px;
}
.empty{ color:#98a2b3; font-weight: 700; }

.chip{
  text-align:left;
  border: 0;
  background: #eef6ff;
  color:#0f3a63;
  border-radius: 10px;
  padding: 10px 10px;
  cursor:pointer;
  display:flex;
  flex-direction:column;
  gap: 4px;
}
.chip:hover{ filter: brightness(.98); }
.chipTime{ font-size: 0.75rem; font-weight: 700; opacity: .85; }
.chipTitle{ font-size: 0.85rem; font-weight: 700; }

.weekHint{
  margin-top: 12px;
  color:#98a2b3;
  font-weight: 600;
  font-size: 0.8rem;
}

/* RWD */
@media (max-width: 1100px){
  .track{ grid-template-columns: repeat(2, 1fr); }
  .row{ grid-template-columns: 200px 1fr 140px; }
  .weekGrid{ grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 640px){
  .eventCard{ padding: 22px 18px 18px; border-radius: 20px; }
  .head{ flex-direction:column; align-items:flex-start; }
  .body{ padding: 0; }
  .nav{ display:none; }
  .track{ grid-template-columns: 1fr; }
  .row{ grid-template-columns: 1fr; }
  .rAct{ justify-content:flex-start; }
  .weekGrid{ grid-template-columns: 1fr; }
}
</style>