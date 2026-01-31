<template>
  <div class="donation-card">
    <div class="card-image">
      <img :src="image" :alt="title" />
    </div>
    <div class="card-content">
      <h3 class="card-title">{{ title }}</h3>
      <div class="card-description">
        <slot></slot> 
      </div>
      <div class="card-actions">
        <div class="action-group">
          <a :href="detailUrl" class="btn-detail">詳細資訊</a>
          <span class="sep">|</span>
          <a :href="donateUrl" class="btn-donate">我要捐款 <span class="arrow">→</span></a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  image: String,
  title: String,
  detailUrl: { type: String, default: '#' },
  donateUrl: { type: String, default: '#' }
});
</script>

<style scoped>
.donation-card {
  display: flex;
  background: #fff;
  border-radius: 1rem;
  border: 1px solid rgba(16, 24, 40, 0.1);
  overflow: hidden;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.donation-card:hover {
  transform: translateY(-5px);
}

.card-image {
  flex: 0 0 40%;
  max-width: 400px;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  flex: 1;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  position: relative;
}

.card-title {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.card-description {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #4b5563;
  margin-bottom: 4rem; /* 為底部按鈕留空間 */
}

.card-actions {
  position: absolute;
  right: 1.5rem;
  bottom: 1.5rem;
}

.action-group {
  display: flex;
  align-items: center;
  background: #bfa37e; /* 截圖中的大地色系按鈕 */
  border-radius: 999px;
  padding: 0.5rem 1.5rem;
  color: #fff;
}

.action-group a {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
}

.sep {
  margin: 0 0.8rem;
  opacity: 0.6;
}

.arrow {
  margin-left: 5px;
}

/* RWD */
@media (max-width: 768px) {
  .donation-card {
    flex-direction: column;
  }
  .card-image {
    flex: 0 0 auto;
    max-width: 100%;
    height: 200px;
  }
  .card-actions {
    position: static;
    margin-top: 1rem;
    display: flex;
    justify-content: flex-end;
  }
}
</style>