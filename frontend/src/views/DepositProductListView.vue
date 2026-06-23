<template>
  <section class="card panel products-page">
    <h2>모든 상품</h2>

    <div class="category-tabs">
      <button :class="{ active: productCategory === 'deposit' }" @click="setProductCategory('deposit')">
        예적금
      </button>
      <button :class="{ active: productCategory === 'card' }" @click="setProductCategory('card')">
        카드
      </button>
      <button :class="{ active: productCategory === 'loan' }" @click="setProductCategory('loan')">
        주식
      </button>
      <button :class="{ active: productCategory === 'investment' }" @click="setProductCategory('investment')">
        현물
      </button>
    </div>

    <div v-if="productCategory === 'deposit'" class="filter-row">
      <input
        v-model="productFilters.q"
        placeholder="상품명 검색"
        @input="onSearchInput"
      />

      <select v-model="productFilters.company" @change="loadDepositProducts">
        <option value="">전체 은행</option>
        <option
          v-for="company in productCompanies"
          :key="company"
          :value="company"
        >
          {{ company }}
        </option>
      </select>

      <select v-model="productFilters.kind" @change="loadDepositProducts">
        <option value="">예금+적금</option>
        <option value="deposit">예금</option>
        <option value="saving">적금</option>
      </select>

      <select v-model="productFilters.ordering" @change="loadDepositProducts">
        <option value="rate">금리 높은순</option>
        <option value="company">은행순</option>
        <option value="name">상품명순</option>
      </select>
    </div>

    <div v-if="productCategory === 'loan'" class="filter-row">
      <input
        v-model="stockFilters.q"
        placeholder="종목명 또는 종목코드 검색"
        @input="onStockSearchInput"
      />

      <select v-model="stockFilters.market" @change="loadStockProducts">
        <option value="">전체 시장</option>
        <option
          v-for="market in stockMarkets"
          :key="market"
          :value="market"
        >
          {{ market }}
        </option>
      </select>

      <select v-model="stockFilters.ordering" @change="loadStockProducts">
        <option value="market_cap">시가총액 높은순</option>
        <option value="price">현재가 높은순</option>
        <option value="change_rate">등락률 높은순</option>
        <option value="name">종목명순</option>
      </select>
    </div>

    <div v-if="loading" class="status-box">
      상품을 불러오는 중입니다.
    </div>

    <div v-else-if="error" class="status-box error">
      {{ error }}
    </div>

    <template v-else>
      <div v-if="productCategory === 'deposit' && !depositProducts.length" class="empty">
        표시할 예적금 상품이 없습니다.
      </div>

      <div v-if="productCategory === 'loan' && !stockProducts.length" class="empty">
        표시할 주식 종목이 없습니다.
      </div>

      <div v-if="productCategory === 'deposit'" class="product-list">
        <article
          v-for="item in depositProducts"
          :key="item.id"
          class="product product-card"
          @click="openDepositProduct(item.id)"
        >
          <button
            class="favorite-btn"
            :class="{ active: item.is_favorite }"
            type="button"
            :title="item.is_favorite ? '관심상품 해제' : '관심상품 추가'"
            @click.stop="toggleFavoriteProduct(item)"
          >
            {{ item.is_favorite ? '★' : '☆' }}
          </button>

          <small>{{ item.product_type === 'deposit' ? '예금' : '적금' }}</small>
          <h3>{{ item.product_name }}</h3>
          <p>{{ item.financial_company_name }}</p>

          <div class="rate">
            최고 <span>{{ item.max_interest_rate || item.interest_rate || '-' }}%</span>
          </div>

          <div class="product-meta">
            <span>{{ item.best_term ? item.best_term + '개월' : '기간 정보 없음' }}</span>
            <span>{{ item.join_way || '가입 방법 정보 없음' }}</span>
          </div>
        </article>
      </div>

      <div v-if="productCategory === 'loan'" class="product-list stock-list">
        <article
          v-for="item in stockProducts"
          :key="item.code || item.isin_code"
          class="product product-card stock-card"
        >
          <small>{{ item.market || '주식' }}</small>
          <h3>{{ item.name }}</h3>
          <p>{{ item.code }}</p>

          <div class="rate">
            현재가 <span>{{ formatWon(item.current_price) }}</span>
          </div>

          <div class="product-meta">
            <span :class="{ positive: item.change_rate > 0, negative: item.change_rate < 0 }">
              등락률 {{ formatRate(item.change_rate) }}
            </span>
            <span>거래량 {{ formatNumber(item.volume) }}</span>
            <span>기준일 {{ formatStockDate(item.base_date) }}</span>
          </div>
        </article>
      </div>

      <div v-if="productCategory === 'investment'" class="result-box spot-panel">
        <h3>현물 가격 변화</h3>

        <div class="category-tabs spot-tabs">
          <button :class="{ active: spotFilters.asset === 'gold' }" @click="setSpotAsset('gold')">
            금(Gold)
          </button>
          <button :class="{ active: spotFilters.asset === 'silver' }" @click="setSpotAsset('silver')">
            은(Silver)
          </button>
        </div>

        <div class="spot-toolbar">
          <label>
            시작일
            <input type="date" v-model="spotFilters.start" @change="loadSpotPrices()" />
          </label>

          <label>
            종료일
            <input type="date" v-model="spotFilters.end" @change="loadSpotPrices()" />
          </label>

          <button class="secondary-btn" type="button" @click="resetSpotPeriod">
            전체 기간
          </button>
        </div>

        <p v-if="spotMessage" class="lock-note">{{ spotMessage }}</p>

        <div v-if="spotPrices.length" class="spot-summary">
          <div>
            <small>선택 자산</small>
            <strong>{{ spotAssetName }}</strong>
          </div>
          <div>
            <small>최근 가격</small>
            <strong>{{ spotLatestPrice }}</strong>
          </div>
          <div>
            <small>조회 기간</small>
            <strong>{{ spotDateRange }}</strong>
          </div>
        </div>

        <svg
          v-if="spotChartPoints"
          :key="`${spotFilters.asset}-${spotPrices.length}-${spotDateRange}`"
          class="spot-chart"
          viewBox="0 0 720 320"
          preserveAspectRatio="none"
        >
          <g v-for="tick in spotYAxisTicks" :key="`y-${tick.label}`">
            <line class="spot-grid" :x1="44" :y1="tick.y" :x2="696" :y2="tick.y"></line>
            <text class="spot-label" :x="38" :y="tick.y + 4" text-anchor="end">{{ tick.label }}</text>
          </g>

          <g v-for="tick in spotXAxisTicks" :key="`x-${tick.label}`">
            <line class="spot-grid" :x1="tick.x" :y1="286" :x2="tick.x" :y2="292"></line>
            <text class="spot-label" :x="tick.x" y="308" text-anchor="middle">{{ tick.label }}</text>
          </g>

          <line class="spot-axis" x1="44" y1="24" x2="44" y2="286"></line>
          <line class="spot-axis" x1="44" y1="286" x2="696" y2="286"></line>
          <text class="spot-title" x="44" y="16">가격($)</text>
          <text class="spot-title" x="696" y="318" text-anchor="end">날짜</text>
          <polyline :points="spotChartPoints"></polyline>
          <circle
            v-for="point in spotChartDots"
            :key="point.date"
            :cx="point.x"
            :cy="point.y"
            r="4"
          >
            <title>{{ point.date }} {{ point.price }}</title>
          </circle>
        </svg>

        <div v-if="!spotPrices.length" class="empty">
          선택한 기간의 현물 가격 데이터가 없습니다.
        </div>
      </div>

      <div
        v-if="productCategory !== 'deposit' && productCategory !== 'investment' && productCategory !== 'loan' && !filteredRecommendations.length"
        class="empty"
      >
        표시할 상품이 없습니다.
      </div>

      <div v-if="productCategory !== 'deposit' && productCategory !== 'investment' && productCategory !== 'loan'" class="product-list">
        <article
          v-for="item in filteredRecommendations"
          :key="item.name"
          class="product product-card"
        >
          <small>{{ categoryLabel(productCategory) }}</small>
          <h3>{{ item.name }}</h3>
          <p>{{ item.reason }}</p>
        </article>
      </div>
    </template>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const productCategory = ref('deposit')
