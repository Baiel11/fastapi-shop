<!-- frontend/src/components/Header.vue -->
<!--
  Header component.
  Contains logo, navigation, and shopping cart counter.
-->

<template>
  <header class="bg-white border-b-2 border-black sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex items-center justify-between h-20">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2 group">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-8 w-8 group-hover:scale-110 transition-transform"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
            />
          </svg>
          <span class="text-2xl font-bold text-black">FastAPI Shop</span>
        </router-link>

        <!-- Navigation -->
        <nav class="flex items-center space-x-6">
          <!-- Catalog link -->
          <router-link
            to="/"
            class="text-gray-700 hover:text-black transition-colors font-medium"
            active-class="text-black font-semibold"
          >
            Catalog
          </router-link>

          <!-- Cart -->
          <router-link
            to="/cart"
            class="relative flex items-center space-x-2 text-gray-700 hover:text-black transition-colors font-medium mr-2"
            active-class="text-black font-semibold"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
            <span>Cart</span>

            <!-- Items counter -->
            <span
              v-if="cartStore.itemsCount > 0"
              class="absolute -top-2 -right-2 bg-black text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center"
            >
              {{ cartStore.itemsCount }}
            </span>
          </router-link>

          <span class="h-6 w-px bg-gray-300"></span>

          <!-- Auth Links -->
          <template v-if="authStore.isAuthenticated">
            <div class="flex items-center space-x-4">
              <span class="text-sm font-semibold text-black bg-yellow-100 px-3 py-1.5 border-2 border-black rounded-lg shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
                👤 {{ authStore.user?.username || 'User' }}
              </span>
              <button
                @click="handleLogout"
                class="px-4 py-2 border-2 border-black text-sm font-bold rounded-xl text-black hover:bg-black hover:text-white transition-all active:translate-y-px"
              >
                Logout
              </button>
            </div>
          </template>
          <template v-else>
            <router-link
              to="/login"
              class="text-gray-700 hover:text-black font-medium transition-colors"
            >
              Sign In
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 bg-black text-white border-2 border-black font-bold rounded-xl hover:bg-white hover:text-black hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all active:translate-y-px"
            >
              Register
            </router-link>
          </template>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const authStore = useAuthStore()
const router = useRouter()

function handleLogout() {
  authStore.logout()
  router.push('/')
}
</script>