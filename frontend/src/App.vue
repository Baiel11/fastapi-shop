<!-- frontend/src/App.vue -->
<!--
  Root application component.
  Contains general structure with Header and RouterView.
-->

<template>
  <div id="app" class="min-h-screen bg-gray-50 dark:bg-zinc-950 text-black dark:text-white transition-colors duration-300">
    <Header />

    <RouterView />

    <footer class="bg-white dark:bg-zinc-900 border-t-2 border-black dark:border-white mt-16 transition-colors duration-300">
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
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
import ToastContainer from '@/components/ToastContainer.vue'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const authStore = useAuthStore()
const themeStore = useThemeStore()

onMounted(async () => {
  themeStore.initTheme()
  await authStore.initAuth()
})
</script>

<style scoped>
/* Remove all style overrides for #app */
/* Tailwind classes fully control layout */
</style>