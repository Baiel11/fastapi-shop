import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('auth_token') || null)
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin || false)

  async function initAuth() {
    if (token.value && !user.value) {
      loading.value = true
      try {
        const response = await authAPI.getMe()
        user.value = response.data
      } catch (err) {
        console.error('Failed to init auth user:', err)
        logout()
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
      localStorage.setItem('auth_token', accessToken)
      token.value = accessToken
      
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

  function logout() {
    localStorage.removeItem('auth_token')
    token.value = null
    user.value = null
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    initAuth,
    login,
    register,
    logout,
  }
})
