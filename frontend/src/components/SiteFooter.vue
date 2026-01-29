<template>
  <footer class="footer">
    <div class="container inner">
      <div class="cols">
        <div class="col">
          <div class="h">聯絡資訊</div>

          <div class="row">
            <span class="ico" aria-hidden="true">📍</span>
            <div class="txt">(320317)桃園市中壢區中大路300號</div>
          </div>

          <div class="row">
            <span class="ico" aria-hidden="true">📞</span>
            <div class="txt">(03) 422-7151 分機57200</div>
          </div>

          <div class="row">
            <span class="ico" aria-hidden="true">✉️</span>
            <a class="txt link" href="mailto:ncu7200@ncu.edu.tw">ncu7200@ncu.edu.tw</a>
          </div>

          <div class="row">
            <span class="ico" aria-hidden="true">🕘</span>
            <div class="txt">週一～五 8:00-17:00</div>
          </div>
        </div>

        <div class="col">
          <div class="h">重要連結</div>
          <a class="item" href="#">學校首頁</a>
          <a class="item" href="#">學籍系統</a>
          <a class="item" href="#">獎助學金系統</a>
          <a class="item" href="#">性平專區</a>
        </div>

        <div class="col">
        <div class="h">關注我們</div>

        <a
            class="social"
            href="https://www.facebook.com/ncu.tw/?locale=zh_TW"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Facebook"
        >
            <span class="sIco" aria-hidden="true">📘</span>
            <span>Facebook</span>
        </a>

        <a
            class="social"
            href="https://line.me/R/ti/p/@ncu"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LINE"
        >
            <span class="sIco" aria-hidden="true">💬</span>
            <span>LINE</span>
        </a>
        </div>
      </div>

      <div class="vline" aria-hidden="true"></div>

      <div class="right">
        <div class="badge">
          <img class="badgeImg" src="https://via.placeholder.com/130x46?text=AA" alt="無障礙標章" />
          <div class="badgeTxt">本網站已通過無障礙網站 AA 級標章檢測</div>
        </div>

        <div class="badgeTxt">
          國立中央大學 學務處 版權所有 Copyright©2026
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer{
  margin-top: 26px;
  background: #0f3a63; 
  color: rgba(255,255,255,.88);
  padding: 28px 0 30px;
}

.inner{
  display:grid;
  grid-template-columns: 1fr 1px 420px; 
  gap: 26px;
  align-items: start;
}

.cols{
  display:grid;
  grid-template-columns: 1.25fr 1fr 1fr;
  gap: 26px;
}

.h{
  font-weight: 800;
  color:#f2cf57;
  font-size: 20px;
  margin: 6px 0 16px;
  letter-spacing: .02em;
}

.row{
  display:flex;
  align-items:flex-start;
  gap: 12px;
  margin: 14px 0;
}
.ico{
  width: 22px;
  flex: 0 0 22px;
  opacity: .95;
  line-height: 1;
  margin-top: 2px;
}
.txt{
  font-size: 16px;
  line-height: 1.7;
  color: rgba(255,255,255,.9);
}

.item{
  display:block;
  font-size: 16px;
  line-height: 1.9;
  color: rgba(255,255,255,.9);
  text-decoration: none;
  margin: 10px 0;
}
.item:hover{ text-decoration: underline; }

.social{
  display:flex;
  align-items:center;
  gap: 10px;
  font-size: 16px;
  color: rgba(255,255,255,.9);
  text-decoration: none;
  margin: 14px 0;
}
.social:hover{ text-decoration: underline; }
.sIco{
  width: 22px;
  height: 22px;
  display:grid;
  place-items:center;
  border-radius: 6px;
  background: rgba(255,255,255,.10);
  border: 1px solid rgba(255,255,255,.14);
  font-size: 14px;
}

.vline{
  width: 1px;
  background: rgba(255,255,255,.55);
  height: 100%;
  opacity: .85;
}

.right{
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  min-height: 190px;
  padding-top: 10px;
}

.badge{
  display:flex;
  flex-direction:column;
  gap: 12px;
  align-items:flex-start;
}
.badgeImg{
  width: 140px;
  height: auto;
  display:block;
  border-radius: 6px;
}
.badgeTxt{
  font-size: 16px;
  line-height: 1.7;
  color: rgba(255,255,255,.9);
}

.copyright{
  margin-top: 22px;
  font-size: 16px;
  line-height: 1.7;
  color: rgba(255,255,255,.92);
  text-align: center;
}

.link{ color: rgba(255,255,255,.92); text-decoration:none; }
.link:hover{ text-decoration: underline; }

/* RWD */
@media (max-width: 1100px){
  .inner{
    grid-template-columns: 1fr; 
    gap: 18px;
  }
  .vline{ display:none; }
  .cols{
    grid-template-columns: 1fr 1fr;
  }
  .right{
    min-height: auto;
    padding-top: 0;
  }
}

@media (max-width: 640px){
  .cols{ grid-template-columns: 1fr; }
  .h{ font-size: 18px; }
  .txt, .item, .social, .badgeTxt, .copyright{ font-size: 14px; }
}
</style>