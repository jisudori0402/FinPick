<template>
  <section class="community-video-detail">
    <RouterLink
      class="secondary-btn back-btn icon-back-btn"
      to="/community"
      aria-label="而ㅻ??덊떚濡??뚯븘媛湲?
      title="而ㅻ??덊떚濡??뚯븘媛湲?
    >
      ??    </RouterLink>

    <div v-if="loading" class="status-box">
      ?곸긽??遺덈윭?ㅻ뒗 以묒엯?덈떎.
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
        <p>{{ video.description || '?곸긽 ?ㅻ챸???놁뒿?덈떎.' }}</p>

        <div class="youtube-detail-meta">
          <span>梨꾨꼸 {{ video.channel_title }}</span>
          <span>?낅줈??{{ formatVideoDate(video.published_at) }}</span>
          <span>議고쉶??{{ formatNumber(video.view_count) }}</span>
          <span>醫뗭븘??{{ formatNumber(video.like_count) }}</span>
        </div>
      </article>
    </template>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '../services/api'

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
    const response = await axios.get(`${API_BASE_URL}/api/youtube/videos/${route.params.videoId}/`, {
      withCredentials: true,
    })

    video.value = response.data.video
  } catch (err) {
    error.value = err.response?.data?.message || '?곸긽 ?뺣낫瑜?遺덈윭?ㅼ? 紐삵뻽?듬땲??'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadVideo()
})
</script>
