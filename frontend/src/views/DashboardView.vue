<template>
  <section class="my-page">
    <aside class="my-sidebar">
      <nav class="my-side-nav" aria-label="내 정보 메뉴">
        <button class="active" type="button">
          <span>♙</span>
          내 정보
        </button>
        <RouterLink to="/deposit-products?category=favorites">
          <span>☆</span>
          관심 상품
        </RouterLink>
        <button type="button">
          <span>💰</span>
          내 자산
        </button>
      </nav>

      <div class="my-tip-card">
        <strong>더 나은 금융 습관,<br />FinPick과 함께</strong>
        <RouterLink to="/diagnosis-result">
          성장 로드맵 보기
          <span>→</span>
        </RouterLink>
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
              <img v-if="profileImageSrc" :src="profileImageSrc" alt="프로필 이미지" />
              <span v-else>{{ avatarInitial }}</span>
              <input
                ref="profileImageInput"
                type="file"
                accept="image/*"
                @change="handleProfileImageChange"
              />
              <button type="button" aria-label="프로필 사진 변경" @click="openProfileImagePicker">⌘</button>
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
              <button type="button" aria-label="내 소개 수정" @click="toggleIntroEdit">✎</button>
            </div>
            <textarea
              v-if="isIntroEditing"
              v-model="profileForm.intro"
              rows="4"
              placeholder="나를 소개하는 문장을 입력해 주세요."
            ></textarea>
            <p v-else>{{ introText }}</p>
            <div v-if="isIntroEditing" class="intro-actions">
              <button type="button" @click="cancelIntroEdit">취소</button>
              <button type="button" @click="saveProfile">저장</button>
            </div>
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
                <span class="field-label">이름 <em>*</em></span>
                <input v-model="profileForm.name" />
              </label>
              <label>
                <span class="field-label">생년월일</span>
                <div class="date-segment-input">
                  <input
                    ref="profileBirthYearInput"
                    v-model="profileBirthYear"
                    inputmode="numeric"
                    maxlength="4"
                    placeholder="YYYY"
                    @input="handleProfileBirthPartInput('year')"
                  />
                  <span>/</span>
                  <input
                    ref="profileBirthMonthInput"
                    v-model="profileBirthMonth"
                    inputmode="numeric"
                    maxlength="2"
                    placeholder="MM"
                    @input="handleProfileBirthPartInput('month')"
                  />
                  <span>/</span>
                  <input
                    ref="profileBirthDayInput"
                    v-model="profileBirthDay"
                    inputmode="numeric"
                    maxlength="2"
                    placeholder="DD"
                    @input="handleProfileBirthPartInput('day')"
                  />
                </div>
              </label>
              <label>
                <span class="field-label">아이디 <em>*</em></span>
                <input v-model="profileForm.username" />
              </label>
              <label>
                <span class="field-label">이메일 <em>*</em></span>
                <input v-model="profileForm.email" type="email" />
              </label>
              <label>
                <span class="field-label">거주 지역</span>
                <select v-model="profileForm.region">
                  <option>서울특별시</option>
                  <option>경기도</option>
                  <option>인천광역시</option>
                  <option>부산광역시</option>
                  <option>기타</option>
                </select>
              </label>
              <label>
                <span class="field-label">직업</span>
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
              <button class="primary-btn" type="button" @click="saveProfile">
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
              <div class="lock-icon">🔒</div>
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
  profile_image_url: '',
})

const diagnosisResult = ref(null)
const roadmap = ref(null)
const typeImageErrors = ref({})
const loading = ref(true)
const saveMessage = ref('')
const isIntroEditing = ref(false)
const passwordChangedAt = ref(localStorage.getItem('passwordChangedAt') || '변경 이력 없음')
const profileBirthYear = ref('')
const profileBirthMonth = ref('')
const profileBirthDay = ref('')
const profileBirthYearInput = ref(null)
const profileBirthMonthInput = ref(null)
const profileBirthDayInput = ref(null)
const profileImageInput = ref(null)

const profileForm = ref({
  name: '',
  username: '',
  email: '',
  birth_date: '',
  region: '서울특별시',
  job: '직장인',
  intro: '',
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

const profileImageSrc = computed(() => profile.value.profile_image_url || '')

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
  if (profile.value.intro) {
    return profile.value.intro
  }

  const income = profile.value.monthly_income ? `월 소득 ${profile.value.monthly_income}만원` : '소득 정보를 준비 중'
  const saving = profile.value.saving_status || '저축 습관을 만들어가는 중'
  return `${income}, ${saving}. 차근차근 자산을 키워가고 있어요.`
})

