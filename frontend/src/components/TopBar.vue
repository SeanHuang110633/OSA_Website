<template>
  <div class="topbar">
    <div class="container inner">
      <div class="spacer"></div>
      <div class="right">
        <a class="link" href="#">中大首頁</a>
        <span class="sep">|</span>
        <a class="link" href="#">English</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.topbar {
  background: var(--blue-900);
  color: #fff;
  /* 修正：使用規範中的輔助資訊大小 (14px) */
  font-size: var(--text-sm);
}

.inner {
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
  /* 增加行高規範以統一全站文字渲染 */
  line-height: var(--leading-tight);
  font-weight: 700;
}

.link {
  color: #fff;
  opacity: .95;
  text-decoration: none;
}

.link:hover {
  opacity: 1;
  text-decoration: underline;
}

.sep {
  opacity: .7;
}
</style>