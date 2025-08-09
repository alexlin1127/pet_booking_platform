<script setup>
import { ref, computed, watch } from 'vue'
import { posts as rawPosts } from '@/data/postsfakedata.js'
import Pagination from '@/components/common/Pagination.vue'
import { useRouter } from 'vue-router' // 引入路由
import ModalBox from '@/components/UI/ModalBox.vue'

const router = useRouter()

const allPosts = ref([...rawPosts])  // rawPosts 就是從檔案 import 的資料

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
// 查看文章
function viewPost(id) {
  router.push(`/stores/posts/${id}`)  // 根據實際路由設計修改
}
const showModal = ref(false)
const selectedPost = ref(null)
const infoRows = ref([])
// 點擊刪除按鈕：觸發開啟 Modal 並帶入該篇文章
function openDeleteModal(post) {
  console.log('🔍 傳進來的 post:', post)
  if (!post) {
    console.warn('⚠️ post 是 undefined，請檢查按鈕綁定位置！')
    return
  }
  selectedPost.value = post
  infoRows.value = [
    [`「${post.title}」`, post.content ]
  ]
  showModal.value = true
}


// 刪除文章
function deletePost() {
  if (!selectedPost.value) return
  console.log('🧪 刪除這筆：', selectedPost.value)
// ✅ 實際刪除
 const before = allPosts.value.length  
allPosts.value = allPosts.value.filter(p => String(p.id) !== String(selectedPost.value.id))

const after = allPosts.value.length

  console.log(`📉 刪除前 ${before} 筆，刪除後 ${after} 筆`)
  // ✅ 關閉 modal
  showModal.value = false
  selectedPost.value = null
}
//按鈕-新增貼文跳轉
function goToNewPost() {
  router.push('/stores/newpost')
}
function debug(post) {
  console.log('🔥 debug post:', post)
}
//modelbox按鈕點擊處理
function handleButtonClick({ action, data, button }) {
  console.log('🔥 收到 Modal 回傳:', action, data)

  if (action === 'cancel') {
    showModal.value = false
    selectedPost.value = null
  } else if (action === 'confirm') {
    deletePost()
  }
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
      <button class="post-button" @click="goToNewPost">新增貼文</button>
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
        <button class="post-button" @click="viewPost(post.id)">查看完整文章</button>
        <button class="post-button"@click="() => { console.log(post); openDeleteModal(post) }">刪除文章</button>
      </div>
    </div>
  </div>
</div>
<Pagination
  :current-page="currentPage"
  :total-pages="totalPages"
  @page-change="handlePageChange"
/>
<ModalBox class="store-page"
    :visible="showModal"
    :title=" `確定刪除此貼文?`"
    :infoRows="infoRows"
    :buttons="[
      {
        text: '取消並返回',
        action: 'cancel',
        class: 'modal-btn-cancel'
      },
      {
        text: '刪除',
        action: 'confirm',
        class: 'modal-btn-danger'
      }
    ]"
    @close="showModal = false"
    @button-click="handleButtonClick"
  />
</template>
<style src="@/styles/pages/admin/Stores/storemanagement.css"></style>
