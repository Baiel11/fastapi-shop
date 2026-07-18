<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Products Catalog</h2>
        <p class="text-sm text-gray-500 dark:text-zinc-400 mt-1">Manage products, update stock details, prices and descriptions.</p>
      </div>
      <button
        @click="openCreateModal"
        class="flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition-all duration-200 shadow-sm"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        New Product
      </button>
    </div>

    <!-- Filters Header Panel -->
    <div class="bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border border-gray-100 dark:border-zinc-800 p-5 rounded-2xl flex flex-col md:flex-row gap-4 items-center justify-between shadow-sm">
      <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
        <!-- Search bar -->
        <div class="relative w-full sm:w-64">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-gray-400">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </span>
          <input
            v-model="searchQuery"
            @input="resetPaginationAndFetch"
            type="text"
            placeholder="Search by name..."
            class="w-full pl-9 pr-4 py-2 border border-gray-200 dark:border-zinc-800 rounded-xl bg-gray-50 dark:bg-zinc-900/50 text-sm text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
          />
        </div>

        <!-- Category filter -->
        <select
          v-model="selectedCategory"
          @change="resetPaginationAndFetch"
          class="px-4 py-2 border border-gray-200 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-900/50 rounded-xl text-sm text-gray-700 dark:text-zinc-300 focus:outline-none"
        >
          <option value="">All Categories</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
      </div>

      <!-- Total summary indicator -->
      <span class="text-xs text-gray-400 font-semibold uppercase tracking-wider">
        Showing {{ products.length }} of {{ totalProducts }} Products
      </span>
    </div>

    <!-- Products List Card -->
    <div class="bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border border-gray-100 dark:border-zinc-800 rounded-2xl overflow-hidden shadow-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-gray-50 dark:bg-zinc-900/50 text-xs font-bold text-gray-400 dark:text-zinc-500 border-b border-gray-100 dark:border-zinc-800 uppercase tracking-wider">
              <th class="py-4 px-6">Product</th>
              <th class="py-4 px-6">Category</th>
              <th class="py-4 px-6">Price</th>
              <th class="py-4 px-6">Status</th>
              <th class="py-4 px-6 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-zinc-800 text-sm text-gray-700 dark:text-zinc-300">
            <tr v-if="loading">
              <td colspan="5" class="py-16 text-center">
                <span class="inline-block animate-pulse text-indigo-500 font-medium">Loading catalog...</span>
              </td>
            </tr>
            <tr v-else-if="products.length === 0">
              <td colspan="5" class="py-16 text-center text-gray-400">
                No products found. Add a product to get started.
              </td>
            </tr>
            <tr
              v-else
              v-for="prod in products"
              :key="prod.id"
              class="hover:bg-gray-50/50 dark:hover:bg-zinc-900/30 transition-colors duration-150"
            >
              <!-- Info Name & Image -->
              <td class="py-4 px-6">
                <div class="flex items-center gap-3">
                  <img
                    :src="prod.image_url || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=100'"
                    alt="image"
                    class="w-10 h-10 object-cover rounded-lg border border-gray-100 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-900"
                  />
                  <div>
                    <span class="font-semibold text-gray-900 dark:text-white block">{{ prod.name }}</span>
                    <span class="text-xs text-gray-400 font-mono">ID: {{ prod.id }}</span>
                  </div>
                </div>
              </td>

              <!-- Category -->
              <td class="py-4 px-6 text-gray-600 dark:text-zinc-400">
                {{ prod.category?.name || 'Unassigned' }}
              </td>

              <!-- Price -->
              <td class="py-4 px-6 font-semibold text-indigo-600 dark:text-indigo-400">
                ${{ parseFloat(prod.price).toFixed(2) }}
              </td>

              <!-- Status (Active / Soft Deleted) -->
              <td class="py-4 px-6">
                <span
                  :class="prod.is_active ? 'bg-emerald-50 text-emerald-600 dark:bg-emerald-950/20 dark:text-emerald-400' : 'bg-red-50 text-red-600 dark:bg-red-950/20 dark:text-red-400'"
                  class="text-xs font-semibold px-2 py-0.5 rounded-full inline-block"
                >
                  {{ prod.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>

              <!-- Actions -->
              <td class="py-4 px-6 text-right">
                <div class="inline-flex gap-2">
                  <!-- Edit -->
                  <button
                    @click="openEditModal(prod)"
                    class="p-2 text-gray-500 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-gray-100 dark:hover:bg-zinc-900 rounded-lg transition-colors"
                    title="Edit Product"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <!-- Soft Delete Deactivate -->
                  <button
                    v-if="prod.is_active"
                    @click="confirmDeactivate(prod)"
                    class="p-2 text-gray-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-gray-100 dark:hover:bg-zinc-900 rounded-lg transition-colors"
                    title="Deactivate Product"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Footer -->
      <div v-if="totalPages > 1" class="p-5 border-t border-gray-100 dark:border-zinc-800 flex items-center justify-between">
        <button
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
          class="px-4 py-2 border border-gray-200 dark:border-zinc-850 hover:bg-gray-50 dark:hover:bg-zinc-900 text-sm font-semibold rounded-xl transition disabled:opacity-50"
        >
          Previous
        </button>
        <span class="text-sm text-gray-400">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
          class="px-4 py-2 border border-gray-200 dark:border-zinc-850 hover:bg-gray-50 dark:hover:bg-zinc-900 text-sm font-semibold rounded-xl transition disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>

    <!-- Create / Edit Drawer Overlay Modal -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
    >
      <div class="bg-white dark:bg-zinc-950 border border-gray-200 dark:border-zinc-800 p-6 rounded-2xl max-w-lg w-full shadow-2xl overflow-y-auto max-h-[90vh]">
        <div class="flex items-center justify-between mb-6">
          <h3 class="font-bold text-lg text-gray-900 dark:text-white">
            {{ isEditing ? 'Edit Product' : 'Add Product' }}
          </h3>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-zinc-200">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Name -->
          <div>
            <label class="block text-xs font-bold text-gray-400 dark:text-zinc-500 uppercase tracking-wider mb-2">
              Product Name (min 5 characters)
            </label>
            <input
              v-model="form.name"
              type="text"
              required
              placeholder="e.g. Wireless Headset Pro"
              class="w-full px-4 py-2.5 border border-gray-200 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-900/50 rounded-xl text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-sm"
            />
          </div>

          <!-- Category -->
          <div>
            <label class="block text-xs font-bold text-gray-400 dark:text-zinc-500 uppercase tracking-wider mb-2">
              Category
            </label>
            <select
              v-model="form.category_id"
              required
              class="w-full px-4 py-2.5 border border-gray-200 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-900/50 rounded-xl text-gray-700 dark:text-zinc-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-sm"
            >
              <option value="" disabled>Select category</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>

          <!-- Description -->
          <div>
            <label class="block text-xs font-bold text-gray-400 dark:text-zinc-500 uppercase tracking-wider mb-2">
              Description (nullable)
            </label>
            <textarea
              v-model="form.description"
              rows="3"
              placeholder="Describe the product..."
              class="w-full px-4 py-2.5 border border-gray-200 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-900/50 rounded-xl text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-sm resize-none"
            ></textarea>
          </div>

          <!-- Price -->
          <div>
            <label class="block text-xs font-bold text-gray-400 dark:text-zinc-500 uppercase tracking-wider mb-2">
              Price ($)
            </label>
            <input
              v-model="form.price"
              type="number"
              step="0.01"
              min="0.01"
              required
              placeholder="e.g. 99.99"
              class="w-full px-4 py-2.5 border border-gray-200 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-900/50 rounded-xl text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-sm font-mono"
            />
          </div>

          <!-- Image URL -->
          <div>
            <label class="block text-xs font-bold text-gray-400 dark:text-zinc-500 uppercase tracking-wider mb-2">
              Image URL (nullable)
            </label>
            <input
              v-model="form.image_url"
              type="url"
              placeholder="https://example.com/image.jpg"
              class="w-full px-4 py-2.5 border border-gray-200 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-900/50 rounded-xl text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-sm font-mono"
            />
          </div>

          <!-- Actions -->
          <div class="flex gap-3 pt-4 border-t border-gray-150 dark:border-zinc-800 mt-6">
            <button
              type="button"
              @click="closeModal"
              class="w-1/2 py-2.5 text-sm font-semibold text-gray-700 dark:text-zinc-300 bg-gray-100 dark:bg-zinc-900 hover:bg-gray-200 rounded-xl transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="saving"
              class="w-1/2 py-2.5 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition disabled:opacity-50"
            >
              {{ saving ? 'Saving...' : 'Save Product' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Soft Delete Deactivate Confirmation Alert Modal -->
    <div
      v-if="productToDeactivate"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
    >
      <div class="bg-white dark:bg-zinc-950 border border-gray-200 dark:border-zinc-800 p-6 rounded-2xl max-w-sm w-full shadow-xl">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">Deactivate Product?</h3>
        <p class="text-sm text-gray-500 dark:text-zinc-400 mb-6">
          Are you sure you want to deactivate <strong>{{ productToDeactivate.name }}</strong>? It will no longer show in the public store catalog.
        </p>
        <div class="flex gap-3">
          <button
            @click="productToDeactivate = null"
            class="w-1/2 py-2.5 text-sm font-semibold text-gray-700 dark:text-zinc-300 bg-gray-100 dark:bg-zinc-900 hover:bg-gray-200 rounded-xl"
          >
            Cancel
          </button>
          <button
            @click="handleDeactivate"
            class="w-1/2 py-2.5 text-sm font-semibold text-white bg-red-600 hover:bg-red-700 rounded-xl"
          >
            Deactivate
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { categoriesAPI, adminAPI } from '@/services/api'
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()
const route = useRoute()

// States
const products = ref([])
const categories = ref([])
const loading = ref(true)
const saving = ref(false)

const searchQuery = ref('')
const selectedCategory = ref('')

// Pagination
const currentPage = ref(1)
const totalPages = ref(1)
const totalProducts = ref(0)
const pageSize = 10

const isModalOpen = ref(false)
const isEditing = ref(false)

const form = ref({
  id: null,
  name: '',
  description: '',
  price: '',
  category_id: '',
  image_url: ''
})

const productToDeactivate = ref(null)

// Fetch categories for filtering and select dropdown
const fetchCategories = async () => {
  try {
    const res = await categoriesAPI.getAll()
    categories.value = res.data
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  }
}

// Fetch paginated products (admin listing)
const fetchProducts = async () => {
  loading.value = true
  try {
    // If a category is selected, we filter by category using customer API (since it returns paginated items for that cat),
    // otherwise we query all products via the admin paginated API.
    let response
    if (selectedCategory.value) {
      response = await categoriesAPI.getById(selectedCategory.value) // Just mock category details or let's use search filters
      // Wait, let's look at getByCategory:
      response = await adminAPI.getProducts(currentPage.value, pageSize)
      // Since admin product list fetches all, we can filter locally on client if they select a category,
      // or query backend if it supported filters. Since the backend lists all in adminAPI.getProducts,
      // we filter client-side or use public getByCategory if they select category.
      // But admin view needs to see ALL products (active and inactive), so we fetch all and filter locally:
    } else {
      response = await adminAPI.getProducts(currentPage.value, pageSize)
    }

    const data = response.data
    // Handle paginated structure
    products.value = data.items
    totalPages.value = data.pages
    totalProducts.value = data.total
  } catch (err) {
    console.error('Failed to fetch products:', err)
    toastStore.error('Could not load products.')
  } finally {
    loading.value = false
  }
}

// Client-side local filtering combining category & search query
const fetchFilteredProducts = async () => {
  // Simple paginated fetch
  await fetchProducts()
  
  // Local filtering filter by category ID and search query if selected
  if (selectedCategory.value || searchQuery.value) {
    let filtered = [...products.value]
    if (selectedCategory.value) {
      filtered = filtered.filter(p => p.category_id === parseInt(selectedCategory.value))
    }
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase().trim()
      filtered = filtered.filter(p => p.name.toLowerCase().includes(q))
    }
    products.value = filtered
  }
}

const resetPaginationAndFetch = () => {
  currentPage.value = 1
  fetchFilteredProducts()
}

const changePage = (page) => {
  currentPage.value = page
  fetchFilteredProducts()
}

onMounted(async () => {
  await fetchCategories()
  await fetchFilteredProducts()

  // Handle ?action=new deep link from dashboard quick actions
  if (route.query.action === 'new') {
    openCreateModal()
  }
})

const openCreateModal = () => {
  isEditing.value = false
  form.value = { id: null, name: '', description: '', price: '', category_id: '', image_url: '' }
  isModalOpen.value = true
}

const openEditModal = (prod) => {
  isEditing.value = true
  form.value = {
    id: prod.id,
    name: prod.name,
    description: prod.description || '',
    price: parseFloat(prod.price).toFixed(2),
    category_id: prod.category_id,
    image_url: prod.image_url || ''
  }
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

const handleSubmit = async () => {
  if (form.value.name.length < 5) {
    toastStore.error('Product name must be at least 5 characters.')
    return
  }
  if (parseFloat(form.value.price) <= 0) {
    toastStore.error('Price must be greater than 0.')
    return
  }

  saving.value = true
  try {
    const payload = {
      name: form.value.name,
      description: form.value.description || null,
      price: parseFloat(form.value.price),
      category_id: parseInt(form.value.category_id),
      image_url: form.value.image_url || null
    }

    if (isEditing.value) {
      await adminAPI.updateProduct(form.value.id, payload)
      toastStore.success('Product updated successfully!')
    } else {
      await adminAPI.createProduct(payload)
      toastStore.success('Product created successfully!')
    }
    closeModal()
    await fetchFilteredProducts()
  } catch (error) {
    console.error('Submit product error:', error)
    toastStore.error(error.response?.data?.detail || 'Failed to save product.')
  } finally {
    saving.value = false
  }
}

const confirmDeactivate = (prod) => {
  productToDeactivate.value = prod
}

const handleDeactivate = async () => {
  if (!productToDeactivate.value) return
  try {
    await adminAPI.deleteProduct(productToDeactivate.value.id)
    toastStore.success(`Product "${productToDeactivate.value.name}" deactivated.`)
    productToDeactivate.value = null
    await fetchFilteredProducts()
  } catch (error) {
    console.error('Deactivate product error:', error)
    toastStore.error(error.response?.data?.detail || 'Could not deactivate product.')
    productToDeactivate.value = null
  }
}
</script>
