<template>
  <div>
    <section v-if="!isLoggedIn" class="landing-hero panel">
      <div class="hero-copy">
        <h2>
          금융, 무엇부터<br />
          시작해야 할지 모르겠다면
        </h2>

        <p>
          FinPick이 나에게 맞는<br />
          금융 성장 순서를 알려드릴게요.
        </p>

        <div class="hero-actions">
          <RouterLink class="primary-btn" to="/signup">
            회원가입하고 시작하기
          </RouterLink>

          <RouterLink class="secondary-btn" to="/login">
            로그인
          </RouterLink>
        </div>
      </div>

      <div class="hero-art" aria-hidden="true">
        <div class="chart">
          <div class="arrow"></div>
          <div class="bar one"></div>
          <div class="bar two"></div>
          <div class="bar three"></div>
          <div class="check-card">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <div class="coin">₩</div>
        </div>
      </div>
    </section>

    <template v-else>
      <section class="dashboard-hero panel">
        <div class="home-summary">
          <h2>안녕하세요, {{ displayName }}님 <span aria-hidden="true">👋</span></h2>

          <div class="financial-type">
            <span class="type-icon" aria-hidden="true">{{ financialTypeIcon }}</span>
            <span>{{ financialTypeName }}</span>
          </div>

          <p>{{ finpickComment }}</p>

          <RouterLink
            class="primary-btn dashboard-btn"
            :to="hasDiagnosisResult ? '/diagnosis-result' : '/diagnosis'"
          >
            {{ hasDiagnosisResult ? '금융 진단 결과 자세히 보기' : '금융 진단 시작하기' }}
          </RouterLink>
        </div>

        <aside class="progress-card" aria-label="금융 성장 현황">
          <p class="card-label">현재 로드맵 레벨</p>
          <strong class="roadmap-level">{{ roadmapLevel }}</strong>

          <div class="progress-head">
            <span>금융 성장 진행률</span>
            <strong class="progress-percent">{{ dashboardProgress }}%</strong>
          </div>

          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: dashboardProgress + '%' }"
            ></div>
          </div>

          <div class="next-goal">
            <div class="round-icon">◎</div>
            <div>
              <div class="muted">다음 목표</div>
              <strong>{{ nextMissionTitle }}</strong>
            </div>
          </div>
        </aside>
      </section>

      <div class="dashboard-grid">
        <section class="summary-card panel">
          <div class="section-head">
            <h2>나의 금융 성장 로드맵</h2>
            <RouterLink class="text-link" to="/roadmap">전체 보기 ›</RouterLink>
          </div>

          <div class="roadmap-list compact">
            <div
              v-for="(mission, index) in dashboardMissions"
              :key="mission.id || index"
              class="roadmap-row"
            >
              <div
                class="step-badge"
                :class="{ done: mission.is_completed, active: !mission.is_completed && index === firstPendingIndex }"
              >
                {{ mission.is_completed ? '✓' : index + 1 }}
              </div>

              <div>
                <small>
                  STEP {{ index + 1 }}
                  <span class="state-chip" :class="{ done: mission.is_completed }">
                    {{ mission.is_completed ? '완료' : (index === firstPendingIndex ? '진행중' : '예정') }}
                  </span>
                </small>
                <strong>{{ mission.title }}</strong>
              </div>

              <span class="row-arrow">›</span>
            </div>
          </div>
        </section>

        <section class="summary-card panel">
          <div class="section-head">
            <h2>관심종목</h2>
            <RouterLink class="text-link" to="/deposit-products">전체 보기 ›</RouterLink>
          </div>

          <div v-if="!dashboardFavorites.length" class="recommend-box">
            <span class="hot-chip">아직 관심상품이 없어요</span>
            <h3>상품을 별표로 저장해보세요</h3>
            <p>
              모든 상품에서 마음에 드는 상품을<br />
              한눈에 모아볼 수 있어요.
            </p>
            <RouterLink class="detail-btn" to="/deposit-products">
              상품 보러가기 →
            </RouterLink>
          </div>

          <div v-else class="roadmap-list compact">
            <RouterLink
              v-for="item in dashboardFavorites"
              :key="item.id"
              class="roadmap-row product-row"
              :to="`/deposit-products/${item.id}`"
            >
              <div class="step-badge done">★</div>
              <div>
                <small>{{ item.financial_company_name }}</small>
                <strong>{{ item.product_name }}</strong>
                <small>최고 {{ item.max_interest_rate || item.interest_rate || '-' }}%</small>
              </div>
              <span class="row-arrow">›</span>
            </RouterLink>
          </div>
        </section>
      </div>

      <section class="tip-card panel">
        <div class="tip-icon">💡</div>
        <div>
          <h3>오늘의 금융 한마디</h3>
          <p>
            월 소득의 10%만 저축해도<br />
            1년 뒤 360만원을 모을 수 있어요.
          </p>
        </div>
        <RouterLink class="text-link" to="/roadmap">더 알아보기 ›</RouterLink>
      </section>
    </template>

    <section v-if="!isLoggedIn" class="feature-grid">
      <div class="feature-card panel">
        <div class="feature-icon green">✓</div>
        <h3>금융 진단</h3>
        <p>
          내 금융 상태를<br />
          쉽게 파악해요.
        </p>
      </div>

      <div class="feature-card panel">
        <div class="feature-icon blue">→</div>
        <h3>성장 로드맵</h3>
        <p>
          비상금부터 투자까지<br />
          순서대로 안내해요.
        </p>
      </div>

      <div class="feature-card panel">
        <div class="feature-icon purple">₩</div>
        <h3>모든 상품</h3>
        <p>
          지금 필요한 금융상품을<br />
          비교해볼 수 있어요.
        </p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'

