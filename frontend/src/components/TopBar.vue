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
.topbar{
  background: var(--blue-900);
  color:#fff;
  font-size: 14px;
}
.inner{
  height: 44px;
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.right{
  margin-left:auto;
  display:flex;
  align-items:center;
  gap:10px;
  font-weight: 700;
}
.link{ color:#fff; opacity:.95; }
.link:hover{ opacity:1; text-decoration:underline; }
.sep{ opacity:.7; }
</style>