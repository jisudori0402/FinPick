import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Homeview.vue'
import DepositProductListView from '../views/DepositProductListView.vue'
import DepositProductDetailView from '../views/DepositProductDetailView.vue'
import StockProductDetailView from '../views/StockProductDetailView.vue'
import BankSearchView from '../views/BankSearchView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import PasswordChangeView from '../views/PasswordChangeView.vue'
import PasswordResetView from '../views/PasswordResetView.vue'
import DiagnosisView from '../views/DiagnosisView.vue'
import DiagnosisResultView from '../views/DiagnosisResultView.vue'
import RoadmapView from '../views/RoadmapView.vue'
import CommunityView from '../views/CommunityView.vue'
import CommunityVideoDetailView from '../views/CommunityVideoDetailView.vue'
import { notifyAuthChanged, syncAuthFromSession } from '../services/auth'


const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/deposit-products',
      name: 'deposit-products',
      component: DepositProductListView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/deposit-products/:id',
      name: 'deposit-product-detail',
      component: DepositProductDetailView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/stocks/:code',
      name: 'stock-product-detail',
      component: StockProductDetailView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/bank-search/:productId',
      name: 'bank-search',
      component: BankSearchView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/password-reset',
      name: 'password-reset',
      component: PasswordResetView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/password-change',
      name: 'password-change',
      component: PasswordChangeView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/diagnosis',
      name: 'diagnosis',
      component: DiagnosisView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/diagnosis-result',
      name: 'diagnosis-result',
      component: DiagnosisResultView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/roadmap',
      name: 'roadmap',
      component: RoadmapView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/community/videos/:videoId',
      name: 'community-video-detail',
      component: CommunityVideoDetailView,
      meta: {
        requiresAuth: true,
      },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const isLoggedIn = await syncAuthFromSession()
  notifyAuthChanged()

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
    return
  }

  if ((to.path === '/login' || to.path === '/signup') && isLoggedIn) {
    next('/')
    return
  }

  next()
})

export default router
