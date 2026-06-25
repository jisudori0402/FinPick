<template>
  <div class="wrap login-wrap">
    <div class="card login-card signup-card">
      <span class="login-kicker">Start FinPick</span>
      <h1><strong>FinPick</strong> 회원가입</h1>
      <p>나만의 금융 성장 로드맵을 시작할 계정을 만들어 주세요.</p>

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
        <div class="date-segment-input">
          <input
            ref="birthYearInput"
            v-model="birthYear"
            inputmode="numeric"
            maxlength="4"
            placeholder="YYYY"
            required
            @input="handleBirthPartInput('year')"
          />
          <span>/</span>
          <input
            ref="birthMonthInput"
            v-model="birthMonth"
            inputmode="numeric"
            maxlength="2"
            placeholder="MM"
            required
            @input="handleBirthPartInput('month')"
          />
          <span>/</span>
          <input
            ref="birthDayInput"
            v-model="birthDay"
            inputmode="numeric"
            maxlength="2"
            placeholder="DD"
            required
            @input="handleBirthPartInput('day')"
          />
        </div>

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
const birthYear = ref('')
const birthMonth = ref('')
const birthDay = ref('')
const birthYearInput = ref(null)
const birthMonthInput = ref(null)
const birthDayInput = ref(null)
const password1 = ref('')
const password2 = ref('')
const error = ref('')
const message = ref('')

const submitSignup = async () => {
  error.value = ''
  message.value = ''
  const birthDate = `${birthYear.value}-${birthMonth.value.padStart(2, '0')}-${birthDay.value.padStart(2, '0')}`

  if (birthYear.value.length !== 4 || birthMonth.value.length !== 2 || birthDay.value.length !== 2) {
    error.value = '생년월일을 YYYY/MM/DD 형식으로 입력해주세요.'
    return
  }

  if (password1.value !== password2.value) {
    error.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  try {
    const response = await axios.post('http://localhost:8000/api/signup/', {
      username: username.value,
      email: email.value,
      name: name.value,
      birth_date: birthDate,
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

const handleBirthPartInput = (part) => {
  birthYear.value = birthYear.value.replace(/\D/g, '').slice(0, 4)
  birthMonth.value = birthMonth.value.replace(/\D/g, '').slice(0, 2)
  birthDay.value = birthDay.value.replace(/\D/g, '').slice(0, 2)

  if (part === 'year' && birthYear.value.length === 4) {
    birthMonthInput.value?.focus()
  }

  if (part === 'month' && birthMonth.value.length === 2) {
    birthDayInput.value?.focus()
  }
}
</script>

