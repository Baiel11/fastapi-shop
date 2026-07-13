<!-- frontend/src/components/ProductCardSkeleton.vue -->
<!--
  Skeleton loading placeholder for ProductCard.
  Provides a pulsing preview of card layout during loading transitions.
-->

<template>
  <div
    class="border-2 border-gray-200 dark:border-zinc-800 rounded-lg overflow-hidden animate-pulse bg-white dark:bg-zinc-900 flex flex-col h-full"
  >
    <!-- Image placeholder -->
    <div class="aspect-square bg-gray-100 dark:bg-zinc-800"></div>

    <!-- Details placeholders -->
    <div class="p-4 flex flex-col flex-grow bg-white dark:bg-zinc-900 transition-colors duration-300">
      <!-- Category -->
      <div class="h-3 bg-gray-100 dark:bg-zinc-800 rounded w-1/4 mb-2"></div>
      
      <!-- Name -->
      <div class="h-5 bg-gray-200 dark:bg-zinc-700 rounded w-3/4 mb-1"></div>
      <div class="h-5 bg-gray-200 dark:bg-zinc-700 rounded w-1/2 mb-3"></div>
      
      <!-- Price -->
      <div class="h-8 bg-gray-200 dark:bg-zinc-700 rounded w-1/3 mt-auto mb-4"></div>
      
      <!-- Add to Cart Button -->
      <div class="h-12 bg-gray-200 dark:bg-zinc-700 rounded w-full"></div>
    </div>
  </div>
</template>
