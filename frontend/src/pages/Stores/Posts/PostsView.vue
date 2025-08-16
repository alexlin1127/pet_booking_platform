<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { posts } from '../../../data/postsfakedata'
import '../../../styles/pages/Stores/Posts/postsview.css'

const route = useRoute()
const router = useRouter()
const postId = route.params.id
// 取得對應貼文
const post = computed(() => posts.find(p => String(p.id) === String(postId)))

const imgSrc = ref('https://images.unsplash.com/photo-1601758228041-f3b2795255f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80') // 預設封面圖
// const imgSrc = computed(() => post.value?.img || '')
const title = computed(() => post.value?.title || '')
const content = computed(() => {
    // 假設 content 可能是字串或陣列
    if (!post.value) return []
    if (Array.isArray(post.value.content)) return post.value.content
    return [post.value.content]
})

function goBack() {
    router.push('/stores/posts/manage')
}
function goEdit() {
    router.push(`/stores/posts/edit/${postId}`)
}
</script>
<template>
    <!-- 整頁結構，外層負責佈局 -->
    <div class="page-layout">
        <main class="page-main">
            <div class="article-header">
                <div class="article-buttons-fixed">
                    <button class="postsview-btn-back" @click="goBack">返回</button>
                    <button class="postsview-btn-edit" @click="goEdit">編輯</button>
                </div>
            </div>
            <div class="img-container">
                <img :src="imgSrc" alt="封面圖" class="article-img" />
            </div>
            <h1 class="article-title">{{ title }}</h1>
            <div class="article-content">
                <p v-for="(para, idx) in content" :key="idx">{{ para }}</p>
            </div>
        </main>
    </div>
</template>
<style scoped src="../../../styles/pages/Stores/Posts/postsview.css"></style>