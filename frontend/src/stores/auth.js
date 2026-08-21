import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  authAPI,
  getAccessToken,
  storeAccessToken,
  clearTokens,
  onTokensRefreshed,
} from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // The access token is read from storage so a page reload keeps the session.
  // The refresh token lives in an HttpOnly cookie managed by the backend.
  const token = ref(getAccessToken())
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  // Keep the in-memory ref in sync when the interceptor rotates the access token.
  onTokensRefreshed((accessToken) => {
    token.value = accessToken
  })

  async function initAuth() {
    if (token.value && !user.value) {
      loading.value = true
      try {
        const response = await authAPI.getMe()
        user.value = response.data
      } catch (err) {
        // getMe already attempted a refresh via the interceptor; if it still
        // failed the session is genuinely dead, so drop local state.
        console.error('Failed to init auth user:', err)
        clearLocalSession()
      } finally {
        loading.value = false
      }
    }
  }

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const response = await authAPI.login(email, password)
      const accessToken = response.data.access_token
      storeAccessToken(accessToken)
      token.value = accessToken
      // The refresh token arrived as an HttpOnly cookie — nothing to store here.

      // Fetch user details immediately after login
      const userResponse = await authAPI.getMe()
      user.value = userResponse.data
      return true
    } catch (err) {
      console.error('Login error:', err)
      error.value = err.response?.data?.detail || 'Invalid email or password'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(email, username, password) {
    loading.value = true
    error.value = null
    try {
      await authAPI.register(email, username, password)
      // Auto login user after registration
      return await login(email, password)
    } catch (err) {
      console.error('Registration error:', err)
      error.value = err.response?.data?.detail || 'Registration failed'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * User-initiated logout: revoke the current refresh token server-side
   * (sent via cookie), then clear local state. Best-effort — a network
   * error shouldn't strand the user in a "still logged in" UI, since we
   * clear locally regardless.
   */
  async function logout() {
    try {
      await authAPI.logout()
    } catch (err) {
      console.error('Failed to revoke refresh token on logout:', err)
    }
    clearLocalSession()
  }

  /**
   * Revoke every active session for this user server-side, then clear locally.
   */
  async function logoutAll() {
    try {
      await authAPI.logoutAll()
    } catch (err) {
      console.error('Failed to revoke all sessions:', err)
    }
    clearLocalSession()
  }

  /**
   * Invoked when the interceptor determines the session can no longer be
   * refreshed (e.g. revoked/expired refresh cookie). No API call here — the
   * backend already rejected the token.
   */
  function handleSessionExpired() {
    clearLocalSession()
  }

  function clearLocalSession() {
    clearTokens()
    token.value = null
    user.value = null
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    initAuth,
    login,
    register,
    logout,
    logoutAll,
    handleSessionExpired,
  }
})
