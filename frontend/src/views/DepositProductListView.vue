<template>
  <SidebarLayout class="products-page product-hub-page" surface="soft">
    <template #sidebar>
      <AppSidebar>
        <template #top>
      <div class="product-mascot" aria-hidden="true">
        <img src="/product-sidebar-character.png" alt="" />
      </div>
        </template>

        <template #nav>

      <nav class="product-side-nav" aria-label="?곹뭹 移댄뀒怨좊━">
        <button
          v-for="item in productNavItems"
          :key="item.key"
          type="button"
          :class="{ active: productCategory === item.key }"
          @click="setProductCategory(item.key)"
        >
          <span>{{ item.icon }}</span>
          {{ item.label }}
        </button>
      </nav>
        </template>

        <template #support>

      <div class="product-tip-card daily-finance-word-card">
        <strong>오늘의 금융 테마</strong>
        <p>{{ todayTip }}</p>
        <small v-if="todayTipLoading">臾몄옣??遺덈윭?ㅻ뒗 以묒엯?덈떎.</small>
        <small v-else-if="todayTipError">{{ todayTipError }}</small>
      </div>
        </template>
      </AppSidebar>
    </template>

    <div class="product-main">
      <div class="product-toolbar">
        <div>
          <h1>{{ currentCategoryTitle }}</h1>
          <p>{{ currentCategoryDescription }}</p>
        </div>

        <label class="product-search">
          <input
            v-model="activeSearchKeyword"
            :placeholder="searchPlaceholder"
            @input="onUnifiedSearch"
          />
          <span aria-hidden="true">??</span>
        </label>
      </div>

      <div v-if="productCategory === 'recommended'" class="recommended-products">
        <div v-if="aiRecommendationMessage" class="recommendation-ai-note">
          {{ aiRecommendationMessage }}
        </div>

        <div class="recommend-card">
          <div class="recommend-card-head">
            <div class="recommend-icon category-image-icon">
              <img src="/product_category_icons/deposit-piggy.png" alt="예적금 아이콘" />
            </div>
            <div>
              <h2>예적금</h2>
              <p>?덉젙?곸쑝濡??먯궛??紐⑥쑝怨??댁옄瑜?諛쏆븘蹂댁꽭??</p>
            </div>
            <button type="button" @click="setProductCategory('deposit')">
              ?꾩껜蹂닿린
              <span>??</span>
            </button>
          </div>

          <div class="recommend-list">
            <article
              v-for="item in topDepositProducts"
              :key="item.id"
              class="recommend-row"
              @click="openDepositProduct(item.id)"
            >
              <span class="row-icon bank-icon">
                <img
                  v-if="getBankLogoUrl(item.financial_company_name)"
                  :src="getBankLogoUrl(item.financial_company_name)"
                  :alt="`${item.financial_company_name} 濡쒓퀬`"
                />
                <template v-else>{{ item.financial_company_name?.slice(0, 1) || '?' }}</template>
              </span>
              <div>
        <strong>오늘의 금융 테마</strong>
                <small v-if="item.recommendation_reason" class="recommend-reason">
                  {{ item.recommendation_reason }}
                </small>
                <small>理쒓퀬 ??{{ item.max_interest_rate || item.interest_rate || '-' }}%</small>
              </div>
              <span class="row-arrow">??</span>
            </article>
          </div>

          <button class="more-button" type="button" @click="setProductCategory('deposit')">
            ?붾낫湲?<span>??</span>
          </button>
        </div>

        <div class="recommend-card">
          <div class="recommend-card-head">
            <div class="recommend-icon category-image-icon">
              <img src="/product_category_icons/stock-chart.png" alt="주식 아이콘" />
            </div>
            <div>
              <h2>二쇱떇</h2>
              <p>?쒖옣 媛?μ꽦???믪? 湲곗뾽???ъ옄?대낫?몄슂.</p>
            </div>
            <button type="button" @click="setProductCategory('stock')">
              ?꾩껜蹂닿린
              <span>??</span>
            </button>
          </div>

          <div class="recommend-list">
            <article
              v-for="item in topStockProducts"
              :key="item.code || item.isin_code"
              class="recommend-row"
              @click="openStockProduct(item.code)"
            >
              <span class="row-icon stock-icon">
                <img v-if="item.logo_url" :src="item.logo_url" :alt="`${item.name} 濡쒓퀬`" />
                <template v-else>{{ item.name?.slice(0, 1) || 'S' }}</template>
              </span>
              <div>
        <strong>오늘의 금융 테마</strong>
                <small>{{ formatWon(item.current_price) }}</small>
              </div>
              <em :class="{ positive: item.change_rate > 0, negative: item.change_rate < 0 }">
                {{ formatRate(item.change_rate) }}
              </em>
              <span class="row-arrow">??</span>
            </article>
          </div>

          <button class="more-button" type="button" @click="setProductCategory('stock')">
            ?붾낫湲?<span>??</span>
          </button>
        </div>

      </div>

      <template v-else>
        <div v-if="productCategory === 'deposit'" class="product-filter-card">
          <select v-model="productFilters.company" @change="loadDepositProducts">
            <option value="">전체 은행</option>
            <option v-for="company in productCompanies" :key="company" :value="company">
              {{ company }}
            </option>
          </select>

          <select v-model="productFilters.kind" @change="loadDepositProducts">
            <option value="">?덇툑+?곴툑</option>
            <option value="deposit">?덇툑</option>
            <option value="saving">?곴툑</option>
          </select>

          <select v-model="productFilters.ordering" @change="loadDepositProducts">
            <option value="rate">湲덈━ ?믪???</option>
            <option value="company">??됱닚</option>
            <option value="name">?곹뭹紐낆닚</option>
          </select>
        </div>

        <div v-if="productCategory === 'stock'" class="product-filter-card two">
          <select v-model="stockFilters.market" @change="loadStockProducts">
            <option value="">?꾩껜 ?쒖옣</option>
            <option v-for="market in stockMarkets" :key="market" :value="market">
              {{ market }}
            </option>
          </select>

          <select v-model="stockFilters.ordering" @change="loadStockProducts">
            <option value="market_cap">?쒓?珥앹븸 ?믪???</option>
            <option value="price">?꾩옱媛 ?믪???</option>
            <option value="change_rate">?깅씫瑜??믪???</option>
            <option value="name">醫낅ぉ紐낆닚</option>
          </select>
        </div>

        <div v-if="loading" class="status-box">
          ?곹뭹??遺덈윭?ㅻ뒗 以묒엯?덈떎.
        </div>

        <div v-else-if="error" class="status-box error">
          {{ error }}
        </div>

        <template v-else>
          <div v-if="productCategory === 'deposit' && !depositProducts.length" class="empty product-empty">
            ?쒖떆???덉쟻湲??곹뭹???놁뒿?덈떎.
          </div>

          <div v-if="productCategory === 'stock' && !stockProducts.length" class="empty product-empty">
            ?쒖떆??二쇱떇 醫낅ぉ???놁뒿?덈떎.
          </div>

          <p v-if="productCategory === 'stock' && stockMessage" class="lock-note">
            {{ stockMessage }}
          </p>

          <div v-if="productCategory === 'deposit'" class="product-list product-grid-list">
            <article
              v-for="item in depositProducts"
              :key="item.id"
              class="product product-card product-list-card"
              @click="openDepositProduct(item.id)"
            >
              <button
                class="favorite-btn"
                :class="{ active: item.is_favorite }"
                type="button"
                :title="item.is_favorite ? '愿???곹뭹 ?댁젣' : '愿???곹뭹 異붽?'"
                @click.stop="toggleFavoriteProduct(item)"
              >
                {{ item.is_favorite ? '★' : '☆' }}
              </button>

              <span class="bank-card-logo">
                <img
                  v-if="getBankLogoUrl(item.financial_company_name)"
                  :src="getBankLogoUrl(item.financial_company_name)"
                  :alt="`${item.financial_company_name} 濡쒓퀬`"
                />
                <template v-else>{{ item.financial_company_name?.slice(0, 1) || '?' }}</template>
              </span>
              <small>{{ item.product_type === 'deposit' ? '?덇툑' : '?곴툑' }}</small>
              <h3>{{ item.product_name }}</h3>
              <p>{{ item.financial_company_name }}</p>

              <div class="rate">
                理쒓퀬 <span>{{ item.max_interest_rate || item.interest_rate || '-' }}%</span>
              </div>

              <div class="product-meta">
                <span>{{ item.best_term ? item.best_term + '媛쒖썡' : '湲곌컙 ?뺣낫 ?놁쓬' }}</span>
                <span>{{ item.join_way || '媛??諛⑸쾿 ?뺣낫 ?놁쓬' }}</span>
              </div>
            </article>
          </div>

          <div v-if="productCategory === 'stock'" class="product-list product-grid-list stock-list">
            <article
              v-for="item in stockProducts"
              :key="item.code || item.isin_code"
              class="product product-card product-list-card stock-card"
              @click="openStockProduct(item.code)"
            >
              <button
                class="favorite-btn"
                :class="{ active: item.is_favorite }"
                type="button"
                :title="item.is_favorite ? '愿???곹뭹 ?댁젣' : '愿???곹뭹 異붽?'"
                @click.stop="toggleFavoriteStock(item)"
              >
                {{ item.is_favorite ? '★' : '☆' }}
              </button>

              <span class="stock-card-logo">
                <img v-if="item.logo_url" :src="item.logo_url" :alt="`${item.name} 濡쒓퀬`" />
                <template v-else>{{ item.name?.slice(0, 1) || 'S' }}</template>
              </span>
              <small>{{ item.market || '二쇱떇' }}</small>
              <h3>{{ item.name }}</h3>
              <p>{{ item.code }}</p>

              <div class="rate">
                ?꾩옱媛 <span>{{ formatWon(item.current_price) }}</span>
              </div>

              <div class="product-meta">
                <span :class="{ positive: item.change_rate > 0, negative: item.change_rate < 0 }">
                  ?깅씫瑜?{{ formatRate(item.change_rate) }}
                </span>
                <span>嫄곕옒??{{ formatNumber(item.volume) }}</span>
                <span>湲곗???{{ formatStockDate(item.base_date) }}</span>
              </div>
            </article>
          </div>

          <div v-if="productCategory === 'spot'" class="spot-panel product-spot-panel">
            <h2>?꾨Ъ 媛寃?蹂??</h2>

            <div class="category-tabs spot-tabs">
              <button :class="{ active: spotFilters.asset === 'gold' }" @click="setSpotAsset('gold')">
                湲?Gold)
              </button>
              <button :class="{ active: spotFilters.asset === 'silver' }" @click="setSpotAsset('silver')">
                ?(Silver)
              </button>
            </div>

            <div class="spot-toolbar">
              <label>
                ?쒖옉??
                <input type="date" v-model="spotFilters.start" @change="loadSpotPrices()" />
              </label>

              <label>
                醫낅즺??
                <input type="date" v-model="spotFilters.end" @change="loadSpotPrices()" />
              </label>

              <button class="secondary-btn" type="button" @click="resetSpotPeriod">
                ?꾩껜 湲곌컙
              </button>
            </div>

            <p v-if="spotMessage" class="lock-note">{{ spotMessage }}</p>

            <div v-if="spotPrices.length" class="spot-summary">
              <div>
                <small>?좏깮 ?먯궛</small>
        <strong>오늘의 금융 테마</strong>
              </div>
              <div>
                <small>理쒓렐 媛寃?</small>
        <strong>오늘의 금융 테마</strong>
              </div>
              <div>
                <small>議고쉶 湲곌컙</small>
        <strong>오늘의 금융 테마</strong>
              </div>
            </div>

            <svg
              v-if="spotChartPoints"
              :key="`${spotFilters.asset}-${spotPrices.length}-${spotDateRange}`"
              class="spot-chart"
              viewBox="0 0 760 350"
              preserveAspectRatio="none"
            >
              <g v-for="tick in spotYAxisTicks" :key="`y-${tick.label}`">
                <line class="spot-grid" :x1="76" :y1="tick.y" :x2="690" :y2="tick.y"></line>
                <text class="spot-label" :x="68" :y="tick.y + 4" text-anchor="end">{{ tick.label }}</text>
              </g>

              <g v-for="tick in spotXAxisTicks" :key="`x-${tick.label}`">
                <line class="spot-grid" :x1="tick.x" :y1="292" :x2="tick.x" :y2="298"></line>
                <text class="spot-label" :x="tick.x" y="316" text-anchor="middle">{{ tick.label }}</text>
              </g>

              <line class="spot-axis" x1="76" y1="28" x2="76" y2="292"></line>
              <line class="spot-axis" x1="76" y1="292" x2="690" y2="292"></line>
              <text class="spot-title" x="44" y="16">媛寃?$)</text>
              <text class="spot-title" x="696" y="318" text-anchor="end">?좎쭨</text>
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

            <div v-if="!spotPrices.length" class="empty product-empty">
              ?좏깮??湲곌컙???꾨Ъ 媛寃??곗씠?곌? ?놁뒿?덈떎.
            </div>
          </div>

          <div
            v-if="productCategory === 'favorites' && !filteredFavoriteItems.length"
            class="favorite-preview-panel"
          >
            <div class="favorite-empty-icon">?</div>
            <h2>愿???곹뭹</h2>
            <p>蹂꾪몴瑜??꾨Ⅴ嫄곕굹 ?곸꽭 ?붾㈃?먯꽌 愿?щぉ濡앹뿉 異붽????곹뭹???ш린???쒖떆?⑸땲??</p>
            <button class="primary-btn" type="button" @click="setProductCategory('recommended')">
              異붿쿇 ?곹뭹 ?섎윭蹂닿린
            </button>
          </div>

          <div
            v-if="productCategory === 'favorites' && filteredFavoriteItems.length"
            class="product-list product-grid-list"
          >
            <article
              v-for="item in filteredFavoriteItems"
              :key="item.favorite_key"
              class="product product-card product-list-card"
              :class="{ 'stock-card': item.favorite_type === 'stock' }"
              @click="openFavoriteItem(item)"
            >
              <button
                class="favorite-btn"
                :class="{ active: item.favorite_type === 'stock' ? item.is_favorite : item.is_favorite || item.is_subscribed }"
                type="button"
                title="愿???곹뭹 ?댁젣"
                @click.stop="item.favorite_type === 'stock' ? toggleFavoriteStock(item) : removeFavoriteDepositItem(item)"
              >
                {{ item.favorite_type === 'stock' ? (item.is_favorite ? '★' : '☆') : '★' }}
              </button>

              <span v-if="item.favorite_type === 'stock'" class="stock-card-logo">
                <img v-if="item.logo_url" :src="item.logo_url" :alt="`${item.name} 濡쒓퀬`" />
                <template v-else>{{ item.name?.slice(0, 1) || 'S' }}</template>
              </span>
              <span v-else class="bank-card-logo">
                <img
                  v-if="getBankLogoUrl(item.financial_company_name)"
                  :src="getBankLogoUrl(item.financial_company_name)"
                  :alt="`${item.financial_company_name} 濡쒓퀬`"
                />
                <template v-else>{{ item.financial_company_name?.slice(0, 1) || '?' }}</template>
              </span>
              <small>{{ item.favorite_type === 'stock' ? item.market || '二쇱떇' : item.product_type === 'deposit' ? '?덇툑' : '?곴툑' }}</small>
              <h3>{{ item.favorite_type === 'stock' ? item.name : item.product_name }}</h3>
              <p>{{ item.favorite_type === 'stock' ? item.code : item.financial_company_name }}</p>

              <div class="rate">
                <template v-if="item.favorite_type === 'stock'">
                  ?꾩옱媛 <span>{{ formatWon(item.current_price) }}</span>
                </template>
                <template v-else>
                  理쒓퀬 <span>{{ item.max_interest_rate || item.interest_rate || '-' }}%</span>
                </template>
              </div>

              <div class="product-meta">
                <template v-if="item.favorite_type === 'stock'">
                  <span :class="{ positive: item.change_rate > 0, negative: item.change_rate < 0 }">
                    ?깅씫瑜?{{ formatRate(item.change_rate) }}
                  </span>
                  <span>湲곗???{{ formatStockDate(item.base_date) }}</span>
                </template>
                <template v-else>
                  <span>{{ item.best_term ? item.best_term + '媛쒖썡' : '湲곌컙 ?뺣낫 ?놁쓬' }}</span>
                  <span>{{ item.is_subscribed ? '가입 관심 추가됨' : '관심 상품' }}</span>
                </template>
              </div>
            </article>
          </div>
        </template>
      </template>
    </div>
  </SidebarLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '../services/api'
