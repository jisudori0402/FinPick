<template>
  <section class="diagnosis-container">
    <div class="diagnosis-intro-panel">
      <p class="diagnosis-eyebrow">금융 진단</p>
      <h1>나의 금융 성장<br />레벨을 알아볼까요?</h1>
      <p class="diagnosis-copy">
        쉽게 질문으로 진단해 보며 내 금융 습관과 성장 방향을 확인해보세요.
      </p>

      <div class="diagnosis-illustration" aria-hidden="true">
        <div class="clipboard">
          <div class="clip"></div>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="coin-mark">₩</div>
        <div class="plant">
          <span></span>
        </div>
      </div>
    </div>

    <div class="diagnosis-workspace">
      <div class="diagnosis-progress">
        <span class="step-counter">{{ currentStep }} / {{ totalSteps }}</span>
        <div class="progress-segments" aria-hidden="true">
          <span
            v-for="step in totalSteps"
            :key="step"
            :class="{ active: step <= currentStep }"
          ></span>
        </div>
      </div>

      <div class="diagnosis-question-panel">
        <div v-if="currentQuestion" class="question-content">
          <div class="question-header">
            <h2 class="question-title">Q{{ currentStep }}.</h2>
            <p class="question-text">{{ currentQuestion.question }}</p>
            <p class="question-hint">{{ currentQuestion.hint }}</p>
          </div>

          <div class="question-options">
            <label
              v-for="option in currentQuestion.options"
              :key="option"
              class="option-label"
              :class="{ selected: isSelected(currentQuestion.field, option) }"
            >
              <input
                type="radio"
                :name="currentQuestion.field"
                :value="option"
                :checked="isSelected(currentQuestion.field, option)"
                @change="selectOption(currentQuestion.field, option)"
              />
              <span class="option-dot"></span>
              <span class="option-text">{{ option }}</span>
            </label>
          </div>
        </div>

        <p v-if="diagnosisError" class="error-message">
          {{ diagnosisError }}
        </p>

        <div class="diagnosis-actions">
          <button
            class="secondary-btn"
            :disabled="currentStep === 1"
            type="button"
            @click="previousQuestion"
          >
            이전
          </button>

          <button
            v-if="currentStep < totalSteps"
            class="primary-btn"
            :disabled="!currentAnswer"
            type="button"
            @click="nextQuestion"
          >
            다음
          </button>

          <button
            v-else
            class="primary-btn"
            :disabled="!isAllAnswered()"
            type="button"
            @click="submitDiagnosis"
          >
            결과 보기
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const currentStepIndex = ref(0)
const diagnosisError = ref('')

const form = ref({
  income_level: '',
  spending_style: '',
  financial_goal: '',
  investment_style: '',
  asset_level: '',
  loan_type: '',
})

const questions = [
  {
    field: 'income_level',
    question: '현재 월 소득은 어느 정도인가요?',
    hint: '최근 본인의 기준으로 선택해주세요.',
    options: ['200만원 미만', '200~300만원', '300~400만원', '400~500만원', '500만원 이상'],
  },
  {
    field: 'spending_style',
    question: '평소 소비 스타일은 어떤 편인가요?',
    hint: '가장 가까운 생활 패턴을 골라주세요.',
    options: ['월급 들어오면 바로 쓴다', '필요한 만큼만 쓴다', '계획적으로 소비한다', '저축을 우선한다'],
  },
  {
    field: 'financial_goal',
    question: '지금 가장 이루고 싶은 금융 목표는 무엇인가요?',
    hint: '현재 가장 중요한 목표 하나를 선택해주세요.',
    options: ['비상금 만들기', '여행 자금 모으기', '결혼 자금 준비', '내 집 마련', '투자 시작하기', '노후 준비'],
  },
  {
    field: 'investment_style',
    question: '투자에 대해 어떻게 생각하시나요?',
    hint: '원금 손실 가능성을 기준으로 골라주세요.',
    options: ['원금 손실은 절대 싫다', '조금은 감수 가능', '수익을 위해 위험 감수 가능', '공격적으로 투자하고 싶다'],
  },
  {
    field: 'asset_level',
    question: '현재 자산 규모는 어느 정도인가요?',
    hint: '예금, 적금, 투자금 등을 합쳐서 생각해주세요.',
    options: ['500만원 미만', '500~1,000만원', '1,000~3,000만원', '3,000만원 이상'],
  },
  {
    field: 'loan_type',
    question: '현재 보유한 대출이 있나요?',
    hint: '가장 큰 비중을 차지하는 대출을 선택해주세요.',
    options: ['없음', '학자금 대출', '전세 대출', '신용 대출', '기타'],
  },
]

const totalSteps = questions.length
const currentStep = computed(() => currentStepIndex.value + 1)
const currentQuestion = computed(() => questions[currentStepIndex.value])
const currentAnswer = computed(() => form.value[currentQuestion.value?.field] || '')

const isSelected = (field, value) => {
  return form.value[field] === value
}

const selectOption = (field, option) => {
  form.value[field] = option
  diagnosisError.value = ''
}

const nextQuestion = () => {
  if (!currentAnswer.value) {
    diagnosisError.value = '답변을 선택해주세요.'
    return
  }

  if (currentStepIndex.value < totalSteps - 1) {
    currentStepIndex.value++
  }
}

const previousQuestion = () => {
  if (currentStepIndex.value > 0) {
    currentStepIndex.value--
  }
}

const isAllAnswered = () => {
  return Object.values(form.value).every((value) => value !== '')
}

const submitDiagnosis = async () => {
  diagnosisError.value = ''

  if (!isAllAnswered()) {
    diagnosisError.value = '모든 문항에 답변해주세요.'
    return
  }

  try {
    const response = await axios.post('http://localhost:8000/api/diagnosis/', form.value, {
      withCredentials: true,
    })

    const resultPayload = response.data.result || response.data

    if (!resultPayload?.financial_type) {
      throw new Error('Invalid diagnosis response')
    }

    localStorage.setItem('latestDiagnosisResult', JSON.stringify(resultPayload))
    localStorage.removeItem('latestRoadmap')
    window.dispatchEvent(new Event('auth-state-changed'))

    router.push('/diagnosis-result')
  } catch (err) {
    diagnosisError.value = err.response?.data?.message || '진단 결과를 저장하지 못했습니다.'
    console.error(err)
  }
}
</script>
