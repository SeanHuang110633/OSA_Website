<template>
  <div class="page">
    <TopBar />
    <NavBar />
    <router-view />
    <SiteFooter />
  </div>
</template>

<script setup>
import TopBar from "./components/TopBar.vue";
import NavBar from "./components/NavBar.vue";
import SiteFooter from "./components/SiteFooter.vue";
</script>
