<template>
  <section class="my-page">
    <aside class="my-sidebar">
      <nav class="my-side-nav" aria-label="내 정보 메뉴">
        <button class="active" type="button">
          <span>♙</span>
          내 정보
        </button>
        <button type="button">
          <span>▣</span>
          내 금융 현황
        </button>
        <button type="button">
          <span>♡</span>
          관심 목록
        </button>
        <button type="button">
          <span>☑</span>
          활동 내역
        </button>
      </nav>

      <div class="my-tip-card">
        <strong>더 나은 금융 습관,<br />FinPick과 함께</strong>
        <RouterLink to="/diagnosis-result">
          성장 로드맵 보기
          <span>→</span>
        </RouterLink>
      </div>

      <div class="profile-mascot" aria-hidden="true">
        <span></span>
        <strong>₩</strong>
      </div>
    </aside>

    <div class="my-main">
      <div class="my-page-head">
        <h1>내 정보</h1>
        <p>회원님의 정보를 확인하고 관리할 수 있습니다.</p>
      </div>

      <div v-if="loading" class="status-box">
        내 정보를 불러오는 중입니다.
      </div>

      <div v-else class="my-layout">
        <div class="my-left-column">
          <section class="my-card profile-card-main">
            <div class="profile-avatar">
              <span>{{ avatarInitial }}</span>
              <button type="button" aria-label="프로필 사진 변경">⌘</button>
            </div>

            <div class="profile-summary">
              <h2>{{ displayName }}</h2>
              <p>{{ user.email || '-' }}</p>
              <span>FinPick 회원</span>
              <small>{{ joinedAt }} 가입</small>
            </div>

            <div class="profile-stats">
              <div>
                <span>현재 금융 레벨</span>
                <strong>{{ currentLevel }} {{ financialTypeName }}</strong>
              </div>
              <div>
                <span>로드맵 진행률</span>
                <strong>{{ roadmapProgress }}%</strong>
                <div class="mini-progress"><i :style="{ width: roadmapProgress + '%' }"></i></div>
              </div>
            </div>
          </section>

          <section class="my-card financial-type-card">
            <h2>내 금융 유형</h2>
            <div class="financial-type-body">
              <div class="type-emoji type-character-thumb">
                <img
                  v-if="financialTypeImageSrc"
                  :src="financialTypeImageSrc"
                  :alt="`${financialTypeName} 캐릭터`"
                  @error="markFinancialTypeImageError"
                />
                <span v-else>{{ financialTypeIcon }}</span>
              </div>
              <div>
                <strong>{{ financialTypeName }}</strong>
                <p>{{ financialTypeDescription }}</p>
                <RouterLink to="/diagnosis-result">
                  자세히 보기
                  <span>→</span>
                </RouterLink>
              </div>
            </div>
          </section>

          <section class="my-card intro-card">
            <div class="card-title-row">
              <h2>내 소개</h2>
              <button type="button" aria-label="내 소개 수정">✎</button>
            </div>
            <p>{{ introText }}</p>
          </section>
        </div>

        <div class="my-right-column">
          <section class="my-card member-info-card">
            <div class="card-title-row">
              <div>
                <h2>회원 정보</h2>
              </div>
              <small>* 필수 입력 항목</small>
            </div>

            <div class="info-form-grid">
              <label>
                이름 <em>*</em>
                <input v-model="profileForm.name" />
              </label>
              <label>
                이메일 <em>*</em>
                <input v-model="profileForm.email" />
              </label>
              <label class="full">
                닉네임 <em>*</em>
                <input v-model="profileForm.nickname" />
              </label>
              <label class="phone-row">
                휴대폰 번호
                <div>
                  <input v-model="profileForm.phone" />
                  <button type="button">변경</button>
                </div>
              </label>
              <label>
                생년월일
                <input v-model="profileForm.birth_date" type="date" />
              </label>
              <fieldset>
                <legend>성별</legend>
                <label>
                  <input v-model="profileForm.gender" type="radio" value="male" />
                  남성
                </label>
                <label>
                  <input v-model="profileForm.gender" type="radio" value="female" />
                  여성
                </label>
              </fieldset>
              <label>
                거주 지역
                <select v-model="profileForm.region">
                  <option>서울특별시</option>
                  <option>경기도</option>
                  <option>인천광역시</option>
                  <option>부산광역시</option>
                  <option>기타</option>
                </select>
              </label>
              <label>
                직업
                <select v-model="profileForm.job">
                  <option>직장인</option>
                  <option>학생</option>
                  <option>자영업자</option>
                  <option>프리랜서</option>
                  <option>기타</option>
                </select>
              </label>
            </div>

            <div class="member-actions">
              <span>{{ saveMessage }}</span>
              <button class="primary-btn" type="button" @click="saveProfilePreview">
                저장하기
              </button>
            </div>
          </section>

          <section class="my-card password-card">
            <div class="card-title-row">
              <h2>비밀번호 변경</h2>
              <span>⌃</span>
            </div>

            <div class="password-body">
              <div class="lock-icon">▢</div>
              <div>
                <span>마지막 변경일</span>
                <strong>{{ passwordChangedAt }}</strong>
              </div>
              <RouterLink class="password-change-link" to="/password-change">
                비밀번호 변경하기
              </RouterLink>
            </div>

            <p>안전한 계정 보호를 위해 주기적으로 비밀번호를 변경해 주세요.</p>
          </section>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'

