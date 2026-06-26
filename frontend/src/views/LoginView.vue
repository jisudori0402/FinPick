<template>
  <div class="wrap login-wrap">
    <div class="card login-card">
      <span class="login-kicker">Welcome back</span>
      <h1><strong>FinPick</strong> 濡쒓렇??</h1>
      <p>?섎쭔??湲덉쑖 ?깆옣 濡쒕뱶留듭쓣 ?댁뼱媛?ㅻ㈃ 濡쒓렇?명빐 二쇱꽭??</p>

      <div v-if="error" class="msg">
        {{ error }}
      </div>

      <div v-if="message" class="msg ok">
        {{ message }}
      </div>

      <form @submit.prevent="submitLogin">
        <label>?꾩씠??</label>
        <input
          v-model="username"
          required
          autocomplete="username"
        />

        <label>鍮꾨?踰덊샇</label>
        <input
          v-model="password"
          type="password"
          required
          autocomplete="current-password"
        />

        <button class="btn" type="submit">
          濡쒓렇??        </button>
      </form>

      <p class="password-find-link">
        鍮꾨?踰덊샇瑜??딆쑝?⑤굹??
        <RouterLink to="/password-reset">鍮꾨?踰덊샇 李얘린</RouterLink>
      </p>

      <p class="signup-link">
        ?꾩쭅 怨꾩젙???녿굹??
        <RouterLink to="/signup">?뚯썝媛??</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '../services/api'
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
      `${API_BASE_URL}/api/login/`,
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

    message.value = response.data.message || '濡쒓렇?몃릺?덉뒿?덈떎.'

    await router.push('/')
  } catch (err) {
    error.value = err.response?.data?.message || '濡쒓렇?몄뿉 ?ㅽ뙣?덉뒿?덈떎.'
    console.error(err)
  }
}
</script>

