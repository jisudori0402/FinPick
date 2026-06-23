<template>
  <section class="community-page community-hub-page">
    <aside class="community-sidebar">
      <button class="write-button" type="button" @click="toggleComposer">
        ✎ 글 작성하기
      </button>

      <nav class="community-side-nav" aria-label="커뮤니티 메뉴">
        <button class="active" type="button">
          <span>🔥</span>
          인기 주제
        </button>
        <button type="button" @click="scrollToVideos">
          <span>▣</span>
          유튜브
          <em>NEW</em>
        </button>
        <button type="button" @click="scrollToBoard">
          <span>☷</span>
          자유 게시판
        </button>
        <button type="button" @click="scrollToBoard">
          <span>☏</span>
          질문 & 답변
        </button>
      </nav>

      <div class="youtube-tip-card">
        <strong>금융 지식은 영상으로!</strong>
        <p>FinPick 유튜브와 함께 똑똑하게 성장해요.</p>
        <div class="youtube-mascot" aria-hidden="true">
          <span>▶</span>
        </div>
        <button type="button" @click="scrollToVideos">
          유튜브 바로가기
        </button>
      </div>
    </aside>

    <div class="community-main">
      <section ref="videosSection" class="video-section">
        <div class="community-head">
          <div>
            <h1>인기 주제 유튜브</h1>
            <p>지금 가장 핫한 금융 주제의 영상을 모아봤어요!</p>
          </div>

          <label class="community-search">
            <input placeholder="검색어를 입력하세요" disabled />
            <span aria-hidden="true">⌕</span>
          </label>
        </div>

        <div class="topic-tabs">
          <button
            v-for="topic in videoTopics"
            :key="topic"
            type="button"
            :class="{ active: selectedTopic === topic }"
            @click="selectedTopic = topic"
          >
            {{ topic }}
          </button>
        </div>

        <div class="video-grid">
          <article v-for="video in filteredVideos" :key="video.title" class="video-card">
            <div class="video-thumb" :class="video.theme">
              <strong>{{ video.headline }}</strong>
              <span>{{ video.duration }}</span>
            </div>
            <h2>{{ video.title }}</h2>
            <p>{{ video.channel }}</p>
            <small>조회수 {{ video.views }} · {{ video.age }}</small>
          </article>
        </div>

        <button class="load-more-videos" type="button">
          더 많은 영상 보기
          <span>⌄</span>
        </button>
      </section>

      <section ref="boardSection" class="community-board-section">
        <div class="board-header-row">
          <div>
            <h1>커뮤니티 게시판</h1>
            <p>금융 고민과 상품 후기를 함께 나눠보세요.</p>
          </div>
        </div>

        <form v-if="showComposer" class="post-composer" @submit.prevent="createPost">
          <div class="composer-row">
            <select v-model="postForm.board">
              <option v-for="board in boards" :key="board.value" :value="board.value">
                {{ board.label }}
              </option>
            </select>
            <input v-model="postForm.title" placeholder="제목을 입력하세요" />
          </div>
          <textarea v-model="postForm.content" rows="4" placeholder="내용을 입력하세요"></textarea>
          <div class="composer-actions">
            <span>{{ formMessage }}</span>
            <button class="primary-btn" type="submit" :disabled="submittingPost">
              등록하기
            </button>
          </div>
        </form>

        <div v-if="loading" class="status-box">
          게시글을 불러오는 중입니다.
        </div>

        <div v-else-if="error" class="status-box error">
          {{ error }}
        </div>

        <template v-else>
          <div class="community-tabs">
            <button :class="{ active: selectedBoard === '' }" type="button" @click="selectBoard('')">
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

          <div v-if="posts.length === 0" class="empty-box community-empty">
            아직 등록된 게시글이 없습니다.
          </div>

          <div v-else class="community-content-grid">
            <div class="community-list">
              <article
                v-for="post in posts"
                :key="post.id"
                class="community-post"
                :class="{ active: selectedPost?.id === post.id }"
                @click="selectPost(post)"
              >
                <div>
                  <span class="board-chip">{{ post.board_label }}</span>
                  <h2>{{ post.title }}</h2>
                  <p>{{ post.content }}</p>
                </div>

                <div class="post-meta">
                  <span>{{ post.author }}</span>
                  <span>{{ post.created_at }}</span>
                  <span>댓글 {{ post.comment_count }}</span>
                </div>
              </article>
            </div>

            <aside class="post-detail-panel">
              <div v-if="!selectedPost" class="detail-placeholder">
                게시글을 선택하면 댓글을 볼 수 있어요.
              </div>

              <template v-else>
                <span class="board-chip">{{ selectedPost.board_label }}</span>
                <h2>{{ selectedPost.title }}</h2>
                <p class="detail-content">{{ selectedPost.content }}</p>

                <div class="post-meta detail-meta">
                  <span>{{ selectedPost.author }}</span>
                  <span>{{ selectedPost.created_at }}</span>
                </div>

                <div class="comment-list">
                  <h3>댓글 {{ selectedPost.comments?.length || 0 }}</h3>
                  <div v-if="!selectedPost.comments?.length" class="comment-empty">
                    아직 댓글이 없습니다.
                  </div>
                  <article v-for="comment in selectedPost.comments" :key="comment.id" class="comment-item">
                    <strong>{{ comment.author }}</strong>
                    <p>{{ comment.content }}</p>
                    <small>{{ comment.created_at }}</small>
                  </article>
                </div>

                <form class="comment-form" @submit.prevent="createComment">
                  <textarea v-model="commentContent" rows="3" placeholder="댓글을 입력하세요"></textarea>
                  <button class="primary-btn" type="submit" :disabled="submittingComment">
                    댓글 달기
                  </button>
                </form>
              </template>
            </aside>
          </div>
        </template>
      </section>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'

