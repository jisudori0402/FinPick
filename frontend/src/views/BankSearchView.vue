<template>
  <section class="card panel bank-search-page">
    <RouterLink
      class="secondary-btn back-btn icon-back-btn bank-back-btn"
      :to="product ? `/deposit-products/${product.id}` : '/deposit-products'"
      aria-label="상품 상세로"
      title="상품 상세로"
    >
      ??    </RouterLink>

    <h2>근처 은행 검색</h2>

    <p v-if="product">
        <strong>오늘의 금융 테마</strong>
      <span> ?곸뾽?먯쓣 吏?꾩뿉??李얠븘蹂댁꽭??</span>
    </p>

    <div class="filter-row bank-filter-row">
      <input
        v-model="bankSearchKeyword"
        placeholder="주소 또는 장소를 입력하세요"
        @keyup.enter="searchBankLocation"
      />
      <button class="primary-btn" type="button" @click="searchBankLocation">
        寃??
      </button>
    </div>

    <p v-if="bankSearchMessage" class="lock-note">{{ bankSearchMessage }}</p>
    <p v-if="routeMessage" class="lock-note">{{ routeMessage }}</p>

    <div id="bank-map" class="map-box"></div>

    <div class="bank-list">
      <button
        v-for="bank in nearbyBanks"
        :key="bank.id || bank.place_name"
        class="bank-item"
        type="button"
        @click="moveToBank(bank)"
      >
        <h3>{{ bank.place_name }}</h3>
        <p>{{ bank.road_address_name || bank.address_name || '-' }}</p>
        <small>{{ bank.distance ? bank.distance + 'm' : '' }}</small>
      </button>
    </div>
  </section>
</template>

<script setup>
import { nextTick, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '../services/api'

const route = useRoute()

const product = ref(null)
const bankSearchKeyword = ref('')
const bankSearchMessage = ref('')
const routeMessage = ref('')
const nearbyBanks = ref([])

let kakaoMapAppKey = ''
let bankMap = null
let bankMarkers = []
let bankInfoWindow = null
let routePolyline = null
let routeStartMarker = null

const loadProduct = async () => {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/deposit-products/${route.params.productId}/`,
      {
        withCredentials: true,
      },
    )
    product.value = response.data.product
  } catch (err) {
    bankSearchMessage.value = err.response?.data?.message || '?곹뭹 ?뺣낫瑜?遺덈윭?ㅼ? 紐삵뻽?듬땲??'
    console.error(err)
  }
}

const loadMapConfig = async () => {
  const response = await axios.get(`${API_BASE_URL}/api/map-config/`, {
    withCredentials: true,
  })
  kakaoMapAppKey = response.data.kakao_map_app_key || ''
}

const loadKakaoMap = () => {
  return new Promise((resolve, reject) => {
    if (!kakaoMapAppKey) {
      reject(new Error('Kakao Maps JavaScript ?ㅺ? ?ㅼ젙?섏? ?딆븯?듬땲??'))
      return
    }

    if (window.kakao?.maps) {
      window.kakao.maps.load(resolve)
      return
    }

    const existingScript = document.querySelector('script[data-kakao-map-sdk="true"]')
    if (existingScript) {
      existingScript.addEventListener('load', () => window.kakao.maps.load(resolve), { once: true })
      existingScript.addEventListener('error', () => reject(new Error('Kakao Maps瑜?遺덈윭?ㅼ? 紐삵뻽?듬땲??')), { once: true })
      return
    }

    const script = document.createElement('script')
    script.dataset.kakaoMapSdk = 'true'
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${kakaoMapAppKey}&libraries=services&autoload=false`
    script.onload = () => window.kakao.maps.load(resolve)
    script.onerror = () => reject(new Error('Kakao Maps瑜?遺덈윭?ㅼ? 紐삵뻽?듬땲??'))
    document.head.appendChild(script)
  })
}

const clearBankMarkers = () => {
  bankMarkers.forEach((marker) => marker.setMap(null))
  bankMarkers = []

  if (bankInfoWindow) {
    bankInfoWindow.close()
  }
}

const clearRoute = () => {
  if (routePolyline) {
    routePolyline.setMap(null)
    routePolyline = null
  }

  if (routeStartMarker) {
    routeStartMarker.setMap(null)
    routeStartMarker = null
  }

  routeMessage.value = ''
}

const renderBankMap = async (lat = 37.566826, lng = 126.9786567) => {
  await loadKakaoMap()
  await nextTick()

  const container = document.getElementById('bank-map')
  const center = new window.kakao.maps.LatLng(lat, lng)
  bankMap = new window.kakao.maps.Map(container, { center, level: 4 })
  bankInfoWindow = new window.kakao.maps.InfoWindow({ zIndex: 1 })
  clearRoute()
}

const normalizeBankName = (name) => {
  return (name || '')
    .replace(/주식회사/g, '')
    .replace(/\(주\)/g, '')
    .replace(/은행/g, '은행')
    .trim()
}

