<template>
  <section class="roadmap-page">
    <div class="roadmap-title-row">
      <div>
        <h1>湲덉쑖 ?깆옣 濡쒕뱶留?</h1>
        <p class="roadmap-type">{{ roadmap?.type_code || '로드맵 준비 중' }}</p>
      </div>

      <div v-if="roadmap" class="roadmap-progress-summary">
        <span>吏꾪뻾瑜?</span>
        <strong>오늘의 금융 테마</strong>
        <small>{{ roadmap.completed_count }} / {{ roadmap.total_count }} 誘몄뀡 ?꾨즺</small>
        <div class="roadmap-progress-track">
          <span :style="{ width: roadmap.progress + '%' }"></span>
        </div>
      </div>
    </div>

    <div v-if="loading" class="status-box roadmap-status">
      濡쒕뱶留듭쓣 遺덈윭?ㅻ뒗 以묒엯?덈떎.
    </div>

    <div v-else-if="error" class="status-box error roadmap-status">
      {{ error }}
    </div>

    <div v-else-if="!roadmap" class="roadmap-empty">
      <h2>?꾩쭅 濡쒕뱶留듭씠 ?놁뒿?덈떎</h2>
      <p>湲덉쑖 吏꾨떒??癒쇱? ?꾨즺?섎㈃ ?섏뿉寃?留욌뒗 ?깆옣 誘몄뀡??留뚮뱾 ???덉뼱??</p>
      <RouterLink class="primary-btn single-btn" to="/diagnosis">
        湲덉쑖 吏꾨떒 癒쇱? ?섍린
      </RouterLink>
    </div>

    <template v-else>
      <div class="roadmap-next-card">
        <div class="target-icon" aria-hidden="true">?렞</div>
        <div>
          <span>?ㅼ쓬 異붿쿇 ?쒕룞</span>
          <h2>{{ nextMissionTitle }}</h2>
          <p>{{ nextMissionDescription }}</p>
        </div>
        <img class="road-visual" src="/home-mountain-road-cutout.png" alt="" aria-hidden="true" />
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
              <span class="level-caret">{{ level.is_locked ? '+' : '-' }}</span>
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
            ?댁쟾 ?덈꺼??誘몄뀡??紐⑤몢 ?꾨즺?섎㈃ ?대┰?덈떎.
          </p>
        </article>
      </div>

      <div class="roadmap-comment-card">
        <span class="comment-bubble" aria-hidden="true">?뮠</span>
        <div>
          <h2>FinPick 코멘트</h2>
          <p>{{ roadmap.comment }}</p>
        </div>
      </div>

      <div class="result-actions roadmap-actions">
        <RouterLink class="primary-btn" to="/deposit-products">
          異붿쿇 ?곹뭹 蹂닿린
          <span aria-hidden="true">??</span>
        </RouterLink>

        <RouterLink class="secondary-btn" to="/diagnosis-result">
          吏꾨떒 寃곌낵 ?ㅼ떆 蹂닿린
        </RouterLink>
      </div>
    </template>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '../services/api'

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
    ? '?대쾲 誘몄뀡???꾨즺?섍퀬 ?ㅼ쓬 ?깆옣 ?④퀎濡??섏뼱媛蹂댁꽭??'
    : '?꾨즺???댁슜???먭??섍퀬 ?ㅼ쓬 濡쒕뱶留듭쓣 以鍮꾪빐蹂댁꽭??'
})

const loadRoadmap = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get(`${API_BASE_URL}/api/roadmap/`, {
      withCredentials: true,
    })

    roadmap.value = response.data.roadmap
    syncRoadmapCache()
  } catch (err) {
    error.value = err.response?.data?.message || '濡쒕뱶留듭쓣 遺덈윭?ㅼ? 紐삵뻽?듬땲??'
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
      `${API_BASE_URL}/api/missions/${missionId}/toggle/`,
      {},
      {
        withCredentials: true,
      },
    )

    roadmap.value = response.data.roadmap
    syncRoadmapCache()
  } catch (err) {
    error.value = err.response?.data?.message || '誘몄뀡 ?곹깭瑜?蹂寃쏀븯吏 紐삵뻽?듬땲??'
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
    return '?좉툑'
  }

  return isLevelCompleted(level) ? '완료' : '진행중'
}

const levelProgressText = (level) => {
  if (level.is_locked) {
    return '?좉툑'
  }

  return `吏꾪뻾瑜?${levelProgress(level)}%`
}

onMounted(() => {
  loadRoadmap()
})
</script>