import AppSidebar from '../components/AppSidebar.vue'
import SidebarLayout from '../components/SidebarLayout.vue'

const route = useRoute()
const router = useRouter()

const allowedProductCategories = ['recommended', 'deposit', 'stock', 'spot', 'favorites']
const initialCategory = allowedProductCategories.includes(route.query.category)
  ? route.query.category
  : 'recommended'

const productCategory = ref(initialCategory)
const depositProducts = ref([])
const favoriteProducts = ref([])
const favoriteStocks = ref([])
const stockProducts = ref([])
const aiDepositProducts = ref([])
const aiStockProducts = ref([])
const productCompanies = ref([])
const stockMarkets = ref([])
const loading = ref(false)
const error = ref('')
const spotPrices = ref([])
const spotMessage = ref('')
const stockMessage = ref('')
const aiRecommendationMessage = ref('')
const todayTip = ref('?묒? ?異??듦????댁씪???좏깮吏瑜??볧?以섏슂.')
const todayTipLoading = ref(false)
const todayTipError = ref('')
let depositRequestSeq = 0
let stockRequestSeq = 0

const productNavItems = [
  { key: 'recommended', label: '추천 상품', icon: '*' },
  { key: 'deposit', label: '예적금', icon: 'D' },
  { key: 'stock', label: '주식', icon: 'S' },
  { key: 'spot', label: '금은', icon: 'G' },
  { key: 'favorites', label: '관심 상품', icon: 'F' },
]

