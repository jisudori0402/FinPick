<template>
  <section class="password-change-page">
    <RouterLink class="back-btn icon-back-btn" to="/dashboard" aria-label="내 정보로 돌아가기">
      ←
    </RouterLink>

    <div class="password-change-card">
      <span class="detail-kicker">계정 보안</span>
      <h1>비밀번호 변경</h1>
      <p>현재 비밀번호를 확인한 뒤 새 비밀번호로 변경할 수 있어요.</p>

      <form @submit.prevent="submitPasswordChange">
        <label>
          기존 비밀번호
          <input
            v-model="currentPassword"
            type="password"
            autocomplete="current-password"
            required
          />
        </label>

        <label>
          새 비밀번호
          <input
            v-model="newPassword"
            type="password"
            autocomplete="new-password"
            required
          />
        </label>

        <label>
          새 비밀번호 확인
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
            취소
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
    error.value = '새 비밀번호가 일치하지 않습니다.'
    return
  }

  isSubmitting.value = true

  try {
    const response = await axios.post(
      'http://localhost:8000/api/password-change/',
      {
        current_password: currentPassword.value,
        new_password: newPassword.value,
        new_password_confirm: newPasswordConfirm.value,
      },
      {
        withCredentials: true,
      },
    )

    message.value = response.data.message || '비밀번호가 변경되었습니다.'
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
    error.value = err.response?.data?.message || '비밀번호 변경에 실패했습니다.'
    console.error(err)
  } finally {
    isSubmitting.value = false
  }
}
</script>
