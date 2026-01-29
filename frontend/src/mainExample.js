import { createApp } from 'vue'
import './styleExamples.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)
app.mount('#app')
