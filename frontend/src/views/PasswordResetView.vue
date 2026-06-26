<template>
  <section class="password-change-page">
    <div class="password-change-card">
      <span class="detail-kicker">怨꾩젙 李얘린</span>
      <h1>鍮꾨?踰덊샇 李얘린</h1>
      <p>?꾩씠?붿? ?대쫫???뺤씤??????鍮꾨?踰덊샇濡??ъ꽕?뺥븷 ???덉뼱??</p>

      <form @submit.prevent="submitPasswordReset">
        <label>
          ?꾩씠??          <input
            v-model="username"
            autocomplete="username"
            required
          />
        </label>

        <label>
          ?대쫫
          <input
            v-model="name"
            autocomplete="name"
            required
          />
        </label>

        <label>
          ??鍮꾨?踰덊샇
          <input
            v-model="newPassword"
            type="password"
            autocomplete="new-password"
            required
          />
        </label>

        <label>
          ??鍮꾨?踰덊샇 ?뺤씤
          <input
            v-model="newPasswordConfirm"
            type="password"
            autocomplete="new-password"
            required
          />
        </label>

        <p v-if="error" class="form-message error">
          {{ error }}
        </p>

        <p v-if="message" class="form-message ok">
          {{ message }}
        </p>

        <div class="password-change-actions">
          <RouterLink class="secondary-btn" to="/login">
            痍⑥냼
          </RouterLink>
          <button class="primary-btn" type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? '확인 중...' : '재설정하기' }}
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '../services/api'

const router = useRouter()

const username = ref('')
const name = ref('')
const newPassword = ref('')
const newPasswordConfirm = ref('')
const error = ref('')
const message = ref('')
const isSubmitting = ref(false)

const submitPasswordReset = async () => {
  error.value = ''
  message.value = ''

  if (newPassword.value !== newPasswordConfirm.value) {
    error.value = '??鍮꾨?踰덊샇媛 ?쇱튂?섏? ?딆뒿?덈떎.'
    return
  }

  isSubmitting.value = true

  try {
    const response = await axios.post(`${API_BASE_URL}/api/password-reset/`, {
      username: username.value,
      name: name.value,
      new_password: newPassword.value,
      new_password_confirm: newPasswordConfirm.value,
    })

    message.value = response.data.message || '鍮꾨?踰덊샇媛 ?ъ꽕?뺣릺?덉뒿?덈떎.'
    username.value = ''
    name.value = ''
    newPassword.value = ''
    newPasswordConfirm.value = ''

    window.setTimeout(() => {
      router.push('/login')
    }, 900)
  } catch (err) {
    error.value = err.response?.data?.message || '鍮꾨?踰덊샇 ?ъ꽕?뺤뿉 ?ㅽ뙣?덉뒿?덈떎.'
    console.error(err)
  } finally {
    isSubmitting.value = false
  }
}
</script>
