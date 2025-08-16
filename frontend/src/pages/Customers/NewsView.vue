<script setup>
import { computed, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { newsItems } from '../../data/news.js'

const route = useRoute()
const router = useRouter()

// 1) 取得路由參數 id（字串化）
const postId = computed(() => String(route.params.id))

// 2) 找到對應文章（computed）
const article = computed(() =>
    newsItems.find(n => String(n.id) === postId.value)
)

// 3) 將需要的欄位「投影」成 computed，模板直接吃
const title = computed(() => article.value?.title ?? '')
const imgSrc = computed(() => article.value?.imgSrc ?? '')
const content = computed(() => article.value?.content ?? [])
const store = computed(() => article.value?.store ?? '')
const date = computed(() => article.value?.date ?? '')

// 4) 找不到就回列表（用 watchEffect 保證在值變更時也會反應）
watchEffect(() => {
    if (!article.value) {
        console.warn('找不到文章 id =', postId.value)
        router.replace('/news')
    }
})

// 返回
const goBack = () => router.push('/news')
</script>

<template>
    <div class="content-area" v-if="article">
        <img :src="imgSrc" :alt="title" class="article-img" />
        <h1 class="article-title">{{ title }}</h1>
        <div class="article-meta">
            <span>{{ store }}</span>
            <span>·</span>
            <span>{{ date }}</span>
        </div>

        <div class="article-content">
            <p v-for="(para, idx) in content" :key="idx">{{ para }}</p>
        </div>

        <div style="display: flex; justify-content: center; gap: 0.75rem; margin-top: 1.5rem;">
            <button class="btn-back" @click="goBack">返回</button>
        </div>
    </div>
</template>

<style scoped src="../../styles/pages/Customers/newsview.css"></style>