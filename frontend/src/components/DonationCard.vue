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
          <a :href="detailUrl" target="_blank" rel="noopener noreferrer" class="btn-detail">詳細資訊 ｜ 我要捐款<span class="arrow">→</span></a>
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
  border-bottom-right-radius: 0;
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
  /* 右側內距設為0，讓按鈕可以貼齊卡片邊界 */
  padding: 2rem 0 2rem 2rem;
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
  line-height: 1.9; /* 增加段落內行距 */
  color: #4b5563;
  margin-bottom: 4.5rem; /* 為底部按鈕留空間 */
}

.card-description p {
  margin-bottom: 1rem; /* 段落之間加大間距 */
}

.card-actions {
  position: absolute;
  right: 0;
  bottom: 0;
}

.action-group {
  display: flex;
  align-items: center;
  background: #bfa37e; /* 截圖中的大地色系按鈕 */
  /* 只有左上角為圓角，其餘為尖角 */
  border-top-left-radius: 3rem;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  padding: 0; /* 由內部連結填滿空間，確保整塊可點擊 */
  color: #fff;
  overflow: hidden;
  height: 64px;
}

.action-group a {
  display: flex;
  align-items: center;
  color: #fff;
  text-decoration: none;
  font-weight: 400; /* 字體再細一些 */
  font-size: 0.92rem;
  padding: 0 3rem; /* 由群組控制高度，按鈕左右給予空間 */
  height: 100%;
}

.action-group span {
   padding-left: 0.5rem;
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
  .action-group {
    min-width: 0;
    width: 100%;
    height: 56px;
    border-radius: 12px;
  }
  .action-group a { padding: 0 1rem; }
}
</style>