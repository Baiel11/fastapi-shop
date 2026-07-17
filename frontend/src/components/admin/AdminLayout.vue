<template>
  <div class="min-h-screen bg-gray-50 dark:bg-zinc-900 transition-colors duration-300">
    <!-- Mobile Sidebar Trigger overlay button -->
    <div
      v-if="isSidebarOpen"
      @click="isSidebarOpen = false"
      class="fixed inset-0 z-30 bg-black/40 backdrop-blur-sm sm:hidden"
    ></div>

    <!-- Sidebar component -->
    <AdminSidebar
      :class="{
        'translate-x-0': isSidebarOpen,
        '-translate-x-full': !isSidebarOpen
      }"
      class="transition-transform duration-300"
    />

    <!-- Top and Main content wrapper -->
    <div class="sm:ml-64 flex flex-col min-h-screen">
      <!-- Top navbar -->
      <header
        class="sticky top-0 z-20 flex items-center justify-between h-16 px-6 border-b border-gray-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md transition-colors duration-300"
      >
        <!-- Sidebar Toggle and Page Title -->
        <div class="flex items-center gap-4">
          <!-- Sidebar Toggle (Mobile only) -->
          <button
            @click="isSidebarOpen = !isSidebarOpen"
            type="button"
            class="inline-flex items-center p-2 text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 dark:hover:bg-zinc-800 focus:outline-none"
          >
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
            </svg>
          </button>
          <h1 class="text-lg font-bold text-gray-800 dark:text-zinc-100 tracking-wide">
            {{ pageTitle }}
          </h1>
        </div>

        <!-- Right Side: Theme Toggle / Settings -->
        <div class="flex items-center gap-3">
          <!-- Dark Mode Toggle Button -->
          <button
            @click="themeStore.toggleTheme()"
            class="p-2.5 rounded-xl border border-gray-200 dark:border-zinc-800 text-gray-600 dark:text-zinc-300 hover:bg-gray-50 dark:hover:bg-zinc-900 transition-colors duration-200"
            title="Toggle theme"
          >
            <!-- Sun Icon (shown in dark mode) -->
            <svg v-if="themeStore.theme === 'dark'" class="w-5 h-5 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 2.293a1 1 0 010 1.414L13.293 6.7a1 1 0 11-1.414-1.414l1.414-1.414a1 1 0 011.414 0zM17 10a1 1 0 00-1-1h-1a1 1 0 100 2h1a1 1 0 001-1zm-2.293 4.707a1 1 0 011.414 0L17.586 16.12a1 1 0 11-1.414 1.414l-1.414-1.414a1 1 0 010-1.414zM10 17a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zm-5.707-3.707a1 1 0 010-1.414L5.707 10.586a1 1 0 011.414 1.414l-1.414 1.414a1 1 0 01-1.414 0zm0-7.293a1 1 0 011.414 0L6.7 4.293a1 1 0 01-1.414 1.414L3.88 5.707a1 1 0 010-1.414zM10 5a5 5 0 100 10 5 5 0 000-10z" />
            </svg>
            <!-- Moon Icon (shown in light mode) -->
            <svg v-else class="w-5 h-5 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
            </svg>
          </button>
        </div>
      </header>

      <!-- Main body container -->
      <main class="flex-1 p-6">
        <RouterView v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </RouterView>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import AdminSidebar from './AdminSidebar.vue'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()
const route = useRoute()
const isSidebarOpen = ref(false)

// Page title from route metadata
const pageTitle = computed(() => {
  if (route.meta && route.meta.title) {
    // Strip "Admin - " prefix if present for top bar presentation
    return route.meta.title.replace('Admin - ', '')
  }
  return 'Dashboard'
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