const user = ref({
  username: '',
  email: '',
  name: '',
})

const profile = ref({
  age: '',
  job: '',
  monthly_income: '',
  monthly_expense: '',
  residence_type: '',
  saving_status: '',
  invest_experience: '',
  birth_date: '',
  created_at: '',
})

const diagnosisResult = ref(null)
const roadmap = ref(null)
const typeImageErrors = ref({})
const loading = ref(true)
const saveMessage = ref('')
const passwordChangedAt = ref(localStorage.getItem('passwordChangedAt') || '변경 이력 없음')

const profileForm = ref({
  name: '',
  email: '',
  nickname: '',
  phone: '010-1234-5678',
  birth_date: '',
  gender: 'male',
  region: '서울특별시',
  job: '직장인',
})

const typeCopy = {
  안정형: {
    icon: '🐢',
    description: '차분하게 모으고 지키는 데 강한 유형이에요.',
  },
  계획형: {
    icon: '🐿',
    description: '목표를 세우고 꾸준히 자금을 모으는 유형이에요.',
  },
  소비러: {
    icon: '🦊',
    description: '소비 관리 감각이 있고 균형 잡힌 선택을 잘해요.',
  },
  투자러: {
    icon: '🐯',
    description: '성장을 위해 투자 지식을 넓혀가면 좋아요.',
  },
  점검러: {
    icon: '🐻',
    description: '재정 흐름을 점검하며 기초를 탄탄히 만들면 좋아요.',
  },
  자산러: {
    icon: '🦁',
    description: '자산을 키우는 감각이 있고 리스크 관리가 중요해요.',
  },
}

const typeCharacterImages = {
  안정형: '/financial-types/stable-saver.png',
  계획형: '/financial-types/planner-saver.png',
  소비러: '/financial-types/smart-spender.png',
  투자러: '/financial-types/growth-investor.png',
  점검러: '/financial-types/finance-checker.png',
  자산러: '/financial-types/aggressive-asset.png',
}

const displayName = computed(() => {
  return user.value.name || user.value.username || 'FinPick 회원'
})

const avatarInitial = computed(() => {
  return displayName.value.slice(0, 1).toUpperCase()
})

const joinedAt = computed(() => {
  return profile.value.created_at || '2024.03.15'
})

const financialTypeName = computed(() => {
  return (diagnosisResult.value?.financial_type || '금융 새싹').replace(/^[^\s]+\s*/, '')
})

const getRoadmapLevelLabel = () => {
  if (roadmap.value?.current_level_label) {
    return roadmap.value.current_level_label
  }

  if (typeof roadmap.value?.current_level === 'number') {
    return `Lv.${roadmap.value.current_level}`
  }

  const levels = roadmap.value?.levels || []
  const currentLevel = levels.find((level) => {
    if (level.is_locked) {
      return false
    }

    const missions = level.missions || []
    return missions.some((mission) => !mission.is_completed)
  })

  if (currentLevel?.level) {
    return `Lv.${currentLevel.level}`
  }

  const maxLevel = Math.max(...levels.map((level) => Number(level.level) || 0))
  return maxLevel > 0 ? `Lv.${maxLevel}` : ''
}

