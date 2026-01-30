<template>
  <section id="quick-links" class="wrap">
    <img class="squirrel" :src="squirrel" alt="" aria-hidden="true" />

    <div class="container inner">
      <div class="title">快速連結</div>

      <div class="grid">
        <section class="card c1">
          <div class="head">
            <span class="ico">🎓</span>
            <h3>就學資源與學生福利</h3>
          </div>
          <ul>
            <li><a href="#">安心就學支持計畫</a></li>
            <li><a href="#">就學補助系統</a></li>
            <li><a href="#">獎助學金暨工讀系統</a></li>
            <li><a href="#">學生兼任助理勞動權益保障專區</a></li>
            <li><a href="#">外宿資訊網</a></li>
            <li><a href="#">失物招領資訊網</a></li>
          </ul>
        </section>

        <section class="card c2">
          <div class="head">
            <span class="ico">💬</span>
            <h3>輔導諮詢與學生關懷</h3>
          </div>
          <ul>
            <li><a href="#">導師輔導資源系統</a></li>
            <li><a href="#">職涯諮詢預約系統</a></li>
            <li><a href="#">臺聯大諮輔系統</a></li>
            <li><a href="#">性別平等教育委員會</a></li>
            <li><a href="#">防制學生藥物濫用資源網</a></li>
          </ul>
        </section>

        <section class="card c3">
          <div class="head">
            <span class="tag">NEW</span>
            <h3>新生與校園活動</h3>
          </div>
          <ul>
            <li><a href="#">新生知訊網</a></li>
            <li><a href="#">大一週會</a></li>
            <li><a href="#">學生意見反映</a></li>
            <li><a href="#">小中大電視台</a></li>
          </ul>
        </section>

        <section class="card c4">
          <div class="head">
            <span class="ico">🔗</span>
            <h3>其他</h3>
          </div>
          <ul>
            <li><a href="#">校外實習網</a></li>
            <li><a href="#">兵役查詢</a></li>
            <li><a href="#">智慧財產權</a></li>
            <li><a href="#">隱私權政策聲明</a></li>
          </ul>
        </section>
      </div>
    </div>
  </section>
</template>

<script setup>
import squirrel from "../assets/OHD_squirrel.png";
</script>

<style scoped>


.wrap{
  position: relative;
  background: #d7d7d7;
  padding: 3.5rem 0 3.5rem;
  margin-top: 1.25rem;
}

.squirrel{
  position:absolute;
  left: 3.75rem;
  top: -3rem;
  width: 6rem;
  height:auto;
}

.title{
  text-align:center;
  font-weight: 700;         
  font-size: 1.55rem;        
  letter-spacing: .12em;
  color:#0f3a63;
  margin-bottom: 1.6rem;
}

.grid{
  display:grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.4rem;
  align-items: stretch;
}

.card{
  background:#fff;
  border-radius: 1.35rem;
  padding: 1.25rem 1.25rem 1.05rem;
  box-shadow:
    0 .75rem 1.35rem rgba(16,24,40,.16),
    0 .125rem 0 rgba(255,255,255,.55) inset;
  border: .25rem solid transparent;
  min-height: 26rem;
}

.c1{ border-color:#0f3a63; }
.c2{ border-color:#6b1e1e; }
.c3{ border-color:#5c6b12; }
.c4{ border-color:#1a6b4b; }

.head{
  display:flex;
  align-items:center;
  gap: .75rem;
  margin-bottom: 1.1rem;
}

.head h3{
  margin:0;
  font-size: 1.5rem;
  font-weight: 700;
  color:#111827;
  line-height: 1.25;
}

.ico{
  width: 1.9rem;
  height: 1.9rem;
  border-radius: .65rem;
  background: #f2f4f7;
  display:grid;
  place-items:center;
  font-size: .95rem;
  border: 1px solid rgba(16,24,40,.10);
}

.tag{
  font-size: .78rem;
  font-weight: 700;
  color:#0f3a63;
  background:#e8f1ff;
  border: 1px solid rgba(15,58,99,.22);
  padding: .35rem .55rem;
  border-radius: .55rem;
}

ul{
  list-style: none;
  padding: 0;
  margin: 0;
  display:flex;
  flex-direction:column;
  gap: .85rem;
}

a{
  color:#111827;
  font-size: .95rem;
  font-weight: 500;
  line-height: 1.55;
}
a:hover{ text-decoration: underline; }

/* RWD */
@media (max-width: 1100px){
  .grid{ grid-template-columns: repeat(2, 1fr); }
  .squirrel{ left: 1.4rem; width: 5.2rem; top: -2.6rem; }
}
@media (max-width: 640px){
  .grid{ grid-template-columns: 1fr; }
  .wrap{ padding: 3.5rem 0 3.5rem; }
  .title{ font-size: 1.4rem; }
}
</style>