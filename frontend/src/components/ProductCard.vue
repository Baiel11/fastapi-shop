<!-- frontend/src/components/ProductCard.vue -->
<!--
  Product card component for display in catalog.
  Shows main product information and an add-to-cart button.
-->

<template>
  <div
    class="flex flex-col h-full bg-white border-2 border-gray-200 rounded-lg overflow-hidden hover:border-black transition-all duration-300 hover:shadow-lg"
  >
    <!-- Product image -->
    <router-link :to="`/product/${product.id}`">
      <div class="aspect-square overflow-hidden bg-gray-100">
        <img
          :src="product.image_url || PLACEHOLDER_IMAGE"
          :alt="product.name"
          class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
          @error="handleImageError"
        />
      </div>
    </router-link>

    <!-- Product info -->
    <div class="p-4 flex flex-col flex-grow">
      <!-- Category -->
      <div class="text-xs text-gray-500 uppercase tracking-wide mb-2">
        {{ product.category?.name }}
      </div>

      <!-- Product name -->
      <router-link :to="`/product/${product.id}`" class="mb-2">
        <h3 class="text-lg font-semibold text-black hover:text-gray-700 transition-colors line-clamp-2">
          {{ product.name }}
        </h3>
      </router-link>

      <!-- Price -->
      <p class="text-2xl font-bold text-black mb-4 mt-auto">${{ formatPrice(product.price) }}</p>

      <!-- Add to cart button -->
      <button
        @click="handleAddToCart"
        :disabled="adding"
        class="w-full bg-black text-white py-3 px-4 rounded-lg hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
      >
        {{ adding ? 'Adding...' : 'Add to Cart' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import { formatPrice, PLACEHOLDER_IMAGE } from '@/utils/format'

// Props
const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
})

// Stores & Router
const cartStore = useCartStore()
const authStore = useAuthStore()
const toastStore = useToastStore()
const router = useRouter()

// State
const adding = ref(false)

/**
 * Adds the product to cart.
 * Redirects unauthenticated users to the login page,
 * preserving the product detail page as the post-login redirect destination.
 */
async function handleAddToCart() {
  if (!authStore.isAuthenticated) {
    toastStore.info('Please sign in to add products to your cart.')
    router.push({ name: 'login', query: { next: `/product/${props.product.id}` } })
    return
  }

  adding.value = true
  const success = await cartStore.addToCart(props.product.id, 1)

  if (success) {
    toastStore.success(`"${props.product.name}" added to cart!`)
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
</script>