import { createRouter, createWebHistory } from 'vue-router'
import Home from "../pages/Home.vue";
import NewsList from "../pages/NewsList.vue";
import ServiceResources from "../pages/ServiceResources.vue";
// import Downloads from "../pages/Downloads.vue"; 先改成下面這個
import DownloadPage from "../pages/DownloadPage.vue";
import AboutUs from "../pages/AboutUs.vue";
import OriginalExamples from '../pages/originalExamples.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: Home },
    { path: "/news", name: "news", component: NewsList },
    { path: "/resources", name: "resources", component: ServiceResources },
    // { path: "/downloads", name: "downloads", component: Downloads }, 先改成下面這個
    { path: "/downloads", name: "downloads", component: DownloadPage },
    { path: "/about", name: "about", component: AboutUs },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition;
    if (to.hash) {
      return { el: to.hash, behavior: "smooth", top: 90 };
    }
    return { top: 0 };
  },
});

export default router;