const boards = ref([])
const posts = ref([])
const selectedBoard = ref('')
const selectedPost = ref(null)
const selectedTopic = ref('전체')
const loading = ref(true)
const error = ref('')
const showComposer = ref(false)
const submittingPost = ref(false)
const submittingComment = ref(false)
const formMessage = ref('')
const commentContent = ref('')
const videosSection = ref(null)
const boardSection = ref(null)

const postForm = ref({
  board: 'free',
  title: '',
  content: '',
})

const videoTopics = ['전체', '재테크 기초', '주식 투자', 'ETF', '절세 전략', '부동산', '연금·노후', '가격 관리']

const videoItems = [
  {
    topic: '재테크 기초',
    theme: 'mint',
    headline: '재테크 첫걸음',
    duration: '10:34',
    title: '사회초년생 재테크, 지금부터 이렇게 시작하세요!',
    channel: '돈 톡톡TV',
    views: '12.3만회',
    age: '2일 전',
  },
  {
    topic: 'ETF',
    theme: 'blue',
    headline: 'ETF 투자',
    duration: '8:45',
    title: 'ETF 투자, 초보자가 꼭 알아야 할 5가지',
    channel: '머니가이드',
    views: '9.8만회',
    age: '4일 전',
  },
  {
    topic: '가격 관리',
    theme: 'pink',
    headline: '지출 습관',
    duration: '7:32',
    title: '월급 관리의 정석, 돈이 모이는 지출 습관 3가지',
    channel: '재테크하는 제이',
    views: '8.1만회',
    age: '1주 전',
  },
  {
    topic: '연금·노후',
    theme: 'green',
    headline: '연금저축 vs IRP',
    duration: '9:12',
    title: '연금저축 vs IRP, 어떻게 더 유리할까?',
    channel: '연금연구소',
    views: '6.7만회',
    age: '1주 전',
  },
  {
    topic: '주식 투자',
    theme: 'line',
    headline: '주식 초보가 반드시 알아야 할 투자 원칙 3가지',
    duration: '11:08',
    title: '주식 초보가 반드시 알아야 할 투자 원칙 3가지',
    channel: '주식하는 친구',
    views: '15.6만회',
    age: '1주 전',
  },
  {
    topic: '절세 전략',
    theme: 'dark',
    headline: 'ISA 계좌 완벽 정리!',
    duration: '6:55',
    title: 'ISA 계좌 완벽 정리! 혜택부터 활용법까지',
    channel: '절세노트',
    views: '7.2만회',
    age: '2주 전',
  },
  {
    topic: '부동산',
    theme: 'house',
    headline: '부동산 투자 지금 들어가도 괜찮을까?',
    duration: '10:21',
    title: '부동산 투자, 지금 들어가도 괜찮을까?',
    channel: '부동산 인사이트',
    views: '11.4만회',
    age: '2주 전',
  },
  {
    topic: '재테크 기초',
    theme: 'news',
    headline: '경제 뉴스 쉽게 이해하기',
    duration: '5:49',
    title: '하루 10분! 경제 뉴스 쉽게 이해하기',
    channel: '경제 읽어주는 남자',
    views: '5.3만회',
    age: '3주 전',
  },
]

