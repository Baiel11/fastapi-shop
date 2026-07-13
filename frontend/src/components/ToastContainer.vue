<template>
  <!-- Teleport renders directly inside <body> so z-index always wins -->
  <teleport to="body">
    <div
      class="fixed top-6 right-6 z-[200] flex flex-col gap-3"
      style="min-width: 320px; max-width: 400px"
      aria-live="polite"
      aria-label="Notifications"
    >
      <transition-group name="toast" tag="div" class="flex flex-col gap-3">
        <div
          v-for="toast in toastStore.toasts"
          :key="toast.id"
          class="flex items-start gap-4 px-5 py-4 rounded-xl border-2 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] cursor-pointer select-none"
          :class="toastClass(toast.type)"
          role="alert"
          @click="toastStore.remove(toast.id)"
        >
          <span class="text-xl flex-shrink-0 mt-0.5">{{ toastIcon(toast.type) }}</span>
          <p class="flex-grow text-sm font-semibold leading-snug">{{ toast.message }}</p>
          <span class="text-lg opacity-50 ml-2 flex-shrink-0">✕</span>
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script setup>
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()

function toastClass(type) {
  return {
    success: 'bg-white border-black text-black',
    error: 'bg-red-50 border-red-500 text-red-800',
    info: 'bg-yellow-50 border-yellow-500 text-yellow-900',
  }[type]
}

function toastIcon(type) {
  return { success: '✓', error: '✕', info: 'ℹ' }[type]
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.35s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-move {
  transition: transform 0.3s ease;
}
</style>
