<template>
  <section class="card panel deposit-detail-page stock-detail-page">
    <RouterLink
      class="secondary-btn back-btn icon-back-btn"
      to="/deposit-products?category=stock"
      aria-label="二쇱떇 ?꾩껜?곹뭹 紐⑸줉?쇰줈"
      title="二쇱떇 ?꾩껜?곹뭹 紐⑸줉?쇰줈"
    >
      ??
    </RouterLink>

    <div v-if="loading" class="status-box">
      二쇱떇 ?뺣낫瑜?遺덈윭?ㅻ뒗 以묒엯?덈떎.
    </div>

    <div v-else-if="error" class="status-box error">
      {{ error }}
    </div>

    <div v-else-if="stock">
      <div class="stock-detail-head">
        <span class="stock-detail-logo">
          <img v-if="stock.logo_url" :src="stock.logo_url" :alt="`${stock.name} 濡쒓퀬`" />
          <template v-else>{{ stock.name?.slice(0, 1) || 'S' }}</template>
        </span>
        <div>
          <small class="detail-kicker">{{ stock.market || '二쇱떇' }}</small>
          <h2>{{ stock.name }}</h2>
        </div>
      </div>

      <div class="stock-price-grid">
        <article class="stock-price-card main">
          <small>?꾩옱媛</small>
          <strong>{{ formatWon(stock.current_price) }}</strong>
          <span>湲곗???{{ formatStockDate(stock.base_date) }}</span>
        </article>

        <article class="stock-price-card">
          <small>?꾩씪 ?鍮?</small>
          <strong :class="{ positive: stock.change > 0, negative: stock.change < 0 }">
            {{ formatSignedWon(stock.change) }}
          </strong>
        </article>

        <article class="stock-price-card">
          <small>?깅씫瑜?</small>
          <strong :class="{ positive: stock.change_rate > 0, negative: stock.change_rate < 0 }">
            {{ formatRate(stock.change_rate) }}
          </strong>
        </article>
      </div>

      <div class="stock-info-grid">
        <article class="stock-info-card">
          <small>醫낅ぉ 肄붾뱶</small>
          <strong>{{ stock.code || '-' }}</strong>
        </article>

        <article class="stock-info-card">
          <small>?쒖옣</small>
          <strong>{{ stock.market || '-' }}</strong>
        </article>

        <article class="stock-info-card">
          <small>嫄곕옒??</small>
          <strong>{{ formatNumber(stock.volume) }}</strong>
        </article>

        <article class="stock-info-card">
          <small>?쒓?珥앹븸</small>
          <strong>{{ formatWon(stock.market_cap) }}</strong>
        </article>

        <article class="stock-info-card wide">
          <small>ISIN</small>
          <strong>{{ stock.isin_code || '-' }}</strong>
        </article>
      </div>

      <div class="button-row">
        <button
          class="primary-btn"
          type="button"
          @click="toggleFavoriteStock"
        >
          {{ stock.is_favorite ? '愿???곹뭹?먯꽌 ?쒓굅?섍린' : '愿???곹뭹 異붽??섍린' }}
        </button>
      </div>

      <p v-if="favoriteMessage" class="lock-note">{{ favoriteMessage }}</p>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '../services/api'

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
    const response = await axios.get(`${API_BASE_URL}/api/stocks/${route.params.code}/`, {
      withCredentials: true,
    })

    stock.value = response.data.stock
  } catch (err) {
    error.value = err.response?.data?.message || '二쇱떇 ?뺣낫瑜?遺덈윭?ㅼ? 紐삵뻽?듬땲??'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const toggleFavoriteStock = async () => {
  favoriteMessage.value = ''

  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/stocks/${stock.value.code}/favorite/`,
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
    favoriteMessage.value = err.response?.data?.message || '愿???곹뭹??蹂寃쏀븯吏 紐삵뻽?듬땲??'
    console.error(err)
  }
}

onMounted(() => {
  loadStock()
})
</script>
