<script setup>
import { ref, computed, watch } from 'vue'
import { posts as rawPosts } from '@/data/postsfakedata.js'
import Pagination from '@/components/common/Pagination.vue'

const allPosts = ref(rawPosts)  // rawPosts 就是從檔案 import 的資料

// 篩選類別
const isGrooming = ref(true) // 初始為「美容」
const groomingPosts = computed(() => allPosts.value.filter(post => post.tag === '寵物美容'))
const lodgingPosts = computed(() => allPosts.value.filter(post => post.tag === '寵物住宿'))
const currentPosts = computed(() => (isGrooming.value ? groomingPosts.value : lodgingPosts.value))

// 分頁
const currentPage = ref(1)
const pageSize = 3 // 每頁顯示3個貼文

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return currentPosts.value.slice(start, start + pageSize)
})

const totalPages = computed(() => Math.ceil(currentPosts.value.length / pageSize))

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}
function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}
function toggleFilter() {
  isGrooming.value = !isGrooming.value
  currentPage.value = 1 // 切換篩選時重置到第一頁
}
watch(isGrooming, () => {
  currentPage.value = 1
})
//頁碼
function handlePageChange(page) {
  currentPage.value = page
}
</script>
<template>
<!-- 外層容器 -->
<div class="postmanage-wrapper">
  <div class="postmanage-header">
    <div class="flex flex-col md:flex-row items-start md:items-center gap-4">
     <!-- 左側：撐開寬度 -->
      <h1 class="postmanage-title">貼文管理</h1>
    </div>
      <div class="post-header-actions">
      <button class="post-button">新增貼文</button>
      <button class="post-button">送出審核</button>
      </div>
    </div>

  <!-- 篩選切換 -->
<div class="postmanage-filter-toggle">
  <label class="postmanage-filter-label">美容</label>
  <label class="postmanage-switch">
    <input type="checkbox" class="sr-only peer" v-model="isGrooming"/>
    <div class="postmanage-switch-bar"></div>
  </label>
  <span class="postmanage-filter-label">住宿</span>
</div>

  <div class="post-card-list">
     <div v-for="post in paginatedPosts" :key="post.id" class="post-card">
      <div class="post-thumb"></div>

      <div class="post-content">
        <h2 class="font-semibold">{{ post.title }}</h2>
        <p class="text-xs text-gray-500">日期 {{ post.date }}</p>
        <p class="text-xs text-gray-400 truncate">{{ post.content }}</p>
        <span class="inline-block mt-2 text-xs border px-2 py-0.5 rounded">{{ post.tag }}</span>
      </div>

      <div class="post-actions">
        <div class="post-status">
          <i class="i-bi-check2-all text-lg"></i>
          <span>{{ post.status }}</span>
        </div>
        <button class="post-button">查看全文</button>
        <button class="post-button">刪除文章</button>
      </div>
    </div>
  </div>
</div>
<Pagination
  :current-page="currentPage"
  :total-pages="totalPages"
  @page-change="handlePageChange"
/>
</template>
<style src="@/styles/pages/admin/Stores/storemanagement.css"></style>