const filteredVideos = computed(() => {
  if (selectedTopic.value === '전체') {
    return videoItems
  }

  return videoItems.filter((video) => video.topic === selectedTopic.value)
})

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

    if (!postForm.value.board && boards.value[0]) {
      postForm.value.board = boards.value[0].value
    }

    if (selectedPost.value) {
      const nextSelected = posts.value.find((post) => post.id === selectedPost.value.id)
      selectedPost.value = nextSelected || null
      if (nextSelected) {
        await loadPostDetail(nextSelected.id)
      }
    }
  } catch (err) {
    error.value = err.response?.data?.message || '커뮤니티 게시글을 불러오지 못했습니다.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const loadPostDetail = async (postId) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/community/posts/${postId}/`, {
      withCredentials: true,
    })
    selectedPost.value = response.data.post
  } catch (err) {
    error.value = err.response?.data?.message || '게시글 상세를 불러오지 못했습니다.'
    console.error(err)
  }
}

const selectBoard = (board) => {
  selectedBoard.value = board
  selectedPost.value = null
  loadPosts()
}

const selectPost = (post) => {
  loadPostDetail(post.id)
}

const toggleComposer = () => {
  showComposer.value = !showComposer.value
  scrollToBoard()
}

const createPost = async () => {
  formMessage.value = ''
  submittingPost.value = true

  const formData = new FormData()
  formData.append('board', postForm.value.board || 'free')
  formData.append('title', postForm.value.title)
  formData.append('content', postForm.value.content)

  try {
    const response = await axios.post('http://localhost:8000/api/community/posts/', formData, {
      withCredentials: true,
    })

    postForm.value.title = ''
    postForm.value.content = ''
    formMessage.value = '게시글이 등록되었습니다.'
    showComposer.value = false
    selectedPost.value = response.data.post
    await loadPosts()
  } catch (err) {
    formMessage.value = err.response?.data?.message || '게시글을 등록하지 못했습니다.'
    console.error(err)
  } finally {
    submittingPost.value = false
  }
}

const createComment = async () => {
  if (!selectedPost.value) {
    return
  }

  submittingComment.value = true

  const formData = new FormData()
  formData.append('content', commentContent.value)

  try {
    await axios.post(
      `http://localhost:8000/api/community/posts/${selectedPost.value.id}/comments/`,
      formData,
      {
        withCredentials: true,
      },
    )

    commentContent.value = ''
    await loadPostDetail(selectedPost.value.id)
    await loadPosts()
  } catch (err) {
    error.value = err.response?.data?.message || '댓글을 등록하지 못했습니다.'
    console.error(err)
  } finally {
    submittingComment.value = false
  }
}

const scrollToVideos = () => {
  videosSection.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const scrollToBoard = () => {
  boardSection.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

onMounted(() => {
  loadPosts()
})
</script>