const bankLogoRules = [
  { keywords: ['shinhan', '신한'], file: 'shinhan.png' },
  { keywords: ['kb', '국민'], file: 'kb.png' },
  { keywords: ['hana', '하나'], file: 'hana.png' },
  { keywords: ['woori', '우리'], file: 'woori.png' },
  { keywords: ['nh', '농협'], file: 'nonghyup.png' },
  { keywords: ['ibk', '기업'], file: 'ibk.png' },
  { keywords: ['kakao', '카카오'], file: 'kakao.png' },
  { keywords: ['kbank', '케이'], file: 'kbank.png' },
  { keywords: ['toss', '토스'], file: 'toss.png' },
  { keywords: ['sc'], file: 'sc.png' },
]

const getBankLogoUrl = (companyName = '') => {
  const normalizedName = String(companyName).toLowerCase()
  const matched = bankLogoRules.find((rule) => {
    return rule.keywords.some((keyword) => normalizedName.includes(keyword.toLowerCase()))
  })

  return matched ? `/bank_logos/${matched.file}` : ''
}

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
  gold: '湲?Gold)',
  silver: '?(Silver)',
}

const categoryMeta = {
  recommended: {
    title: '추천 상품',
    description: '나에게 맞는 금융 상품을 확인해보세요.',
    placeholder: '검색어를 입력하세요',
  },
  deposit: {
    title: '예적금',
    description: '은행별 예금과 적금을 비교해보세요.',
    placeholder: '상품명 또는 은행명 검색',
  },
  stock: {
    title: '주식',
    description: '종목명 또는 종목코드로 주식을 조회해보세요.',
    placeholder: '종목명 또는 종목코드 검색',
  },
  spot: {
    title: '금은',
    description: '금과 은 가격 흐름을 확인해보세요.',
    placeholder: '검색어를 입력하세요',
  },
  favorites: {
    title: '관심 상품',
    description: '저장한 관심 상품을 모아볼 수 있습니다.',
    placeholder: '관심 상품 검색',
  },
}

