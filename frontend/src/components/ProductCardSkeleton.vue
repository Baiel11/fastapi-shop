<!-- frontend/src/components/ProductCardSkeleton.vue -->
<!--
  Skeleton loading placeholder for ProductCard.
  Provides a pulsing preview of card layout during loading transitions.
-->

<template>
  <div
    class="border-2 border-gray-200 rounded-lg overflow-hidden animate-pulse bg-white flex flex-col h-full"
  >
    <!-- Image placeholder -->
    <div class="aspect-square bg-gray-100"></div>

    <!-- Details placeholders -->
    <div class="p-4 flex flex-col flex-grow">
      <!-- Category -->
      <div class="h-3 bg-gray-100 rounded w-1/4 mb-2"></div>
      
      <!-- Name -->
      <div class="h-5 bg-gray-200 rounded w-3/4 mb-1"></div>
      <div class="h-5 bg-gray-200 rounded w-1/2 mb-3"></div>
      
      <!-- Price -->
      <div class="h-8 bg-gray-200 rounded w-1/3 mt-auto mb-4"></div>
      
      <!-- Add to Cart Button -->
      <div class="h-12 bg-gray-200 rounded w-full"></div>
    </div>
  </div>
</template>
