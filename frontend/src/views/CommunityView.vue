<template>
  <SidebarLayout class="community-page community-hub-page" surface="white">
    <template #sidebar>
      <AppSidebar>
        <template #top>
      <button class="write-button" type="button" @click="toggleComposer">
        ✎ 글 작성하기
      </button>
        </template>

        <template #nav>

      <nav class="community-side-nav" aria-label="커뮤니티 메뉴">
        <button
          type="button"
          :class="{ active: activeSection === 'youtube' }"
          @click="showYoutube"
        >
          <span>🔥</span>
          인기 영상
          <em>NEW</em>
        </button>
        <button
          type="button"
          :class="{ active: activeSection === 'board' }"
          @click="showBoard"
        >
          <span>💬</span>
          게시판
        </button>
      </nav>
        </template>

        <template #support>

      <div class="youtube-tip-card trending-keyword-card">
        <div class="trending-card-head">
          <strong>실시간 검색어</strong>
        </div>
        <ol>
          <li v-for="item in trendingKeywords" :key="item.keyword">
            <button type="button" @click="searchTrendingKeyword(item.keyword)">
              <span>{{ item.rank }}</span>
              <strong>{{ item.keyword }}</strong>
            </button>
          </li>
        </ol>
      </div>
        </template>
      </AppSidebar>
    </template>

    <div class="community-main">
      <section v-if="activeSection === 'youtube'" class="video-section">
        <div class="community-head">
          <div>
            <h1>인기 영상</h1>
            <p>관심 있는 금융 주제의 영상을 검색해보세요.</p>
          </div>

          <form class="community-search youtube-search" @submit.prevent="searchYoutubeVideos">
            <input v-model="youtubeQuery" placeholder="관심 종목 또는 금융 키워드 검색" />
            <button type="submit" :disabled="youtubeLoading">검색</button>
          </form>
        </div>

        <div class="topic-tabs">
          <button
            v-for="topic in videoTopics"
            :key="topic"
            type="button"
            :class="{ active: selectedTopic === topic }"
            @click="selectVideoTopic(topic)"
          >
            {{ topic }}
          </button>
        </div>

        <div v-if="youtubeLoading" class="status-box">
          영상을 검색하는 중입니다.
        </div>

        <div v-else-if="youtubeError" class="status-box error">
          {{ youtubeError }}
        </div>

        <div class="video-grid">
          <article
            v-for="video in youtubeVideos"
            :key="video.video_id"
            class="video-card"
            @click="openVideo(video.video_id)"
          >
            <div class="video-thumb youtube-thumb">
              <img v-if="video.thumbnail" :src="video.thumbnail" :alt="video.title" />
              <strong v-else>{{ video.title }}</strong>
              <span>▶</span>
            </div>
            <h2>{{ video.title }}</h2>
            <p>{{ video.channel_title }}</p>
            <small>{{ formatVideoDate(video.published_at) }}</small>
          </article>
        </div>

        <div v-if="!youtubeLoading && !youtubeVideos.length" class="empty-box community-empty">
          검색 결과가 없습니다.
        </div>
      </section>

      <section v-if="activeSection === 'board'" class="community-board-section only-board-section">
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
              {{ editingPostId ? '수정하기' : '등록하기' }}
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

                <div v-if="selectedPost.can_edit" class="post-actions">
                  <button class="secondary-btn" type="button" @click="startEditPost">
                    수정
                  </button>
                  <button class="danger-btn" type="button" @click="deletePost">
                    삭제
                  </button>
                </div>

                <div class="comment-list">
                  <h3>댓글 {{ selectedPost.comments?.length || 0 }}</h3>
                  <div v-if="!selectedPost.comments?.length" class="comment-empty">
                    아직 댓글이 없습니다.
                  </div>
                  <article v-for="comment in selectedPost.comments" :key="comment.id" class="comment-item">
                    <div class="comment-head">
                      <strong>{{ comment.author }}</strong>
                      <small>{{ comment.created_at }}</small>
                    </div>
                    <template v-if="editingCommentId === comment.id">
                      <textarea v-model="editingCommentContent" rows="3"></textarea>
                      <div class="comment-actions">
                        <button class="secondary-btn" type="button" @click="cancelEditComment">
                          취소
                        </button>
                        <button class="primary-btn" type="button" @click="updateComment(comment)">
                          저장
                        </button>
                      </div>
                    </template>
                    <template v-else>
                      <p>{{ comment.content }}</p>
                      <div v-if="comment.can_edit || comment.can_delete" class="comment-actions">
                        <button v-if="comment.can_edit" class="secondary-btn" type="button" @click="startEditComment(comment)">
                          수정
                        </button>
                        <button v-if="comment.can_delete" class="danger-btn" type="button" @click="deleteComment(comment)">
                          삭제
                        </button>
                      </div>
                    </template>
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
  </SidebarLayout>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AppSidebar from '../components/AppSidebar.vue'
import SidebarLayout from '../components/SidebarLayout.vue'

const router = useRouter()

const boards = ref([])
const posts = ref([])
const selectedBoard = ref('')
const selectedPost = ref(null)
const activeSection = ref('youtube')
const selectedTopic = ref('전체')
const youtubeQuery = ref('금융 투자')
const youtubeVideos = ref([])
const youtubeLoading = ref(false)
const youtubeError = ref('')
const trendingKeywords = ref([])
const loading = ref(true)
const error = ref('')
const showComposer = ref(false)
const submittingPost = ref(false)
const submittingComment = ref(false)
const formMessage = ref('')
const commentContent = ref('')
const editingPostId = ref(null)
const editingCommentId = ref(null)
const editingCommentContent = ref('')

