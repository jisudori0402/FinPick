<template>
  <div class="wrap">
    <div class="card">
      <h1>FinPick 회원가입</h1>

      <form @submit.prevent="submitSignup">
        <label>아이디</label>
        <input
          v-model="username"
          autocomplete="username"
          required
        />

        <label>이메일</label>
        <input
          v-model="email"
          type="email"
          autocomplete="email"
          required
        />

        <label>이름</label>
        <input
          v-model="name"
          autocomplete="name"
          required
        />

        <label>생년월일</label>
        <input
          v-model="birthDate"
          type="date"
          required
        />

        <div class="row">
          <div>
            <label>비밀번호</label>
            <input
              v-model="password1"
              type="password"
              autocomplete="new-password"
              required
            />
          </div>

          <div>
            <label>비밀번호 확인</label>
            <input
              v-model="password2"
              type="password"
              autocomplete="new-password"
              required
            />
          </div>
        </div>

        <p v-if="error" class="error">
          {{ error }}
        </p>

        <p v-if="message" class="message">
          {{ message }}
        </p>

        <button class="btn" type="submit">
          회원가입 완료
        </button>
      </form>

      <p class="login-link">
        이미 계정이 있나요?
        <RouterLink to="/login">로그인</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const username = ref('')
const email = ref('')
const name = ref('')
const birthDate = ref('')
const password1 = ref('')
const password2 = ref('')
const error = ref('')
const message = ref('')

const submitSignup = async () => {
  error.value = ''
  message.value = ''

  if (password1.value !== password2.value) {
    error.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  try {
    const response = await axios.post('http://localhost:8000/api/signup/', {
      username: username.value,
      email: email.value,
      name: name.value,
      birth_date: birthDate.value,
      password1: password1.value,
      password2: password2.value,
    })

    message.value = response.data.message || '회원가입이 완료되었습니다.'

    await router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.message || '회원가입에 실패했습니다.'
    console.error(err)
  }
}
</script>

