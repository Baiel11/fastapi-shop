<!-- frontend/src/components/ThemeToggle.vue -->
<template>
  <button
    @click="themeStore.toggleTheme"
    class="p-2 border-2 border-black dark:border-white rounded-xl bg-white dark:bg-zinc-900 text-black dark:text-white transition-all hover:bg-gray-50 dark:hover:bg-zinc-800 hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] dark:hover:shadow-[2px_2px_0px_0px_rgba(255,255,255,1)] active:translate-x-px active:translate-y-px cursor-pointer flex items-center justify-center"
    aria-label="Toggle Theme"
  >
    <!-- Sun icon (shows when in dark mode to switch to light) -->
    <svg
      v-if="themeStore.theme === 'dark'"
      xmlns="http://www.w3.org/2000/svg"
      class="h-5 w-5 text-yellow-400"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.364 17.636l-.707.707M6.364 5.636l.707.707m10.657 10.657l.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
      />
    </svg>
    <!-- Moon icon (shows when in light mode to switch to dark) -->
    <svg
      v-else
      xmlns="http://www.w3.org/2000/svg"
      class="h-5 w-5 text-zinc-700"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
      />
    </svg>
  </button>
</template>

<script setup>
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()
</script>
