<template>
  <div class="home-page">
    <section class="home-hero">
      <div class="hero-copy">
        <h1>금융도 순서가 있습니다.</h1>
        <p>
          진단부터 저축, 투자까지<br />
          나만의 금융 성장 로드맵을 지금 시작해보세요.
        </p>

        <RouterLink class="primary-btn hero-cta" :to="diagnosisStartLink">
          금융 진단 시작하기
        </RouterLink>
      </div>

      <div class="journey-visual" aria-label="금융 성장 단계 미리보기">
        <img class="journey-illustration" src="/home-mountain-road-cutout.png" alt="" />

        <div class="level-card level-one">
          <span class="level-icon wallet-icon"></span>
          <strong>시작</strong>
          <p>금융 기초 다지기</p>
          <small>비상금 만들기</small>
        </div>

        <div class="level-card level-two">
          <span class="level-icon piggy-icon"></span>
          <strong>성장</strong>
          <p>목돈 마련하기</p>
          <small>저축 시작하기</small>
        </div>

        <div class="level-card level-three">
          <span class="level-icon chart-icon"></span>
          <strong>도약</strong>
          <p>자산 성장하기</p>
          <small>투자 시작하기</small>
        </div>
      </div>

      <aside class="roadmap-preview">
        <h2>서비스 가이드 미리보기</h2>
        <ol>
          <li v-for="step in roadmapPreview" :key="step.title">
            <span class="guide-step-number">{{ step.number }}</span>
            <div>
              <strong>{{ step.title }}</strong>
              <p>{{ step.description }}</p>
            </div>
          </li>
        </ol>
      </aside>
    </section>

    <section class="home-dashboard-grid" aria-label="홈 요약">
      <RouterLink
        v-if="isLoggedIn"
        class="home-card level-summary"
        :class="{ locked: !hasDiagnosisResult }"
        :to="levelCardLink"
      >
        <div class="card-title-row">
          <h2>현재 금융 레벨</h2>
        </div>

        <div class="level-content">
          <div class="home-type-avatar" :class="{ 'has-image': homeTypeImageSrc }" aria-hidden="true">
            <img
              v-if="homeTypeImageSrc"
              :src="homeTypeImageSrc"
              :alt="`${financialTypeName} 캐릭터`"
              @error="markHomeTypeImageError"
            />
            <span v-else></span>
          </div>
          <div>
            <strong>{{ currentLevelLabel }}</strong>
            <h3>{{ financialTypeName }}</h3>
            <p>{{ levelDescription }}</p>
            <div class="level-progress">
              <span :style="{ width: dashboardProgress + '%' }"></span>
            </div>
            <small>{{ dashboardProgress }}%</small>
          </div>
        </div>
      </RouterLink>

      <div v-else class="home-card level-summary locked">
        <div class="card-title-row">
          <h2>현재 금융 레벨</h2>
        </div>
        <div class="locked-state">
          <strong>로그인이 필요해요</strong>
          <p>금융 진단 결과와 현재 레벨은 로그인 후 확인할 수 있어요.</p>
          <RouterLink class="secondary-btn compact-btn" to="/login">로그인하기</RouterLink>
        </div>
      </div>

      <article class="home-card goal-card">
        <h2>다음 목표</h2>
        <div class="goal-body">
          <span class="goal-target-icon" aria-hidden="true"></span>
          <div>
            <strong>{{ nextMissionTitle }}</strong>
            <p>{{ nextMissionDescription }}</p>
          </div>
        </div>
        <RouterLink class="outline-btn" to="/roadmap">
          목표 자세히 보기
          <span aria-hidden="true">-></span>
        </RouterLink>
      </article>

      <article class="home-card product-card-home">
        <div class="card-title-row">
          <h2>추천 상품</h2>
          <RouterLink class="more-link" to="/deposit-products?category=recommended">더보기</RouterLink>
        </div>

        <div class="mini-product-list">
          <RouterLink
            v-for="product in recommendedProducts"
            :key="product.key"
            class="mini-product"
            :to="product.to"
          >
            <span class="mini-product-logo" :class="product.kind">
              <img v-if="product.logoUrl" :src="product.logoUrl" :alt="`${product.name} 로고`" />
              <template v-else>{{ product.name?.slice(0, 1) || '상' }}</template>
            </span>
            <div>
              <strong>{{ product.name }}</strong>
              <small>{{ product.company }}</small>
            </div>
          </RouterLink>
        </div>
      </article>
    </section>

    <section class="today-tip">
      <div class="quote-mark" aria-hidden="true">"</div>
      <div>
        <h2>오늘의 금융 한마디</h2>
        <p>{{ todayTip }}</p>
        <small v-if="todayTipLoading">AI가 오늘의 문장을 준비하고 있어요.</small>
        <small v-else-if="todayTipError">{{ todayTipError }}</small>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'

