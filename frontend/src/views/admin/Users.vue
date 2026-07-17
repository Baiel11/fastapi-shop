<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">User Management</h2>
      <p class="text-sm text-gray-500 dark:text-zinc-400 mt-1">Monitor users, toggle account access, and assign admin role privileges.</p>
    </div>

    <!-- Users List Card -->
    <div class="bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border border-gray-100 dark:border-zinc-800 rounded-2xl overflow-hidden shadow-sm">
      <div class="p-5 border-b border-gray-100 dark:border-zinc-800 flex items-center justify-between">
        <h3 class="font-bold text-gray-800 dark:text-zinc-200">System Users</h3>
        <span class="text-xs text-gray-400 font-semibold uppercase tracking-wider">
          Total Users: {{ totalUsers }}
        </span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-gray-50 dark:bg-zinc-900/50 text-xs font-bold text-gray-400 dark:text-zinc-500 border-b border-gray-100 dark:border-zinc-800 uppercase tracking-wider">
              <th class="py-4 px-6">User</th>
              <th class="py-4 px-6">Registration Date</th>
              <th class="py-4 px-6">Active Status</th>
              <th class="py-4 px-6">Administrator Role</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-zinc-800 text-sm text-gray-700 dark:text-zinc-300">
            <tr v-if="loading">
              <td colspan="4" class="py-16 text-center">
                <span class="inline-block animate-pulse text-indigo-500 font-medium">Loading user database...</span>
              </td>
            </tr>
            <tr v-else-if="users.length === 0">
              <td colspan="4" class="py-16 text-center text-gray-400">
                No users found.
              </td>
            </tr>
            <tr
              v-else
              v-for="u in users"
              :key="u.id"
              class="hover:bg-gray-50/50 dark:hover:bg-zinc-900/30 transition-colors duration-150"
            >
              <!-- Info Name & Email -->
              <td class="py-4 px-6">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-indigo-50 dark:bg-indigo-950/40 flex items-center justify-center text-indigo-600 dark:text-indigo-400 font-bold">
                    {{ u.username.slice(0, 2).toUpperCase() }}
                  </div>
                  <div>
                    <span class="font-semibold text-gray-900 dark:text-white block">{{ u.username }}</span>
                    <span class="text-xs text-gray-400">{{ u.email }}</span>
                  </div>
                </div>
              </td>

              <!-- Date -->
              <td class="py-4 px-6 text-gray-500 dark:text-zinc-400">
                {{ formatDate(u.created_at) }}
              </td>

              <!-- Active status Switch (Ban / Unban) -->
              <td class="py-4 px-6">
                <div class="flex items-center">
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      :checked="u.is_active"
                      @change="toggleUserStatus(u)"
                      class="sr-only peer"
                    />
                    <div class="w-11 h-6 bg-gray-250 dark:bg-zinc-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
                    <span class="ml-3 text-xs font-semibold" :class="u.is_active ? 'text-emerald-500' : 'text-red-500'">
                      {{ u.is_active ? 'Active' : 'Disabled' }}
                    </span>
                  </label>
                </div>
              </td>

              <!-- Admin role Switch (Promote / Demote) -->
              <td class="py-4 px-6">
                <div class="flex items-center">
                  <label class="relative inline-flex items-center" :class="u.id === currentAdminUser?.id ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'">
                    <input
                      type="checkbox"
                      :checked="u.is_admin"
                      :disabled="u.id === currentAdminUser?.id"
                      @change="toggleUserRole(u)"
                      class="sr-only peer"
                    />
                    <div class="w-11 h-6 bg-gray-250 dark:bg-zinc-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                    <span class="ml-3 text-xs font-semibold" :class="u.is_admin ? 'text-indigo-600 dark:text-indigo-400' : 'text-gray-400'">
                      {{ u.is_admin ? 'Admin' : 'Customer' }}
                    </span>
                  </label>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Footer -->
      <div v-if="totalPages > 1" class="p-5 border-t border-gray-100 dark:border-zinc-800 flex items-center justify-between">
        <button
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
          class="px-4 py-2 border border-gray-200 dark:border-zinc-850 hover:bg-gray-50 dark:hover:bg-zinc-900 text-sm font-semibold rounded-xl transition disabled:opacity-50"
        >
          Previous
        </button>
        <span class="text-sm text-gray-400">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
          class="px-4 py-2 border border-gray-200 dark:border-zinc-850 hover:bg-gray-50 dark:hover:bg-zinc-900 text-sm font-semibold rounded-xl transition disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminAPI } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'

const authStore = useAuthStore()
const toastStore = useToastStore()

// States
const users = ref([])
const loading = ref(true)

// Pagination
const currentPage = ref(1)
const totalPages = ref(1)
const totalUsers = ref(0)
const pageSize = 10

// Currently logged-in admin user to prevent self-role edits
const currentAdminUser = computed(() => authStore.user)

const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await adminAPI.getUsers(currentPage.value, pageSize)
    users.value = response.data.items
    totalPages.value = response.data.pages
    totalUsers.value = response.data.total
  } catch (error) {
    console.error('Failed to load users:', error)
    toastStore.error('Could not load user list.')
  } finally {
    loading.value = false
  }
}

const changePage = (page) => {
  currentPage.value = page
  fetchUsers()
}

onMounted(fetchUsers)

const toggleUserStatus = async (user) => {
  const targetStatus = !user.is_active
  try {
    const response = await adminAPI.updateUserStatus(user.id, targetStatus)
    user.is_active = response.data.is_active
    toastStore.success(`User "${user.username}" status updated to ${user.is_active ? 'Active' : 'Disabled'}.`)
  } catch (error) {
    console.error('Failed to toggle active status:', error)
    toastStore.error('Could not update user status.')
  }
}

const toggleUserRole = async (user) => {
  const targetRole = !user.is_admin
  try {
    const response = await adminAPI.updateUserRole(user.id, targetRole)
    user.is_admin = response.data.is_admin
    toastStore.success(`User "${user.username}" role updated to ${user.is_admin ? 'Admin' : 'Customer'}.`)
  } catch (error) {
    console.error('Failed to toggle admin role:', error)
    toastStore.error(error.response?.data?.detail || 'Could not update user role.')
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>
