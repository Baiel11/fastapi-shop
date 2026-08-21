// frontend/src/services/api.js
/**
 * API service for interacting with the backend.
 * Centralizes all HTTP requests to the FastAPI server.
 * Uses axios for performing requests.
 *
 * Auth (JWT) handling lives here so that every request automatically:
 *  - attaches the current access token, and
 *  - transparently rotates the session via `/auth/refresh` when the
 *    access token expires (401), retrying the original request once.
 *
 * The refresh token never touches JS: it lives in an HttpOnly cookie that
 * the browser attaches to /auth/* calls on its own. A refresh that can no
 * longer be exchanged ends the session.
 */

import axios from 'axios'

// Base API URL from environment variables or default value
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

// Single source of truth for how the access token is persisted.
// (The refresh token is server-set HttpOnly cookie territory.)
const TOKEN_KEY = 'auth_token'

export function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function storeAccessToken(accessToken) {
  if (accessToken) {
    localStorage.setItem(TOKEN_KEY, accessToken)
  } else {
    localStorage.removeItem(TOKEN_KEY)
  }
}

export function clearTokens() {
  localStorage.removeItem(TOKEN_KEY)
}

// Create axios instance with default settings.
// withCredentials lets the browser send/receive the refresh-token cookie
// on cross-origin calls (localhost:5173 -> localhost:8000).
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Automatically add the current access token to every request.
apiClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// ─────────────────────────────────────────────────────────────
// Session-expired notification.
// `api.js` must not import the Pinia store (circular dependency),
// so main.js registers a handler that clears auth state + redirects.
// ─────────────────────────────────────────────────────────────
let sessionExpiredHandler = null
let sessionExpiredNotified = false

export function onSessionExpired(handler) {
  sessionExpiredHandler = handler
}

function notifySessionExpired() {
  if (sessionExpiredNotified) return
  sessionExpiredNotified = true
  if (sessionExpiredHandler) sessionExpiredHandler()
}

// ─────────────────────────────────────────────────────────────
// Token-refresh notification, so the store keeps its ref in sync.
// ─────────────────────────────────────────────────────────────
let tokensRefreshedHandler = null

export function onTokensRefreshed(handler) {
  tokensRefreshedHandler = handler
}

function notifyTokensRefreshed(accessToken) {
  if (tokensRefreshedHandler) tokensRefreshedHandler(accessToken)
}

// Single-flight refresh: concurrent 401s share one `/auth/refresh` call
// instead of each firing its own request (which would rotate the token
// multiple times and invalidate the earlier rotations).
let refreshPromise = null

async function refreshAccessToken() {
  // The current refresh token rides along in its HttpOnly cookie —
  // nothing to read in JS. A missing/expired/revoked cookie simply 401s.
  const { data } = await apiClient.post('/auth/refresh')
  storeAccessToken(data.access_token)
  sessionExpiredNotified = false // a successful refresh means the session is alive again
  notifyTokensRefreshed(data.access_token)
  return data.access_token
}

// On a 401 that is not the refresh call itself and has not been retried yet,
// rotate the token pair once and replay the original request. If rotation
// fails (revoked/expired refresh token) or the retry is rejected again
// (e.g. account now blocked), the session is over.
// A 401 on these endpoints means "credentials rejected" (or "rate limited"
// for other auth calls), NOT "your access token expired". Refreshing there
// would be wrong — e.g. a failed login must surface its error immediately.
const REFRESH_EXEMPT_PATHS = ['/auth/refresh', '/auth/login', '/auth/register']

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { response, config } = error
    const isRefreshExempt = REFRESH_EXEMPT_PATHS.some((path) => config?.url?.includes(path))

    if (response?.status === 401 && config && !config._retried && !isRefreshExempt) {
      try {
        if (!refreshPromise) {
          refreshPromise = refreshAccessToken().finally(() => {
            refreshPromise = null
          })
        }
        const newAccessToken = await refreshPromise
        config._retried = true
        config.headers.Authorization = `Bearer ${newAccessToken}`
        return await apiClient(config)
      } catch (refreshError) {
        clearTokens()
        notifySessionExpired()
        throw refreshError
      }
    }
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
  },
  refresh() {
    return apiClient.post('/auth/refresh')
  },
  logout() {
    // The refresh token arrives via cookie and gets revoked + cleared server-side.
    return apiClient.post('/auth/logout')
  },
  logoutAll() {
    return apiClient.post('/auth/logout-all')
  },
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