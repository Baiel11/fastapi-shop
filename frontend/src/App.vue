<template>
  <div id="app" class="min-h-screen bg-gray-50 dark:bg-zinc-950 text-black dark:text-white transition-colors duration-300">
    <!-- Render customer Header only outside admin views -->
    <Header v-if="!isAdminRoute" />

    <RouterView />

    <!-- Render customer Footer only outside admin views -->
    <footer v-if="!isAdminRoute" class="bg-white dark:bg-zinc-900 border-t-2 border-black dark:border-white mt-16 transition-colors duration-300">
      <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="text-center text-gray-600 dark:text-zinc-400">
          <p class="mb-2">© 2024 FastAPI Shop. All rights reserved.</p>
          <p class="text-sm">Built with FastAPI + Vue.js</p>
        </div>
      </div>
    </footer>

    <!-- Global toast notification container — renders via Teleport above all content -->
    <ToastContainer />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import Header from '@/components/Header.vue'
import ToastContainer from '@/components/ToastContainer.vue'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const route = useRoute()

// Check if we are currently inside the admin panel
const isAdminRoute = computed(() => route.path.startsWith('/admin'))

onMounted(async () => {
  themeStore.initTheme()
  await authStore.initAuth()
})
</script>

<style scoped>
/* Remove all style overrides for #app */
/* Tailwind classes fully control layout */
</style>