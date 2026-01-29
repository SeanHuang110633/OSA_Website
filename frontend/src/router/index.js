import { createRouter, createWebHistory } from 'vue-router'
import OriginalExamples from '../pages/originalExamples.vue'
import Donate from '../pages/donationPage.vue'

const routes = [
  { path: '/example', name: 'OriginalExamples', component: OriginalExamples },
  { path: '/donate', name: 'Donate', component: Donate },
  { path: '/', redirect: '/example' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
