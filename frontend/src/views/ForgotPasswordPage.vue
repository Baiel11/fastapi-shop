<template>
  <div class="min-h-[80vh] bg-white dark:bg-zinc-950 transition-colors duration-300 flex items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white dark:bg-zinc-900 p-8 rounded-2xl border-2 border-black dark:border-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] dark:shadow-[4px_4px_0px_0px_rgba(255,255,255,1)] transition-all duration-300">
      <div class="text-center">
        <h2 class="text-3xl font-extrabold text-black dark:text-white">Forgot your password?</h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-zinc-400">
          Enter your email and we'll send you a reset link.
          Or
          <router-link to="/login" class="font-medium text-black dark:text-white underline hover:text-gray-800 dark:hover:text-zinc-300 transition-colors">
            back to sign in
          </router-link>
        </p>
      </div>

      <!-- Success state: identical wording whether or not the email exists -->
      <div v-if="sent" class="bg-green-50 dark:bg-green-950 border-2 border-green-500 text-green-700 dark:text-green-200 p-4 rounded-xl text-sm font-medium">
        If an account with that email exists, a reset link is on its way. Check your inbox (and spam).
      </div>

      <form v-else class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div>
          <label for="email" class="block text-sm font-semibold text-black dark:text-white mb-1">Email address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            autocomplete="username"
            class="w-full px-4 py-3 border-2 border-black dark:border-zinc-700 rounded-xl text-black dark:text-white bg-white dark:bg-zinc-900 focus:outline-none focus:bg-yellow-50 dark:focus:bg-zinc-800 focus:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] dark:focus:shadow-[2px_2px_0px_0px_rgba(255,255,255,1)] transition-all"
            placeholder="you@example.com"
          />
        </div>

        <!-- Error only for network/validation failures, never "email not found" -->
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
            Send reset link
          </button>
        </div>
      </form>

      <div v-if="sent" class="text-center">
        <router-link
          to="/login"
          class="inline-block py-3 px-6 border-2 border-black dark:border-white text-sm font-bold rounded-xl text-black dark:text-white bg-white dark:bg-zinc-900 hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] dark:hover:shadow-[4px_4px_0px_0px_rgba(255,255,255,1)] active:translate-x-0.5 active:translate-y-0.5 transition-all"
        >
          Return to sign in
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { authAPI } from '@/services/api'

const email = ref('')
const loading = ref(false)
const sent = ref(false)
const error = ref(null)

async function handleSubmit() {
  if (!email.value) return

  loading.value = true
  error.value = null
  try {
    // The API answers 204 for known AND unknown emails — the UI can't and
    // shouldn't reveal which addresses are registered.
    await authAPI.forgotPassword(email.value)
    sent.value = true
  } catch (err) {
    console.error('Forgot password error:', err)
    error.value = err.response?.data?.detail || 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
