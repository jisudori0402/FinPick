<template>
  <section class="diagnosis-container">
    <div class="diagnosis-intro-panel">
      <p class="diagnosis-eyebrow">湲덉쑖 吏꾨떒</p>
      <h1>?섏쓽 湲덉쑖 ?깆옣<br />?덈꺼???뚯븘蹂쇨퉴??</h1>
      <p class="diagnosis-copy">
        ?쎄쾶 吏덈Ц?쇰줈 吏꾨떒??蹂대ŉ ??湲덉쑖 ?듦?怨??깆옣 諛⑺뼢???뺤씤?대낫?몄슂.
      </p>

      <div class="diagnosis-illustration" aria-hidden="true">
        <div class="clipboard">
          <div class="clip"></div>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="coin-mark">?</div>
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
            ?댁쟾
          </button>

          <button
            v-if="currentStep < totalSteps"
            class="primary-btn"
            :disabled="!currentAnswer"
            type="button"
            @click="nextQuestion"
          >
            ?ㅼ쓬
          </button>

          <button
            v-else
            class="primary-btn"
            :disabled="!isAllAnswered()"
            type="button"
            @click="submitDiagnosis"
          >
            寃곌낵 蹂닿린
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
import { API_BASE_URL } from '../services/api'

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
    question: '?꾩옱 ???뚮뱷? ?대뒓 ?뺣룄?멸???',
    hint: '理쒓렐 蹂몄씤??湲곗??쇰줈 ?좏깮?댁＜?몄슂.',
    options: ['200留뚯썝 誘몃쭔', '200~300留뚯썝', '300~400留뚯썝', '400~500留뚯썝', '500留뚯썝 ?댁긽'],
  },
  {
    field: 'spending_style',
    question: '?됱냼 ?뚮퉬 ?ㅽ??쇱? ?대뼡 ?몄씤媛??',
    hint: '媛??媛源뚯슫 ?앺솢 ?⑦꽩??怨⑤씪二쇱꽭??',
    options: ['?붽툒 ?ㅼ뼱?ㅻ㈃ 諛붾줈 ?대떎', '?꾩슂??留뚰겮留??대떎', '怨꾪쉷?곸쑝濡??뚮퉬?쒕떎', '?異뺤쓣 ?곗꽑?쒕떎'],
  },
  {
    field: 'financial_goal',
    question: '吏湲?媛???대（怨??띠? 湲덉쑖 紐⑺몴??臾댁뾿?멸???',
    hint: '?꾩옱 媛??以묒슂??紐⑺몴 ?섎굹瑜??좏깮?댁＜?몄슂.',
    options: ['비상금 만들기', '여행 자금 모으기', '결혼 자금 준비', '내 집 마련', '투자 시작하기', '은퇴 준비'],
  },
  {
    field: 'investment_style',
    question: '?ъ옄??????대뼸寃??앷컖?섏떆?섏슂?',
    hint: '?먭툑 ?먯떎 媛?μ꽦??湲곗??쇰줈 怨⑤씪二쇱꽭??',
    options: ['원금 손실은 피하고 싶다', '조금은 감수 가능', '수익을 위해 위험 감수 가능', '공격적으로 투자하고 싶다'],
  },
  {
    field: 'asset_level',
    question: '?꾩옱 ?먯궛 洹쒕え???대뒓 ?뺣룄?멸???',
    hint: '?덇툑, ?곴툑, ?ъ옄湲??깆쓣 ?⑹퀜???앷컖?댁＜?몄슂.',
    options: ['500留뚯썝 誘몃쭔', '500~1,000留뚯썝', '1,000~3,000留뚯썝', '3,000留뚯썝 ?댁긽'],
  },
  {
    field: 'loan_type',
    question: '?꾩옱 蹂댁쑀???異쒖씠 ?덈굹??',
    hint: '媛????鍮꾩쨷??李⑥??섎뒗 ?異쒖쓣 ?좏깮?댁＜?몄슂.',
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
    diagnosisError.value = '?듬????좏깮?댁＜?몄슂.'
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
    diagnosisError.value = '紐⑤뱺 臾명빆???듬??댁＜?몄슂.'
    return
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/api/diagnosis/`, form.value, {
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
    diagnosisError.value = err.response?.data?.message || '吏꾨떒 寃곌낵瑜???ν븯吏 紐삵뻽?듬땲??'
    console.error(err)
  }
}
</script>