const syncProfileForm = () => {
  profileForm.value.name = user.value.name || user.value.username || ''
  profileForm.value.username = user.value.username || ''
  profileForm.value.email = user.value.email || ''
  profileForm.value.birth_date = profile.value.birth_date || ''
  profileForm.value.job = profile.value.job || '직장인'
  profileForm.value.region = profile.value.residence_type || '서울특별시'
  profileForm.value.intro = profile.value.intro || introText.value
  syncProfileBirthParts()
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
const saveProfile = async () => {
  saveMessage.value = ''
  syncProfileBirthDate()

  const formData = new FormData()
  formData.append('name', profileForm.value.name)
  formData.append('username', profileForm.value.username)
  formData.append('email', profileForm.value.email)
  formData.append('birth_date', profileForm.value.birth_date)
  formData.append('job', profileForm.value.job)
  formData.append('residence_type', profileForm.value.region)
  formData.append('intro', profileForm.value.intro)

  try {
    const response = await axios.post(
      'http://localhost:8000/api/profile/',
      formData,
      {
        withCredentials: true,
      },
    )

    user.value = {
      ...user.value,
      name: response.data.profile?.name || profileForm.value.name,
      username: response.data.profile?.username || profileForm.value.username,
      email: response.data.profile?.email || profileForm.value.email,
    }
    localStorage.setItem('username', user.value.username)
    localStorage.setItem('email', user.value.email)
    profile.value = {
      ...profile.value,
      birth_date: response.data.profile?.birth_date || '',
      age: response.data.profile?.age || '',
      job: response.data.profile?.job || '',
      residence_type: response.data.profile?.residence_type || '',
      intro: response.data.profile?.intro || '',
      profile_image_url: response.data.profile?.profile_image_url || profile.value.profile_image_url || '',
    }
    saveMessage.value = '회원 정보가 변경되었습니다.'
    isIntroEditing.value = false
    syncProfileForm()
  } catch (err) {
    saveMessage.value = err.response?.data?.message || '회원 정보를 저장하지 못했습니다.'
    console.error(err)
  }
}

const openProfileImagePicker = () => {
  profileImageInput.value?.click()
}

const uploadProfileImage = async (file) => {
  saveMessage.value = ''
  syncProfileBirthDate()

  const formData = new FormData()
  formData.append('name', profileForm.value.name)
  formData.append('username', profileForm.value.username)
  formData.append('email', profileForm.value.email)
  formData.append('birth_date', profileForm.value.birth_date)
  formData.append('job', profileForm.value.job)
  formData.append('residence_type', profileForm.value.region)
  formData.append('intro', profileForm.value.intro)
  formData.append('profile_image', file)

  try {
    const response = await axios.post('http://localhost:8000/api/profile/', formData, {
      withCredentials: true,
    })

    profile.value = {
      ...profile.value,
      profile_image_url: response.data.profile?.profile_image_url || '',
    }
    saveMessage.value = '프로필 이미지가 변경되었습니다.'
  } catch (err) {
    saveMessage.value = err.response?.data?.message || '프로필 이미지를 저장하지 못했습니다.'
    console.error(err)
  }
}

const handleProfileImageChange = async (event) => {
  const file = event.target.files?.[0]
  if (!file) {
    return
  }

  await uploadProfileImage(file)
  event.target.value = ''
}

const syncProfileBirthParts = () => {
  const [year = '', month = '', day = ''] = (profileForm.value.birth_date || '').split('-')
  profileBirthYear.value = year
  profileBirthMonth.value = month
  profileBirthDay.value = day
}

const syncProfileBirthDate = () => {
  const year = profileBirthYear.value
  const month = profileBirthMonth.value
  const day = profileBirthDay.value
  profileForm.value.birth_date = year && month && day
    ? `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
    : ''
}

const handleProfileBirthPartInput = (part) => {
  profileBirthYear.value = profileBirthYear.value.replace(/\D/g, '').slice(0, 4)
  profileBirthMonth.value = profileBirthMonth.value.replace(/\D/g, '').slice(0, 2)
  profileBirthDay.value = profileBirthDay.value.replace(/\D/g, '').slice(0, 2)
  syncProfileBirthDate()

  if (part === 'year' && profileBirthYear.value.length === 4) {
    profileBirthMonthInput.value?.focus()
  }

  if (part === 'month' && profileBirthMonth.value.length === 2) {
    profileBirthDayInput.value?.focus()
  }
}

const toggleIntroEdit = () => {
  isIntroEditing.value = true
  profileForm.value.intro = profile.value.intro || introText.value
}

const cancelIntroEdit = () => {
  isIntroEditing.value = false
  profileForm.value.intro = profile.value.intro || introText.value
}

onMounted(async () => {
  await Promise.all([loadDashboard(), loadDiagnosisResult(), loadRoadmap()])
})
</script>
