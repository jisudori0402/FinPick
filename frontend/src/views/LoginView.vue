<template>
  <div class="wrap login-wrap">
    <div class="card login-card">
      <span class="login-kicker">Welcome back</span>
      <h1><strong>FinPick</strong> 로그인</h1>
      <p>나만의 금융 성장 로드맵을 이어가려면 로그인해 주세요.</p>

      <div v-if="error" class="msg">
        {{ error }}
      </div>

      <div v-if="message" class="msg ok">
        {{ message }}
      </div>

      <form @submit.prevent="submitLogin">
        <label>아이디</label>
        <input
          v-model="username"
          required
          autocomplete="username"
        />

        <label>비밀번호</label>
        <input
          v-model="password"
          type="password"
          required
          autocomplete="current-password"
        />

        <button class="btn" type="submit">
          로그인
        </button>
      </form>

      <p class="signup-link">
        아직 계정이 없나요?
        <RouterLink to="/signup">회원가입</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'
import { notifyAuthChanged } from '../services/auth'

const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')
const message = ref('')

const submitLogin = async () => {
  error.value = ''
  message.value = ''

  try {
    const response = await axios.post(
      'http://localhost:8000/api/login/',
      {
        username: username.value,
        password: password.value,
      },
      {
        withCredentials: true,
      },
    )

    localStorage.setItem('isLoggedIn', 'true')
    localStorage.setItem('username', response.data.user?.username || username.value)
    localStorage.setItem('email', response.data.user?.email || '')
    localStorage.setItem('name', response.data.user?.name || '')
    notifyAuthChanged()

    message.value = response.data.message || '로그인되었습니다.'

    await router.push('/')
  } catch (err) {
    error.value = err.response?.data?.message || '로그인에 실패했습니다.'
    console.error(err)
  }
}
</script>

