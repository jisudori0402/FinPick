<template>
  <SidebarLayout class="my-page" surface="soft">
    <template #sidebar>
      <AppSidebar>
        <template #top>
      <div class="my-sidebar-mascot" aria-hidden="true">
        <img src="/my-sidebar-character.png" alt="" />
      </div>
        </template>

        <template #nav>
      <nav class="my-side-nav" aria-label="???뺣낫 硫붾돱">
        <button class="active" type="button">
          <span>??</span>
          ???뺣낫
        </button>
        <RouterLink to="/deposit-products?category=favorites">
          <span>狩?</span>
          愿???곹뭹
        </RouterLink>
        <button type="button">
          <span>?뮥</span>
          ???먯궛
        </button>
      </nav>
        </template>

        <template #support>

      <div class="my-tip-card">
        <strong>???섏? 湲덉쑖 ?듦?,<br />FinPick怨??④퍡</strong>
        <RouterLink to="/diagnosis-result">
          ?깆옣 濡쒕뱶留?蹂닿린
          <span>??</span>
        </RouterLink>
      </div>
        </template>
      </AppSidebar>


    </template>

    <div class="my-main">
      <div class="my-page-head">
        <h1>???뺣낫</h1>
        <p>?뚯썝?섏쓽 ?뺣낫瑜??뺤씤?섍퀬 愿由ы븷 ???덉뒿?덈떎.</p>
      </div>

      <div v-if="loading" class="status-box">
        ???뺣낫瑜?遺덈윭?ㅻ뒗 以묒엯?덈떎.
      </div>

      <div v-else class="my-layout">
        <div class="my-left-column">
          <section class="my-card profile-card-main">
            <div class="profile-avatar">
              <img v-if="profileImageSrc" :src="profileImageSrc" alt="?꾨줈???대?吏" />
              <span v-else>{{ avatarInitial }}</span>
              <input
                ref="profileImageInput"
                type="file"
                accept="image/*"
                @change="handleProfileImageChange"
              />
              <button type="button" aria-label="프로필 사진 변경" @click="openProfileImagePicker">?</button>
            </div>

            <div class="profile-summary">
              <h2>{{ displayName }}</h2>
              <p>{{ user.email || '-' }}</p>
              <span>FinPick ?뚯썝</span>
              <small>{{ joinedAt }} 媛??</small>
            </div>

            <div class="profile-stats">
              <div>
                <span>?꾩옱 湲덉쑖 ?덈꺼</span>
                <strong>{{ currentLevel }} {{ financialTypeName }}</strong>
              </div>
              <div>
                <span>濡쒕뱶留?吏꾪뻾瑜?</span>
                <strong>{{ roadmapProgress }}%</strong>
                <div class="mini-progress"><i :style="{ width: roadmapProgress + '%' }"></i></div>
              </div>
            </div>
          </section>

          <section class="my-card financial-type-card">
            <h2>??湲덉쑖 ?좏삎</h2>
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
                  ?먯꽭??蹂닿린
                  <span>??</span>
                </RouterLink>
              </div>
            </div>
          </section>

          <section class="my-card intro-card">
            <div class="card-title-row">
              <h2>???뚭컻</h2>
              <button type="button" aria-label="소개 수정" @click="toggleIntroEdit">?</button>
            </div>
            <textarea
              v-if="isIntroEditing"
              v-model="profileForm.intro"
              rows="4"
              placeholder="?섎? ?뚭컻?섎뒗 臾몄옣???낅젰??二쇱꽭??"
            ></textarea>
            <p v-else>{{ introText }}</p>
            <div v-if="isIntroEditing" class="intro-actions">
              <button type="button" @click="cancelIntroEdit">痍⑥냼</button>
              <button type="button" @click="saveProfile">저장</button>
            </div>
          </section>
        </div>

        <div class="my-right-column">
          <section class="my-card member-info-card">
            <div class="card-title-row">
              <div>
                <h2>?뚯썝 ?뺣낫</h2>
              </div>
              <small>* ?꾩닔 ?낅젰 ??ぉ</small>
            </div>

            <div class="info-form-grid">
              <label>
                <span class="field-label">?대쫫 <em>*</em></span>
                <input v-model="profileForm.name" />
              </label>
              <label>
                <span class="field-label">?앸뀈?붿씪</span>
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
                <span class="field-label">?꾩씠??<em>*</em></span>
                <input v-model="profileForm.username" />
              </label>
              <label>
                <span class="field-label">?대찓??<em>*</em></span>
                <input v-model="profileForm.email" type="email" />
              </label>
              <label>
                <span class="field-label">嫄곗＜ 吏??</span>
                <select v-model="profileForm.region">
                  <option>?쒖슱?밸퀎??</option>
                  <option>寃쎄린??</option>
                  <option>?몄쿇愿묒뿭??</option>
                  <option>遺?곌킅??떆</option>
                  <option>湲고?</option>
                </select>
              </label>
              <label>
                <span class="field-label">吏곸뾽</span>
                <select v-model="profileForm.job">
                  <option>吏곸옣??</option>
                  <option>?숈깮</option>
                  <option>?먯쁺?낆옄</option>
                  <option>?꾨━?쒖꽌</option>
                  <option>湲고?</option>
                </select>
              </label>
            </div>

            <div class="member-actions">
              <span>{{ saveMessage }}</span>
              <button class="primary-btn" type="button" @click="saveProfile">
                ??ν븯湲?
              </button>
            </div>
          </section>

          <section class="my-card password-card">
            <div class="card-title-row">
              <h2>鍮꾨?踰덊샇 蹂寃?</h2>
              <span>??</span>
            </div>

            <div class="password-body">
              <div class="lock-icon">?뵏</div>
              <div>
                <span>留덉?留?蹂寃쎌씪</span>
                <strong>{{ passwordChangedAt }}</strong>
              </div>
              <RouterLink class="password-change-link" to="/password-change">
                鍮꾨?踰덊샇 蹂寃쏀븯湲?
              </RouterLink>
            </div>

            <p>?덉쟾??怨꾩젙 蹂댄샇瑜??꾪빐 二쇨린?곸쑝濡?鍮꾨?踰덊샇瑜?蹂寃쏀빐 二쇱꽭??</p>
          </section>
        </div>
      </div>
    </div>
  </SidebarLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '../services/api'
