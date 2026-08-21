import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { onSessionExpired } from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Wire the "session can no longer be refreshed" signal from the axios
// interceptor to the auth store and a redirect to the login page.
onSessionExpired(() => {
  const authStore = useAuthStore()
  authStore.handleSessionExpired()
  router.push({ name: 'login' })
})

app.mount('#app')