const currentCategoryTitle = computed(() => categoryMeta[productCategory.value]?.title || '?곹뭹')
const currentCategoryDescription = computed(() => categoryMeta[productCategory.value]?.description || '')
const searchPlaceholder = computed(() => categoryMeta[productCategory.value]?.placeholder || '검색어를 입력하세요')

const activeSearchKeyword = computed({
  get() {
    if (productCategory.value === 'deposit') {
      return productFilters.value.q
    }

    if (productCategory.value === 'stock') {
      return stockFilters.value.q
    }

    if (productCategory.value === 'favorites') {
      return productFilters.value.q
    }

    return ''
  },
  set(value) {
    if (productCategory.value === 'deposit') {
      productFilters.value.q = value
    }

    if (productCategory.value === 'stock') {
      stockFilters.value.q = value
    }

    if (productCategory.value === 'favorites') {
      productFilters.value.q = value
    }
  },
})

const filteredFavoriteProducts = computed(() => {
  const keyword = productFilters.value.q.trim().toLowerCase()
  if (!keyword) {
    return favoriteProducts.value
  }

  return favoriteProducts.value.filter((item) => {
    return (
      item.product_name.toLowerCase().includes(keyword) ||
      item.financial_company_name.toLowerCase().includes(keyword)
    )
  })
})