import AppSidebar from '../components/AppSidebar.vue'
import SidebarLayout from '../components/SidebarLayout.vue'

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
const passwordChangedAt = ref(localStorage.getItem('passwordChangedAt') || '蹂寃??대젰 ?놁쓬')
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
  region: '서울',
  job: '직장인',
  intro: '',
})

const typeCopy = {
  default: {
    icon: 'F',
    description: '진단 결과에 맞춰 금융 습관을 관리해보세요.',
  },
}

const typeCharacterImages = {
  default: '/financial-types/stable-saver.png',
}

const displayName = computed(() => {
  return user.value.name || user.value.username || 'FinPick ?뚯썝'
})

const avatarInitial = computed(() => {
  return displayName.value.slice(0, 1).toUpperCase()
})

const profileImageSrc = computed(() => profile.value.profile_image_url || '')

const joinedAt = computed(() => {
  return profile.value.created_at || '2024.03.15'
})

const financialTypeName = computed(() => {
  return (diagnosisResult.value?.financial_type || '湲덉쑖 ?덉떦').replace(/^[^\s]+\s*/, '')
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
  return Object.keys(typeCopy).find((key) => name.includes(key)) || 'default'
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

  const income = profile.value.monthly_income ? `월 소득 ${profile.value.monthly_income}만원` : '소득 정보 준비 중'
  const saving = profile.value.saving_status || '저축 습관을 만드는 중'
  return `${income}, ${saving}. 차근차근 자산을 키워가고 있어요.`
})

const syncProfileForm = () => {
  profileForm.value.name = user.value.name || user.value.username || ''
  profileForm.value.username = user.value.username || ''
  profileForm.value.email = user.value.email || ''
  profileForm.value.birth_date = profile.value.birth_date || ''
  profileForm.value.job = profile.value.job || '직장인'
  profileForm.value.region = profile.value.residence_type || '서울'
  profileForm.value.intro = profile.value.intro || introText.value
}

const loadDashboard = async () => {
  loading.value = true

  try {
    const response = await axios.get(`${API_BASE_URL}/api/dashboard/`, {
      withCredentials: true,
    })

    user.value = {
      ...response.data.user,
      name: response.data.user?.name || response.data.user?.username || '',
    }
    profile.value = response.data.profile
    passwordChangedAt.value = response.data.profile?.password_changed_at || '蹂寃??대젰 ?놁쓬'
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
    const response = await axios.get(`${API_BASE_URL}/api/roadmap/`, {
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
      `${API_BASE_URL}/api/profile/`,
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
    saveMessage.value = '?뚯썝 ?뺣낫媛 蹂寃쎈릺?덉뒿?덈떎.'
    isIntroEditing.value = false
    syncProfileForm()
  } catch (err) {
    saveMessage.value = err.response?.data?.message || '?뚯썝 ?뺣낫瑜???ν븯吏 紐삵뻽?듬땲??'
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
    const response = await axios.post(`${API_BASE_URL}/api/profile/`, formData, {
      withCredentials: true,
    })

    profile.value = {
      ...profile.value,
      profile_image_url: response.data.profile?.profile_image_url || '',
    }
    saveMessage.value = '?꾨줈???대?吏媛 蹂寃쎈릺?덉뒿?덈떎.'
  } catch (err) {
    saveMessage.value = err.response?.data?.message || '?꾨줈???대?吏瑜???ν븯吏 紐삵뻽?듬땲??'
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


