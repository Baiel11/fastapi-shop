<template>
  <div class="min-h-[80vh] bg-white dark:bg-zinc-950 transition-colors duration-300 flex items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white dark:bg-zinc-900 p-8 rounded-2xl border-2 border-black dark:border-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] dark:shadow-[4px_4px_0px_0px_rgba(255,255,255,1)] transition-all duration-300">
      <!-- Success state -->
      <template v-if="success">
        <div class="text-center">
          <h2 class="text-3xl font-extrabold text-black dark:text-white">Password updated</h2>
          <p class="mt-2 text-sm text-gray-600 dark:text-zinc-400">
            Your password has been changed and all other sessions were signed out.
          </p>
        </div>
        <div class="text-center">
          <router-link
            to="/login"
            class="inline-block py-3 px-6 border-2 border-black dark:border-white text-sm font-bold rounded-xl text-black dark:text-white bg-white dark:bg-zinc-900 hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] dark:hover:shadow-[4px_4px_0px_0px_rgba(255,255,255,1)] active:translate-x-0.5 active:translate-y-0.5 transition-all"
          >
            Sign in with your new password
          </router-link>
        </div>
      </template>

      <!-- Missing token (e.g. page opened without following the email link) -->
      <template v-else-if="!token">
        <div class="text-center">
          <h2 class="text-3xl font-extrabold text-black dark:text-white">Invalid link</h2>
          <p class="mt-2 text-sm text-gray-600 dark:text-zinc-400">
            This page needs a reset token from your email.
          </p>
        </div>
        <div class="text-center">
          <router-link
            to="/forgot-password"
            class="font-medium text-black dark:text-white underline hover:text-gray-800 dark:hover:text-zinc-300 transition-colors"
          >
            Request a new reset link
          </router-link>
        </div>
      </template>

      <!-- Reset form -->
      <template v-else>
        <div class="text-center">
          <h2 class="text-3xl font-extrabold text-black dark:text-white">Choose a new password</h2>
          <p class="mt-2 text-sm text-gray-600 dark:text-zinc-400">
            Must contain an uppercase letter, a lowercase letter and a number.
          </p>
        </div>

        <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
          <div>
            <label for="password" class="block text-sm font-semibold text-black dark:text-white mb-1">New password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              minlength="8"
              autocomplete="new-password"
              class="w-full px-4 py-3 border-2 border-black dark:border-zinc-700 rounded-xl text-black dark:text-white bg-white dark:bg-zinc-900 focus:outline-none focus:bg-yellow-50 dark:focus:bg-zinc-800 focus:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] dark:focus:shadow-[2px_2px_0px_0px_rgba(255,255,255,1)] transition-all"
              placeholder="At least 8 characters"
            />
          </div>

          <div v-if="error" class="bg-red-50 dark:bg-red-950 border-2 border-red-500 text-red-700 dark:text-red-200 p-4 rounded-xl text-sm font-medium">
            {{ error }}
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading"
              class="group relative w-full flex justify-center py-3 px-4 border-2 border-black dark:border-white text-sm font-bold rounded-xl text-white dark:text-black bg-black dark:bg-white hover:bg-white dark:hover:bg-zinc-900 hover:text-black dark:hover:text-white hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] dark:hover:shadow-[4px_4px_0px_0px_rgba(255,255,255,1)] active:translate-x-0.5 active:translate-y-0.5 transition-all disabled:opacity-50 cursor-pointer"
            >
              <span v-if="loading" class="animate-spin mr-2 h-5 w-5 border-t-2 border-r-2 border-white rounded-full"></span>
              Update password
            </button>
          </div>
        </form>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { authAPI } from '@/services/api'

const route = useRoute()

// Token arrives via the emailed link: /reset-password?token=...
const token = route.query.token || null

const password = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(null)

async function handleSubmit() {
  if (!password.value) return

  loading.value = true
  error.value = null
  try {
    await authAPI.resetPassword(token, password.value)
    success.value = true
  } catch (err) {
    console.error('Reset password error:', err)
    const detail = err.response?.data?.detail
    // A 401 here usually means the single-use link was already consumed
    // or expired — tell the user to request a fresh one.
    error.value = detail === 'Invalid or expired reset link'
      ? 'This reset link is invalid or has expired. Please request a new one.'
      : detail || 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