const favoriteDepositItems = computed(() => {
  return favoriteProducts.value.map((item) => ({
    ...item,
    favorite_type: 'deposit',
    favorite_key: `deposit-${item.id}`,
  }))
})

const favoriteStockItems = computed(() => {
  return favoriteStocks.value.map((item) => ({
    ...item,
    favorite_type: 'stock',
    favorite_key: `stock-${item.code}`,
  }))
})

const filteredFavoriteItems = computed(() => {
  const keyword = productFilters.value.q.trim().toLowerCase()
  const items = [...favoriteDepositItems.value, ...favoriteStockItems.value]
  if (!keyword) {
    return items
  }

  return items.filter((item) => {
    if (item.favorite_type === 'stock') {
      return item.name.toLowerCase().includes(keyword) || item.code.toLowerCase().includes(keyword)
    }

    return (
      item.product_name.toLowerCase().includes(keyword) ||
      item.financial_company_name.toLowerCase().includes(keyword)
    )
  })
})

const topDepositProducts = computed(() => {
  return aiDepositProducts.value.length ? aiDepositProducts.value.slice(0, 5) : depositProducts.value.slice(0, 5)
})
const topStockProducts = computed(() => {
  return aiStockProducts.value.length ? aiStockProducts.value.slice(0, 5) : stockProducts.value.slice(0, 5)
})

