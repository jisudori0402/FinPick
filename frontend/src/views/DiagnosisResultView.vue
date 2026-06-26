<template>
  <section class="diagnosis-result-container">
    <div v-if="!result" class="no-result-panel">
      <h2>吏꾨떒 寃곌낵媛 ?놁뒿?덈떎</h2>
      <p>湲덉쑖 吏꾨떒???듯빐 ?섏쓽 湲덉쑖 ?깊뼢???뚯븘蹂댁꽭??</p>
      <RouterLink class="primary-btn" to="/diagnosis">
        湲덉쑖 吏꾨떒?섎윭 媛湲?
      </RouterLink>
    </div>

    <div v-else class="result-wrapper">
      <div class="result-hero">
        <div>
          <p class="result-eyebrow">?럦 吏꾨떒???꾨즺?섏뿀?댁슂!</p>
          <span class="result-kicker">?뱀떊??湲덉쑖 ?깆옣 ?덈꺼?</span>
          <h1>
            <span v-if="resultLevel">{{ resultLevel }}</span>
            <span v-else class="level-loading">?덈꺼 ?뺤씤 以?</span>
            {{ resultName }}
          </h1>
          <p>{{ result.intro }}</p>
        </div>

        <div class="result-mascot" aria-hidden="true">
          <img src="/diagnosis-result-character.png" alt="" />
        </div>
      </div>

      <div class="result-dashboard">
        <div class="result-card readiness-section">
          <div class="card-title-row">
            <h2>금융 건강도</h2>
            <span class="info-tooltip" tabindex="0">
              i
              <span class="tooltip-bubble">
                吏꾨떒 ?듬????異??듦?, ?뚮퉬 愿由? ?ъ옄 以鍮꾨룄, 紐⑺몴 紐낇솗?꾨? 100??湲곗??쇰줈 ?섏궛???먯닔?덉슂.
              </span>
            </span>
          </div>

          <div class="readiness-body">
            <div class="readiness-circle">
              <svg class="circle-chart" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="43" class="circle-bg" />
                <circle
                  cx="50"
                  cy="50"
                  r="43"
                  class="circle-fill"
                  :style="{ 'stroke-dasharray': `${readinessCircle} ${circleCircumference}` }"
                />
              </svg>
              <div class="circle-text">
                <span class="score">{{ result.readiness_score }}</span>
                <span class="label">(100??留뚯젏)</span>
              </div>
            </div>

            <div class="profile-bars">
              <div v-for="item in profileScoreItems" :key="item.label" class="profile-bar-row">
                <span class="profile-icon">{{ item.icon }}</span>
                <div>
                  <div class="bar-label">
                    <strong>{{ item.label }}</strong>
                    <span>{{ item.score }}??</span>
                  </div>
                  <div class="mini-bar">
                    <span :style="{ width: item.percent + '%' }"></span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="readiness-comment">
            <span class="quote-mark">??</span>
            <div>
              <h2>FinPick 肄붾찘??</h2>
              <p>{{ result.finpick_comment }}</p>
            </div>
          </div>
        </div>

        <div class="result-card type-card">
          <div class="card-title-row">
            <h2>?섏쓽 湲덉쑖 ?좏삎</h2>
            <span class="info-tooltip" tabindex="0">
              i
              <span class="tooltip-bubble">
                ?뚮뱷怨?吏異?洹좏삎, ?異??곹깭, ?ъ옄 寃쏀뿕, 湲덉쑖 紐⑺몴 ?듬???醫낇빀??媛??媛源뚯슫 ?좏삎?쇰줈 遺꾨쪟?댁슂.
              </span>
            </span>
          </div>

          <div class="type-avatar type-character-avatar">
            <img
              v-if="typeImageSrc"
              :src="typeImageSrc"
              :alt="`${resultName} 캐릭터`"
              @error="markTypeImageError"
            />
            <span v-else>{{ typeIcon }}</span>
          </div>
          <strong>{{ resultName }}</strong>
          <p>{{ typeDescription }}</p>

          <div class="type-tags">
            <span v-for="tag in typeTags" :key="tag">{{ tag }}</span>
          </div>
        </div>

        <div class="result-card insight-card strengths-card">
          <h2>媛뺤젏</h2>
          <ul class="insight-list">
            <li v-for="item in result.strengths" :key="item">
              <span>??</span>
              {{ item }}
            </li>
          </ul>
        </div>

        <div class="result-card insight-card improvements-card">
          <h2>蹂댁셿??</h2>
          <ul class="insight-list">
            <li v-for="item in result.improvements" :key="item">
              <span>!</span>
              {{ item }}
            </li>
          </ul>
        </div>
      </div>

      <div class="result-actions">
        <RouterLink class="primary-btn" to="/roadmap">
          湲덉쑖 ?깆옣 濡쒕뱶留?蹂닿린
          <span aria-hidden="true">??</span>
        </RouterLink>
        <RouterLink class="secondary-btn" to="/diagnosis">
          吏꾨떒 ?ㅼ떆?섍린
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '../services/api'

