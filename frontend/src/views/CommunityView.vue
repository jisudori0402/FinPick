<template>
  <section class="card panel community-page">
    <div class="page-head">
      <div>
        <h2>커뮤니티</h2>
        <p>금융 고민과 상품 후기를 함께 나눠보세요.</p>
      </div>
    </div>

    <div v-if="loading" class="status-box">
      게시글을 불러오는 중입니다.
    </div>

    <div v-else-if="error" class="status-box error">
      {{ error }}
    </div>

    <template v-else>
      <div class="community-tabs">
        <button
          :class="{ active: selectedBoard === '' }"
          type="button"
          @click="selectBoard('')"
        >
          전체
        </button>
        <button
          v-for="board in boards"
          :key="board.value"
          :class="{ active: selectedBoard === board.value }"
          type="button"
          @click="selectBoard(board.value)"
        >
          {{ board.label }}
        </button>
      </div>

      <div v-if="posts.length === 0" class="empty-box">
        아직 등록된 게시글이 없습니다.
      </div>

      <div v-else class="community-list">
        <article v-for="post in posts" :key="post.id" class="community-post">
          <div>
            <span class="board-chip">{{ post.board_label }}</span>
            <h3>{{ post.title }}</h3>
            <p>{{ post.content }}</p>
          </div>

          <div class="post-meta">
            <span>{{ post.author }}</span>
            <span>{{ post.created_at }}</span>
            <span>댓글 {{ post.comment_count }}</span>
          </div>
        </article>
      </div>
    </template>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const boards = ref([])
const posts = ref([])
const selectedBoard = ref('')
const loading = ref(true)
const error = ref('')

const loadPosts = async () => {
  loading.value = true
  error.value = ''

  try {
    const params = selectedBoard.value ? { board: selectedBoard.value } : {}
    const response = await axios.get('http://localhost:8000/api/community/posts/', {
      params,
      withCredentials: true,
    })

    boards.value = response.data.boards || []
    posts.value = response.data.posts || []
  } catch (err) {
    error.value = err.response?.data?.message || '커뮤니티 게시글을 불러오지 못했습니다.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const selectBoard = (board) => {
  selectedBoard.value = board
  loadPosts()
}

onMounted(() => {
  loadPosts()
})
</script>
