import { createRouter, createWebHistory } from 'vue-router'
import Home from "../pages/HomePage.vue";
import NewsList from "../pages/NewsList.vue";
import ServiceResources from "../pages/ServiceResources.vue";
// import Downloads from "../pages/Downloads.vue"; 先改成下面這個
import DownloadPage from "../pages/DownloadPage.vue";
import AboutUsPage from "../pages/AboutUsPage.vue";
import EventDetailPage from "../pages/EventDetailPage.vue";
import DonationPage from "../pages/DonationPage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: Home },
    { path: "/news", name: "news", component: NewsList },
    { path: "/events/:id", name: "event-detail", component: EventDetailPage },
    { path: "/resources", name: "resources", component: ServiceResources },
    // { path: "/downloads", name: "downloads", component: Downloads }, 先改成下面這個
    { path: "/downloads", name: "downloads", component: DownloadPage },
    { path: "/about", name: "about", component: AboutUsPage },
    { path: "/donate", name: "donate", component: DonationPage },
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
