import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import NewsList from "../pages/NewsList.vue";
import ServiceResources from "../pages/ServiceResources.vue";
import Downloads from "../pages/Downloads.vue";
import AboutUs from "../pages/AboutUs.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Home },
    { path: "/news", component: NewsList },
    { path: "/resources", component: ServiceResources },
    { path: "/downloads", name: "downloads", component: Downloads },
    { path: "/about", name: "about", component: AboutUs },
  ],

  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition;

    if (to.hash) {
      return {
        el: to.hash,
        behavior: "smooth",
        top: 90, 
      };
    }
    return { top: 0 };
  },
});

export default router;