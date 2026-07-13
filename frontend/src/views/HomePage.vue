<!-- frontend/src/views/HomePage.vue -->
<!--
  Main page with product catalog.
  Displays the list of products and category filter.
-->

<template>
  <div class="min-h-screen bg-white">
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-extrabold text-black mb-2">Product Catalog</h1>
        <p class="text-gray-500">Discover our amazing products</p>
      </div>

      <div class="flex gap-8">
        <!-- Sidebar with filter -->
        <aside class="w-64 flex-shrink-0 sticky top-24 self-start">
          <CategoryFilter />
        </aside>

        <!-- Main content -->
        <main class="flex-grow">
          <!-- Filtering info -->
          <div class="mb-6 flex items-center justify-between">
            <p class="text-gray-700">
              <span class="font-bold">{{ productsStore.productsCount }}</span>
              {{ productsStore.productsCount === 1 ? 'product' : 'products' }} found
            </p>

            <!-- Clear filter button -->
            <button
              v-if="productsStore.selectedCategory"
              @click="productsStore.clearCategoryFilter"
              class="text-sm text-gray-500 hover:text-black transition-colors font-medium"
            >
              Clear filter
            </button>
          </div>

          <Transition name="fade" mode="out-in">
            <!-- Loading state with Skeleton Cards -->
            <div v-if="productsStore.loading" key="loading">
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <ProductCardSkeleton v-for="i in 9" :key="i" />
              </div>
            </div>

            <!-- Error -->
            <div v-else-if="productsStore.error" class="text-center py-12" key="error">
              <p class="text-red-600 font-medium">{{ productsStore.error }}</p>
            </div>

            <!-- Product list -->
            <div v-else-if="productsStore.filteredProducts.length > 0" key="products">
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <ProductCard
                  v-for="product in productsStore.filteredProducts"
                  :key="product.id"
                  :product="product"
                />
              </div>

              <!-- Modern Numbered Pagination -->
              <div v-if="productsStore.totalPages > 1" class="mt-12 flex justify-center items-center space-x-2">
                <!-- Previous button -->
                <button
                  @click="productsStore.setPage(productsStore.currentPage - 1)"
                  :disabled="productsStore.currentPage === 1"
                  class="p-2.5 border-2 border-black text-black font-bold rounded-lg transition-colors hover:bg-black hover:text-white disabled:opacity-30 disabled:hover:bg-white disabled:hover:text-black cursor-pointer mr-2 flex items-center justify-center"
                  aria-label="Previous page"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
                  </svg>
                </button>

                <!-- Page numbers -->
                <template v-for="(page, idx) in visiblePages" :key="idx">
                  <span
                    v-if="page === '...'"
                    class="px-3 py-2 text-gray-500 font-bold select-none"
                  >
                    ...
                  </span>
                  <button
                    v-else
                    @click="productsStore.setPage(page)"
                    :class="[
                      'px-4 py-2 border-2 text-sm font-bold rounded-lg transition-colors cursor-pointer select-none',
                      productsStore.currentPage === page
                        ? 'bg-black border-black text-white'
                        : 'border-gray-200 text-black hover:border-black'
                    ]"
                  >
                    {{ page }}
                  </button>
                </template>

                <!-- Next button -->
                <button
                  @click="productsStore.setPage(productsStore.currentPage + 1)"
                  :disabled="productsStore.currentPage === productsStore.totalPages"
                  class="p-2.5 border-2 border-black text-black font-bold rounded-lg transition-colors hover:bg-black hover:text-white disabled:opacity-30 disabled:hover:bg-white disabled:hover:text-black cursor-pointer ml-2 flex items-center justify-center"
                  aria-label="Next page"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Empty state -->
            <div v-else class="text-center py-12" key="empty">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-16 w-16 mx-auto text-gray-400 mb-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2 2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
                />
              </svg>
              <p class="text-gray-500 text-lg font-medium">No products found</p>
              <button
                @click="productsStore.clearCategoryFilter"
                class="mt-4 text-black hover:underline font-medium"
              >
                View all products
              </button>
            </div>
          </Transition>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, watch } from 'vue'
import { useProductsStore } from '@/stores/products'
import ProductCard from '@/components/ProductCard.vue'
import ProductCardSkeleton from '@/components/ProductCardSkeleton.vue'
import CategoryFilter from '@/components/CategoryFilter.vue'

const productsStore = useProductsStore()

/**
 * Calculates page numbers to display in modern numbered pagination.
 */
const visiblePages = computed(() => {
  const current = productsStore.currentPage
  const total = productsStore.totalPages

  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  const pages = []
  pages.push(1)

  if (current > 3) {
    pages.push('...')
  }

  const start = Math.max(2, current - 1)
  const end = Math.min(total - 1, current + 1)
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  if (current < total - 2) {
    pages.push('...')
  }

  pages.push(total)
  return pages
})

/**
 * Reactively scrolls the window back to the top when the page changes.
 * Kept in the component layer as scrolling is a visual UI concern.
 */
watch(
  () => productsStore.currentPage,
  () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
)

/**
 * Load data when the component is mounted
 */
onMounted(async () => {
  await Promise.all([productsStore.fetchProducts(), productsStore.fetchCategories()])
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>