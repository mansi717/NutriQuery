// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeSection from '../components/HomeSection.vue'
import AboutPage from '../components/AboutPage.vue'
import Contact from '../components/ContactPage.vue'
import RecommendationSection from '../components/RecommendationSection.vue'
import FavoritePage from '../components/FavoritePage.vue'
import SignupPage from '../views/SignupPage.vue'
import LoginPage from '../views/LoginPage.vue'

const routes = [
  {
    path: '/',
    component: LoginPage
  },
  {
    path: '/signup',      
    name: 'Signup',
    component: SignupPage
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/home',
    component: HomeSection,
    meta: { requiresAuth: true }
  },
  {
    path: '/about',
    component: AboutPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/contact',
    component: Contact,
    meta: { requiresAuth: true }
  },
  {
    path: '/recommendations',
    name: 'recommendations',
    component: RecommendationSection,
    meta: { requiresAuth: true }
  },
  {
    path: '/favorite',
    component: FavoritePage,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 🔐 Global navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('auth') === 'true'

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.path === '/' || to.path === '/login') && isAuthenticated) {
    next('/home')
  } else {
    next()
  }
})

export default router
