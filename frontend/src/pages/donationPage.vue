<template>
  <main class="container page pl-10">
    <div class="crumb">
      <RouterLink class="crumb__home" to="/">首頁</RouterLink>
      <span class="crumb__sep">/</span>
      <b>募款專區</b>
    </div>

    <section class="donation-header">
      <h2 class="page-title">募款項目</h2>
      <p class="page-intro">
        學務處以「安心就學、校園傳承、全人照顧」為核心，推動三大募款計畫：安心就學支持計畫，協助經濟弱勢學生無後顧之憂完成學業；中正圖書館翻修計畫，保存校園記憶、再現知識殿堂風華；以及守護學子．逐夢共好方案，整合學生事務資源，提供學生全方位的學習與生活支持。誠摯邀請您一同投入，陪伴學子安心成長、逐夢未來。
      </p>
    </section>

    <div class="donation-list">
      <DonationCard 
        :image="img1" 
        title="【全校】安心就學支持計畫"
        donateUrl="https://give.ncu.edu.tw/project_/30"
      >
        <p>每年近800名符合學雜費減免和弱勢助學資格的學生，我們希望能持續協助有經濟困境的學子。考量教育部補助會依學校每年外部募款金額(matching fund)，給予等比例補助(1:1)，因此我們迫切需要各界的支持，協助更多積極向學的同學，讓更多中大的學生能安心求學。</p>
        <p class="">您的支持能夠：</p>
        <ul class="benefit-list">
          <li>溫暖這些孩子，讓他們不再為學費煩惱</li>
          <li>幫助他們在兼顧經濟的情況下順利完成學業，獲得學位</li>
          <li>為他們的未來點燃希望與翻轉人生的機會</li>
        </ul>
      </DonationCard>

      <DonationCard 
        :image="img2" 
        title="【全校】學務處：中正圖書館翻修計畫"
        donateUrl="https://give.ncu.edu.tw/project_/42"
      >
        <p>不論您曾在此默默讀書、等待摯友或只是路過這片白色廊道，中正圖書館都收藏過您的一段青春。</p>
        <p>一筆捐款，是一次感謝；一份參與，是一段連結。</p>
        <p>今日，我們希望與您共同守護這份記憶，攜手，為這棟象徵「知識」、「歷史」與「情感」的建築注入新生命。</p>
        <p>時光迴廊，歷史新生，中正圖書館翻修計畫，讓它能以嶄新姿態，承載更多故事與感動，再現風華。</p>
      </DonationCard>

      <DonationCard 
        :image="img3" 
        title="【全校】學務處：守護學子．逐夢共好"
        donateUrl="https://give.ncu.edu.tw/project_/40"
      >
        <p>本方案透過整合學務處各業務單位之資源與募款需求，統籌運用於學生事務各項推展與服務，建立一套更為完善之支持系統，守護學生在校安心就學及身心就醫、提供諮商輔導、促進課外社團活動、強化住宿服務，支持職涯輔導與實務學習，獎勵卓越人才，傳承原民文化等。陪伴學子逐夢，培育優秀青年，創造社會共好。 </p>
        <p>誠摯邀請您，陪伴學子逐夢，培育優秀青年，創造社會共好。</p>
      </DonationCard>
    </div>
  </main>
</template>

<script setup>
import { RouterLink } from "vue-router";
import DonationCard from "../components/DonationCard.vue";
// images from assets
import img1 from "../assets/img/donation/安心就學支持計畫.png";
import img2 from "../assets/img/donation/中正圖書館翻修.jpg";
import img3 from "../assets/img/donation/守護學子築夢共好.png";
</script>

<style scoped>
.page { 
  padding-top: 1.2rem; 
  padding-left: 5rem;
  padding-right: 5rem;
}

/* 沿用您的麵包屑樣式 */
.crumb {
  display: flex;
  align-items: center;
  gap: .4rem;
  margin: .6rem 0 1rem;
  font-size: .86rem;
  color: #6b7280;
}
.crumb__home { color: #6b7280; text-decoration: none; }
.crumb__home:hover { text-decoration: underline; }

.donation-header {
  margin-bottom: 2.5rem;
}

.page-title {
  font-size: 1.8rem;
  color: #1a1a1a;
  margin-bottom: 1rem;
  position: relative;
  padding-left: 1rem;
}

/* 標題左側的黃色裝飾線 */
.page-title::before {
  content: "";
  position: absolute;
  left: 0;
  top: 15%;
  height: 70%;
  width: 6px;
  background: #f2cf57;
}

.page-intro {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.8;
}

.benefit-list {
  margin-top: 10px;
  padding-left: 1.2rem;
}
.benefit-list li {
  margin-bottom: 5px;
  list-style-type: disc;
}

.donation-list {
  width: min(65rem, 100%);
  margin: 0 auto;
}
</style>