<template>
  <section class="password-change-page">
    <div class="password-change-card">
      <span class="detail-kicker">怨꾩젙 蹂댁븞</span>
      <h1>鍮꾨?踰덊샇 蹂寃?</h1>
      <p>?꾩옱 鍮꾨?踰덊샇瑜??뺤씤??????鍮꾨?踰덊샇濡?蹂寃쏀븷 ???덉뼱??</p>

      <form @submit.prevent="submitPasswordChange">
        <label>
          湲곗〈 鍮꾨?踰덊샇
          <input
            v-model="currentPassword"
            type="password"
            autocomplete="current-password"
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
          <RouterLink class="secondary-btn" to="/dashboard">
            痍⑥냼
          </RouterLink>
          <button class="primary-btn" type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? '변경 중...' : '변경하기' }}
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

const currentPassword = ref('')
const newPassword = ref('')
const newPasswordConfirm = ref('')
const error = ref('')
const message = ref('')
const isSubmitting = ref(false)

const submitPasswordChange = async () => {
  error.value = ''
  message.value = ''

  if (newPassword.value !== newPasswordConfirm.value) {
    error.value = '??鍮꾨?踰덊샇媛 ?쇱튂?섏? ?딆뒿?덈떎.'
    return
  }

  isSubmitting.value = true

  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/password-change/`,
      {
        current_password: currentPassword.value,
        new_password: newPassword.value,
        new_password_confirm: newPasswordConfirm.value,
      },
      {
        withCredentials: true,
      },
    )

    message.value = response.data.message || '鍮꾨?踰덊샇媛 蹂寃쎈릺?덉뒿?덈떎.'
    if (response.data.password_changed_at) {
      localStorage.setItem('passwordChangedAt', response.data.password_changed_at)
    }
    currentPassword.value = ''
    newPassword.value = ''
    newPasswordConfirm.value = ''

    window.setTimeout(() => {
      router.push('/dashboard')
    }, 700)
  } catch (err) {
    error.value = err.response?.data?.message || '鍮꾨?踰덊샇 蹂寃쎌뿉 ?ㅽ뙣?덉뒿?덈떎.'
    console.error(err)
  } finally {
    isSubmitting.value = false
  }
}
</script>
