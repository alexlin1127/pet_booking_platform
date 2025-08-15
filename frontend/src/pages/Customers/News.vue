<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import Card from '@/components/UI/Card.vue'
import { newsItems } from '@/data/news.js' // 引入假資料
import Pagination from '@/components/common/Pagination.vue' // 如果需要分頁功能

/* ✅ 新增：可選的控制用 props */
const props = defineProps({
  storeId: { type: [String, Number], default: null },   // 有值就只看該店家
  storeName: { type: String, default: '' },             // 有值就顯示「xxx 店家最新消息」
})

const tabs = ['全部', '店休', '住宿服務', '美容服務']
const selectedTab = ref('全部')
const setTab = (tab) => {
  selectedTab.value = tab
}

// ✅ 新增：點擊卡片開啟詳情（用 params 帶 id）
const router = useRouter()
const open = (item) => {
  // 直接帶 params.id 導到 /news/view/:id
  router.push({ path: `/news/view/${item.id}` })
}
const handleOpen = (item) => {
  console.log('[Card click] id=', item.id)   // <— 應該會看到
  router.push({ path: `/news/view/${item.id}` })
}
// ===== 分頁設定 =====
const pageSize = 10                 // 每頁 10 筆
const currentPage = ref(1)

// 先做篩選（不切片）
const filteredAll = computed(() => {
  /* 先依 storeId（若有）篩一次，再依分類篩 */
   const base = props.storeId
    ? newsItems.filter(n => String(n.storeId) === String(props.storeId))
    : newsItems

  return selectedTab.value === '全部'
    ? newsItems
    : newsItems.filter(n => n.tags.includes(selectedTab.value))
})

// 總頁數
const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredAll.value.length / pageSize))
)

// 目前頁面的資料
const pagedNews = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredAll.value.slice(start, start + pageSize)
})

// 換分類就回到第 1 頁
watch(selectedTab, () => { currentPage.value = 1 })

// Pagination 元件回傳的新頁碼
const handlePageChange = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  // 捲到頁面上方（可選）
  window.scrollTo({ top: 0, behavior: 'smooth' })
}



</script>

<template>
  <div class="news-page max-w-screen-xl mx-auto px-4 md:px-8 py-8">
    <!-- Title -->
    <header class="text-center mb-6">
   <!-- ✅ 額外一行：當有 storeName 時顯示 -->
    <p v-if="props.storeName" class="mt-1 text-base md:text-lg text-amber-700">
    {{ props.storeName }}
    </p>
      <h1 class="text-3xl md:text-4xl font-bold tracking-wide">最新消息</h1>
      <p class="text-gray-600 mt-2">掌握店家最新活動、公告與重要訊息</p>
    </header>

    <!-- Filter Tabs -->
    <nav class="news-filter flex flex-wrap items-center justify-start gap-3 md:justify-start gap-4 mb-8">
      <button
        v-for="tab in tabs"
        :key="tab"
        class="tab"
        :class="selectedTab === tab ? 'is-active' : ''"
        @click="setTab(tab)"
      >
        {{ tab }}
      </button>
    </nav>

    <!-- Cards Grid：手機 1 欄、平板/桌機 2 欄；每欄 5 張（總共 10 張） -->
    <section class="news-grid grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8">
      <Card
        v-for="item in pagedNews"
        :key="item.id"
        type="horizontal"
        :clickable="true"
        class="news-card  card--service-look"
        @click="handleOpen(item)"
      >
        <!-- 左側圖片 -->
        <template #image>
          <img
            :src="item.imgSrc"
            :alt="item.title"
            class="h-full w-full object-cover"
            loading="lazy"
          />
        </template>

        <!-- 標題 -->
        <template #title>
          <h3 class="text-lg font-semibold leading-snug line-clamp-1">
            {{ item.title }}
          </h3>
        </template>

        <!-- 內容＋標籤 -->
        <template #content>
          <p class="mt-1 text-sm text-gray-600 line-clamp-2">
            {{ item.summary }}
          </p>
          <p class="text-xs text-[#d8c9b8]">{{ item.brand }}</p> <!-- 新增品牌 -->
          <div class="mt-3 flex flex-wrap gap-2">
            <span
              v-for="t in item.tags"
              :key="t"
              class="news-badge"
            >
              {{ t }}
            </span>
          </div>
        </template>
      </Card>
    </section>
  </div>

  <Pagination
    :current-page="currentPage"
    :total-pages="totalPages"
    @page-change="handlePageChange"
  />
</template>



<style scoped>
.news-page {
  min-height: calc(100vh - 80px);
  padding-top: 80px; /* 導航欄高度 */
}

</style>