const spotAssetName = computed(() => {
  return spotAssetLabels[spotFilters.value.asset] || '?꾨Ъ'
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

  const width = 760
  const height = 350
  const padding = { left: 76, right: 70, top: 28, bottom: 58 }
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
    const y = 28 + ratio * (292 - 28)

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
  loading.value = productCategory.value !== 'recommended'
  error.value = ''

  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/deposit-products/?${buildDepositParams(overrides).toString()}`,
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

    error.value = err.response?.data?.message || '?곹뭹 紐⑸줉??遺덈윭?ㅼ? 紐삵뻽?듬땲??'
    console.error(err)
  } finally {
    if (requestId === depositRequestSeq) {
      loading.value = false
    }
  }
}

const loadStockProducts = async (overrides = {}) => {
  const requestId = ++stockRequestSeq
  loading.value = productCategory.value !== 'recommended'
  error.value = ''
  stockMessage.value = ''

  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/stocks/?${buildStockParams(overrides).toString()}`,
      {
        withCredentials: true,
      },
    )

    if (requestId !== stockRequestSeq) {
      return
    }

    stockProducts.value = response.data.stocks || []
    stockMarkets.value = response.data.markets || []
    stockMessage.value = response.data.is_fallback ? response.data.message || '' : ''
  } catch (err) {
    if (requestId !== stockRequestSeq) {
      return
    }

    if (productCategory.value !== 'recommended') {
      error.value = err.response?.data?.message || '二쇱떇 紐⑸줉??遺덈윭?ㅼ? 紐삵뻽?듬땲??'
    }
    console.error(err)
  } finally {
    if (requestId === stockRequestSeq) {
      loading.value = false
    }
  }
}

