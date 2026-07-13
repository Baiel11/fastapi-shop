// frontend/src/stores/products.js
/**
 * Pinia store for managing product state.
 * Stores product list, filtering, pagination, and loading state.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { productsAPI, categoriesAPI } from '@/services/api'

export const useProductsStore = defineStore('products', () => {
  // State
  const products = ref([])
  const categories = ref([])
  const selectedCategory = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Pagination State
  const currentPage = ref(1)
  const pageSize = ref(9) // 9 items per page fits a 3-column layout nicely
  const totalProducts = ref(0)
  const totalPages = ref(1)

  // Getters
  // The API performs filtering, so filteredProducts is just the current page's items.
  const filteredProducts = computed(() => products.value)
  const productsCount = computed(() => totalProducts.value)

  // Actions
  /**
   * Load products from the server considering selected category and page
   */
  async function fetchProducts() {
    loading.value = true
    error.value = null
    try {
      const params = {
        page: currentPage.value,
        size: pageSize.value,
      }

      let response
      if (selectedCategory.value) {
        response = await productsAPI.getByCategory(selectedCategory.value, params)
      } else {
        response = await productsAPI.getAll(params)
      }

      // Update state with response details
      products.value = response.data.items
      totalProducts.value = response.data.total
      totalPages.value = response.data.pages
    } catch (err) {
      error.value = 'Failed to load products'
      console.error('Error fetching products:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * Load product by ID
   */
  async function fetchProductById(id) {
    loading.value = true
    error.value = null
    try {
      const response = await productsAPI.getById(id)
      return response.data
    } catch (err) {
      error.value = 'Failed to load product'
      console.error('Error fetching product:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Load all categories
   */
  async function fetchCategories() {
    try {
      const response = await categoriesAPI.getAll()
      categories.value = response.data
    } catch (err) {
      console.error('Error fetching categories:', err)
    }
  }

  /**
   * Set category filter and load products
   */
  async function setCategory(categoryId) {
    selectedCategory.value = categoryId
    currentPage.value = 1 // Reset to first page
    await fetchProducts()
  }

  /**
   * Clear category filter and load products
   */
  async function clearCategoryFilter() {
    selectedCategory.value = null
    currentPage.value = 1 // Reset to first page
    await fetchProducts()
  }

  /**
   * Navigate to a specific page
   */
  async function setPage(page) {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
      await fetchProducts()
    }
  }

  return {
    // State
    products,
    categories,
    selectedCategory,
    loading,
    error,
    currentPage,
    pageSize,
    totalProducts,
    totalPages,
    // Getters
    filteredProducts,
    productsCount,
    // Actions
    fetchProducts,
    fetchProductById,
    fetchCategories,
    setCategory,
    clearCategoryFilter,
    setPage,
  }
})