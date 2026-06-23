<template>
  <div class="app">
    <div class="shell">
      <header>
        <h1>FinPick</h1>
        <p>사회초년생 금융 성장 로드맵 서비스</p>

        <nav>
          <RouterLink class="pill-link" to="/">홈</RouterLink>

          <template v-if="isLoggedIn">
            <RouterLink class="pill-link" :to="diagnosisLink">
              금융 진단
            </RouterLink>

            <RouterLink class="pill-link" to="/roadmap">로드맵</RouterLink>
            <RouterLink class="pill-link" to="/deposit-products">모든 상품</RouterLink>
            <RouterLink class="pill-link" to="/community">커뮤니티</RouterLink>
            <RouterLink class="pill-link" to="/dashboard">프로필</RouterLink>

            <button class="pill-link" type="button" @click="logout">
              로그아웃
            </button>
          </template>

          <template v-else>
            <RouterLink class="pill-link" to="/deposit-products">모든 상품</RouterLink>
            <RouterLink class="pill-link" to="/community">커뮤니티</RouterLink>
            <RouterLink class="pill-link" to="/signup">회원가입</RouterLink>
            <RouterLink class="pill-link" to="/login">로그인</RouterLink>
          </template>
        </nav>
      </header>

      <RouterView />
    </div>
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
