/**
 * Global toast notification store.
 * Any component can call toastStore.success() / .error() / .info()
 * without prop drilling or event emitting.
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'

let nextId = 0

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])

  function add(message, type = 'success', duration = 3500) {
    const id = nextId++
    toasts.value.push({ id, message, type })
    setTimeout(() => remove(id), duration)
  }

  function remove(id) {
    const idx = toasts.value.findIndex((t) => t.id === id)
    if (idx !== -1) toasts.value.splice(idx, 1)
  }

  const success = (message) => add(message, 'success')
  const error = (message) => add(message, 'error', 5000)
  const info = (message) => add(message, 'info')

  return { toasts, success, error, info, remove }
})
