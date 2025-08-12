<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Card from '@/components/UI/Card.vue'
import { newsItems } from '@/data/news.js' // 引入假資料
import Pagination from '@/components/common/Pagination.vue' // 如果需要分頁功能
const tabs = ['全部', '店休', '住宿服務', '美容服務']
const selectedTab = ref('全部')
const setTab = (tab) => {
  selectedTab.value = tab
}

const filteredNews = computed(() => {
  if (selectedTab.value === '全部') return newsItems.slice(0, 10)
  return newsItems.filter(n => n.tags.includes(selectedTab.value)).slice(0, 10)
})

// ✅ 新增：點擊卡片開啟詳情（用 params 帶 id）
const router = useRouter()
const open = (item) => {
  // 直接帶 params.id 導到 /news/view/:id
  router.push({ path: `/news/view/${item.id}` })
}


const handleOpen = (item) => {
  console.log('[Card click] id=', item.id)   // <— 應該會看到
  router.push(`/news/view/${item.id}`)
}
</script>

<template>
  <div class="news-page max-w-screen-xl mx-auto px-4 md:px-8 py-8">
    <!-- Title -->
    <header class="text-center mb-6">
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
        v-for="item in filteredNews"
        :key="item.id"
        type="horizontal"
        :clickable="true"
        class="news-card"
        @click="handleOpen(item)"
      >
        <!-- 左側圖片 -->
        <template #image>
          <img
            :src="item.image"
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

  <!-- <Pagination
    :current-page="currentPage"
    :total-pages="totalPages"
    @page-change="handlePageChange"
  /> -->
</template>



<style scoped>
.news-page {
  min-height: calc(100vh - 80px);
  padding-top: 80px; /* 導航欄高度 */
}
</style>