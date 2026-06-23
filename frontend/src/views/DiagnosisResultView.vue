<template>
  <section class="card panel">
    <h2>진단 결과</h2>

    <div v-if="!result">
      <p>진단 결과가 없습니다.</p>

      <RouterLink class="primary-btn single-btn" to="/diagnosis">
        금융 진단하러 가기
      </RouterLink>
    </div>

    <div v-else>
      <h3>{{ result.financial_type }}</h3>
      <p>{{ result.intro }}</p>

      <h3>금융 준비도</h3>
      <div class="result-box">
        <strong>{{ result.readiness_score }}점</strong>
      </div>

      <h3>나의 금융 프로필</h3>
      <div class="profile-grid">
        <div
          v-for="item in profileScoreItems"
          :key="item.label"
          class="profile-item"
        >
          <strong>{{ item.icon }} {{ item.label }}</strong>
          <div>{{ item.stars }}</div>
        </div>
      </div>

      <h3>강점</h3>
      <div class="result-box">
        <p
          v-for="item in result.strengths"
          :key="item"
          class="list-line"
        >
          ✅ {{ item }}
        </p>
      </div>

      <h3>보완점</h3>
      <div class="result-box">
        <p
          v-for="item in result.improvements"
          :key="item"
          class="list-line"
        >
          ⚠ {{ item }}
        </p>
      </div>

      <h3>FinPick 코멘트</h3>
      <div class="result-box">
        <p>"{{ result.finpick_comment }}"</p>
      </div>

      <div class="cta-row">
        <RouterLink class="primary-btn" to="/roadmap">
          진단 로드맵 보기
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

const profileIcons = {
  '저축 습관': '💰',
  '소비 관리': '🛒',
  '투자 성향': '📈',
  '자산 관리': '🏦',
}

const profileScoreItems = computed(() => {
  if (!result.value || !result.value.profile_scores) {
    return []
  }

  return Object.entries(result.value.profile_scores).map(([label, stars]) => {
    return {
      label,
      stars,
      icon: profileIcons[label] || '',
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
    }
  } catch (err) {
    console.error(err)
  }
})
</script>