const depositProducts = ref([])
const stockProducts = ref([])
const productCompanies = ref([])
const stockMarkets = ref([])
const recommendations = ref([])
const loading = ref(false)
const error = ref('')
const spotPrices = ref([])
const spotMessage = ref('')
let depositRequestSeq = 0
let stockRequestSeq = 0

const productFilters = ref({
  q: '',
  company: '',
  kind: '',
  ordering: 'rate',
})

const stockFilters = ref({
  q: '',
  market: '',
  ordering: 'market_cap',
})

const spotFilters = ref({
  asset: 'gold',
  start: '',
  end: '',
})

const spotAssetLabels = {
  gold: '금(Gold)',
  silver: '은(Silver)',
}

const categoryMap = {
  card: ['card'],
  loan: ['loan', 'loans'],
}

const filteredRecommendations = computed(() => {
  const categories = categoryMap[productCategory.value] || []
  return recommendations.value.filter((item) => categories.includes(item.category))
})

const spotAssetName = computed(() => {
  return spotAssetLabels[spotFilters.value.asset] || '현물'
})

const spotLatestPrice = computed(() => {
  if (!spotPrices.value.length) {
    return '-'
  }

  const latest = spotPrices.value[spotPrices.value.length - 1]
  return `$${Number(latest.price).toLocaleString()}`
})

