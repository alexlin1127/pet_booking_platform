<script setup>

import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { bookings } from '../../../data/bookingfakedata'
import Table from '../../../components/UI/Table.vue'
import Pagination from '../../../components/common/Pagination.vue'
import HistoryCard from './Card/HistoryCard.vue'

const pageSize = 5
const route = useRoute()
const router = useRouter()
const isGrooming = ref(route.path === '/stores/grooming-bookings/history')
const currentPage = ref(1) // 分頁  
const searchText = ref('')

// 監聽路由變化，自動切換滑軌
watch(() => route.path, (newPath) => {
    isGrooming.value = newPath === '/stores/grooming-bookings/history'
    currentPage.value = 1 // 重置分頁
})

// 監聽滑軌變化，自動切換路由
watch(isGrooming, (newValue) => {
    const targetPath = newValue ? '/stores/grooming-bookings/history' : '/stores/boarding-bookings/history'
    if (route.path !== targetPath) {
        router.push(targetPath)
    }
})


// 先依服務類型再依姓名篩選
const filteredHistory = computed(() => {
    let arr = bookings.filter(item => item.status === '已完成')
        .filter(item => isGrooming.value ? item.service_type === '美容' : item.service_type === '住宿');
    if (searchText.value.trim()) {
        arr = arr.filter(item => item.customer_name.includes(searchText.value.trim()))
    }
    return arr;
})

// 分頁
const totalPages = computed(() => Math.ceil(filteredHistory.value.length / pageSize))
const paginatedBookingshistory = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    return filteredHistory.value.slice(start, start + pageSize)
})


const handlePageChange = (page) => { currentPage.value = page }

function handleSearch() {
    currentPage.value = 1
}
</script>

<template>

    <div class="history-container">
        <h1 class="history-title">歷史預約紀錄</h1>

        <div class="postmanage-filter-toggle">
            <!-- 篩選切換（滑軌樣式） -->
            <label class="postmanage-filter-label" :class="{ 'grooming-active': isGrooming }" @click="isGrooming = true" style="cursor:pointer;">美容</label>
            <label class="postmanage-switch">
                <input type="checkbox" class="sr-only peer" v-model="isGrooming" aria-label="切換美容/住宿" />
                <div class="postmanage-switch-bar"></div>
                <div class="postmanage-switch-slider" :class="{ right: !isGrooming }"></div>
            </label>
            <label class="postmanage-filter-label" :class="{ 'boarding-active': !isGrooming }" @click="isGrooming = false" style="cursor:pointer;">住宿</label>
            <!-- 搜尋顧客姓名 -->
            <label class="grooming-filter-label">
                <span>搜尋顧客姓名：</span>
                <input type="text" v-model="searchText" @keyup.enter="handleSearch" placeholder="請輸入姓名"
                    class="grooming-search-input" />
            </label>
            <button class="grooming-search-btn" @click="handleSearch">搜尋</button>
        </div>

        <div class="history-table-container">
            <Table>
                <template #header>
                    <th>編號</th>
                    <th>客戶姓名</th>
                    <th>聯絡電話</th>
                    <th>毛孩姓名</th>
                    <th>毛孩種類</th>
                    <th>預約日期</th>
                    <th>服務項目</th>
                    <th>訂單狀態</th>
                    <th>操作</th>
                </template>
                <template #body>
                    <tr v-for="history in paginatedBookingshistory" :key="history.id">
                        <HistoryCard :history="history" />
                    </tr>
                </template>
            </Table>
            <Pagination :current-page="currentPage" :total-pages="totalPages" @page-change="handlePageChange" />
        </div>
    </div>


</template>

<style scoped></style>