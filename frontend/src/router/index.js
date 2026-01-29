import { createRouter, createWebHistory } from 'vue-router'
import OriginalExamples from '../pages/originalExamples.vue'

const routes = [
  { path: '/example', name: 'OriginalExamples', component: OriginalExamples },
  { path: '/', redirect: '/example' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
