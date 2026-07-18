<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Categories Management</h2>
        <p class="text-sm text-gray-500 dark:text-zinc-400 mt-1">Add, update, or remove product categories.</p>
      </div>
      <button
        @click="openCreateModal"
        class="flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition-all duration-200 shadow-sm shadow-indigo-100 dark:shadow-none"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        New Category
      </button>
    </div>

    <!-- Main Content Area -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6 items-start">
      <!-- Categories Table List (Takes 2/3 space on big screens) -->
      <div class="xl:col-span-2 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border border-gray-100 dark:border-zinc-800 rounded-2xl overflow-hidden shadow-sm">
        <div class="p-5 border-b border-gray-100 dark:border-zinc-800 flex items-center justify-between">
          <h3 class="font-bold text-gray-800 dark:text-zinc-200">All Categories</h3>
          <!-- Filter Search -->
          <div class="relative w-64">
            <span class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search categories..."
              class="w-full pl-9 pr-4 py-2 border border-gray-200 dark:border-zinc-800 rounded-xl bg-gray-50 dark:bg-zinc-900/50 text-sm text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
            />
          </div>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-gray-50 dark:bg-zinc-900/50 text-xs font-bold text-gray-400 dark:text-zinc-500 border-b border-gray-100 dark:border-zinc-800 uppercase tracking-wider">
                <th class="py-4 px-6">ID</th>
                <th class="py-4 px-6">Category Name</th>
                <th class="py-4 px-6">Slug</th>
                <th class="py-4 px-6 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-zinc-800 text-sm text-gray-700 dark:text-zinc-300">
              <tr v-if="filteredCategories.length === 0">
                <td colspan="4" class="py-12 text-center text-gray-400">
                  No categories found.
                </td>
              </tr>
              <tr
                v-else
                v-for="cat in filteredCategories"
                :key="cat.id"
                class="hover:bg-gray-50/50 dark:hover:bg-zinc-900/30 transition-colors duration-150"
              >
                <td class="py-4 px-6 font-mono text-xs text-gray-400">{{ cat.id }}</td>
                <td class="py-4 px-6 font-semibold text-gray-900 dark:text-white">{{ cat.name }}</td>
                <td class="py-4 px-6 font-mono text-xs text-indigo-600 dark:text-indigo-400 bg-indigo-50/30 dark:bg-indigo-950/20 px-2 py-1 rounded-md inline-block my-3">
                  {{ cat.slug }}
                </td>
                <td class="py-4 px-6 text-right">
                  <div class="inline-flex gap-2">
                    <!-- Edit -->
                    <button
                      @click="openEditModal(cat)"
                      class="p-2 text-gray-500 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-gray-100 dark:hover:bg-zinc-900 rounded-lg transition-colors"
                      title="Edit Category"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <!-- Delete -->
                    <button
                      @click="confirmDelete(cat)"
                      class="p-2 text-gray-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-gray-100 dark:hover:bg-zinc-900 rounded-lg transition-colors"
                      title="Delete Category"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Add/Edit form Card (Right Column) -->
      <div
        v-if="isModalOpen"
        class="bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border border-gray-100 dark:border-zinc-800 p-6 rounded-2xl shadow-sm transition-all duration-300"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-lg text-gray-900 dark:text-white">
            {{ isEditing ? 'Edit Category' : 'Create Category' }}
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
              Category Name
            </label>
            <input
              v-model="form.name"
              @input="handleNameInput"
              type="text"
              required
              placeholder="e.g. Smart Phones"
              class="w-full px-4 py-2.5 border border-gray-200 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-900/50 rounded-xl text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-sm"
            />
          </div>

          <!-- Slug -->
          <div>
            <label class="block text-xs font-bold text-gray-400 dark:text-zinc-500 uppercase tracking-wider mb-2">
              Slug (URL slug)
            </label>
            <input
              v-model="form.slug"
              @input="isSlugManuallyEdited = true"
              type="text"
              required
              placeholder="e.g. smart-phones"
              class="w-full px-4 py-2.5 border border-gray-200 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-900/50 rounded-xl text-gray-900 dark:text-white font-mono placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-sm"
            />
            <p class="text-xs text-gray-400 mt-1.5">Slug format: lowercase words separated by hyphens.</p>
          </div>

          <!-- Actions -->
          <div class="flex gap-3 pt-2">
            <button
              type="button"
              @click="closeModal"
              class="w-1/2 py-2.5 text-sm font-semibold text-gray-700 dark:text-zinc-300 bg-gray-100 dark:bg-zinc-900 hover:bg-gray-200 dark:hover:bg-zinc-850 rounded-xl transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="saving"
              class="w-1/2 py-2.5 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition disabled:opacity-50"
            >
              {{ saving ? 'Saving...' : 'Save' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Custom Delete Confirmation Alert Modal -->
    <div
      v-if="categoryToDelete"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
    >
      <div class="bg-white dark:bg-zinc-950 border border-gray-200 dark:border-zinc-800 p-6 rounded-2xl max-w-sm w-full shadow-xl">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">Delete Category?</h3>
        <p class="text-sm text-gray-500 dark:text-zinc-400 mb-6">
          Are you sure you want to delete category <strong>{{ categoryToDelete.name }}</strong>? This action is permanent.
        </p>
        <div class="flex gap-3">
          <button
            @click="categoryToDelete = null"
            class="w-1/2 py-2.5 text-sm font-semibold text-gray-700 dark:text-zinc-300 bg-gray-100 dark:bg-zinc-900 hover:bg-gray-200 rounded-xl"
          >
            Cancel
          </button>
          <button
            @click="handleDelete"
            class="w-1/2 py-2.5 text-sm font-semibold text-white bg-red-600 hover:bg-red-700 rounded-xl"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { categoriesAPI, adminAPI } from '@/services/api'
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()

const categories = ref([])
const searchQuery = ref('')
const isModalOpen = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const isSlugManuallyEdited = ref(false)

const form = ref({
  id: null,
  name: '',
  slug: ''
})

const categoryToDelete = ref(null)

// Client-side search filtration
const filteredCategories = computed(() => {
  if (!searchQuery.value) return categories.value
  const q = searchQuery.value.toLowerCase().trim()
  return categories.value.filter(c =>
    c.name.toLowerCase().includes(q) ||
    c.slug.toLowerCase().includes(q)
  )
})

// Fetch all categories
const fetchCategories = async () => {
  try {
    const response = await categoriesAPI.getAll()
    categories.value = response.data
  } catch (error) {
    console.error('Failed to load categories:', error)
    toastStore.error('Could not load categories.')
  }
}

onMounted(fetchCategories)

// Auto Slug Generation: matches a-z0-9 with hyphens
const generateSlug = (val) => {
  return val
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')     // replace spaces & non-alphanumeric chars with -
    .replace(/(^-|-$)/g, '')         // remove leading/trailing hyphens
}

const handleNameInput = () => {
  if (!isSlugManuallyEdited.value) {
    form.value.slug = generateSlug(form.value.name)
  }
}

const openCreateModal = () => {
  isEditing.value = false
  isSlugManuallyEdited.value = false
  form.value = { id: null, name: '', slug: '' }
  isModalOpen.value = true
}

const openEditModal = (cat) => {
  isEditing.value = true
  isSlugManuallyEdited.value = true
  form.value = { ...cat }
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

const handleSubmit = async () => {
  // Validate slug pattern before sending to backend
  const slugPattern = /^[a-z0-9]+(-[a-z0-9]+)*$/
  if (!slugPattern.test(form.value.slug)) {
    toastStore.error('Slug must contain only lowercase letters, numbers, and hyphens.')
    return
  }

  saving.value = true
  try {
    if (isEditing.value) {
      await adminAPI.updateCategory(form.value.id, {
        name: form.value.name,
        slug: form.value.slug
      })
      toastStore.success('Category updated successfully!')
    } else {
      await adminAPI.createCategory({
        name: form.value.name,
        slug: form.value.slug
      })
      toastStore.success('Category created successfully!')
    }
    closeModal()
    await fetchCategories()
  } catch (error) {
    console.error('Submit category error:', error)
    toastStore.error(error.response?.data?.detail || 'Failed to save category.')
  } finally {
    saving.value = false
  }
}

const confirmDelete = (cat) => {
  categoryToDelete.value = cat
}

const handleDelete = async () => {
  if (!categoryToDelete.value) return
  try {
    await adminAPI.deleteCategory(categoryToDelete.value.id)
    toastStore.success(`Category "${categoryToDelete.value.name}" deleted.`)
    categoryToDelete.value = null
    await fetchCategories()
  } catch (error) {
    console.error('Delete category error:', error)
    toastStore.error(error.response?.data?.detail || 'Could not delete category.')
    categoryToDelete.value = null
  }
}
</script>
