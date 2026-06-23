<template>
  <section class="card panel">
    <h2>금융 진단 테스트</h2>

    <div class="question-block">
      <h3>STEP 1. 소득 수준</h3>
      <p>월 소득은 어느 정도인가요?</p>

      <div class="options">
        <label
          v-for="option in options.income_level"
          :key="option"
          class="option"
        >
          <input
            v-model="form.income_level"
            type="radio"
            name="income_level"
            :value="option"
          />
          <span>{{ option }}</span>
        </label>
      </div>
    </div>

    <div class="question-block">
      <h3>STEP 2. 소비 성향</h3>
      <p>평소 소비 스타일은 어떤 편인가요?</p>

      <div class="options">
        <label
          v-for="option in options.spending_style"
          :key="option"
          class="option"
        >
          <input
            v-model="form.spending_style"
            type="radio"
            name="spending_style"
            :value="option"
          />
          <span>{{ option }}</span>
        </label>
      </div>
    </div>

    <div class="question-block">
      <h3>STEP 3. 금융 목표</h3>
      <p>지금 가장 이루고 싶은 목표는?</p>

      <div class="options">
        <label
          v-for="option in options.financial_goal"
          :key="option"
          class="option"
        >
          <input
            v-model="form.financial_goal"
            type="radio"
            name="financial_goal"
            :value="option"
          />
          <span>{{ option }}</span>
        </label>
      </div>
    </div>

    <div class="question-block">
      <h3>STEP 4. 투자 성향</h3>
      <p>투자에 대해 어떻게 생각하시나요?</p>

      <div class="options">
        <label
          v-for="option in options.investment_style"
          :key="option"
          class="option"
        >
          <input
            v-model="form.investment_style"
            type="radio"
            name="investment_style"
            :value="option"
          />
          <span>{{ option }}</span>
        </label>
      </div>
    </div>

    <div class="question-block">
      <h3>STEP 5. 자산 및 부채</h3>

      <h4 class="sub-title">자산</h4>
      <div class="options">
        <label
          v-for="option in options.asset_level"
          :key="option"
          class="option"
        >
          <input
            v-model="form.asset_level"
            type="radio"
            name="asset_level"
            :value="option"
          />
          <span>{{ option }}</span>
        </label>
      </div>

      <h4 class="sub-title">대출</h4>
      <div class="options">
        <label
          v-for="option in options.loan_type"
          :key="option"
          class="option"
        >
          <input
            v-model="form.loan_type"
            type="radio"
            name="loan_type"
            :value="option"
          />
          <span>{{ option }}</span>
        </label>
      </div>
    </div>

    <p v-if="diagnosisError" class="error">
      {{ diagnosisError }}
    </p>

    <button class="primary-btn submit-btn" @click="submitDiagnosis">
      결과 보기
    </button>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const diagnosisError = ref('')

const form = ref({
  income_level: '',
  spending_style: '',
  financial_goal: '',
  investment_style: '',
  asset_level: '',
  loan_type: '',
})

const options = {
  income_level: [
    '200만원 미만',
    '200~300만원',
    '300~400만원',
    '400~500만원',
    '500만원 이상',
  ],
  spending_style: [
    '월급 들어오면 바로 쓴다',
    '필요한 만큼만 쓴다',
    '계획적으로 소비한다',
    '저축을 우선한다',
  ],
  financial_goal: [
    '비상금 만들기',
    '여행 자금 모으기',
    '결혼 자금 준비',
    '내 집 마련',
    '투자 시작하기',
    '노후 준비',
  ],
  investment_style: [
    '원금 손실은 절대 싫다',
    '조금은 감수 가능',
    '수익을 위해 위험 감수 가능',
    '공격적으로 투자하고 싶다',
  ],
  asset_level: [
    '500만원 미만',
    '500~1,000만원',
    '1,000~3,000만원',
    '3,000만원 이상',
  ],
  loan_type: [
    '없음',
    '학자금 대출',
    '전세 대출',
    '신용 대출',
    '기타',
  ],
}

const submitDiagnosis = async () => {
  diagnosisError.value = ''

  const values = Object.values(form.value)
  const hasEmptyValue = values.some((value) => !value)

  if (hasEmptyValue) {
    diagnosisError.value = '모든 문항에 답변해주세요.'
    return
  }

  try {
    const response = await axios.post(
      'http://localhost:8000/api/diagnosis/',
      form.value,
      {
        withCredentials: true,
      },
    )

    const resultPayload = response.data.result || response.data

    if (!resultPayload?.financial_type) {
      throw new Error('Invalid diagnosis response')
    }

    localStorage.setItem('latestDiagnosisResult', JSON.stringify(resultPayload))

    router.push('/diagnosis-result')
  } catch (err) {
    diagnosisError.value =
      err.response?.data?.message || '진단 결과를 저장하지 못했습니다.'
    console.error(err)
  }
}
</script>