const spotDateRange = computed(() => {
  const selectedStart = spotFilters.value.start
  const selectedEnd = spotFilters.value.end

  if (selectedStart || selectedEnd) {
    const fallbackStart = spotPrices.value[0]?.date || '-'
    const fallbackEnd = spotPrices.value[spotPrices.value.length - 1]?.date || '-'

    return `${selectedStart || fallbackStart} ~ ${selectedEnd || fallbackEnd}`
  }

  if (!spotPrices.value.length) {
    return '-'
  }

  return `${spotPrices.value[0].date} ~ ${spotPrices.value[spotPrices.value.length - 1].date}`
})

const spotChartDots = computed(() => {
  if (!spotPrices.value.length) {
    return []
  }

  const width = 720
  const height = 320
  const padding = { left: 44, right: 24, top: 24, bottom: 34 }
  const values = spotPrices.value.map((item) => Number(item.price))
  const min = Math.min(...values)
  const max = Math.max(...values)
  const range = max - min || 1

  return spotPrices.value.map((item, index) => {
    const x = padding.left + ((width - padding.left - padding.right) * index) / Math.max(spotPrices.value.length - 1, 1)
    const y = padding.top + ((max - Number(item.price)) / range) * (height - padding.top - padding.bottom)

    return {
      x: Number(x.toFixed(2)),
      y: Number(y.toFixed(2)),
      date: item.date,
      price: `$${Number(item.price).toLocaleString()}`,
    }
  })
})

const spotChartPoints = computed(() => {
  return spotChartDots.value.map((point) => `${point.x},${point.y}`).join(' ')
})

const spotYAxisTicks = computed(() => {
  if (!spotPrices.value.length) {
    return []
  }

  const values = spotPrices.value.map((item) => Number(item.price))
  const min = Math.min(...values)
  const max = Math.max(...values)
  const range = max - min || 1

  return [0, 1, 2, 3, 4].map((step) => {
    const ratio = step / 4
    const price = max - range * ratio
    const y = 24 + ratio * (286 - 24)

    return {
      y: Number(y.toFixed(2)),
      label: `$${price.toLocaleString(undefined, { maximumFractionDigits: 2 })}`,
    }
  })
})

const spotXAxisTicks = computed(() => {
  if (!spotChartDots.value.length) {
    return []
  }

  const dots = spotChartDots.value
  const tickIndexes = [0, Math.floor((dots.length - 1) / 2), dots.length - 1]
    .filter((value, index, array) => array.indexOf(value) === index)

  return tickIndexes.map((index) => ({
    x: dots[index].x,
    label: dots[index].date.slice(0, 7),
  }))
})

const buildDepositParams = (overrides = {}) => {
  const params = new URLSearchParams()
  const filters = {
    ...productFilters.value,
    ...overrides,
  }

  Object.entries(filters).forEach(([key, value]) => {
    if (value) {
      params.append(key, value)
    }
  })

  return params
}

const buildStockParams = (overrides = {}) => {
  const params = new URLSearchParams()
  const filters = {
    ...stockFilters.value,
    ...overrides,
  }

  Object.entries(filters).forEach(([key, value]) => {
    if (value) {
      params.append(key, value)
    }
  })

  return params
}