const onUnifiedSearch = (event) => {
  const q = event.target.value

  if (productCategory.value === 'deposit') {
    productFilters.value.q = q
    loadDepositProducts({ q })
  }

  if (productCategory.value === 'stock') {
    stockFilters.value.q = q
    loadStockProducts({ q })
  }

  if (productCategory.value === 'favorites') {
    productFilters.value.q = q
  }
}

const loadRecommendations = async () => {
  try {
    aiRecommendationMessage.value = 'AI媛 湲덉쑖 ?좏삎??留욌뒗 ?곹뭹??異붿쿇?섍퀬 ?덉뼱??'

    const response = await axios.get(`${API_BASE_URL}/api/ai/recommend-products/`, {
      withCredentials: true,
    })

    aiDepositProducts.value = response.data.products || response.data.deposits || []
    aiStockProducts.value = response.data.stocks || []
    aiRecommendationMessage.value = response.data.message || `${response.data.financial_type || '湲덉쑖 ?덉떦'} ?좏삎 湲곗? ?ㅻ뒛??異붿쿇 ?곹뭹?댁뿉??`
  } catch (err) {
    aiRecommendationMessage.value = err.response?.data?.message || 'AI 異붿쿇??遺덈윭?ㅼ? 紐삵빐 湲곕낯 ?곹뭹??蹂댁뿬?쒕젮??'
    console.error(err)
  }
}

const loadTodayTip = async () => {
  todayTipLoading.value = true
  todayTipError.value = ''

  try {
    const response = await axios.get(`${API_BASE_URL}/api/ai/today-message/`, {
      withCredentials: true,
    })
    if (response.data.message) {
      todayTip.value = response.data.message
    }
  } catch (err) {
    todayTipError.value = err.response?.data?.message || '?ㅻ뒛??湲덉쑖 ?쒕쭏?붾? 遺덈윭?ㅼ? 紐삵뻽?듬땲??'
  } finally {
    todayTipLoading.value = false
  }
}

