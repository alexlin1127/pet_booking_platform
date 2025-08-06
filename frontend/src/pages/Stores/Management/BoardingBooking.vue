<script setup>
import { ref, computed } from 'vue'
import Table from "../../../components/UI/Table.vue"
import Pagination from "../../../components/common/Pagination.vue"

const pageSize = 5 // 每頁顯示5個

// 第一個表格的分頁邏輯（審核中的店家）
const currentPage1 = ref(1)

// 第二個表格的分頁邏輯（營運中的店家）
const currentPage2 = ref(1)

// 篩選狀態
const selectedStatus = ref('首次申請')

// 根據狀態篩選店家
const pendingStores = computed(() => {
    return stores.filter(store => store.applystatus === selectedStatus.value)
})

const operatingStores = computed(() => {
    return stores.filter(store => store.applystatus === "已通過")
})

// 篩選按鈕處理函數
const filterByStatus = (status) => {
    selectedStatus.value = status
    currentPage1.value = 1 // 重置到第一頁
}

// 第一個表格的分頁邏輯（審核中的店家）
const totalPages1 = computed(() => Math.ceil(pendingStores.value.length / pageSize))
const paginatedPendingStores = computed(() => {
    const start = (currentPage1.value - 1) * pageSize
    return pendingStores.value.slice(start, start + pageSize)
})

// 第二個表格的分頁邏輯（營運中的店家，已結合搜尋）
const totalPages2 = computed(() => Math.ceil(filteredStores.value.length / pageSize))
const paginatedFilteredStores = computed(() => {
    const start = (currentPage2.value - 1) * pageSize
    return filteredStores.value.slice(start, start + pageSize)
})

// 搜尋店家（即時搜尋）
const searchText = ref('')
const filteredStores = computed(() => {
    const keyword = searchText.value.trim().toLowerCase()
    if (!keyword) return operatingStores.value
    return operatingStores.value.filter(store =>
        store.storeName.toLowerCase().includes(keyword)
    )
})

// 分頁處理函數
const handlePageChange1 = (page) => {
    currentPage1.value = page
}

const handlePageChange2 = (page) => {
    currentPage2.value = page
}
</script>

<template>
    <div class="storemanage-container">
        <h1 class="storemanage-title">店家帳號審核及管理</h1>

        <div class="filter-buttons">
            <div class="storemanage-list">
                <p>{{ selectedStatus }}店家列表</p>
            </div>

            <button class="btn" :class="{ 'btn-active': selectedStatus === '首次申請' }" @click="filterByStatus('首次申請')">
                首次申請
            </button>
            <button class="btn" :class="{ 'btn-active': selectedStatus === '補件申請' }" @click="filterByStatus('補件申請')">
                補件申請
            </button>
            <button class="btn" :class="{ 'btn-active': selectedStatus === '退回補件' }" @click="filterByStatus('退回補件')">
                退回補件
            </button>
        </div>

        <div class="storemanage-table-container">
            <Table>
                <template #header>
                    <th>店家</th>
                    <th>負責人</th>
                    <th>聯絡電話</th>
                    <th>店址</th>
                    <th>服務項目</th>
                    <th>註冊日期</th>
                    <th>申請狀態</th>
                    <th>操作</th>
                </template>
                <template #body>
                    <tr v-for="store in paginatedPendingStores" :key="store.id" class="card-row">
                        <StoreCard :store="store" />
                    </tr>
                </template>
            </Table>

            <Pagination :current-page="currentPage1" :total-pages="totalPages1" @page-change="handlePageChange1" />
        </div>
    </div>

    <div class="storemanage-container">
        <h1 class="storemanage-title">營運中</h1>
        <div class="flex flex-wrap items-center gap-4 py-2">
            <!-- 搜尋店家 -->
            <label class="flex items-center gap-2 px-2">
                <span class="text-base font-medium">搜尋店家：</span>
                <input type="text" v-model="searchText" @keyup.enter="handleSearch" placeholder="請輸入關鍵字"
                    class="storemanage-search-input" />
            </label>

            <!-- 選擇日期 -->
            <label class="storemanage-filter-label flex items-center gap-2">
                <span>註冊日期：</span>
                <input type="date" v-model="selectedDate" class="accmanage-filter-input" />
                <span>~</span>
                <input type="date" v-model="selectedDate" class="accmanage-filter-input" />
            </label>

            <button class="btn bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
                @click="handleSearch">搜尋</button>
        </div>



        <div class="storemanage-table-container">
            <Table>
                <template #header>
                    <th>店家</th>
                    <th>負責人</th>
                    <th>聯絡電話</th>
                    <th>店址</th>
                    <th>店家狀況</th>
                    <th>註冊日期</th>
                    <th>操作</th>
                </template>
                <template #body>
                    <tr v-for="store in paginatedFilteredStores" :key="store.id" class="card-row">
                        <StoreCard :store="store" />
                    </tr>
                </template>
            </Table>

            <Pagination :current-page="currentPage2" :total-pages="totalPages2" @page-change="handlePageChange2" />
        </div>
    </div>


</template>

<style></style>