const loadDepositProducts = async (overrides = {}) => {
  const requestId = ++depositRequestSeq
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get(
      `http://localhost:8000/api/deposit-products/?${buildDepositParams(overrides).toString()}`,
      {
        withCredentials: true,
      },
    )

    if (requestId !== depositRequestSeq) {
      return
    }

    depositProducts.value = response.data.products || []
    productCompanies.value = response.data.companies || []
  } catch (err) {
    if (requestId !== depositRequestSeq) {
      return
    }

    error.value = err.response?.data?.message || '상품 목록을 불러오지 못했습니다.'
    console.error(err)
  } finally {
    if (requestId === depositRequestSeq) {
      loading.value = false
    }
  }
}

const onSearchInput = (event) => {
  const q = event.target.value
  productFilters.value.q = q
  loadDepositProducts({ q })
}

const loadStockProducts = async (overrides = {}) => {
  const requestId = ++stockRequestSeq
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get(
      `http://localhost:8000/api/stocks/?${buildStockParams(overrides).toString()}`,
      {
        withCredentials: true,
      },
    )

    if (requestId !== stockRequestSeq) {
      return
    }

    stockProducts.value = response.data.stocks || []
    stockMarkets.value = response.data.markets || []
  } catch (err) {
    if (requestId !== stockRequestSeq) {
      return
    }

    error.value = err.response?.data?.message || '주식 목록을 불러오지 못했습니다.'
    console.error(err)
  } finally {
    if (requestId === stockRequestSeq) {
      loading.value = false
    }
  }
}

const onStockSearchInput = (event) => {
  const q = event.target.value
  stockFilters.value.q = q
  loadStockProducts({ q })
}

const loadRecommendations = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/products/', {
      withCredentials: true,
    })
    recommendations.value = response.data.products || []
  } catch (err) {
    console.error(err)
  }
}

const loadSpotPrices = async (asset = spotFilters.value.asset) => {
  loading.value = true
  error.value = ''
  spotMessage.value = ''

  const params = new URLSearchParams()
  params.append('asset', asset)

  if (spotFilters.value.start) {
    params.append('start', spotFilters.value.start)
  }

  if (spotFilters.value.end) {
    params.append('end', spotFilters.value.end)
  }

  try {
    const response = await axios.get(`http://localhost:8000/api/spot-prices/?${params.toString()}`, {
      withCredentials: true,
    })

    spotPrices.value = response.data.prices || []

    if (!spotPrices.value.length) {
      spotMessage.value = '선택한 기간에 해당하는 데이터가 없습니다.'
    }
  } catch (err) {
    spotPrices.value = []
    spotMessage.value = err.response?.data?.message || '현물 가격 데이터를 불러오지 못했습니다.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const setSpotAsset = async (asset) => {
  spotFilters.value.asset = asset
  spotPrices.value = []
  await loadSpotPrices(asset)
}

const resetSpotPeriod = async () => {
  spotFilters.value.start = ''
  spotFilters.value.end = ''
  await loadSpotPrices()
}

const toggleFavoriteProduct = async (item) => {
  try {
    const response = await axios.post(
      `http://localhost:8000/api/deposit-products/${item.id}/favorite/`,
      {},
      {
        withCredentials: true,
      },
    )

    const updatedProduct = response.data.product
    depositProducts.value = depositProducts.value.map((product) => {
      return product.id === updatedProduct.id ? updatedProduct : product
    })
  } catch (err) {
    error.value = err.response?.data?.message || '관심상품을 변경하지 못했습니다.'
    console.error(err)
  }
}

const openDepositProduct = (productId) => {
  router.push(`/deposit-products/${productId}`)
}

const setProductCategory = (category) => {
  productCategory.value = category

  if (category === 'deposit') {
    loadDepositProducts()
  }

  if (category === 'loan') {
    loadStockProducts()
  }

  if (category === 'investment') {
    loadSpotPrices()
  }
}

const categoryLabel = (category) => {
  return {
    card: '카드',
    loan: '주식',
    investment: '현물',
}[category] || '상품'
}

const formatNumber = (value) => {
  return Number(value || 0).toLocaleString()
}

const formatWon = (value) => {
  return `${formatNumber(value)}원`
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

onMounted(() => {
  loadDepositProducts()
  loadRecommendations()
})
</script>
