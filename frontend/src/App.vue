<template>
  <div class="page">
    <TopBar />
    <NavBar />
    <RouterView />
    <SiteFooter />
  </div>
</template>

<script setup>
import TopBar from "./components/TopBar.vue";
import NavBar from "./components/NavBar.vue";
import SiteFooter from "./components/SiteFooter.vue";
import { RouterView } from "vue-router";
</script>