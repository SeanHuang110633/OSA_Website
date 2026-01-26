<template>
  <main class="container">
    <HeroBanner class="section" />
    <NewsAndLinks class="section" />
    <EventsRow class="section" />
  </main>

  <QuickLinksGrid class="section" />
  <main class="container">
    <MapSection class="section" />
  </main>
</template>

<script setup>
import HeroBanner from "../components/HeroBanner.vue";
import NewsAndLinks from "../components/NewsAndLinks.vue";
import EventsRow from "../components/EventsRow.vue";
import QuickLinksGrid from "../components/QuickLinksGrid.vue";
import MapSection from "../components/MapSection.vue";
</script>