const isLoggedIn = ref(false)
const username = ref('')
const name = ref('')
const diagnosisResult = ref(null)
const roadmap = ref(null)
const favoriteProducts = ref([])

const fallbackMissions = [
  { title: '목표 금액 설정하기', is_completed: true },
  { title: '월 저축 가능 금액 계산하기', is_completed: true },
  { title: '소비 패턴 분석하기', is_completed: true },
  { title: '월급의 20% 자동저축 설정하기', is_completed: true },
]

const hasDiagnosisResult = computed(() => {
  return diagnosisResult.value !== null
})

const displayName = computed(() => {
  return name.value || username.value || '회원'
})

const rawFinancialType = computed(() => {
  return diagnosisResult.value?.financial_type || '금융 진단 전'
})

const financialTypeIcon = computed(() => {
  const firstToken = rawFinancialType.value.split(' ')[0]
  return firstToken.length <= 2 ? firstToken : '●'
})

const financialTypeName = computed(() => {
  const parts = rawFinancialType.value.split(' ')
  if (parts.length > 1 && parts[0].length <= 2) {
    return parts.slice(1).join(' ')
  }

  return rawFinancialType.value
})

const finpickComment = computed(() => {
  return (
    diagnosisResult.value?.finpick_comment ||
    '금융 진단을 완료하면 나에게 맞는 유형과 코멘트를 확인할 수 있어요.'
  )
})

const dashboardMissions = computed(() => {
  const levels = roadmap.value?.levels || []
  const missions = levels.flatMap((level) => level.missions || [])

  return (missions.length ? missions : fallbackMissions).slice(0, 4)
})

const firstPendingIndex = computed(() => {
  const index = dashboardMissions.value.findIndex((mission) => !mission.is_completed)
  return index === -1 ? dashboardMissions.value.length : index
})

const dashboardProgress = computed(() => {
  if (typeof roadmap.value?.progress === 'number') {
    return roadmap.value.progress
  }

  return hasDiagnosisResult.value ? 100 : 0
})

const roadmapLevel = computed(() => {
  const levels = roadmap.value?.levels || []
  const currentLevel = levels[levels.length - 1]

  if (currentLevel) {
    if (currentLevel.title?.startsWith('Lv.')) {
      return currentLevel.title
    }

    return `Lv.${currentLevel.level} ${currentLevel.title}`
  }

  return hasDiagnosisResult.value ? 'Lv.3 자산 성장' : '진단 전'
})

const nextMissionTitle = computed(() => {
  const nextMission = dashboardMissions.value.find((mission) => !mission.is_completed)
  return nextMission?.title || '비상금 300만원 만들기'
})

const dashboardFavorites = computed(() => {
  return favoriteProducts.value.slice(0, 3)
})

const syncHomeState = () => {
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true'
  username.value = localStorage.getItem('username') || ''
  name.value = localStorage.getItem('name') || ''
  diagnosisResult.value = null

  const savedResult = localStorage.getItem('latestDiagnosisResult')

  if (savedResult) {
    diagnosisResult.value = JSON.parse(savedResult)
  }
}

const loadHomeDashboard = async () => {
  if (!isLoggedIn.value) {
    roadmap.value = null
    favoriteProducts.value = []
    return
  }

  try {
    const [roadmapResponse, favoritesResponse] = await Promise.all([
      axios.get('http://localhost:8000/api/roadmap/', { withCredentials: true }),
      axios.get('http://localhost:8000/api/favorite-deposit-products/', { withCredentials: true }),
    ])

    roadmap.value = roadmapResponse.data.roadmap
    favoriteProducts.value = favoritesResponse.data.products || []
  } catch (err) {
    console.error(err)
  }
}

const refreshHome = async () => {
  syncHomeState()
  await loadHomeDashboard()
}

onMounted(() => {
  refreshHome()
  window.addEventListener('auth-state-changed', refreshHome)
})

onUnmounted(() => {
  window.removeEventListener('auth-state-changed', refreshHome)
})
</script>
