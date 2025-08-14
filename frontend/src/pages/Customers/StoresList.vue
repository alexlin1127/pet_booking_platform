<!-- src/pages/Stores/StoresListPage.vue -->
<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import StoreCard from '@/components/UI/StoreCard.vue'
 import { stores } from '@/data/storeData' // 假資料

const PAGE_SIZE = 9
const route = useRoute()
const router = useRouter()
const type = ref(route.params.type === 'boarding' ? 'boarding' : 'grooming')

/* 篩選表單的 v-model */
const selectedService = ref(type.value)           // 與當前路由同步
const selectedCity = ref('')
const selectedDistrict = ref('')

/* 你可以換成實際清單 */
const cities = ['台北市', '新北市', '桃園市', '花蓮縣']
const districts = ['中正區', '大安區', '信義區', '花蓮市']

const keyword = ref('')
const currentPage = ref(1)

watch(() => route.params.type, (v) => {
  type.value = v === 'boarding' ? 'boarding' : 'grooming'
  selectedService.value = type.value        // <- 同步回下拉選單
  currentPage.value = 1
})

const pageTitle = computed(() =>
  (selectedService.value || type.value) === 'grooming'
    ? '美容店家總覽'
    : '住宿店家總覽'
)

const pageContent = computed(() =>
  (selectedService.value || type.value) === 'grooming'
    ? '瀏覽所有合作店家資訊，快速找到適合你毛孩的美容地點'
    : '瀏覽所有合作店家資訊，快速找到適合你毛孩的住宿地點'
)

const filtered = computed(() => {
  // 用既有變數：優先看 selectedService，沒選時回退到 type
  const mode = selectedService.value || type.value  // 非新增狀態，僅區域常數
  let list = stores.filter(s =>
    mode === 'grooming' ? !!s.hasGrooming : !!s.hasBoarding
  )
  if (selectedCity.value) {
    list = list.filter(s => (s.address || '').includes(selectedCity.value))
  }
  if (selectedDistrict.value) {
    list = list.filter(s => (s.address || '').includes(selectedDistrict.value))
  }
  if (keyword.value.trim()) {
    const kw = keyword.value.trim().toLowerCase()
    list = list.filter(s =>
      (s.storeName || '').toLowerCase().includes(kw) ||
      (s.address || '').toLowerCase().includes(kw) ||
      (s.owner || '').toLowerCase().includes(kw)
    )
  }
  return list
})


const totalPages = computed(() =>
  Math.max(1, Math.ceil(filtered.value.length / PAGE_SIZE))
)

const paginated = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filtered.value.slice(start, start + PAGE_SIZE)
})


watch(selectedService, (v) => {
  if (v === 'grooming' || v === 'boarding') {
    
  }
})
function go(p) {
  if (p >= 1 && p <= totalPages.value) currentPage.value = p
}
/* 點搜尋或任何篩選改變 -> 回到第 1 頁 */
function handleSearch() { go(1) }
watch([selectedService, selectedCity, selectedDistrict, keyword], () => {
  currentPage.value = 1
})
</script>

<template>
  <main class="page">
    <header class="page-header">
      <h1 class="page-title">{{ pageTitle }}</h1>
      <h3 class="page-title text-sm">{{ pageContent }}</h3>

      <div class="toolbar">
           <!-- 服務項目 -->
        <div class="filter-group">
          <label for="service" class="filter-label">選擇服務項目</label>
          <select id="service" v-model="selectedService" class="filter-select">
            <option value="">請選擇服務項目</option>
            <option value="grooming">美容</option>
            <option value="boarding">住宿</option>
          </select>
        </div>

        <!-- 縣市 -->
        <div class="filter-group">
          <label for="city" class="filter-label">選擇縣市</label>
          <select id="city" v-model="selectedCity" class="filter-select">
            <option value="">請選擇縣市</option>
            <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
          </select>
        </div>

        <!-- 地區 -->
        <div class="filter-group">
          <label for="district" class="filter-label">選擇地區</label>
          <select id="district" v-model="selectedDistrict" class="filter-select">
            <option value="">請選擇地區</option>
            <option v-for="d in districts" :key="d" :value="d">{{ d }}</option>
          </select>
        </div>
        <div class="search">
          <input v-model="keyword" type="search" placeholder="請搜尋地區"
                 class="search__input" aria-label="搜尋店家" />
          <button class="btn-search" @click="handleSearch">搜尋</button>
        </div>
      </div>
    </header>

    <section class="store-grid">
      <StoreCard v-for="s in paginated" :key="s.id" :store="s" />
    </section>

    <nav class="pagination" aria-label="分頁">
      <button class="btn btn-ghost" :disabled="currentPage===1" @click="go(currentPage-1)">上一頁</button>
      <span class="pagination__state">第 {{ currentPage }} / {{ totalPages }} 頁</span>
      <button class="btn btn-ghost" :disabled="currentPage===totalPages" @click="go(currentPage+1)">下一頁</button>
    </nav>
  </main>
</template>
