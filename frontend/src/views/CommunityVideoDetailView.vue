<template>
  <section class="community-video-detail">
    <RouterLink
      class="secondary-btn back-btn icon-back-btn"
      to="/community"
      aria-label="커뮤니티로 돌아가기"
      title="커뮤니티로 돌아가기"
    >
      ←
    </RouterLink>

    <div v-if="loading" class="status-box">
      영상을 불러오는 중입니다.
    </div>

    <div v-else-if="error" class="status-box error">
      {{ error }}
    </div>

    <template v-else-if="video">
      <div class="youtube-player-card">
        <iframe
          :src="`https://www.youtube.com/embed/${video.video_id}`"
          :title="video.title"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowfullscreen
        ></iframe>
      </div>

      <article class="youtube-detail-card">
        <span class="board-chip">YouTube</span>
        <h1>{{ video.title }}</h1>
        <p>{{ video.description || '영상 설명이 없습니다.' }}</p>

        <div class="youtube-detail-meta">
          <span>채널 {{ video.channel_title }}</span>
          <span>업로드 {{ formatVideoDate(video.published_at) }}</span>
          <span>조회수 {{ formatNumber(video.view_count) }}</span>
          <span>좋아요 {{ formatNumber(video.like_count) }}</span>
        </div>
      </article>
    </template>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()

const video = ref(null)
const loading = ref(true)
const error = ref('')

const formatNumber = (value) => {
  return Number(value || 0).toLocaleString()
}

const formatVideoDate = (dateText) => {
  if (!dateText) {
    return '-'
  }

  return new Date(dateText).toLocaleDateString('ko-KR')
}

const loadVideo = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get(`http://localhost:8000/api/youtube/videos/${route.params.videoId}/`, {
      withCredentials: true,
    })

    video.value = response.data.video
  } catch (err) {
    error.value = err.response?.data?.message || '영상 정보를 불러오지 못했습니다.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadVideo()
})
</script>
