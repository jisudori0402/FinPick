<template>
  <section class="card panel deposit-detail-page">
    <RouterLink
      class="secondary-btn back-btn icon-back-btn"
      to="/deposit-products?category=deposit"
      aria-label="예적금 전체상품 목록으로"
      title="예적금 전체상품 목록으로"
    >
      ←
    </RouterLink>

    <div v-if="loading" class="status-box">
      상품 정보를 불러오는 중입니다.
    </div>

    <div v-else-if="error" class="status-box error">
      {{ error }}
    </div>

    <div v-else-if="product">
      <h2>{{ product.product_name }}</h2>

      <p><strong>은행</strong> {{ product.financial_company_name }}</p>
      <p><strong>가입 방법</strong> {{ product.join_way || '-' }}</p>
      <p><strong>가입 대상</strong> {{ product.join_member || '-' }}</p>
      <p><strong>우대 조건</strong> {{ product.special_condition || '-' }}</p>
      <p><strong>기타 안내</strong> {{ product.etc_note || '-' }}</p>

      <div class="button-row">
        <button
          class="primary-btn"
          type="button"
          @click="toggleInterestProduct"
        >
          {{ product.is_subscribed ? '관심목록에서 제거하기' : '관심목록에 추가하기' }}
        </button>

        <button class="secondary-btn" type="button" @click="goToBankSearch">
          근처 은행 검색
        </button>
      </div>

      <p v-if="joinMessage" class="lock-note">{{ joinMessage }}</p>

      <table class="detail-table">
        <thead>
          <tr>
            <th>기간</th>
            <th>금리유형</th>
            <th>기본금리</th>
            <th>최고금리</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="option in product.options"
            :key="`${option.saving_term}-${option.interest_rate_type_name}-${option.reserve_type_name}`"
          >
            <td>{{ option.saving_term ? option.saving_term + '개월' : '-' }}</td>
            <td>{{ option.interest_rate_type_name || option.reserve_type_name || '-' }}</td>
            <td>{{ option.interest_rate ? option.interest_rate + '%' : '-' }}</td>
            <td>{{ option.max_interest_rate ? option.max_interest_rate + '%' : '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const product = ref(null)
const loading = ref(true)
const error = ref('')
const joinMessage = ref('')

const loadProduct = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get(
      `http://localhost:8000/api/deposit-products/${route.params.id}/`,
      {
        withCredentials: true,
      },
    )

    product.value = response.data.product
  } catch (err) {
    error.value = err.response?.data?.message || '상품 정보를 불러오지 못했습니다.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const toggleInterestProduct = async () => {
  joinMessage.value = ''

  try {
    const requestConfig = {
      withCredentials: true,
    }
    const url = `http://localhost:8000/api/deposit-products/${product.value.id}/join/`
    const response = product.value.is_subscribed
      ? await axios.delete(url, requestConfig)
      : await axios.post(
        url,
        {},
        requestConfig,
      )

    product.value = {
      ...product.value,
      ...response.data.product,
      is_subscribed: response.data.is_subscribed,
    }
    joinMessage.value = response.data.message
  } catch (err) {
    joinMessage.value = err.response?.data?.message || '관심목록을 변경하지 못했습니다.'
    console.error(err)
  }
}

const goToBankSearch = () => {
  router.push(`/bank-search/${product.value.id}`)
}

onMounted(() => {
  loadProduct()
})
</script>
