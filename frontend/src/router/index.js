// frontend/src/router/index.js
/**
 * Vue Router configuration.
 * Defines application routes and maps them to views.
 */

import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import ProductDetailPage from '@/views/ProductDetailPage.vue'
import CartPage from '@/views/CartPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import NotFoundPage from '@/views/NotFoundPage.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
      meta: { title: 'Shop - Home' },
    },
    {
      path: '/product/:id',
      name: 'product-detail',
      component: ProductDetailPage,
      meta: { title: 'Product Details' },
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartPage,
      meta: {
        title: 'Shopping Cart',
        requiresAuth: true, // Redirect to login if not authenticated
      },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: {
        title: 'Sign In',
        guestOnly: true,
      },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage,
      meta: {
        title: 'Create Account',
        guestOnly: true,
      },
    },
    {
      path: '/admin',
      component: () => import('@/components/admin/AdminLayout.vue'),
      meta: { requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: () => import('@/views/admin/Dashboard.vue'),
          meta: { title: 'Admin - Dashboard' },
        },
        {
          path: 'products',
          name: 'admin-products',
          component: () => import('@/views/admin/Products.vue'),
          meta: { title: 'Admin - Products' },
        },
        {
          path: 'categories',
          name: 'admin-categories',
          component: () => import('@/views/admin/Categories.vue'),
          meta: { title: 'Admin - Categories' },
        },
        {
          path: 'users',
          name: 'admin-users',
          component: () => import('@/views/admin/Users.vue'),
          meta: { title: 'Admin - Users' },
        },
      ],
    },
    {
      // Catch all unmatched routes → 404 page
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundPage,
      meta: { title: 'Page Not Found' },
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  },
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'FastAPI Shop'

  const authStore = useAuthStore()

  // If the user is already logged in, prevent accessing login/register pages
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return next({ name: 'home' })
  }

  // If the route requires admin status, check role
  if (to.meta.requiresAdmin) {
    if (!authStore.isAuthenticated) {
      return next({ name: 'login', query: { next: to.fullPath } })
    }
    if (!authStore.isAdmin) {
      return next({ name: 'not-found' })
    }
  }

  // If the route requires auth and the user is not logged in,
  // redirect to login and save the intended URL in the query string
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'login', query: { next: to.fullPath } })
  }

  next()
})

export default router