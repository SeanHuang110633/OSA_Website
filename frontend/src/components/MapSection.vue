<template>
  <section id="location-map" class="card map">
    <div class="title">位置資訊</div>

    <div class="frame">
      <iframe
        title="NCU map"
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?q=National%20Central%20University&output=embed">
      </iframe>
    </div>

    <img class="animal left" :src="a1" alt="" aria-hidden="true" />
    <img class="animal right" :src="a2" alt="" aria-hidden="true" />
  </section>
</template>

<script setup>
import a1 from "../assets/OHD_animal1.png";
import a2 from "../assets/OHD_animal2.png";
</script>

<style scoped>
.map {
  position: relative;
  padding: 1rem;
  overflow: visible;
}

.title {
  text-align: center;
  /* 修正：區塊標題統一使用 24px 並套用緊湊行高 */
  font-size: var(--text-2xl);
  line-height: var(--leading-tight);
  font-weight: 700;
  letter-spacing: .12em;
  color: #0f3a63;
  margin-bottom: .75rem;
}

.frame {
  border-radius: .9rem;
  overflow: hidden;
  border: 1px solid rgba(16, 24, 40, .10);
  background: #fff;
}

iframe {
  width: 100%;
  height: 18rem;
  border: 0;
  display: block;
}

/* 吉祥物 */
.animal {
  position: absolute;
  width: 8rem;
  height: auto;
  bottom: -1.2rem;
}

.left {
  left: 1.1rem;
}

.right {
  right: 1.1rem;
}

/* RWD */
@media (max-width: 560px) {
  iframe {
    height: 15rem;
  }

  .animal {
    width: 3.8rem;
    bottom: -1rem;
  }

  /* 修正：手機版標題適度降級至 18px (lg) */
  .title {
    font-size: var(--text-lg);
  }
}
</style>