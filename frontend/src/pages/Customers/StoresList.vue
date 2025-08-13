<!-- src/pages/Stores/StoresListPage.vue -->
<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import StoreCard from '@/components/Stores/StoreCard.vue'
import '@/styles/pages/Stores/list.css'

// 直接用你提供的假資料檔
import { stores } from '@/data/stores'   // ← 路徑依你的專案調整

const PAGE_SIZE = 9
const route = useRoute()
const router = useRouter()
const type = ref(route.params.type === 'lodging' ? 'lodging' : 'grooming')
const keyword = ref('')
const currentPage = ref(1)

watch(() => route.params.type, (v) => {
  type.value = v === 'lodging' ? 'lodging' : 'grooming'
  currentPage.value = 1
})

const pageTitle = computed(() =>
  type.value === 'grooming' ? '美容店家總覽' : '住宿店家總覽'
)

const filtered = computed(() => {
  // 先依類型（hasGrooming / hasLodging）篩
  const typed = stores.filter(s =>
    type.value === 'grooming' ? s.hasGrooming : s.hasLodging
  )
  if (!keyword.value.trim()) return typed
  const kw = keyword.value.trim().toLowerCase()
  return typed.filter(s =>
    (s.storeName || '').toLowerCase().includes(kw) ||
    (s.address || '').toLowerCase().includes(kw) ||
    (s.owner || '').toLowerCase().includes(kw)
  )
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filtered.value.length / PAGE_SIZE))
)

const paginated = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filtered.value.slice(start, start + PAGE_SIZE)
})

function goto(next) {
  if (next !== type.value)
    router.push({ name: 'StoresList', params: { type: next } })
}
function go(p) {
  if (p >= 1 && p <= totalPages.value) currentPage.value = p
}
</script>

<template>
  <main class="page">
    <header class="page-header">
      <h1 class="page-title">{{ pageTitle }}</h1>

      <div class="toolbar">
        <div class="tabs">
          <button class="tab" :class="{ 'tab--active': type==='grooming' }" @click="goto('grooming')">美容</button>
          <button class="tab" :class="{ 'tab--active': type==='lodging' }"  @click="goto('lodging')">住宿</button>
        </div>

        <div class="search">
          <input v-model="keyword" type="search" placeholder="搜尋店名／地址／負責人"
                 class="search__input" aria-label="搜尋店家" />
          <button class="btn btn-outline" @click="go(1)">搜尋</button>
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