const postForm = ref({
  board: 'free',
  title: '',
  content: '',
})

const videoTopics = ['전체', '재테크 기초', '주식 투자', 'ETF', '절세 전략', '부동산', '연금·노후', '가격 관리']

const searchYoutubeVideos = async () => {
  const query = youtubeQuery.value.trim()
  if (!query) {
    youtubeVideos.value = []
    youtubeError.value = '검색어를 입력해 주세요.'
    return
  }

  youtubeLoading.value = true
  youtubeError.value = ''

  try {
    const response = await axios.get('http://localhost:8000/api/youtube/search/', {
      params: { q: query },
      withCredentials: true,
    })

    youtubeVideos.value = response.data.videos || []
    loadTrendingKeywords()
  } catch (err) {
    youtubeVideos.value = []
    youtubeError.value = err.response?.data?.message || '영상을 검색하지 못했습니다.'
    console.error(err)
  } finally {
    youtubeLoading.value = false
  }
}

const loadTrendingKeywords = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/trending-keywords/', {
      withCredentials: true,
    })
    trendingKeywords.value = response.data.keywords || []
  } catch (err) {
    console.error(err)
  }
}

const searchTrendingKeyword = (keyword) => {
  youtubeQuery.value = keyword
  selectedTopic.value = ''
  activeSection.value = 'youtube'
  searchYoutubeVideos()
}

const selectVideoTopic = (topic) => {
  selectedTopic.value = topic
  youtubeQuery.value = topic === '전체' ? '금융 투자' : topic
  searchYoutubeVideos()
}

const openVideo = (videoId) => {
  if (!videoId) {
    return
  }

  router.push(`/community/videos/${videoId}`)
}

const formatVideoDate = (dateText) => {
  if (!dateText) {
    return '-'
  }

  return new Date(dateText).toLocaleDateString('ko-KR')
}

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
  activeSection.value = 'board'
  showComposer.value = !showComposer.value
  if (!showComposer.value) {
    cancelEditPost()
  }
}

const createPost = async () => {
  formMessage.value = ''
  submittingPost.value = true

  const formData = new FormData()
  formData.append('board', postForm.value.board || 'free')
  formData.append('title', postForm.value.title)
  formData.append('content', postForm.value.content)

  try {
    const url = editingPostId.value
      ? `http://localhost:8000/api/community/posts/${editingPostId.value}/`
      : 'http://localhost:8000/api/community/posts/'
    const response = await axios.post(url, formData, {
      withCredentials: true,
    })

    postForm.value.title = ''
    postForm.value.content = ''
    formMessage.value = editingPostId.value ? '게시글이 수정되었습니다.' : '게시글이 등록되었습니다.'
    editingPostId.value = null
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

const startEditPost = () => {
  if (!selectedPost.value?.can_edit) {
    return
  }

  activeSection.value = 'board'
  showComposer.value = true
  editingPostId.value = selectedPost.value.id
  postForm.value = {
    board: selectedPost.value.board,
    title: selectedPost.value.title,
    content: selectedPost.value.content,
  }
  formMessage.value = ''
}

const cancelEditPost = () => {
  editingPostId.value = null
  postForm.value.title = ''
  postForm.value.content = ''
  formMessage.value = ''
}

const deletePost = async () => {
  if (!selectedPost.value?.can_edit) {
    return
  }

  try {
    await axios.delete(`http://localhost:8000/api/community/posts/${selectedPost.value.id}/`, {
      withCredentials: true,
    })

    selectedPost.value = null
    await loadPosts()
  } catch (err) {
    error.value = err.response?.data?.message || '게시글을 삭제하지 못했습니다.'
    console.error(err)
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

const showYoutube = () => {
  activeSection.value = 'youtube'
  showComposer.value = false
}

const startEditComment = (comment) => {
  if (!comment.can_edit) {
    return
  }

  editingCommentId.value = comment.id
  editingCommentContent.value = comment.content
}

const cancelEditComment = () => {
  editingCommentId.value = null
  editingCommentContent.value = ''
}

const updateComment = async (comment) => {
  if (!comment.can_edit) {
    return
  }

  const formData = new FormData()
  formData.append('content', editingCommentContent.value)

  try {
    await axios.post(`http://localhost:8000/api/community/comments/${comment.id}/`, formData, {
      withCredentials: true,
    })

    cancelEditComment()
    await loadPostDetail(selectedPost.value.id)
    await loadPosts()
  } catch (err) {
    error.value = err.response?.data?.message || '댓글을 수정하지 못했습니다.'
    console.error(err)
  }
}

const deleteComment = async (comment) => {
  if (!comment.can_delete) {
    return
  }

  try {
    await axios.delete(`http://localhost:8000/api/community/comments/${comment.id}/`, {
      withCredentials: true,
    })

    await loadPostDetail(selectedPost.value.id)
    await loadPosts()
  } catch (err) {
    error.value = err.response?.data?.message || '댓글을 삭제하지 못했습니다.'
    console.error(err)
  }
}

const showBoard = () => {
  activeSection.value = 'board'
}

onMounted(() => {
  loadTrendingKeywords()
  searchYoutubeVideos()
  loadPosts()
})
</script>
