<template>
  <section class="hero" aria-label="首頁輪播">
    <div class="shell">
      <button class="nav prev" type="button" aria-label="上一則" @click="prev">‹</button>
      <button class="nav next" type="button" aria-label="下一則" @click="next">›</button>

      <div class="viewport">
        <div
          class="track"
          :style="{
            transform: `translateX(-${index * 100}%)`,
            transitionDuration: isAnimating ? '420ms' : '0ms'
          }"
          @transitionend="isAnimating=false"
        >
          <article v-for="(s, i) in slides" :key="s.id" class="slide">
            <div class="left">
              <img class="photo" :src="s.img" :alt="s.alt" />
            </div>

            <div class="right">
              <h2 class="title">{{ s.title }}</h2>
              <p class="desc">{{ s.desc }}</p>
              <button class="cta" type="button">了解更多</button>
            </div>
          </article>
        </div>
      </div>

      <div class="dots" role="tablist" aria-label="輪播頁碼">
        <button
          v-for="(s, i) in slides"
          :key="s.id"
          class="dot"
          :class="{ on: i === index }"
          type="button"
          :aria-label="`第 ${i + 1} 張`"
          @click="go(i)"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import hero1 from "../assets/image.png";

const slides = ref([
  {
    id: 1,
    img: hero1,
    alt: "活動照片 1",
    title: "中央大學與國泰人壽合作--深化人才培育與實務接軌",
    desc:
      "為強化高等教育與產業實務之連結，培育符合產業發展與社會需求之優質人才，中央大學與國泰人壽正式簽署產學合作備忘錄..."
  },
  {
    id: 2,
    img: "https://picsum.photos/1200/700?2",
    alt: "活動照片 2",
    title: "學生事務處活動公告 2",
    desc: "這裡放第二則事件的摘要內容..."
  },
  {
    id: 3,
    img: "https://picsum.photos/1200/700?3",
    alt: "活動照片 3",
    title: "學生事務處活動公告 3",
    desc: "這裡放第三則事件的摘要內容..."
  }
]);

const index = ref(0);
const isAnimating = ref(false);

function go(i) {
  if (isAnimating.value) return;
  isAnimating.value = true;
  index.value = i;
}

function next() {
  if (isAnimating.value) return;
  isAnimating.value = true;
  index.value = (index.value + 1) % slides.value.length;
}

function prev() {
  if (isAnimating.value) return;
  isAnimating.value = true;
  index.value = (index.value - 1 + slides.value.length) % slides.value.length;
}

let timer = null;
onMounted(() => {
  timer = setInterval(() => {
    next();
  }, 6000);
});
onBeforeUnmount(() => {
  if (timer) clearInterval(timer);
});
</script>

<style scoped>
.hero{
  padding: 1.25rem 0 1.1rem;
  background: #f3f4f6;
}

.shell{
  position: relative;
  width: min(1120px, 100%);
  margin: 0 auto;
  border-radius: 32px;
  overflow: visible;
}

.viewport{
  border-radius: 32px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 16px 38px rgba(16,24,40,.10);
  border: 1px solid rgba(16,24,40,.08);
}

.track{
  display: flex;
  width: 100%;
  will-change: transform;
  transition-property: transform;
  transition-timing-function: cubic-bezier(.2,.9,.2,1);
}

.slide{
  flex: 0 0 100%;
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  min-height: 380px;
}

.left{
  background: #e9edf3;
  display: grid;
  place-items: center;
}
.photo{
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.right{
  background: #0f2f45;
  color: #fff;
  padding: 2.4rem 2.6rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.title{
  margin: 0;
  /* 修正：大幅提升標題氣勢 (36px) 並套用緊湊行高 (1.3) */
  font-size: var(--text-4xl);
  font-weight: 700;
  color: #f2cf57;
  line-height: var(--leading-tight);
}
.desc{
  margin: 0;
  /* 修正：副標題微調大 (18px) 並增加內文行高 (1.6) */
  font-size: var(--text-lg);
  font-weight: 400;
  line-height: var(--leading-normal);
  opacity: .92;
}
.cta{
  margin-top: auto;
  width: 240px;
  height: 56px;
  border-radius: 999px;
  border: 0;
  background: #f2cf57;
  color: #111827;
  font-weight: 700;
  /* 修正：按鈕保持標準 16px 大小 */
  font-size: var(--text-base);
  cursor: pointer;
}

.nav{
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border: 0;
  background: transparent;
  box-shadow: none;
  border-radius: 0;
  cursor: pointer;
  z-index: 5;
  display: grid;
  place-items: center;
  font-size: 44px;
  line-height: 1;
  color: rgba(17,24,39,.55);
  user-select: none;
}

.prev{ left: 12px; }
.next{ right: 12px; }

.nav:hover{
  color: rgba(17,24,39,.85);
}

.nav:active{
  transform: translateY(-50%) scale(.96);
}

.nav:focus-visible{
  outline: 2px solid rgba(242,207,87,.9);
  outline-offset: 3px;
}
.dots{
  display: flex;
  justify-content: center;
  gap: .5rem;
  padding-top: .9rem;
}
.dot{
  width: 6px;
  height: 6px;
  border-radius: 999px;
  border: 0;
  background: rgba(17,24,39,.18);
  cursor: pointer;
}
.dot.on{
  width: 7px;
  height: 7px;
  background: rgba(41, 57, 92, 0.6);
}

/* RWD */
@media (max-width: 980px){
  .slide{ grid-template-columns: 1fr; }
  .right{ padding: 1.6rem 1.4rem; }
  /* 手機版適度降級標題大小以避免破版 */
  .title { font-size: var(--text-2xl); }
  .prev{ left: 10px; }
  .next{ right: 10px; }
}
</style>