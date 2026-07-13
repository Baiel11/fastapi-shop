<!-- frontend/src/views/ProductDetailPage.vue -->
<!--
  Product detail page.
  Displays full product information with add-to-cart option.
-->

<template>
  <div class="min-h-screen bg-white dark:bg-zinc-950 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- "Back" button -->
      <button
        @click="router.push('/')"
        class="flex items-center text-gray-600 dark:text-zinc-400 hover:text-black dark:hover:text-white transition-colors mb-8 font-medium text-lg cursor-pointer"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6 mr-2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 19l-7-7 7-7"
          />
        </svg>
        Back to catalog
      </button>

      <!-- Loading state -->
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-14 w-14 border-b-4 border-black dark:border-white"></div>
        <p class="mt-4 text-lg text-gray-500 dark:text-zinc-400">Loading product...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-16">
        <p class="text-red-600 dark:text-red-400 text-lg font-medium">{{ error }}</p>
        <button
          @click="router.push('/')"
          class="mt-6 bg-black dark:bg-white text-white dark:text-black py-3 px-8 text-lg font-semibold rounded-none hover:bg-gray-900 dark:hover:bg-zinc-100 transition-colors cursor-pointer"
        >
          Return to catalog
        </button>
      </div>

      <!-- Detailed product info -->
      <div
        v-else-if="product"
        class="bg-white dark:bg-zinc-900 border-2 border-gray-100 dark:border-zinc-800 rounded-none shadow-sm overflow-hidden transition-all duration-300"
      >
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 p-8">
          <!-- Image -->
          <div class="aspect-square overflow-hidden rounded-none bg-gray-50 dark:bg-zinc-800">
            <img
              :src="product.image_url || PLACEHOLDER_IMAGE"
              :alt="product.name"
              class="w-full h-full object-cover"
              @error="handleImageError"
            />
          </div>

          <!-- Information -->
          <div class="flex flex-col">
            <!-- Category -->
            <div class="text-sm text-gray-500 dark:text-zinc-400 uppercase tracking-wider mb-3 font-medium">
              {{ product.category?.name }}
            </div>

            <!-- Title -->
            <h1 class="text-3xl sm:text-4xl font-extrabold text-black dark:text-white mb-4">
              {{ product.name }}
            </h1>

            <!-- Price -->
            <div class="text-2xl sm:text-3xl font-bold text-black dark:text-white mb-6">
              ${{ formatPrice(product.price) }}
            </div>

            <!-- Description -->
            <div class="mb-8">
              <h2 class="text-xl font-bold text-black dark:text-white mb-3">Description</h2>
              <p class="text-gray-600 dark:text-zinc-300 leading-relaxed">
                {{ product.description || 'No description available.' }}
              </p>
            </div>

            <!-- Add to cart button -->
            <div class="mt-auto">
              <button
                @click="handleAddToCart"
                :disabled="adding"
                class="w-full bg-black dark:bg-white text-white dark:text-black border-2 border-black dark:border-white py-4 px-6 text-lg font-semibold rounded-none hover:bg-white dark:hover:bg-zinc-900 hover:text-black dark:hover:text-white transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white focus:ring-offset-2 dark:focus:ring-offset-zinc-900 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {{ adding ? 'Adding to cart...' : 'Add to Cart' }}
              </button>
            </div>

            <!-- Additional info -->
            <div class="mt-8 pt-6 border-t-2 border-gray-100 dark:border-zinc-800">
              <p class="text-sm text-gray-500 dark:text-zinc-400">Product ID: {{ product.id }}</p>
              <p class="text-sm text-gray-500 dark:text-zinc-400">Added: {{ formatDate(product.created_at) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductsStore } from '@/stores/products'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import { formatPrice, formatDate, PLACEHOLDER_IMAGE } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const productsStore = useProductsStore()
const cartStore = useCartStore()
const authStore = useAuthStore()
const toastStore = useToastStore()

// State
const product = ref(null)
const loading = ref(false)
const error = ref(null)
const adding = ref(false)

/**
 * Loads product data by ID from the route param.
 */
async function loadProduct() {
  loading.value = true
  error.value = null

  try {
    const productId = parseInt(route.params.id)
    product.value = await productsStore.fetchProductById(productId)
  } catch (err) {
    error.value = 'Product not found'
    console.error('Error loading product:', err)
  } finally {
    loading.value = false
  }
}

/**
 * Adds the product to cart.
 * Redirects unauthenticated users to login, preserving the current page
 * as the post-login redirect destination.
 */
async function handleAddToCart() {
  if (!authStore.isAuthenticated) {
    toastStore.info('Please sign in to add products to your cart.')
    router.push({ name: 'login', query: { next: route.fullPath } })
    return
  }

  adding.value = true
  const success = await cartStore.addToCart(product.value.id, 1)

  if (success) {
    toastStore.success(`"${product.value.name}" added to cart!`)
  } else {
    toastStore.error('Could not add product to cart. Please try again.')
  }

  adding.value = false
}

/**
 * Falls back to a local SVG placeholder if the product image URL fails.
 */
function handleImageError(event) {
  event.target.src = PLACEHOLDER_IMAGE
}

onMounted(() => {
  loadProduct()
})
</script>