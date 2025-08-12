<script setup>
// import { newsreview } from '../../data/postreview';
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {  newsItems } from '@/data/news.js'

const route = useRoute()
const router = useRouter()
// 找對應文章
const title = ref('')
const content = ref([])
const imgSrc = ref(newsItems.imgSrc)



// const show = ref(false)
const infoRows = ref([])
const postId = String(route.params.id) // ✅ 轉成字串
const article = newsItems.find(n => String(n.id) === postId)
// 找不到就回列表
if (!article.value) {
  console.warn('找不到文章 id =', postId.value)
  router.replace('/news')
}
/** 初始化：優先 /stores/Posts/PostReview/:id，其次相容 query */
// onMounted(() => {

//   article.value = newsreview.find(n => n.id === postId)
// })
 
    // ✅ 改：直接用 article 的資料，不從 query 取
  title.value = article.title
  content.value = article.content
  imgSrc.value = article.imgSrc

  infoRows.value = [
    ['編號', article.id],
    ['店家名稱', article.store],
    ['標題', article.title]
  ]




/** 返回（避免回到同頁，建議回列表或上一頁） */
const goBack = () => router.push('/news') // 或 router.back()
</script>

<template>
  <div class="page-layout">
    <main class="page-main">
      <!-- 新增：圖片上方的按鈕列 -->
      <img :src="imgSrc" alt="封面圖" class="article-img" />
      <h1 class="article-title">{{ title }}</h1>

      <div class="article-content">
        <p v-for="(para, idx) in content" :key="idx">{{ para }}</p>
      </div>
        <div class="flex justify-center gap-3 mb-2">
        <button class="btn-back" @click="goBack">返回</button>
      </div>
    </main>
  </div>

</template>
<style></style>