const isLoggedIn = ref(false)
const username = ref('')
const name = ref('')
const diagnosisResult = ref(null)
const roadmap = ref(null)
const favoriteProducts = ref([])
const aiRecommendedProducts = ref([])
const typeImageErrors = ref({})
const todayTip = ref('월 소득의 10%만 저축해도 1년 뒤 360만원을 모을 수 있어요.')
const todayTipLoading = ref(false)
const todayTipError = ref('')

const roadmapPreview = [
  {
    number: 1,
    title: '금융 상태 진단',
    description: '먼저 내 금융 상태를 분석해요',
  },
  {
    number: 2,
    title: '맞춤 로드맵 생성',
    description: '나에게 필요한 금융 계획을 세워요',
  },
  {
    number: 3,
    title: '필요한 상품 추천',
    description: '지금 단계에 맞는 상품을 추천해요',
  },
  {
    number: 4,
    title: '성장 관리 및 피드백',
    description: '목표 달성과 성장을 함께 관리해요',
  },
]

const fallbackMissions = [
  {
    title: '금융 진단 완료하기',
    description: '내 소비와 저축 성향부터 확인해보세요.',
    is_completed: false,
  },
  {
    title: '비상금 100만원 만들기',
    description: '나에게 맞는 첫 저축 목표를 준비해보세요.',
    is_completed: false,
  },
  {
    title: '월 저축액 정하기',
    description: '월급날 자동 저축 습관을 만들어보세요.',
    is_completed: false,
  },
]

const fallbackProducts = [
  {
    key: 'fallback-1',
    name: '청년도약계좌',
    company: '정부 지원 저축',
    icon: 'bank',
    to: '/deposit-products',
  },
  {
    key: 'fallback-2',
    name: 'OO은행 자유적금',
    company: '최대 연 4.5%',
    icon: 'piggy',
    to: '/deposit-products',
  },
  {
    key: 'fallback-3',
    name: '생활비 통장 카드',
    company: '잔돈 자동 모으기',
    icon: 'card',
    to: '/deposit-products',
  },
]

const bankLogoRules = [
  { keywords: ['신한'], file: 'shinhan.png' },
  { keywords: ['국민', 'KB'], file: 'kb.png' },
  { keywords: ['하나'], file: 'hana.png' },
  { keywords: ['우리'], file: 'woori.png' },
  { keywords: ['농협', 'NH'], file: 'nonghyup.png' },
  { keywords: ['기업', 'IBK'], file: 'ibk.png' },
  { keywords: ['카카오'], file: 'kakao.png' },
  { keywords: ['케이뱅크', '케이은행', 'K뱅크', 'Kbank'], file: 'kbank.png' },
  { keywords: ['토스'], file: 'toss.png' },
  { keywords: ['SC', '스탠다드차타드', '제일'], file: 'sc.png' },
]

