// frontend/src/stores/cart.js
import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { cartAPI } from '@/services/api'
import { useAuthStore } from './auth'

export const useCartStore = defineStore('cart', () => {
  const authStore = useAuthStore()

  // State
  const cartDetails = ref(null)
  const loading = ref(false)

  // Getters
  const itemsCount = computed(() => {
    return cartDetails.value?.items_count || 0
  })

  const totalPrice = computed(() => {
    return cartDetails.value?.total || 0
  })

  const hasItems = computed(() => {
    return (cartDetails.value?.items || []).length > 0
  })

  // Actions
  /**
   * Fetch cart details from the backend DB
   */
  async function fetchCartDetails() {
    if (!authStore.isAuthenticated) {
      cartDetails.value = null
      return
    }

    loading.value = true
    try {
      const response = await cartAPI.getCart()
      cartDetails.value = response.data
    } catch (err) {
      console.error('Error fetching cart details:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * Add item to cart
   */
  async function addToCart(productId, quantity = 1) {
    try {
      const response = await cartAPI.addItem({ product_id: productId, quantity })
      cartDetails.value = response.data
      return true
    } catch (err) {
      console.error('Error adding to cart:', err)
      return false
    }
  }

  /**
   * Update item quantity
   */
  async function updateQuantity(productId, quantity) {
    if (quantity <= 0) {
      return removeFromCart(productId)
    }

    try {
      const response = await cartAPI.updateItem({ product_id: productId, quantity })
      cartDetails.value = response.data
      return true
    } catch (err) {
      console.error('Error updating cart:', err)
      return false
    }
  }

  /**
   * Remove item from cart
   */
  async function removeFromCart(productId) {
    try {
      const response = await cartAPI.removeItem(productId)
      cartDetails.value = response.data
      return true
    } catch (err) {
      console.error('Error removing from cart:', err)
      return false
    }
  }

  /**
   * Reset local cart reference
   */
  function clearCart() {
    cartDetails.value = null
  }

  // Reactively fetch cart whenever auth state changes (login / logout)
  watch(
    () => authStore.isAuthenticated,
    (isAuth) => {
      if (isAuth) {
        fetchCartDetails()
      } else {
        clearCart()
      }
    },
    { immediate: true }
  )

  return {
    cartDetails,
    loading,
    itemsCount,
    totalPrice,
    hasItems,
    fetchCartDetails,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
  }
})
