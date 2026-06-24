<template>
  <section class="card panel deposit-detail-page stock-detail-page">
    <RouterLink
      class="secondary-btn back-btn icon-back-btn"
      to="/deposit-products?category=stock"
      aria-label="주식 전체상품 목록으로"
      title="주식 전체상품 목록으로"
    >
      ←
    </RouterLink>

    <div v-if="loading" class="status-box">
      주식 정보를 불러오는 중입니다.
    </div>

    <div v-else-if="error" class="status-box error">
      {{ error }}
    </div>

    <div v-else-if="stock">
      <small class="detail-kicker">{{ stock.market || '주식' }}</small>
      <h2>{{ stock.name }}</h2>

      <p><strong>종목코드</strong> {{ stock.code || '-' }}</p>
      <p><strong>기준일</strong> {{ formatStockDate(stock.base_date) }}</p>
      <p><strong>현재가</strong> {{ formatWon(stock.current_price) }}</p>
      <p>
        <strong>전일대비</strong>
        <span :class="{ positive: stock.change > 0, negative: stock.change < 0 }">
          {{ formatSignedWon(stock.change) }}
        </span>
      </p>
      <p>
        <strong>등락률</strong>
        <span :class="{ positive: stock.change_rate > 0, negative: stock.change_rate < 0 }">
          {{ formatRate(stock.change_rate) }}
        </span>
      </p>

      <div class="button-row">
        <button
          class="primary-btn"
          type="button"
          @click="toggleFavoriteStock"
        >
          {{ stock.is_favorite ? '관심상품에서 제거하기' : '관심상품 추가하기' }}
        </button>
      </div>

      <p v-if="favoriteMessage" class="lock-note">{{ favoriteMessage }}</p>

      <table class="detail-table">
        <thead>
          <tr>
            <th>시장</th>
            <th>거래량</th>
            <th>시가총액</th>
            <th>ISIN</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ stock.market || '-' }}</td>
            <td>{{ formatNumber(stock.volume) }}</td>
            <td>{{ formatWon(stock.market_cap) }}</td>
            <td>{{ stock.isin_code || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()

const stock = ref(null)
const loading = ref(true)
const error = ref('')
const favoriteMessage = ref('')

const formatNumber = (value) => {
  return Number(value || 0).toLocaleString()
}

const formatWon = (value) => {
  return `${formatNumber(value)}원`
}

const formatSignedWon = (value) => {
  const number = Number(value || 0)
  const sign = number > 0 ? '+' : ''
  return `${sign}${formatWon(number)}`
}

const formatRate = (value) => {
  const number = Number(value || 0)
  const sign = number > 0 ? '+' : ''
  return `${sign}${number.toFixed(2)}%`
}

const formatStockDate = (dateText) => {
  if (!dateText || dateText.length !== 8) {
    return dateText || '-'
  }

  return `${dateText.slice(0, 4)}-${dateText.slice(4, 6)}-${dateText.slice(6)}`
}

const loadStock = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get(`http://localhost:8000/api/stocks/${route.params.code}/`, {
      withCredentials: true,
    })

    stock.value = response.data.stock
  } catch (err) {
    error.value = err.response?.data?.message || '주식 정보를 불러오지 못했습니다.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const toggleFavoriteStock = async () => {
  favoriteMessage.value = ''

  try {
    const response = await axios.post(
      `http://localhost:8000/api/stocks/${stock.value.code}/favorite/`,
      {
        code: stock.value.code,
        isin_code: stock.value.isin_code,
        name: stock.value.name,
        market: stock.value.market,
        base_date: stock.value.base_date,
        current_price: stock.value.current_price,
        change: stock.value.change,
        change_rate: stock.value.change_rate,
        volume: stock.value.volume,
        market_cap: stock.value.market_cap,
      },
      {
        withCredentials: true,
      },
    )

    stock.value = {
      ...stock.value,
      ...response.data.stock,
      is_favorite: response.data.is_favorite,
    }
    favoriteMessage.value = response.data.message
  } catch (err) {
    favoriteMessage.value = err.response?.data?.message || '관심상품을 변경하지 못했습니다.'
    console.error(err)
  }
}

onMounted(() => {
  loadStock()
})
</script>
