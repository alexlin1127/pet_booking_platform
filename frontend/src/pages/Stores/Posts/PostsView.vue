<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { posts } from '../../../data/postsfakedata'

const route = useRoute()
const postId = route.params.id
// 取得對應貼文
const post = computed(() => posts.find(p => String(p.id) === String(postId)))

const imgSrc = computed(() => post.value?.img || '')
const title = computed(() => post.value?.title || '')
const content = computed(() => {
  // 假設 content 可能是字串或陣列
  if (!post.value) return []
  if (Array.isArray(post.value.content)) return post.value.content
  return [post.value.content]
})
</script>
<template>
    <!-- 整頁結構，外層負責佈局 -->
    <div class="page-layout">
        <main class="page-main">
            <img :src="imgSrc" alt="封面圖" class="article-img" />
            <h1 class="article-title">{{ title }}</h1>
            <div class="article-content">
                <p v-for="(para, idx) in content" :key="idx">{{ para }}</p>
            </div>
        </main>
    </div>
</template>