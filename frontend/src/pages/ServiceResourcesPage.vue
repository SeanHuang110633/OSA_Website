<template>
  <main class="container page">
    <div class="crumb">
      <RouterLink class="crumbLink" to="/">首頁</RouterLink>
      <span class="sep">/</span>
      <span class="now">服務資源</span>
    </div>

    <section class="grid">
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
          <li v-for="(x,i) in c.items" :key="i">
            <a href="#">{{ x }}</a>
          </li>
        </ul>
      </article>
    </section>
  </main>
</template>

<script setup>
import { RouterLink } from "vue-router";

const cards = [
  {
    id: 1, frame: "f1", icon: "🎓", title: "生活輔導",
    items: ["學生工讀","研究生獎助學金","獎助學金暨工讀管理系統","就學貸款","學雜費減免","急難救助","學生請假","學生兵役","國軍班隊招募專區","役期抵免","失物招領"]
  },
  {
    id: 2, frame: "f2", icon: "🏠", title: "學生住宿",
    items: ["學生宿舍介紹","學生宿舍設備","學生宿舍申請","獎勵團體學生宿舍","學生宿舍退費","學生宿舍修繕通報","學生宿舍管委會","宿舍導師","學生宿舍電子佈告欄申請","校外賃居資訊"]
  },
  {
    id: 3, frame: "f3", icon: "🩺", title: "衛生保健",
    items: ["健康檢查報告","醫療器材借用","學生團體保險","醫療諮詢","衛教諮詢","特約醫院"]
  },
  {
    id: 4, frame: "f4", icon: "💬", title: "諮商輔導",
    items: ["預約心理諮商","心理測驗","導師知能","小松鼠志工隊","輔導股長","資源教室"]
  },
  {
    id: 5, frame: "f5", icon: "🎉", title: "課外活動",
    items: ["學生社團場地借用"]
  },
  {
    id: 6, frame: "f6", icon: "💼", title: "職涯輔導",
    items: ["職涯發展中心FB粉絲專頁","職涯中心活動報名系統","職涯活動預約系統","傑出領導獎學金申請","中央大學校園徵才資訊網","UCAN職涯測評"]
  },
  {
    id: 7, frame: "f7", icon: "🧩", title: "服務學習",
    items: ["服務學習教育認證時數","服務學習表單下載","服務學習最新消息","服務學習活動"]
  },
  {
    id: 8, frame: "f8", icon: "🔗", title: "其他",
    items: ["學務處聯絡資訊","職涯諮詢預約","宿舍導師諮詢預約","學生輔導資訊網","性別平等教育委員會","學生意見反映","學生申訴"]
  },
];
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