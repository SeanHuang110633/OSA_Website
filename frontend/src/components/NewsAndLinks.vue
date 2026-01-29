<template>
  <section class="row">
    <div class="card news">
      <div class="head">
        <div class="hTitle">
          <span class="hIcon">📰</span>
          <span>最新消息</span>
        </div>
      </div>

      <div class="list">
        <div v-for="(n, idx) in news" :key="idx" class="item">
          <div class="left">
            <span class="badge">
              <span class="dot" :class="n.dot"></span>
              <span>{{ n.tag }}</span>
            </span>
            <a class="text" href="#">{{ n.title }}</a>
          </div>
          <div class="date">{{ n.date }}</div>
        </div>
      </div>

      <div class="actions">
        <button class="pill-btn small">查看更多</button>
      </div>
    </div>

    <div class="card links">
      <div class="head">
        <div class="hTitle">
          <span class="hIcon">🔗</span>
          <span>各單位連結</span>
        </div>
      </div>

      <div class="linkList">
        <a v-for="(l,i) in units" :key="i" class="u" href="#">{{ l }}</a>
      </div>
    </div>
  </section>
</template>

<script setup>
const news = [
  { tag: "公告", dot: "blue", title: "113學年度第2學期校外獎學金公告", date: "2025.01.16" },
  { tag: "活動", dot: "green", title: "宿舍生活講座：自我照顧與人際溝通", date: "2025.01.14" },
  { tag: "公告", dot: "gray", title: "就學貸款及學雜費減免申請提醒", date: "2025.01.10" },
  { tag: "活動", dot: "orange", title: "職涯講座：履歷健檢與面試技巧", date: "2025.01.08" },
  { tag: "公告", dot: "blue", title: "寒假期間校園安全與緊急聯絡資訊", date: "2025.01.06" }
];

const units = [
  "諮商輔導中心",
  "課外活動組",
  "生活輔導組",
  "服務學習中心",
  "住宿服務組",
  "衛生保健組",
  "職涯發展中心",
  "原住民族學生資源中心"
];
</script>

<style scoped>
.row{
  display:grid;
  grid-template-columns: 1fr 320px;
  gap: 16px;
}
.news{ padding: 14px 14px 12px; }
.links{ padding: 14px; }

.head{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom: 10px;
}
.hTitle{
  display:flex;
  align-items:center;
  gap:10px;
  font-weight: 900;
}
.hIcon{ width: 26px; height: 26px; display:grid; place-items:center; }

.list{
  border: 1px solid rgba(16,24,40,.08);
  border-radius: 12px;
  overflow:hidden;
  background:#fff;
}
.item{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
}
.item:last-child{ border-bottom: 0; }
.left{
  display:flex;
  align-items:center;
  gap:10px;
  min-width: 0;
}
.text{
  font-size: 13px;
  color:#1b2430;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  max-width: 520px;
}
.text:hover{ text-decoration: underline; }
.date{
  font-size: 12px;
  color: var(--muted);
  flex: 0 0 auto;
}

.actions{
  display:flex;
  justify-content:flex-end;
  padding-top: 10px;
}
.small{ padding: 8px 14px; font-size: 13px; }

.linkList{
  margin-top: 8px;
  display:flex;
  flex-direction:column;
  gap:10px;
  padding: 10px 12px;
  border: 1px solid rgba(16,24,40,.08);
  border-radius: 12px;
}
.u{
  font-size: 13px;
  padding: 6px 8px;
  border-radius: 10px;
  color:#1b2430;
}
.u:hover{
  background: rgba(21,58,99,.06);
}

@media (max-width: 980px){
  .row{ grid-template-columns: 1fr; }
  .text{ max-width: 100%; }
}
.hTitle{
  font-size: 1.5rem;   
  font-weight: 700;     
  line-height: 1.2;
}
</style>