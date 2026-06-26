<template>
  <section class="card panel deposit-detail-page">
    <RouterLink
      class="secondary-btn back-btn icon-back-btn"
      to="/deposit-products?category=deposit"
      aria-label="?덉쟻湲??꾩껜?곹뭹 紐⑸줉?쇰줈"
      title="?덉쟻湲??꾩껜?곹뭹 紐⑸줉?쇰줈"
    >
      ??    </RouterLink>

    <div v-if="loading" class="status-box">
      ?곹뭹 ?뺣낫瑜?遺덈윭?ㅻ뒗 以묒엯?덈떎.
    </div>

    <div v-else-if="error" class="status-box error">
      {{ error }}
    </div>

    <div v-else-if="product">
      <div class="deposit-detail-head">
        <span class="detail-kicker">{{ product.product_type_display || '예적금' }}</span>
        <h2>{{ product.product_name }}</h2>
      </div>

      <div class="deposit-info-grid">
        <article class="deposit-info-card">
          <span class="deposit-info-icon">???</span>
          <div>
            <small>???</small>
            <strong>{{ product.financial_company_name || '-' }}</strong>
          </div>
        </article>

        <article class="deposit-info-card">
          <span class="deposit-info-icon">諛⑸쾿</span>
          <div>
            <small>媛??諛⑸쾿</small>
            <strong>{{ product.join_way || '-' }}</strong>
          </div>
        </article>

        <article class="deposit-info-card">
          <span class="deposit-info-icon">???</span>
          <div>
            <small>媛?????</small>
            <strong>{{ product.join_member || '-' }}</strong>
          </div>
        </article>
      </div>

      <div class="deposit-note-grid">
        <article class="deposit-note-card">
          <small>?곕? 議곌굔</small>
          <ul v-if="formatNoteLines(product.special_condition).length" class="deposit-note-list">
            <li
              v-for="line in formatNoteLines(product.special_condition)"
              :key="line"
            >
              {{ line }}
            </li>
          </ul>
          <p v-else>-</p>
        </article>

        <article class="deposit-note-card">
          <small>湲고? ?덈궡</small>
          <ul v-if="formatNoteLines(product.etc_note).length" class="deposit-note-list">
            <li
              v-for="line in formatNoteLines(product.etc_note)"
              :key="line"
            >
              {{ line }}
            </li>
          </ul>
          <p v-else>-</p>
        </article>
      </div>

      <div class="button-row">
        <button
          class="primary-btn"
          type="button"
          @click="toggleInterestProduct"
        >
          {{ product.is_subscribed ? '愿?щぉ濡앹뿉???쒓굅?섍린' : '愿?щぉ濡앹뿉 異붽??섍린' }}
        </button>

        <button class="secondary-btn" type="button" @click="goToBankSearch">
          洹쇱쿂 ???寃??        </button>
      </div>

      <p v-if="joinMessage" class="lock-note">{{ joinMessage }}</p>

      <table class="detail-table">
        <thead>
          <tr>
            <th>湲곌컙</th>
            <th>湲덈━?좏삎</th>
            <th>湲곕낯湲덈━</th>
            <th>理쒓퀬湲덈━</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="option in product.options"
            :key="`${option.saving_term}-${option.interest_rate_type_name}-${option.reserve_type_name}`"
          >
            <td>{{ option.saving_term ? option.saving_term + '媛쒖썡' : '-' }}</td>
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
import { API_BASE_URL } from '../services/api'

const route = useRoute()
const router = useRouter()

const product = ref(null)
const loading = ref(true)
const error = ref('')
const joinMessage = ref('')

const formatNoteLines = (text) => {
  return String(text || '')
    .replace(/\r\n/g, '\n')
    .split(/\n|(?<=??.)|(?<=??.)|(?<=??.)|(?<=??.)|(?<=\))\s*,|,\s*(?=\d+\.)/g)
    .map((line) => line.replace(/^[-?띉?s]+/, '').trim())
    .filter(Boolean)
}

const loadProduct = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/deposit-products/${route.params.id}/`,
      {
        withCredentials: true,
      },
    )

    product.value = response.data.product
  } catch (err) {
    error.value = err.response?.data?.message || '?곹뭹 ?뺣낫瑜?遺덈윭?ㅼ? 紐삵뻽?듬땲??'
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
    const url = `${API_BASE_URL}/api/deposit-products/${product.value.id}/join/`
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
    joinMessage.value = err.response?.data?.message || '愿?щぉ濡앹쓣 蹂寃쏀븯吏 紐삵뻽?듬땲??'
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