const getBankLogoUrl = (companyName = '') => {
  const normalizedName = String(companyName).toLowerCase()
  const matched = bankLogoRules.find((rule) => {
    return rule.keywords.some((keyword) => normalizedName.includes(keyword.toLowerCase()))
  })

  return matched ? `/bank_logos/${matched.file}` : ''
}

const typeCharacterImages = {
  안정형: '/financial-types/stable-saver.png',
  계획형: '/financial-types/planner-saver.png',
  소비러: '/financial-types/smart-spender.png',
  투자러: '/financial-types/growth-investor.png',
  점검러: '/financial-types/finance-checker.png',
  자산러: '/financial-types/aggressive-asset.png',
}

const hasDiagnosisResult = computed(() => {
  return diagnosisResult.value !== null
})

const diagnosisStartLink = computed(() => {
  if (hasDiagnosisResult.value) {
    return '/diagnosis-result'
  }

  return '/diagnosis'
})

const levelCardLink = computed(() => {
  if (hasDiagnosisResult.value) {
    return '/diagnosis-result'
  }

  return '/diagnosis'
})

const displayName = computed(() => {
  return name.value || username.value || '회원'
})

const rawFinancialType = computed(() => {
  return diagnosisResult.value?.financial_type || '금융 새싹'
})

const matchedType = computed(() => {
  return Object.keys(typeCharacterImages).find((key) => rawFinancialType.value.includes(key)) || ''
})

const homeTypeImageSrc = computed(() => {
  if (!matchedType.value || typeImageErrors.value[matchedType.value]) {
    return ''
  }

  return typeCharacterImages[matchedType.value]
})

const markHomeTypeImageError = () => {
  if (!matchedType.value) {
    return
  }

  typeImageErrors.value = {
    ...typeImageErrors.value,
    [matchedType.value]: true,
  }
}

const currentLevelLabel = computed(() => {
  if (roadmap.value?.current_level_label) {
    return roadmap.value.current_level_label
  }

  if (typeof roadmap.value?.current_level === 'number') {
    return `Lv.${roadmap.value.current_level}`
  }

  const levels = roadmap.value?.levels || []
  const currentLevel = levels.find((level) =>
    (level.missions || []).some((mission) => !mission.is_completed),
  )

  if (currentLevel?.level) {
    return `Lv.${currentLevel.level}`
  }

  return hasDiagnosisResult.value ? 'Lv.1' : '진단 전'
})

const financialTypeName = computed(() => {
  if (!hasDiagnosisResult.value) {
    return '금융 진단 전'
  }

  return rawFinancialType.value
})

const levelDescription = computed(() => {
  if (!hasDiagnosisResult.value) {
    return `${displayName.value}님의 첫 금융 진단을 기다리고 있어요.`
  }

  return diagnosisResult.value?.finpick_comment || '금융을 막 시작한 단계예요.'
})

const dashboardMissions = computed(() => {
  const levels = roadmap.value?.levels || []
  const missions = levels.flatMap((level) => level.missions || [])

  return missions.length ? missions : fallbackMissions
})

const dashboardProgress = computed(() => {
  if (typeof roadmap.value?.progress === 'number') {
    return roadmap.value.progress
  }

  return hasDiagnosisResult.value ? 25 : 0
})

const nextMission = computed(() => {
  return dashboardMissions.value.find((mission) => !mission.is_completed) || fallbackMissions[1]
})

const nextMissionTitle = computed(() => {
  return nextMission.value?.title || nextMission.value?.mission_title || '비상금 100만원 만들기'
})

const nextMissionDescription = computed(() => {
  return (
    nextMission.value?.description ||
    nextMission.value?.mission_description ||
    '다음 단계로 이어갈 금융 활동이에요.'
  )
})

