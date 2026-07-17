<template>
  <div class="space-y-6">
    <!-- Header Block -->
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Welcome back, Admin!</h2>
      <p class="text-sm text-gray-500 dark:text-zinc-400 mt-1">Here is a quick look at your shop stats today.</p>
    </div>

    <!-- Metrics Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Total Users -->
      <div class="bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border border-gray-100 dark:border-zinc-800 p-6 rounded-2xl flex items-center justify-between shadow-sm hover:shadow-md transition-shadow duration-300">
        <div>
          <span class="text-sm font-medium text-gray-400 dark:text-zinc-500 block">Total Customers</span>
          <span v-if="loading" class="text-2xl font-bold text-gray-800 dark:text-zinc-200 mt-2 block animate-pulse">...</span>
          <span v-else class="text-3xl font-extrabold text-gray-900 dark:text-white mt-2 block">{{ stats?.total_users || 0 }}</span>
          <span v-if="!loading" class="text-xs font-semibold text-emerald-500 bg-emerald-50 dark:bg-emerald-950/20 px-2 py-0.5 rounded-full inline-block mt-3">
            {{ stats?.active_users || 0 }} Active
          </span>
        </div>
        <div class="w-12 h-12 rounded-xl bg-blue-50 dark:bg-blue-950/30 flex items-center justify-center text-blue-600 dark:text-blue-400">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </div>
      </div>

      <!-- Total Products -->
      <div class="bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border border-gray-100 dark:border-zinc-800 p-6 rounded-2xl flex items-center justify-between shadow-sm hover:shadow-md transition-shadow duration-300">
        <div>
          <span class="text-sm font-medium text-gray-400 dark:text-zinc-500 block">Total Catalog Items</span>
          <span v-if="loading" class="text-2xl font-bold text-gray-800 dark:text-zinc-200 mt-2 block animate-pulse">...</span>
          <span v-else class="text-3xl font-extrabold text-gray-900 dark:text-white mt-2 block">{{ stats?.total_products || 0 }}</span>
          <span v-if="!loading" class="text-xs font-semibold text-indigo-500 bg-indigo-50 dark:bg-indigo-950/20 px-2 py-0.5 rounded-full inline-block mt-3">
            {{ stats?.active_products || 0 }} Active
          </span>
        </div>
        <div class="w-12 h-12 rounded-xl bg-indigo-50 dark:bg-indigo-950/30 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
        </div>
      </div>

      <!-- Total Categories -->
      <div class="bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border border-gray-100 dark:border-zinc-800 p-6 rounded-2xl flex items-center justify-between shadow-sm hover:shadow-md transition-shadow duration-300">
        <div>
          <span class="text-sm font-medium text-gray-400 dark:text-zinc-500 block">Total Categories</span>
          <span v-if="loading" class="text-2xl font-bold text-gray-800 dark:text-zinc-200 mt-2 block animate-pulse">...</span>
          <span v-else class="text-3xl font-extrabold text-gray-900 dark:text-white mt-2 block">{{ stats?.total_categories || 0 }}</span>
          <span v-if="!loading" class="text-xs font-semibold text-gray-500 dark:text-zinc-500 bg-gray-50 dark:bg-zinc-900/60 px-2 py-0.5 rounded-full inline-block mt-3">
            Active Catalog
          </span>
        </div>
        <div class="w-12 h-12 rounded-xl bg-purple-50 dark:bg-purple-950/30 flex items-center justify-center text-purple-600 dark:text-purple-400">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Quick Actions Panel -->
    <div class="bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border border-gray-100 dark:border-zinc-800 p-6 rounded-2xl">
      <h3 class="text-lg font-bold text-gray-800 dark:text-zinc-100 mb-4">Quick Operations</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        <router-link
          :to="{ name: 'admin-products', query: { action: 'new' } }"
          class="flex items-center gap-3 p-4 rounded-xl border border-dashed border-gray-300 dark:border-zinc-700 hover:border-indigo-500 dark:hover:border-indigo-400 text-gray-600 dark:text-zinc-400 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-indigo-50/20 transition-all duration-200"
        >
          <div class="w-8 h-8 rounded-lg bg-indigo-50 dark:bg-indigo-950/30 flex items-center justify-center">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
          </div>
          <span class="text-sm font-semibold">Add New Product</span>
        </router-link>

        <router-link
          :to="{ name: 'admin-categories' }"
          class="flex items-center gap-3 p-4 rounded-xl border border-dashed border-gray-300 dark:border-zinc-700 hover:border-purple-500 dark:hover:border-purple-400 text-gray-600 dark:text-zinc-400 hover:text-purple-600 dark:hover:text-purple-400 hover:bg-purple-50/20 transition-all duration-200"
        >
          <div class="w-8 h-8 rounded-lg bg-purple-50 dark:bg-purple-950/30 flex items-center justify-center">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0V9a2 2 0 00-2-2" />
            </svg>
          </div>
          <span class="text-sm font-semibold">Manage Categories</span>
        </router-link>

        <router-link
          :to="{ name: 'admin-users' }"
          class="flex items-center gap-3 p-4 rounded-xl border border-dashed border-gray-300 dark:border-zinc-700 hover:border-blue-500 dark:hover:border-blue-400 text-gray-600 dark:text-zinc-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50/20 transition-all duration-200"
        >
          <div class="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-950/30 flex items-center justify-center">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292" />
            </svg>
          </div>
          <span class="text-sm font-semibold">User Management</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminAPI } from '@/services/api'

const stats = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await adminAPI.getStats()
    stats.value = response.data
  } catch (error) {
    console.error('Failed to load admin stats:', error)
  } finally {
    loading.value = false
  }
})
</script>
