<script setup>
import { ref, computed } from 'vue'
import { bookings } from '../../../../data/bookingfakedata'
import Table from '../../../../components/UI/Table.vue'
import Pagination from '../../../../components/common/Pagination.vue'
import GroomingCard from '../Card/GroomingCard.vue'

const pageSize = 5
const currentPage1 = ref(1) // 待審核分頁
const currentPage2 = ref(1) // 已審核/已完成分頁
const searchText = ref('')
const selectedDateStart = ref('')

// 待審核預約
const pendingGroomingbookings = computed(() =>
    bookings.filter(item => item.status === '待審核' && item.service_type === '美容')
)
// 已審核預約
const reviewedGroomingbookings = computed(() =>
    bookings.filter(item => item.status === '已審核' && item.service_type === '美容')
)

// 搜尋與日期篩選（僅針對已審核）
const filteredReviewed = computed(() => {
    let arr = reviewedGroomingbookings.value
    if (searchText.value.trim()) {
        arr = arr.filter(item => item.customer_name.includes(searchText.value.trim()))
    }
    if (selectedDateStart.value) {
        arr = arr.filter(item => item.booking_date === selectedDateStart.value)
    }
    return arr
})

// 分頁
const totalPages1 = computed(() => Math.ceil(pendingGroomingbookings.value.length / pageSize))
const paginatedPendingGrooming = computed(() => {
    const start = (currentPage1.value - 1) * pageSize
    return pendingGroomingbookings.value.slice(start, start + pageSize)
})

const totalPages2 = computed(() => Math.ceil(filteredReviewed.value.length / pageSize))
const paginatedReviewedGrooming = computed(() => {
    const start = (currentPage2.value - 1) * pageSize
    return filteredReviewed.value.slice(start, start + pageSize)
})

const handlePageChange1 = (page) => { currentPage1.value = page }
const handlePageChange2 = (page) => { currentPage2.value = page }

// 近期預約筆數（已審核）
const unreviewCount = computed(() => pendingGroomingbookings.value.length)
const reviewedCount = computed(() => reviewedGroomingbookings.value.length)

function handleSearch() {
    currentPage2.value = 1
}
</script>

<template>

    <div class="grooming-container">
        <div class="grooming-title">
            <h1>待審核預約</h1>
            <p>{{ unreviewCount }} 筆</p>
        </div>

        <div class="grooming-table-container">
            <p><FontAwesomeIcon icon="fa-solid fa-bookmark" /> 此圖表示有備註</p>
            <Table>
                <template #header>
                    <th></th>
                    <th>編號</th>
                    <th>客戶姓名</th>
                    <th>聯絡電話</th>
                    <th>毛孩姓名</th>
                    <th>毛孩種類</th>
                    <th>預約日期</th>
                    <th>預約時間</th>
                    <th>訂單狀況</th>
                    <th>操作</th>
                </template>
                <template #body>
                    <tr v-for="grooming in paginatedPendingGrooming" :key="grooming.id">
                        <GroomingCard :grooming="grooming" />
                    </tr>
                </template>
            </Table>
            <Pagination :current-page="currentPage1" :total-pages="totalPages1" @page-change="handlePageChange1" />
        </div>
    </div>


    <div class="grooming-container">
        <div class="grooming-title">
            <h1>近期預約</h1>
            <p>{{ reviewedCount }} 筆</p>
        </div>
        <div class="grooming-filter-buttons">
            <p><FontAwesomeIcon icon="fa-solid fa-bookmark" /> 此圖表示有備註</p>
            <label class="grooming-filter-label">
                <span>可搜尋顧客姓名：</span>
                <input type="text" v-model="searchText" @keyup.enter="handleSearch" placeholder="請輸入姓名"
                    class="grooming-search-input" />
            </label>
            <label class="grooming-filter-label">
                <span>預約日期：</span>
                <input type="date" v-model="selectedDateStart" class="grooming-filter-input" />
            </label>
            <button class="grooming-search-btn" @click="handleSearch">搜尋</button>
        </div>
        <div class="grooming-table-container">
            <Table>
                <template #header>
                    <th></th>
                    <th>編號</th>
                    <th>客戶姓名</th>
                    <th>聯絡電話</th>
                    <th>毛孩姓名</th>
                    <th>毛孩種類</th>
                    <th>預約日期</th>
                    <th>預約時間</th>
                    <th>訂單狀況</th>
                    <th>操作</th>
                </template>
                <template #body>
                    <tr v-for="grooming in paginatedReviewedGrooming" :key="grooming.id">
                        <GroomingCard :grooming="grooming" />
                    </tr>
                </template>
            </Table>
            <Pagination :current-page="currentPage2" :total-pages="totalPages2" @page-change="handlePageChange2" />
        </div>
    </div>


</template>

<style></style>