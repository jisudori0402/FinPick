<template>
  <section class="card panel roadmap-page">
    <h2>금융 성장 로드맵</h2>

    <div v-if="loading" class="status-box">
      로드맵을 불러오는 중입니다.
    </div>

    <div v-else-if="error" class="status-box error">
      {{ error }}
    </div>

    <div v-else-if="!roadmap">
      <p>로드맵을 만들려면 먼저 금융 진단을 완료해 주세요.</p>

      <RouterLink class="primary-btn single-btn" to="/diagnosis">
        금융 진단 먼저 하기
      </RouterLink>
    </div>

    <div v-else>
      <div class="roadmap-header">
        <h3>{{ roadmap.type_code }}</h3>

        <p class="roadmap-progress-text">
          진행률 <strong>{{ roadmap.progress }}%</strong>
          <span>({{ roadmap.completed_count }}/{{ roadmap.total_count }})</span>
        </p>

        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{ width: roadmap.progress + '%' }"
          ></div>
        </div>
      </div>

      <div class="result-box roadmap-comment">
        <h3>FinPick 코멘트</h3>
        <p>{{ roadmap.comment }}</p>
      </div>

      <div class="roadmap-level-list">
        <article
          v-for="level in roadmap.levels"
          :key="level.id"
          class="roadmap-level-card"
          :class="{ locked: level.is_locked }"
        >
          <div class="level-head">
            <div>
              <h3>{{ level.title }}</h3>
              <p>{{ level.description }}</p>
            </div>

            <span class="state-chip" :class="{ done: isLevelCompleted(level), locked: level.is_locked }">
              {{ levelStateLabel(level) }}
            </span>
          </div>

          <div class="mission-list">
            <label
              v-for="mission in level.missions"
              :key="mission.id"
              class="mission"
              :class="{ done: mission.is_completed, locked: mission.is_locked }"
            >
              <input
                type="checkbox"
                :checked="mission.is_completed"
                :disabled="mission.is_locked || togglingMissionId === mission.id"
                @change="toggleMission(mission.id)"
              />
              <span>{{ mission.title }}</span>
            </label>
          </div>

          <p v-if="level.is_locked" class="lock-note">
            이전 레벨의 미션을 모두 완료하면 다음 레벨이 열립니다.
          </p>
        </article>
      </div>

      <div class="cta-row">
        <RouterLink class="primary-btn" to="/deposit-products">
          추천 상품 보러가기
        </RouterLink>

        <RouterLink class="secondary-btn" to="/diagnosis-result">
          진단 결과 다시 보기
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'

const roadmap = ref(null)
const loading = ref(true)
const error = ref('')
const togglingMissionId = ref(null)

const loadRoadmap = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get('http://localhost:8000/api/roadmap/', {
      withCredentials: true,
    })

    roadmap.value = response.data.roadmap
  } catch (err) {
    error.value = err.response?.data?.message || '로드맵을 불러오지 못했습니다.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const toggleMission = async (missionId) => {
  togglingMissionId.value = missionId
  error.value = ''

  try {
    const response = await axios.post(
      `http://localhost:8000/api/missions/${missionId}/toggle/`,
      {},
      {
        withCredentials: true,
      },
    )

    roadmap.value = response.data.roadmap
  } catch (err) {
    error.value = err.response?.data?.message || '미션 상태를 변경하지 못했습니다.'
    if (err.response?.data?.roadmap) {
      roadmap.value = err.response.data.roadmap
    }
    console.error(err)
  } finally {
    togglingMissionId.value = null
  }
}

const isLevelCompleted = (level) => {
  return level.missions?.length > 0 && level.missions.every((mission) => mission.is_completed)
}

const levelStateLabel = (level) => {
  if (level.is_locked) {
    return '잠금'
  }

  return level.is_past || isLevelCompleted(level) ? '완료' : '진행중'
}

onMounted(() => {
  loadRoadmap()
})
</script>