const recommendedProducts = computed(() => {
  if (aiRecommendedProducts.value.length) {
    return aiRecommendedProducts.value
  }

  if (favoriteProducts.value.length) {
    return favoriteProducts.value.slice(0, 3).map((item, index) => ({
    key: item.id || `favorite-${index}`,
    name: item.product_name,
    company: item.financial_company_name,
    icon: index === 0 ? 'bank' : index === 1 ? 'piggy' : 'card',
    kind: 'deposit',
    logoUrl: getBankLogoUrl(item.financial_company_name),
    to: `/deposit-products/${item.id}`,
    }))
  }

  return fallbackProducts
})

const pickRandomItems = (items, count = 3) => {
  return [...items]
    .sort(() => Math.random() - 0.5)
    .slice(0, count)
}

const syncHomeState = () => {
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true'
  username.value = localStorage.getItem('username') || ''
  name.value = localStorage.getItem('name') || ''
  diagnosisResult.value = null

  const savedResult = localStorage.getItem('latestDiagnosisResult')

  if (savedResult) {
    try {
      diagnosisResult.value = JSON.parse(savedResult)
    } catch {
      localStorage.removeItem('latestDiagnosisResult')
    }
  }
}

const loadHomeDashboard = async () => {
  if (!isLoggedIn.value) {
    roadmap.value = null
    favoriteProducts.value = []
    return
  }

  try {
    const [diagnosisResponse, roadmapResponse, favoritesResponse] = await Promise.all([
      axios.get('http://localhost:8000/api/diagnosis/latest/', { withCredentials: true }),
      axios.get('http://localhost:8000/api/roadmap/', { withCredentials: true }),
      axios.get('http://localhost:8000/api/favorite-deposit-products/', { withCredentials: true }),
    ])

    if (diagnosisResponse.data.result) {
      diagnosisResult.value = diagnosisResponse.data.result
      localStorage.setItem('latestDiagnosisResult', JSON.stringify(diagnosisResponse.data.result))
    } else {
      diagnosisResult.value = null
      localStorage.removeItem('latestDiagnosisResult')
    }

    roadmap.value = roadmapResponse.data.roadmap
    favoriteProducts.value = favoritesResponse.data.products || []
  } catch (err) {
    console.error(err)
  }
}

const loadAiRecommendedProducts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/ai/product-recommendations/', {
      withCredentials: true,
    })

    const deposits = (response.data.deposits || []).map((item) => ({
      key: `deposit-${item.id}`,
      name: item.product_name,
      company: item.financial_company_name,
      icon: item.product_type === 'deposit' ? 'bank' : 'piggy',
      kind: 'deposit',
      logoUrl: getBankLogoUrl(item.financial_company_name),
      to: `/deposit-products/${item.id}`,
    }))
    const stocks = (response.data.stocks || []).map((item) => ({
      key: `stock-${item.code}`,
      name: item.name,
      company: `${item.market || '주식'} · ${item.change_rate > 0 ? '+' : ''}${Number(item.change_rate || 0).toFixed(2)}%`,
      icon: 'card',
      kind: 'stock',
      logoUrl: item.logo_url || '',
      to: `/stocks/${item.code}`,
    }))

    aiRecommendedProducts.value = pickRandomItems([...deposits, ...stocks], 3)
  } catch (err) {
    console.error(err)
  }
}

const loadTodayTip = async () => {
  todayTipLoading.value = true
  todayTipError.value = ''

  try {
    const response = await axios.get('http://localhost:8000/api/ai/today-message/', {
      withCredentials: true,
    })
    if (response.data.message) {
      todayTip.value = response.data.message
    }
  } catch (err) {
    todayTipError.value = err.response?.data?.message || '오늘의 금융 한마디를 불러오지 못했습니다.'
  } finally {
    todayTipLoading.value = false
  }
}

const refreshHome = async () => {
  syncHomeState()
  await loadHomeDashboard()
}

onMounted(() => {
  refreshHome()
  loadTodayTip()
  loadAiRecommendedProducts()
  window.addEventListener('auth-state-changed', refreshHome)
})

onUnmounted(() => {
  window.removeEventListener('auth-state-changed', refreshHome)
})
</script>
