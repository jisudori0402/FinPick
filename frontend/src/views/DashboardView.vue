<template>
  <div class="wrap">
    <div class="card">
      <h1>프로필</h1>
      <p>회원가입 시 저장된 기본 정보입니다.</p>

      <div class="row">
        <div class="box">
          <strong>아이디</strong>
          <br />
          {{ user.username || '-' }}
        </div>

        <div class="box">
          <strong>이메일</strong>
          <br />
          {{ user.email || '-' }}
        </div>
      </div>

      <div class="row">
        <div class="box">
          <strong>나이</strong>
          <br />
          {{ profile.age || '-' }}
        </div>

        <div class="box">
          <strong>직업</strong>
          <br />
          {{ profile.job || '-' }}
        </div>
      </div>

      <div class="row">
        <div class="box">
          <strong>월 소득</strong>
          <br />
          {{ profile.monthly_income || '-' }} 만원
        </div>

        <div class="box">
          <strong>월 지출</strong>
          <br />
          {{ profile.monthly_expense || '-' }} 만원
        </div>
      </div>

      <div class="row">
        <div class="box">
          <strong>거주 형태</strong>
          <br />
          {{ profile.residence_type || '-' }}
        </div>

        <div class="box">
          <strong>저축 상태</strong>
          <br />
          {{ profile.saving_status || '-' }}
        </div>
      </div>

      <div class="row">
        <div class="box">
          <strong>투자 경험</strong>
          <br />
          {{ profile.invest_experience || '-' }}
        </div>

        <div class="box">
          <strong>가입일</strong>
          <br />
          {{ profile.created_at || '-' }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref({
  username: '',
  email: '',
})

const profile = ref({
  age: '',
  job: '',
  monthly_income: '',
  monthly_expense: '',
  residence_type: '',
  saving_status: '',
  invest_experience: '',
  created_at: '',
})

const loadDashboard = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/dashboard/', {
      withCredentials: true,
    })

    user.value = response.data.user
    profile.value = response.data.profile
  } catch (err) {
    console.error(err)

    user.value = {
      username: localStorage.getItem('username') || '',
      email: localStorage.getItem('email') || '',
    }
  }
}

onMounted(() => {
  loadDashboard()
})
</script>

