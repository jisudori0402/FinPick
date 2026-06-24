<template>
  <section class="roadmap-page">
    <div class="roadmap-title-row">
      <div>
        <h1>금융 성장 로드맵</h1>
        <p class="roadmap-type">🧭 {{ roadmap?.type_code || '로드맵 준비 중' }}</p>
      </div>

      <div v-if="roadmap" class="roadmap-progress-summary">
        <span>진행률</span>
        <strong>{{ roadmap.progress }}%</strong>
        <small>{{ roadmap.completed_count }} / {{ roadmap.total_count }} 미션 완료</small>
        <div class="roadmap-progress-track">
          <span :style="{ width: roadmap.progress + '%' }"></span>
        </div>
      </div>
    </div>

    <div v-if="loading" class="status-box roadmap-status">
      로드맵을 불러오는 중입니다.
    </div>

    <div v-else-if="error" class="status-box error roadmap-status">
      {{ error }}
    </div>

    <div v-else-if="!roadmap" class="roadmap-empty">
      <h2>아직 로드맵이 없습니다</h2>
      <p>금융 진단을 먼저 완료하면 나에게 맞는 성장 미션을 만들 수 있어요.</p>
      <RouterLink class="primary-btn single-btn" to="/diagnosis">
        금융 진단 먼저 하기
      </RouterLink>
    </div>

    <template v-else>
      <div class="roadmap-next-card">
        <div class="target-icon" aria-hidden="true">◎</div>
        <div>
          <span>다음 추천 활동</span>
          <h2>{{ nextMissionTitle }}</h2>
          <p>{{ nextMissionDescription }}</p>
        </div>
        <div class="road-visual" aria-hidden="true">
          <span></span>
          <strong></strong>
        </div>
      </div>

      <div class="roadmap-level-list">
        <article
          v-for="level in roadmap.levels"
          :key="level.id"
          class="roadmap-level-card"
          :class="{
            locked: level.is_locked,
            completed: isLevelCompleted(level),
            active: isActiveLevel(level),
          }"
        >
          <div class="level-head">
            <div class="level-title-group">
              <span class="level-caret">{{ level.is_locked ? '›' : '⌄' }}</span>
              <div>
                <h2>{{ level.title }}</h2>
                <p>{{ level.description }}</p>
              </div>
            </div>

            <div class="roadmap-level-progress">
              <span>{{ levelProgressText(level) }}</span>
              <div>
                <strong :style="{ width: levelProgress(level) + '%' }"></strong>
              </div>
            </div>
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
              <span class="mission-check" aria-hidden="true"></span>
              <span class="mission-title">{{ mission.title }}</span>
            </label>
          </div>

          <p v-if="level.is_locked" class="lock-note">
            이전 레벨의 미션을 모두 완료하면 열립니다.
          </p>
        </article>
      </div>

      <div class="roadmap-comment-card">
        <span class="comment-bubble" aria-hidden="true">💬</span>
        <div>
          <h2>FinPick 코멘트</h2>
          <p>{{ roadmap.comment }}</p>
        </div>
      </div>

      <div class="result-actions roadmap-actions">
        <RouterLink class="primary-btn" to="/deposit-products">
          추천 상품 보기
          <span aria-hidden="true">→</span>
        </RouterLink>

        <RouterLink class="secondary-btn" to="/diagnosis-result">
          진단 결과 다시 보기
        </RouterLink>
      </div>
    </template>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'

const roadmap = ref(null)
const loading = ref(true)
const error = ref('')
const togglingMissionId = ref(null)

const syncRoadmapCache = () => {
  if (roadmap.value) {
    localStorage.setItem('latestRoadmap', JSON.stringify(roadmap.value))
  }
}

const activeLevel = computed(() => {
  return roadmap.value?.levels?.find((level) => !level.is_locked && !isLevelCompleted(level))
    || roadmap.value?.levels?.find((level) => !level.is_locked)
    || null
})

const nextMission = computed(() => {
  return activeLevel.value?.missions?.find((mission) => !mission.is_completed && !mission.is_locked)
    || null
})

const nextMissionTitle = computed(() => {
  return nextMission.value?.title || '오늘의 미션을 모두 완료했어요'
})

const nextMissionDescription = computed(() => {
  if (nextMission.value?.description) {
    return nextMission.value.description
  }

  return nextMission.value
    ? '이번 미션을 완료하고 다음 성장 단계로 넘어가보세요.'
    : '완료한 내용을 점검하고 다음 로드맵을 준비해보세요.'
})

const loadRoadmap = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get('http://localhost:8000/api/roadmap/', {
      withCredentials: true,
    })

    roadmap.value = response.data.roadmap
    syncRoadmapCache()
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
    syncRoadmapCache()
  } catch (err) {
    error.value = err.response?.data?.message || '미션 상태를 변경하지 못했습니다.'
    if (err.response?.data?.roadmap) {
      roadmap.value = err.response.data.roadmap
      syncRoadmapCache()
    }
    console.error(err)
  } finally {
    togglingMissionId.value = null
  }
}

const isLevelCompleted = (level) => {
  return level.missions?.length > 0 && level.missions.every((mission) => mission.is_completed)
}

const isActiveLevel = (level) => {
  return activeLevel.value?.id === level.id
}

const levelProgress = (level) => {
  const total = level.missions?.length || 0

  if (!total) {
    return 0
  }

  const completed = level.missions.filter((mission) => mission.is_completed).length
  return Math.round((completed / total) * 100)
}

const levelStateLabel = (level) => {
  if (level.is_locked) {
    return '잠금'
  }

  return isLevelCompleted(level) ? '완료' : '진행률'
}

const levelProgressText = (level) => {
  if (level.is_locked) {
    return '잠금'
  }

  return `진행률 ${levelProgress(level)}%`
}

onMounted(() => {
  loadRoadmap()
})
</script>