const searchNearbyBanks = (lat, lng) => {
  const places = new window.kakao.maps.services.Places()
  const location = new window.kakao.maps.LatLng(lat, lng)
  const bankName = normalizeBankName(product.value?.financial_company_name)
  const keyword = bankName || '은행'

  places.keywordSearch((keyword), (data, status) => {
    if (status !== window.kakao.maps.services.Status.OK) {
      nearbyBanks.value = []
      bankSearchMessage.value = `${keyword} ?곸뾽?먯쓣 李얠? 紐삵뻽?듬땲??`
      return
    }

    clearBankMarkers()

      const bankNameWithoutSuffix = bankName.replace('은행', '')
    const filteredBanks = data.filter((bank) => {
      const bankNameWithoutSuffix = bankName.replace('은행', '')
    })

    nearbyBanks.value = filteredBanks

    filteredBanks.forEach((bank) => {
      const position = new window.kakao.maps.LatLng(bank.y, bank.x)
      const marker = new window.kakao.maps.Marker({ map: bankMap, position })

      window.kakao.maps.event.addListener(marker, 'mouseover', () => {
        bankInfoWindow.setContent(`<div style="padding:6px 10px;font-size:13px;">${bank.place_name}</div>`)
        bankInfoWindow.open(bankMap, marker)
      })

      window.kakao.maps.event.addListener(marker, 'mouseout', () => {
        bankInfoWindow.close()
      })

      bankMarkers.push(marker)
    })

    bankMap.setCenter(location)
    bankSearchMessage.value = `${keyword} ?곸뾽??${filteredBanks.length}媛쒕? 李얠븯?듬땲??`
  }, {
    location,
    radius: 3000,
    sort: window.kakao.maps.services.SortBy.DISTANCE,
  })
}

const searchBankLocation = async () => {
  bankSearchMessage.value = ''

  try {
    await loadKakaoMap()
  } catch (err) {
    bankSearchMessage.value = `${err.message} .env??KAKAO_MAP_APP_KEY瑜??ㅼ젙??二쇱꽭??`
    return
  }

  const keyword = bankSearchKeyword.value.trim()

  if (!keyword) {
    bankSearchMessage.value = '二쇱냼 ?먮뒗 ?μ냼瑜??낅젰??二쇱꽭??'
    return
  }

  const geocoder = new window.kakao.maps.services.Geocoder()
  geocoder.addressSearch(keyword, (result, status) => {
    if (status === window.kakao.maps.services.Status.OK && result.length) {
      const lat = Number(result[0].y)
      const lng = Number(result[0].x)
      renderBankMap(lat, lng).then(() => searchNearbyBanks(lat, lng))
      return
    }

    const places = new window.kakao.maps.services.Places()
    places.keywordSearch(keyword, (data, placeStatus) => {
      if (placeStatus !== window.kakao.maps.services.Status.OK || !data.length) {
        bankSearchMessage.value = '?낅젰???꾩튂瑜?李얠? 紐삵뻽?듬땲??'
        return
      }

      const lat = Number(data[0].y)
      const lng = Number(data[0].x)
      renderBankMap(lat, lng).then(() => searchNearbyBanks(lat, lng))
    })
  })
}

const moveToBank = (bank) => {
  if (!bankMap || !window.kakao?.maps) {
    return
  }

  const position = new window.kakao.maps.LatLng(bank.y, bank.x)
  bankMap.setCenter(position)
  bankMap.setLevel(3)
  drawRouteToBank(bank)
}

const drawRouteToBank = async (bank) => {
  clearRoute()
  routeMessage.value = '硫?곗틺?쇱뒪 ??궪?먯꽌 ?좏깮????됯퉴吏 寃쎈줈瑜?遺덈윭?ㅻ뒗 以묒엯?덈떎.'

  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/bank-route/?lng=${bank.x}&lat=${bank.y}`,
      {
        withCredentials: true,
      },
    )

    const path = (response.data.points || []).map((point) => {
      return new window.kakao.maps.LatLng(point.lat, point.lng)
    })

    if (!path.length) {
      routeMessage.value = '?쒖떆??寃쎈줈 醫뚰몴媛 ?놁뒿?덈떎.'
      return
    }

    routePolyline = new window.kakao.maps.Polyline({
      map: bankMap,
      path,
      strokeWeight: 6,
      strokeColor: '#2563eb',
      strokeOpacity: 0.85,
      strokeStyle: 'solid',
    })

    routeStartMarker = new window.kakao.maps.Marker({
      map: bankMap,
      position: new window.kakao.maps.LatLng(37.5012743, 127.039585),
    })

    const bounds = new window.kakao.maps.LatLngBounds()
    path.forEach((point) => bounds.extend(point))
    bounds.extend(new window.kakao.maps.LatLng(bank.y, bank.x))
    bankMap.setBounds(bounds)

    const km = response.data.distance ? (response.data.distance / 1000).toFixed(1) : '-'
    const min = response.data.duration ? Math.round(response.data.duration / 60) : '-'
    routeMessage.value = `멀티캠에서 ${bank.place_name}: 약 ${km}km, ${min}분`
  } catch (err) {
    routeMessage.value = err.response?.data?.message || '寃쎈줈瑜?遺덈윭?ㅼ? 紐삵뻽?듬땲??'
    console.error(err)
  }
}

onMounted(async () => {
  await loadProduct()
  await loadMapConfig()

  try {
    await renderBankMap()
    bankSearchMessage.value = '주소 또는 장소를 입력한 뒤 은행을 검색해보세요.'
  } catch (err) {
    bankSearchMessage.value = `${err.message} .env의 KAKAO_MAP_APP_KEY를 확인해주세요.`
  }
})

onUnmounted(() => {
  clearBankMarkers()
  clearRoute()
})
</script>
