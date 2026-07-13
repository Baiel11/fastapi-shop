// frontend/src/services/api.js
/**
 * API service for interacting with the backend.
 * Centralizes all HTTP requests to the FastAPI server.
 * Uses axios for performing requests.
 */

import axios from 'axios'

// Base API URL from environment variables or default value
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

// Create axios instance with default settings
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Automatically add JWT token to every request if saved in localStorage
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * API methods for authentication
 */
export const authAPI = {
  register(email, username, password) {
    return apiClient.post('/auth/register', { email, username, password })
  },
  login(email, password) {
    return apiClient.post('/auth/login', { email, password })
  },
  getMe() {
    return apiClient.get('/auth/me')
  }
}

/**
 * API methods for products
 */
export const productsAPI = {
  /**
   * Get all products with pagination parameters
   */
  getAll(params) {
    return apiClient.get('/products', { params })
  },

  /**
   * Get product by ID
   */
  getById(id) {
    return apiClient.get(`/products/${id}`)
  },

  /**
   * Get products by category with pagination parameters
   */
  getByCategory(categoryId, params) {
    return apiClient.get(`/products/category/${categoryId}`, { params })
  },
}

/**
 * API methods for categories
 */
export const categoriesAPI = {
  /**
   * Get all categories
   */
  getAll() {
    return apiClient.get('/categories')
  },

  /**
   * Get category by ID
   */
  getById(id) {
    return apiClient.get(`/categories/${id}`)
  },
}

/**
 * API methods for shopping cart
 */
export const cartAPI = {
  addItem(item) {
    return apiClient.post('/cart/add', item)
  },
  getCart() {
    return apiClient.get('/cart')
  },
  updateItem(item) {
    return apiClient.put('/cart/update', item)
  },
  removeItem(productId) {
    return apiClient.delete(`/cart/remove/${productId}`)
  },
}

export default apiClient