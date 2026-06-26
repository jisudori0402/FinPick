<template>
  <div class="wrap login-wrap">
    <div class="card login-card signup-card">
      <span class="login-kicker">Start FinPick</span>
      <h1><strong>FinPick</strong> ?뚯썝媛??</h1>
      <p>?섎쭔??湲덉쑖 ?깆옣 濡쒕뱶留듭쓣 ?쒖옉??怨꾩젙??留뚮뱾??二쇱꽭??</p>

      <form @submit.prevent="submitSignup">
        <label>?꾩씠??</label>
        <input
          v-model="username"
          autocomplete="username"
          required
        />

        <label>?대찓??</label>
        <input
          v-model="email"
          type="email"
          autocomplete="email"
          required
        />

        <label>?대쫫</label>
        <input
          v-model="name"
          autocomplete="name"
          required
        />

        <label>?앸뀈?붿씪</label>
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
            <label>鍮꾨?踰덊샇</label>
            <input
              v-model="password1"
              type="password"
              autocomplete="new-password"
              required
            />
          </div>

          <div>
            <label>鍮꾨?踰덊샇 ?뺤씤</label>
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
          ?뚯썝媛???꾨즺
        </button>
      </form>

      <p class="login-link">
        ?대? 怨꾩젙???덈굹??
        <RouterLink to="/login">濡쒓렇??</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '../services/api'

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
    error.value = '?앸뀈?붿씪??YYYY/MM/DD ?뺤떇?쇰줈 ?낅젰?댁＜?몄슂.'
    return
  }

  if (password1.value !== password2.value) {
    error.value = '鍮꾨?踰덊샇媛 ?쇱튂?섏? ?딆뒿?덈떎.'
    return
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/api/signup/`, {
      username: username.value,
      email: email.value,
      name: name.value,
      birth_date: birthDate,
      password1: password1.value,
      password2: password2.value,
    })

    message.value = response.data.message || '?뚯썝媛?낆씠 ?꾨즺?섏뿀?듬땲??'

    await router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.message || '?뚯썝媛?낆뿉 ?ㅽ뙣?덉뒿?덈떎.'
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

