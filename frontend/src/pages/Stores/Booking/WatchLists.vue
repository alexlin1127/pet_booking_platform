<script setup>

import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { bookings } from '../../../data/bookingfakedata'
import WatchListCard from './WatchListCard.vue'
import Pagination from '../../../components/common/Pagination.vue'

const pageSize = 5
const route = useRoute()
const router = useRouter()
const isGrooming = ref(route.path === '/stores/grooming/watchlists')
const currentPage = ref(1) // 分頁  
const searchText = ref('')

// 監聽路由變化，自動切換滑軌
watch(() => route.path, (newPath) => {
    isGrooming.value = newPath === '/stores/grooming/watchlists'
    currentPage.value = 1 // 重置分頁
})

// 監聽滑軌變化，自動切換路由
watch(isGrooming, (newValue) => {
    const targetPath = newValue ? '/stores/grooming/watchlists' : '/stores/boarding/watchlists'
    if (route.path !== targetPath) {
        router.push(targetPath)
    }
})

// 只顯示已完成且列入觀察的訂單
const filteredWatchLists = computed(() => {
    let arr = bookings.filter(item => item.status === '已完成' && item.blacklist === true)
        .filter(item => isGrooming.value ? item.service_type === '美容' : item.service_type === '住宿');
    if (searchText.value.trim()) {
        arr = arr.filter(item => item.customer_name.includes(searchText.value.trim()))
    }
    return arr;
})

// 分頁
const totalPages = computed(() => Math.ceil(filteredWatchLists.value.length / pageSize))
const paginatedWatchLists = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    return filteredWatchLists.value.slice(start, start + pageSize)
})

const handlePageChange = (page) => { currentPage.value = page }

function handleSearch() {
    currentPage.value = 1
}
</script>

<template>
    <div class="watch-list-container">
        <h1 class="watch-list-main-title">觀察名單</h1>

        <div class="watch-list-filter-section"> 
            <!-- 篩選切換（滑軌樣式） -->
            <label class="watch-list-tab-label grooming-label" :class="{ 'watch-list-tab-active': isGrooming }" @click="isGrooming = true">美容</label>
            <label class="watch-list-tab-label boarding-label" :class="{ 'watch-list-tab-active': !isGrooming }" @click="isGrooming = false">住宿</label>
            
            <!-- 搜尋顧客姓名 -->
            <label class="watch-list-search-wrapper">
                <span class="watch-list-search-label">搜尋顧客姓名：</span>
                <input type="text" 
                       v-model="searchText" 
                       @keyup.enter="handleSearch" 
                       placeholder="請輸入姓名"
                       class="watch-list-search-input" />
            </label>
            <button class="watch-list-search-button" @click="handleSearch">搜尋</button>
        </div>

        <div class="watch-list-table-wrapper">
            <table class="watch-list-table">
                <thead class="watch-list-table-header">
                    <tr class="watch-list-header-row">
                        <th class="watch-list-header-cell">訂單編號</th>
                        <th class="watch-list-header-cell">客戶姓名</th>
                        <th class="watch-list-header-cell">聯絡電話</th>
                        <th class="watch-list-header-cell">預約服務</th>
                        <th class="watch-list-header-cell">預約日期</th>
                        <th class="watch-list-header-cell">備註</th>
                        <th class="watch-list-header-cell">操作</th>
                    </tr>
                </thead>
                <tbody class="watch-list-table-body">
                    <tr v-for="watchItem in paginatedWatchLists" 
                        :key="watchItem.id" 
                        class="watch-list-data-row">
                        <WatchListCard :watchItem="watchItem" />
                    </tr>
                </tbody>
            </table>
            <div v-if="paginatedWatchLists.length === 0" class="watch-list-empty-state">
                <p class="watch-list-empty-text">目前沒有觀察名單項目</p>
            </div>
            <Pagination 
                :current-page="currentPage" 
                :total-pages="totalPages" 
                @page-change="handlePageChange"
                class="watch-list-pagination" />
        </div>
    </div>
</template>

<style scoped>
/* 主容器 */
.watch-list-container {
    /* 您可以在這裡添加自定義樣式 */
}

/* 主標題 */
.watch-list-main-title {
    /* 您可以在這裡添加自定義樣式 */
}

/* 篩選區域 */
.watch-list-filter-section {
    /* 您可以在這裡添加自定義樣式 */
}

/* 標籤按鈕 */
.watch-list-tab-label {
    /* 您可以在這裡添加自定義樣式 */
    cursor: pointer;
}

.watch-list-tab-active {
    /* 您可以在這裡添加自定義樣式 */
}

.grooming-label {
    /* 您可以在這裡添加自定義樣式 */
}

.boarding-label {
    /* 您可以在這裡添加自定義樣式 */
}

/* 搜尋區域 */
.watch-list-search-wrapper {
    /* 您可以在這裡添加自定義樣式 */
}

.watch-list-search-label {
    /* 您可以在這裡添加自定義樣式 */
}

.watch-list-search-input {
    /* 您可以在這裡添加自定義樣式 */
}

.watch-list-search-button {
    /* 您可以在這裡添加自定義樣式 */
}

/* 表格區域 */
.watch-list-table-wrapper {
    /* 您可以在這裡添加自定義樣式 */
}

.watch-list-table {
    /* 您可以在這裡添加自定義樣式 */
    width: 100%;
    border-collapse: collapse;
}

.watch-list-table-header {
    /* 您可以在這裡添加自定義樣式 */
}

.watch-list-header-row {
    /* 您可以在這裡添加自定義樣式 */
}

.watch-list-header-cell {
    /* 您可以在這裡添加自定義樣式 */
    padding: 12px 8px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}

.watch-list-table-body {
    /* 您可以在這裡添加自定義樣式 */
}

.watch-list-data-row {
    /* 您可以在這裡添加自定義樣式 */
}

.watch-list-data-row:hover {
    /* 您可以在這裡添加自定義樣式 */
    background-color: #f3f4f6;
}

/* 空狀態 */
.watch-list-empty-state {
    /* 您可以在這裡添加自定義樣式 */
    text-align: center;
    padding: 40px 20px;
}

.watch-list-empty-text {
    /* 您可以在這裡添加自定義樣式 */
    color: #6b7280;
}

/* 分頁 */
.watch-list-pagination {
    /* 您可以在這裡添加自定義樣式 */
    margin-top: 20px;
}
</style>