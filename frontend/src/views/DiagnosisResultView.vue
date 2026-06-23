<template>
  <section class="diagnosis-result-container">
    <div v-if="!result" class="no-result-panel">
      <h2>진단 결과가 없습니다</h2>
      <p>금융 진단을 통해 나의 금융 성향을 알아보세요.</p>
      <RouterLink class="primary-btn" to="/diagnosis">
        금융 진단하러 가기
      </RouterLink>
    </div>

    <div v-else class="result-wrapper">
      <div class="result-hero">
        <div>
          <p class="result-eyebrow">🎉 진단이 완료되었어요!</p>
          <span class="result-kicker">당신의 금융 성장 레벨은</span>
          <h1>{{ resultLevel }} {{ resultName }}</h1>
          <p>{{ result.intro }}</p>
        </div>

        <div class="result-mascot" aria-hidden="true">
          <span class="leaf left"></span>
          <span class="leaf right"></span>
          <strong>•</strong>
        </div>
      </div>

      <div class="result-dashboard">
        <div class="result-card readiness-section">
          <div class="card-title-row">
            <h2>금융 건강도</h2>
            <span class="info-dot">i</span>
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
                <span class="label">(100점 만점)</span>
              </div>
            </div>

            <div class="profile-bars">
              <div v-for="item in profileScoreItems" :key="item.label" class="profile-bar-row">
                <span class="profile-icon">{{ item.icon }}</span>
                <div>
                  <div class="bar-label">
                    <strong>{{ item.label }}</strong>
                    <span>{{ item.score }}점</span>
                  </div>
                  <div class="mini-bar">
                    <span :style="{ width: item.percent + '%' }"></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="result-card type-card">
          <div class="card-title-row">
            <h2>나의 금융 유형</h2>
            <span class="info-dot">i</span>
          </div>

          <div class="type-avatar">{{ typeIcon }}</div>
          <strong>{{ resultName }}</strong>
          <p>{{ typeDescription }}</p>

          <div class="type-tags">
            <span v-for="tag in typeTags" :key="tag">{{ tag }}</span>
          </div>
        </div>

        <div class="result-card insight-card strengths-card">
          <h2>강점</h2>
          <ul class="insight-list">
            <li v-for="item in result.strengths" :key="item">
              <span>✓</span>
              {{ item }}
            </li>
          </ul>
        </div>

        <div class="result-card insight-card improvements-card">
          <h2>보완점</h2>
          <ul class="insight-list">
            <li v-for="item in result.improvements" :key="item">
              <span>!</span>
              {{ item }}
            </li>
          </ul>
        </div>
      </div>

      <div class="result-card comment-section">
        <span class="quote-mark">“</span>
        <div>
          <h2>FinPick 코멘트</h2>
          <p>{{ result.finpick_comment }}</p>
        </div>
      </div>

      <div class="result-actions">
        <RouterLink class="primary-btn" to="/roadmap">
          금융 성장 로드맵 보기
          <span aria-hidden="true">→</span>
        </RouterLink>
        <RouterLink class="secondary-btn" to="/diagnosis">
          진단 다시하기
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'

const result = ref(null)
const circleCircumference = 2 * Math.PI * 43

const profileIcons = {
  '저축 습관': '💗',
  '소비 관리': '💳',
  '투자 성향': '📈',
  '자산 관리': '🏦',
}

const typeCopy = {
  안정형: {
    icon: '🐢',
    description: '차분하게 모으고 지키는 데 강한 타입이에요.',
    tags: ['꾸준저축', '안정선호', '계획형'],
  },
  계획형: {
    icon: '🐿',
    description: '목표를 정하고 단계별로 모으는 데 능숙해요.',
    tags: ['목표지향', '계획관리', '목돈형'],
  },
  소비러: {
    icon: '🦊',
    description: '생활 소비를 똑똑하게 조절할 수 있는 타입이에요.',
    tags: ['소비관리', '실속형', '균형감'],
  },
  투자러: {
    icon: '🐯',
    description: '성장을 위해 금융 지식을 넓히면 더 좋아요.',
    tags: ['성장형', '투자관심', '도전형'],
  },
  점검러: {
    icon: '🐻',
    description: '현재 흐름을 점검하고 기초를 다지면 안정적이에요.',
    tags: ['재정점검', '기초관리', '회복형'],
  },
  자산러: {
    icon: '🦁',
    description: '자산을 키우는 감각이 있고 리스크 관리가 중요해요.',
    tags: ['공격형', '자산성장', '리스크관리'],
  },
}

const readinessCircle = computed(() => {
  if (!result.value?.readiness_score) {
    return 0
  }

  return (result.value.readiness_score / 100) * circleCircumference
})

const resultName = computed(() => {
  return (result.value?.financial_type || '금융 새싹').replace(/^[^\s]+\s*/, '')
})

const resultLevel = computed(() => {
  const score = result.value?.readiness_score || 0

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

const matchedType = computed(() => {
  const name = resultName.value
  return Object.keys(typeCopy).find((key) => name.includes(key)) || '계획형'
})

const typeIcon = computed(() => {
  return typeCopy[matchedType.value].icon
})

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
      icon: profileIcons[label] || '•',
    }
  })
})

onMounted(async () => {
  const savedResult = localStorage.getItem('latestDiagnosisResult')

  if (savedResult) {
    result.value = JSON.parse(savedResult)
    return
  }

  try {
    const response = await axios.get('http://localhost:8000/api/diagnosis/latest/', {
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
})
</script>
