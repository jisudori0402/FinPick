<template>
  <div class="home-page">
    <section class="home-hero">
      <div class="hero-copy">
        <h1>湲덉쑖???쒖꽌媛 ?덉뒿?덈떎.</h1>
        <p>
          吏꾨떒遺???異? ?ъ옄源뚯?<br />
          ?섎쭔??湲덉쑖 ?깆옣 濡쒕뱶留듭쓣 吏湲??쒖옉?대낫?몄슂.
        </p>

        <RouterLink class="primary-btn hero-cta" :to="diagnosisStartLink">
          湲덉쑖 吏꾨떒 ?쒖옉?섍린
        </RouterLink>
      </div>

      <div class="journey-visual" aria-label="湲덉쑖 ?깆옣 ?④퀎 誘몃━蹂닿린">
        <img class="journey-illustration" src="/home-mountain-road-cutout.png" alt="" />

        <div class="level-card level-one">
          <span class="level-icon wallet-icon"></span>
        <strong>오늘의 금융 테마</strong>
          <p>금융 기초 다지기</p>
          <small>鍮꾩긽湲?留뚮뱾湲?</small>
        </div>

        <div class="level-card level-two">
          <span class="level-icon piggy-icon"></span>
        <strong>오늘의 금융 테마</strong>
          <p>紐⑸룉 留덈젴?섍린</p>
          <small>?異??쒖옉?섍린</small>
        </div>

        <div class="level-card level-three">
          <span class="level-icon chart-icon"></span>
        <strong>오늘의 금융 테마</strong>
          <p>?먯궛 ?깆옣?섍린</p>
          <small>?ъ옄 ?쒖옉?섍린</small>
        </div>
      </div>

      <aside class="roadmap-preview">
        <h2>?쒕퉬??媛?대뱶 誘몃━蹂닿린</h2>
        <ol>
          <li v-for="step in roadmapPreview" :key="step.title">
            <span class="guide-step-number">{{ step.number }}</span>
            <div>
        <strong>오늘의 금융 테마</strong>
              <p>{{ step.description }}</p>
            </div>
          </li>
        </ol>
      </aside>
    </section>

    <section class="home-dashboard-grid" aria-label="???붿빟">
      <RouterLink
        v-if="isLoggedIn"
        class="home-card level-summary"
        :class="{ locked: !hasDiagnosisResult }"
        :to="levelCardLink"
      >
        <div class="card-title-row">
          <h2>?꾩옱 湲덉쑖 ?덈꺼</h2>
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
        <strong>오늘의 금융 테마</strong>
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
          <h2>?꾩옱 湲덉쑖 ?덈꺼</h2>
        </div>
        <div class="locked-state">
        <strong>오늘의 금융 테마</strong>
          <p>湲덉쑖 吏꾨떒 寃곌낵? ?꾩옱 ?덈꺼? 濡쒓렇?????뺤씤?????덉뼱??</p>
          <RouterLink class="secondary-btn compact-btn" to="/login">濡쒓렇?명븯湲?</RouterLink>
        </div>
      </div>

      <article class="home-card goal-card">
        <h2>?ㅼ쓬 紐⑺몴</h2>
        <div class="goal-body">
          <span class="goal-target-icon" aria-hidden="true"></span>
          <div>
        <strong>오늘의 금융 테마</strong>
            <p>{{ nextMissionDescription }}</p>
          </div>
        </div>
        <RouterLink class="outline-btn" to="/roadmap">
          紐⑺몴 ?먯꽭??蹂닿린
          <span aria-hidden="true">-></span>
        </RouterLink>
      </article>

      <article class="home-card product-card-home">
        <div class="card-title-row">
          <h2>異붿쿇 ?곹뭹</h2>
          <RouterLink class="more-link" to="/deposit-products?category=recommended">?붾낫湲?</RouterLink>
        </div>

        <div class="mini-product-list">
          <RouterLink
            v-for="product in recommendedProducts"
            :key="product.key"
            class="mini-product"
            :to="product.to"
          >
            <span class="mini-product-logo" :class="product.kind">
              <img v-if="product.logoUrl" :src="product.logoUrl" :alt="`${product.name} 濡쒓퀬`" />
              <template v-else>{{ product.name?.slice(0, 1) || '?' }}</template>
            </span>
            <div>
        <strong>오늘의 금융 테마</strong>
              <small>{{ product.company }}</small>
            </div>
          </RouterLink>
        </div>
      </article>
    </section>

    <section class="today-tip">
      <div class="quote-mark" aria-hidden="true">"</div>
      <div>
        <h2>오늘의 금융 테마</h2>
        <p>{{ todayTip }}</p>
        <small v-if="todayTipLoading">AI媛 ?ㅻ뒛??臾몄옣??以鍮꾪븯怨??덉뼱??</small>
        <small v-else-if="todayTipError">{{ todayTipError }}</small>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '../services/api'