const loadFavoriteProducts = async () => {
  loading.value = productCategory.value === 'favorites'
  error.value = ''

  try {
    const response = await axios.get(`${API_BASE_URL}/api/favorite-deposit-products/`, {
      withCredentials: true,
    })

    favoriteProducts.value = response.data.products || []
    favoriteStocks.value = response.data.stocks || []
  } catch (err) {
    error.value = err.response?.data?.message || '愿???곹뭹??遺덈윭?ㅼ? 紐삵뻽?듬땲??'
    console.error(err)
  } finally {
    loading.value = false
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
    const response = await axios.get(`${API_BASE_URL}/api/spot-prices/?${params.toString()}`, {
      withCredentials: true,
    })

    spotPrices.value = response.data.prices || []

    if (!spotPrices.value.length) {
      spotMessage.value = '?좏깮??湲곌컙???대떦?섎뒗 ?곗씠?곌? ?놁뒿?덈떎.'
    }
  } catch (err) {
    spotPrices.value = []
    spotMessage.value = err.response?.data?.message || '?꾨Ъ 媛寃??곗씠?곕? 遺덈윭?ㅼ? 紐삵뻽?듬땲??'
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

const toggleFavoriteStock = async (item) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/stocks/${item.code}/favorite/`,
      {
        code: item.code,
        isin_code: item.isin_code,
        name: item.name,
        market: item.market,
        base_date: item.base_date,
        current_price: item.current_price,
        change: item.change,
        change_rate: item.change_rate,
        volume: item.volume,
        market_cap: item.market_cap,
      },
      {
        withCredentials: true,
      },
    )

    const updatedStock = response.data.stock
    stockProducts.value = stockProducts.value.map((stock) => {
      return stock.code === item.code ? { ...stock, is_favorite: response.data.is_favorite } : stock
    })

    if (response.data.is_favorite) {
      favoriteStocks.value = [
        updatedStock,
        ...favoriteStocks.value.filter((stock) => stock.code !== updatedStock.code),
      ]
    } else {
      favoriteStocks.value = favoriteStocks.value.filter((stock) => stock.code !== item.code)
    }
  } catch (err) {
    error.value = err.response?.data?.message || '愿???곹뭹??蹂寃쏀븯吏 紐삵뻽?듬땲??'
    console.error(err)
  }
}

const toggleFavoriteProduct = async (item) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/deposit-products/${item.id}/favorite/`,
      {},
      {
        withCredentials: true,
      },
    )

    const updatedProduct = response.data.product
    depositProducts.value = depositProducts.value.map((product) => {
      return product.id === updatedProduct.id ? updatedProduct : product
    })

    favoriteProducts.value = favoriteProducts.value
      .map((product) => (product.id === updatedProduct.id ? updatedProduct : product))
      .filter((product) => product.is_favorite || product.is_subscribed)

    if ((updatedProduct.is_favorite || updatedProduct.is_subscribed) && !favoriteProducts.value.some((product) => product.id === updatedProduct.id)) {
      favoriteProducts.value = [updatedProduct, ...favoriteProducts.value]
    }
  } catch (err) {
    error.value = err.response?.data?.message || '愿???곹뭹??蹂寃쏀븯吏 紐삵뻽?듬땲??'
    console.error(err)
  }
}

const removeFavoriteDepositItem = async (item) => {
  try {
    if (item.is_favorite) {
      await axios.post(
        `${API_BASE_URL}/api/deposit-products/${item.id}/favorite/`,
        {},
        {
          withCredentials: true,
        },
      )
    }

    if (item.is_subscribed) {
      await axios.delete(
        `${API_BASE_URL}/api/deposit-products/${item.id}/join/`,
        {
          withCredentials: true,
        },
      )
    }

    favoriteProducts.value = favoriteProducts.value.filter((product) => product.id !== item.id)
    depositProducts.value = depositProducts.value.map((product) => {
      if (product.id !== item.id) {
        return product
      }

      return {
        ...product,
        is_favorite: false,
        is_subscribed: false,
      }
    })
  } catch (err) {
    error.value = err.response?.data?.message || '愿???곹뭹???쒓굅?섏? 紐삵뻽?듬땲??'
    console.error(err)
  }
}

const openDepositProduct = (productId) => {
  router.push(`/deposit-products/${productId}`)
}

const openStockProduct = (stockCode) => {
  if (!stockCode) {
    return
  }

  router.push(`/stocks/${stockCode}`)
}

const openFavoriteItem = (item) => {
  if (item.favorite_type === 'stock') {
    openStockProduct(item.code)
    return
  }

  openDepositProduct(item.id)
}

const setProductCategory = (category) => {
  productCategory.value = category
  error.value = ''

  if (category === 'deposit' && !depositProducts.value.length) {
    loadDepositProducts()
  }

  if (category === 'stock' && !stockProducts.value.length) {
    loadStockProducts()
  }

  if (category === 'spot') {
    loadSpotPrices()
  }

  if (category === 'favorites') {
    loadFavoriteProducts()
  }
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
  loadTodayTip()
  loadDepositProducts()
  loadStockProducts()
  loadRecommendations()
  loadFavoriteProducts()

  if (productCategory.value === 'spot') {
    loadSpotPrices()
  }
})
</script>