const currentLevel = computed(() => {
  const roadmapLevelLabel = getRoadmapLevelLabel()
  if (roadmapLevelLabel) {
    return roadmapLevelLabel
  }

  const score = diagnosisResult.value?.readiness_score || 0

  if (score >= 85) {
    return 'Lv.4'
  }

  if (score >= 70) {
    return 'Lv.3'
  }

  if (score >= 50) {
    return 'Lv.2'
  }

  return 'Lv.1'
})

const roadmapProgress = computed(() => {
  if (typeof roadmap.value?.progress === 'number') {
    return roadmap.value.progress
  }

  return 0
})

const matchedType = computed(() => {
  const name = financialTypeName.value
  return Object.keys(typeCopy).find((key) => name.includes(key)) || '계획형'
})

const financialTypeIcon = computed(() => typeCopy[matchedType.value].icon)
const financialTypeImageSrc = computed(() => {
  if (typeImageErrors.value[matchedType.value]) {
    return ''
  }

  return typeCharacterImages[matchedType.value] || ''
})
const financialTypeDescription = computed(() => typeCopy[matchedType.value].description)

const markFinancialTypeImageError = () => {
  typeImageErrors.value = {
    ...typeImageErrors.value,
    [matchedType.value]: true,
  }
}

const introText = computed(() => {
  const income = profile.value.monthly_income ? `월 소득 ${profile.value.monthly_income}만원` : '소득 정보를 준비 중'
  const saving = profile.value.saving_status || '저축 습관을 만들어가는 중'
  return `${income}, ${saving}. 차근차근 자산을 키워가고 있어요.`
})

const syncProfileForm = () => {
  profileForm.value.name = user.value.name || user.value.username || ''
  profileForm.value.email = user.value.email || ''
  profileForm.value.nickname = displayName.value
  profileForm.value.birth_date = profile.value.birth_date || ''
  profileForm.value.job = profile.value.job || '직장인'
  profileForm.value.region = profile.value.residence_type || '서울특별시'
}

const loadDiagnosisResult = async () => {
  const savedResult = localStorage.getItem('latestDiagnosisResult')

  if (savedResult) {
    diagnosisResult.value = JSON.parse(savedResult)
    return
  }

  try {
    const response = await axios.get('http://localhost:8000/api/diagnosis/latest/', {
      withCredentials: true,
    })

    if (response.data.result) {
      diagnosisResult.value = response.data.result
      localStorage.setItem('latestDiagnosisResult', JSON.stringify(response.data.result))
    }
  } catch (err) {
    console.error(err)
  }
}

const loadDashboard = async () => {
  loading.value = true

  try {
    const response = await axios.get('http://localhost:8000/api/dashboard/', {
      withCredentials: true,
    })

    user.value = {
      ...response.data.user,
      name: response.data.user?.name || response.data.user?.username || '',
    }
    profile.value = response.data.profile
    passwordChangedAt.value = response.data.profile?.password_changed_at || '변경 이력 없음'
    if (response.data.profile?.password_changed_at) {
      localStorage.setItem('passwordChangedAt', response.data.profile.password_changed_at)
    } else {
      localStorage.removeItem('passwordChangedAt')
    }
    syncProfileForm()
  } catch (err) {
    console.error(err)

    user.value = {
      username: localStorage.getItem('username') || '',
      email: localStorage.getItem('email') || '',
      name: localStorage.getItem('username') || '',
    }
    syncProfileForm()
  } finally {
    loading.value = false
  }
}

const loadRoadmap = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/roadmap/', {
      withCredentials: true,
    })

    roadmap.value = response.data.roadmap
  } catch (err) {
    console.error(err)
  }
}

const saveProfilePreview = () => {
  saveMessage.value = '프로필 저장 기능은 다음 단계에서 연결할 예정입니다.'
}

onMounted(async () => {
  await Promise.all([loadDashboard(), loadDiagnosisResult(), loadRoadmap()])
})
</script>
