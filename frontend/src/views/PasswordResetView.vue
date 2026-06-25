<template>
  <section class="password-change-page">
    <div class="password-change-card">
      <span class="detail-kicker">계정 찾기</span>
      <h1>비밀번호 찾기</h1>
      <p>아이디와 이름을 확인한 뒤 새 비밀번호로 재설정할 수 있어요.</p>

      <form @submit.prevent="submitPasswordReset">
        <label>
          아이디
          <input
            v-model="username"
            autocomplete="username"
            required
          />
        </label>

        <label>
          이름
          <input
            v-model="name"
            autocomplete="name"
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
          <RouterLink class="secondary-btn" to="/login">
            취소
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
    error.value = '새 비밀번호가 일치하지 않습니다.'
    return
  }

  isSubmitting.value = true

  try {
    const response = await axios.post('http://localhost:8000/api/password-reset/', {
      username: username.value,
      name: name.value,
      new_password: newPassword.value,
      new_password_confirm: newPasswordConfirm.value,
    })

    message.value = response.data.message || '비밀번호가 재설정되었습니다.'
    username.value = ''
    name.value = ''
    newPassword.value = ''
    newPasswordConfirm.value = ''

    window.setTimeout(() => {
      router.push('/login')
    }, 900)
  } catch (err) {
    error.value = err.response?.data?.message || '비밀번호 재설정에 실패했습니다.'
    console.error(err)
  } finally {
    isSubmitting.value = false
  }
}
</script>
