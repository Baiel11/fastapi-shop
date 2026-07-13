// frontend/src/stores/theme.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // Read initial theme from localStorage or system preference
  const savedTheme = localStorage.getItem('theme')
  
  // Use system preference if no user preference is cached
  const systemPrefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
  
  const theme = ref(savedTheme || (systemPrefersDark ? 'dark' : 'light'))

  /**
   * Initializes the theme state (applies appropriate CSS classes).
   */
  function initTheme() {
    applyThemeClass()
  }

  /**
   * Toggles the theme between light and dark.
   */
  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    localStorage.setItem('theme', theme.value)
    applyThemeClass()
  }

  /**
   * Helper to set class on the HTML document element
   */
  function applyThemeClass() {
    if (theme.value === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return {
    theme,
    initTheme,
    toggleTheme,
  }
})
