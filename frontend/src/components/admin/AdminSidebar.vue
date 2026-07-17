<template>
  <aside
    class="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0 border-r border-gray-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md flex flex-col justify-between"
  >
    <div class="px-3 py-4 overflow-y-auto">
      <!-- Logo / Title -->
      <div class="flex items-center ps-2.5 mb-8">
        <span class="self-center text-xl font-bold tracking-wider text-black dark:text-white flex items-center gap-2">
          <svg class="w-6 h-6 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          FA SHOP ADMIN
        </span>
      </div>

      <!-- Navigation Links -->
      <ul class="space-y-2 font-medium">
        <li>
          <router-link
            :to="{ name: 'admin-dashboard' }"
            exact-active-class="bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400"
            class="flex items-center p-3 text-gray-700 dark:text-zinc-300 rounded-xl hover:bg-gray-100 dark:hover:bg-zinc-900 transition-colors duration-200"
          >
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2v-4zM14 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4z" />
            </svg>
            Dashboard
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'admin-products' }"
            active-class="bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400"
            class="flex items-center p-3 text-gray-700 dark:text-zinc-300 rounded-xl hover:bg-gray-100 dark:hover:bg-zinc-900 transition-colors duration-200"
          >
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
            Products
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'admin-categories' }"
            active-class="bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400"
            class="flex items-center p-3 text-gray-700 dark:text-zinc-300 rounded-xl hover:bg-gray-100 dark:hover:bg-zinc-900 transition-colors duration-200"
          >
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            Categories
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'admin-users' }"
            active-class="bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400"
            class="flex items-center p-3 text-gray-700 dark:text-zinc-300 rounded-xl hover:bg-gray-100 dark:hover:bg-zinc-900 transition-colors duration-200"
          >
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            Users
          </router-link>
        </li>
      </ul>

      <!-- Divider -->
      <div class="h-[1px] bg-gray-200 dark:bg-zinc-800 my-6"></div>

      <!-- General links -->
      <ul class="space-y-2 font-medium">
        <li>
          <router-link
            to="/"
            class="flex items-center p-3 text-gray-600 dark:text-zinc-400 rounded-xl hover:bg-gray-100 dark:hover:bg-zinc-900 transition-colors duration-200"
          >
            <svg class="w-5 h-5 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            Go to Shop
          </router-link>
        </li>
      </ul>
    </div>

    <!-- User Profile & Log Out bottom block -->
    <div class="p-4 border-t border-gray-200 dark:border-zinc-800 bg-gray-50/50 dark:bg-zinc-900/20">
      <div class="flex items-center gap-3 mb-4">
        <!-- Avatar Placeholder -->
        <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-pink-500 flex items-center justify-center text-white font-bold">
          {{ userInitials }}
        </div>
        <div class="overflow-hidden">
          <p class="text-sm font-semibold text-gray-800 dark:text-zinc-200 truncate">
            {{ user?.username || 'Admin User' }}
          </p>
          <p class="text-xs text-gray-500 dark:text-zinc-500 truncate">
            {{ user?.email }}
          </p>
        </div>
      </div>
      <button
        @click="handleLogout"
        class="w-full flex items-center justify-center gap-2 p-2.5 text-sm font-semibold text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-950/20 hover:bg-red-100 dark:hover:bg-red-950/40 rounded-xl transition-all duration-200"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        Sign Out
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const user = computed(() => authStore.user)

const userInitials = computed(() => {
  if (!user.value || !user.value.username) return 'A'
  return user.value.username.slice(0, 2).toUpperCase()
})

const handleLogout = () => {
  authStore.logout()
  router.push({ name: 'login' })
}
</script>
