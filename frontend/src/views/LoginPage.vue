<template>
  <div class="min-h-[80vh] flex items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-2xl border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
      <div class="text-center">
        <h2 class="text-3xl font-extrabold text-black">Sign in to your account</h2>
        <p class="mt-2 text-sm text-gray-600">
          Or
          <router-link to="/register" class="font-medium text-black underline hover:text-gray-800 transition-colors">
            create a new account
          </router-link>
        </p>
      </div>

      <!-- Error Alert -->
      <div v-if="authStore.error" class="bg-red-50 border-2 border-red-500 text-red-700 p-4 rounded-xl text-sm font-medium">
        {{ authStore.error }}
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-semibold text-black mb-1">Email address</label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              autocomplete="username"
              class="w-full px-4 py-3 border-2 border-black rounded-xl text-black focus:outline-none focus:bg-yellow-50 focus:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label for="password" class="block text-sm font-semibold text-black mb-1">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              autocomplete="current-password"
              class="w-full px-4 py-3 border-2 border-black rounded-xl text-black focus:outline-none focus:bg-yellow-50 focus:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all"
              placeholder="••••••••"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="authStore.loading"
            class="group relative w-full flex justify-center py-3 px-4 border-2 border-black text-sm font-bold rounded-xl text-white bg-black hover:bg-white hover:text-black hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] active:translate-x-0.5 active:translate-y-0.5 transition-all disabled:opacity-50"
          >
            <span v-if="authStore.loading" class="animate-spin mr-2 h-5 w-5 border-t-2 border-r-2 border-white rounded-full text-black"></span>
            Sign in
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')

async function handleSubmit() {
  if (!email.value || !password.value) return

  const success = await authStore.login(email.value, password.value)
  if (success) {
    // Redirect back to the page the user originally tried to access,
    // or fall back to home if no redirect param is present
    const redirect = route.query.next || '/'
    router.push(redirect)
  }
}
</script>