const isLoggedIn = ref(false)
const username = ref('')
const name = ref('')
const diagnosisResult = ref(null)
const roadmap = ref(null)
const favoriteProducts = ref([])
const aiRecommendedProducts = ref([])
const typeImageErrors = ref({})
const todayTip = ref('???뚮뱷??10%留??異뺥빐??1????360留뚯썝??紐⑥쓣 ???덉뼱??')
const todayTipLoading = ref(false)
const todayTipError = ref('')

const roadmapPreview = [
  {
    number: 1,
    title: '湲덉쑖 ?곹깭 吏꾨떒',
    description: '나에게 필요한 금융 계획을 세워요',
  },
  {
    number: 2,
    title: '留욎땄 濡쒕뱶留??앹꽦',
    description: '나에게 필요한 금융 계획을 세워요',
  },
  {
    number: 3,
    title: '?꾩슂???곹뭹 異붿쿇',
    description: '吏湲??④퀎??留욌뒗 ?곹뭹??異붿쿇?댁슂',
  },
  {
    number: 4,
    title: '성장 관리 및 피드백',
    description: '목표 달성과 성장을 함께 관리해요',
  },
]

const fallbackMissions = [
  {
    title: '湲덉쑖 吏꾨떒 ?꾨즺?섍린',
    description: '???뚮퉬? ?異??깊뼢遺???뺤씤?대낫?몄슂.',
    is_completed: false,
  },
  {
    title: '비상금 100만원 만들기',
    description: '나에게 필요한 금융 계획을 세워요',
    is_completed: false,
  },
  {
    title: '월 저축액 정하기',
    description: '?붽툒???먮룞 ?異??듦???留뚮뱾?대낫?몄슂.',
    is_completed: false,
  },
]

const fallbackProducts = [
  {
    key: 'fallback-1',
    name: '泥?뀈?꾩빟怨꾩쥖',
    company: '정부 지원 저축',
    icon: 'bank',
    to: '/deposit-products',
  },
  {
    key: 'fallback-2',
    name: 'OO????먯쑀?곴툑',
    company: '理쒕? ??4.5%',
    icon: 'piggy',
    to: '/deposit-products',
  },
  {
    key: 'fallback-3',
    name: '?앺솢鍮??듭옣 移대뱶',
    company: '월급 자동 모으기',
    icon: 'card',
    to: '/deposit-products',
  },
]

const bankLogoRules = [
  { keywords: ['shinhan', '신한'], file: 'shinhan.png' },
  { keywords: ['kb', '국민'], file: 'kb.png' },
  { keywords: ['hana', '하나'], file: 'hana.png' },
  { keywords: ['woori', '우리'], file: 'woori.png' },
  { keywords: ['nh', '농협'], file: 'nonghyup.png' },
  { keywords: ['ibk', '기업'], file: 'ibk.png' },
  { keywords: ['kakao', '카카오'], file: 'kakao.png' },
  { keywords: ['kbank', '케이'], file: 'kbank.png' },
  { keywords: ['toss', '토스'], file: 'toss.png' },
  { keywords: ['sc'], file: 'sc.png' },
]

const getBankLogoUrl = (companyName = '') => {
  const normalizedName = String(companyName).toLowerCase()
  const matched = bankLogoRules.find((rule) => {
    return rule.keywords.some((keyword) => normalizedName.includes(keyword.toLowerCase()))
  })

  return matched ? `/bank_logos/${matched.file}` : ''
}

const typeCharacterImages = {
  default: '/financial-types/stable-saver.png',
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
  return name.value || username.value || '?뚯썝'
})

const rawFinancialType = computed(() => {
  return diagnosisResult.value?.financial_type || '湲덉쑖 ?덉떦'
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
    return `${displayName.value}?섏쓽 泥?湲덉쑖 吏꾨떒??湲곕떎由ш퀬 ?덉뼱??`
  }

  return diagnosisResult.value?.finpick_comment || '湲덉쑖??留??쒖옉???④퀎?덉슂.'
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
  return nextMission.value?.title || '오늘의 미션을 모두 완료했어요'
})

const nextMissionDescription = computed(() => {
  return (
    nextMission.value?.description ||
    nextMission.value?.mission_description ||
    '?ㅼ쓬 ?④퀎濡??댁뼱媛?湲덉쑖 ?쒕룞?댁뿉??'
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
      axios.get(`${API_BASE_URL}/api/diagnosis/latest/`, { withCredentials: true }),
      axios.get(`${API_BASE_URL}/api/roadmap/`, { withCredentials: true }),
      axios.get(`${API_BASE_URL}/api/favorite-deposit-products/`, { withCredentials: true }),
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
    const response = await axios.get(`${API_BASE_URL}/api/ai/product-recommendations/`, {
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
      company: `${item.market || '二쇱떇'} 쨌 ${item.change_rate > 0 ? '+' : ''}${Number(item.change_rate || 0).toFixed(2)}%`,
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
    const response = await axios.get(`${API_BASE_URL}/api/ai/today-message/`, {
      withCredentials: true,
    })
    if (response.data.message) {
      todayTip.value = response.data.message
    }
  } catch (err) {
    todayTipError.value = err.response?.data?.message || '?ㅻ뒛??湲덉쑖 ?쒕쭏?붾? 遺덈윭?ㅼ? 紐삵뻽?듬땲??'
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




