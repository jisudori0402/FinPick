<template>
  <div class="app">
    <header class="site-header">
      <RouterLink class="brand" to="/" aria-label="FinPick 홈">
        <span class="brand-mark" aria-hidden="true">F</span>
        <span>FinPick</span>
      </RouterLink>

      <nav class="site-nav" aria-label="주요 메뉴">
        <RouterLink class="nav-link" to="/">홈</RouterLink>
        <RouterLink class="nav-link" :to="diagnosisLink">금융 진단</RouterLink>
        <RouterLink class="nav-link" to="/roadmap">성장 로드맵</RouterLink>
        <RouterLink class="nav-link" to="/deposit-products">추천 상품</RouterLink>
        <RouterLink class="nav-link" to="/community">커뮤니티</RouterLink>
      </nav>

      <div class="header-actions">
        <template v-if="isLoggedIn">
          <RouterLink class="mini-link" to="/dashboard">내 정보</RouterLink>
          <button class="login-button" type="button" @click="logout">로그아웃</button>
        </template>

        <template v-else>
          <RouterLink class="mini-link" to="/signup">회원가입</RouterLink>
          <RouterLink class="login-button" to="/login">로그인</RouterLink>
        </template>
      </div>
    </header>

    <main class="shell">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { logoutSession, syncAuthFromSession } from './services/auth'

const router = useRouter()
const route = useRoute()

const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true')
const hasDiagnosisResult = ref(!!localStorage.getItem('latestDiagnosisResult'))

const syncState = () => {
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true'
  hasDiagnosisResult.value = !!localStorage.getItem('latestDiagnosisResult')
}

const diagnosisLink = computed(() => {
  if (hasDiagnosisResult.value) {
    return '/diagnosis-result'
  }

  return '/diagnosis'
})

watch(
  () => route.fullPath,
  () => {
    syncState()
  },
)

const syncSessionState = async () => {
  await syncAuthFromSession()
  syncState()
}

onMounted(() => {
  syncSessionState()
  window.addEventListener('auth-state-changed', syncState)
})

onUnmounted(() => {
  window.removeEventListener('auth-state-changed', syncState)
})

const logout = async () => {
  await logoutSession()
  syncState()
  await router.push('/')
}
</script>