const result = ref(null)
const roadmap = ref(null)
const typeImageErrors = ref({})
const circleCircumference = 2 * Math.PI * 43

const profileIcons = {
  '저축 습관': 'S',
  '소비 관리': 'C',
  '투자 성향': 'I',
  '자산 관리': 'A',
}

const typeCopy = {
  default: {
    icon: 'F',
    description: '진단 결과를 바탕으로 금융 습관을 점검해보세요.',
    tags: ['진단', '로드맵', '추천'],
  },
}

const typeCharacterImages = {
  default: '/financial-types/stable-saver.png',
}

const resultLevel = computed(() => {
  const roadmapLevelLabel = getRoadmapLevelLabel()
  if (roadmapLevelLabel) {
    return roadmapLevelLabel
  }

  return ''
})

const matchedType = computed(() => {
  const name = resultName.value
  return Object.keys(typeCopy).find((key) => name.includes(key)) || 'default'
})

const typeImageSrc = computed(() => {
  if (typeImageErrors.value[matchedType.value]) {
    return ''
  }
  return typeCharacterImages[matchedType.value] || ''
})

const markTypeImageError = () => {
  typeImageErrors.value = {
    ...typeImageErrors.value,
    [matchedType.value]: true,
  }
}

const typeDescription = computed(() => {
  return typeCopy[matchedType.value].description
})

const typeTags = computed(() => {
  return typeCopy[matchedType.value].tags
})

const countFilledStars = (value) => {
  if (typeof value === 'number') {
    return value
  }

    if (typeof value === 'string') {
      const matches = value.match(/★/g)
      return matches ? matches.length : parseInt(value) || 0
    }

  return 0
}

const profileScoreItems = computed(() => {
  if (!result.value?.profile_scores) {
    return []
  }

  return Object.entries(result.value.profile_scores).map(([label, stars]) => {
    const filledStars = countFilledStars(stars)
    const score = Math.min(100, Math.max(0, filledStars * 20))

    return {
      label,
      score,
      percent: score,
      icon: profileIcons[label] || '?',
    }
  })
})


const loadLatestDiagnosis = async () => {
  const savedResult = localStorage.getItem('latestDiagnosisResult')

  if (savedResult) {
    try {
      result.value = JSON.parse(savedResult)
    } catch {
      localStorage.removeItem('latestDiagnosisResult')
    }
  }

  try {
    const response = await axios.get(`${API_BASE_URL}/api/diagnosis/latest/`, {
      withCredentials: true,
    })

    if (response.data.result) {
      result.value = response.data.result
      localStorage.setItem('latestDiagnosisResult', JSON.stringify(response.data.result))
      window.dispatchEvent(new Event('auth-state-changed'))
    }
  } catch (err) {
    console.error(err)
  }
}

const loadCachedRoadmap = () => {
  const savedRoadmap = localStorage.getItem('latestRoadmap')

  if (!savedRoadmap) {
    return
  }

  try {
    roadmap.value = JSON.parse(savedRoadmap)
  } catch {
    localStorage.removeItem('latestRoadmap')
  }
}

const loadRoadmap = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/roadmap/`, {
      withCredentials: true,
    })

    roadmap.value = response.data.roadmap
    localStorage.setItem('latestRoadmap', JSON.stringify(response.data.roadmap))
  } catch (err) {
    console.error(err)
  }
}

onMounted(async () => {
  loadCachedRoadmap()
  await Promise.all([loadLatestDiagnosis(), loadRoadmap()])
})
</script>



