<script setup>
import { ref, computed } from 'vue'
import Table from "../../components/Table.vue"
import StoreCard from "./Card/StoreCard.vue";
import Pagination from "../../components/Pagination.vue"

const pageSize = 5 // 每頁顯示5個

// 第一個表格的分頁邏輯（審核中的店家）
const currentPage1 = ref(1)

// 第二個表格的分頁邏輯（營運中的店家）
const currentPage2 = ref(1)

// 篩選狀態
const selectedStatus = ref('待審核')

const stores = [
    {
        id: "H0001",
        storeName: "寵物樂園",
        registerDate: "2025-07-01",
        region: "台北市",
        owner: "王小明",
        phone: "0912345678",
        status: "待審核"
    },
    {
        id: "H0002",
        storeName: "毛孩之家之寵物美容沙龍及住宿",
        registerDate: "2025-07-10",
        region: "新北市",
        owner: "李小華",
        phone: "0922333444",
        status: "退回補件"
    },
    {
        id: "H0003",
        storeName: "寵物小棧",
        registerDate: "2025-07-20",
        region: "桃園市",
        owner: "陳大仁",
        phone: "0933222111",
        status: "已拒絕"
    },
    {
        id: "H0004",
        storeName: "毛寶貝寵物醫院",
        registerDate: "2025-07-25",
        region: "台中市",
        owner: "張美玲",
        phone: "0944555666",
        status: "已通過"
    },
    {
        id: "H0005",
        storeName: "快樂寵物旅館",
        registerDate: "2025-07-28",
        region: "高雄市",
        owner: "林志明",
        phone: "0955777888",
        status: "待審核"
    },
    {
        id: "H0006",
        storeName: "愛心動物診所",
        registerDate: "2025-08-01",
        region: "台南市",
        owner: "黃美華",
        phone: "0966888999",
        status: "退回補件"
    },
    {
        id: "H0007",
        storeName: "寵物天堂",
        registerDate: "2025-08-03",
        region: "基隆市",
        owner: "劉志強",
        phone: "0977111222",
        status: "已通過"
    },
    {
        id: "H0008",
        storeName: "毛毛小屋",
        registerDate: "2025-08-05",
        region: "新竹市",
        owner: "吳雅婷",
        phone: "0988333444",
        status: "已拒絕"
    },
    {
        id: "H0009",
        storeName: "寵愛一生動物醫院",
        registerDate: "2025-08-07",
        region: "苗栗縣",
        owner: "蔡正忠",
        phone: "0999555666",
        status: "待審核"
    },
    {
        id: "H0010",
        storeName: "快樂狗狗美容坊",
        registerDate: "2025-08-09",
        region: "彰化縣",
        owner: "許淑芬",
        phone: "0911777888",
        status: "退回補件"
    },
    {
        id: "H0011",
        storeName: "寵物大本營",
        registerDate: "2025-08-11",
        region: "雲林縣",
        owner: "陳俊宏",
        phone: "0922999000",
        status: "已通過"
    },
    {
        id: "H0012",
        storeName: "毛孩寵物旅館",
        registerDate: "2025-08-13",
        region: "嘉義市",
        owner: "林美玲",
        phone: "0933111222",
        status: "已拒絕"
    },
    {
        id: "H0013",
        storeName: "愛寵動物醫院",
        registerDate: "2025-08-15",
        region: "屏東縣",
        owner: "楊志明",
        phone: "0944333444",
        status: "待審核"
    },
    {
        id: "H0014",
        storeName: "寵物樂活館",
        registerDate: "2025-08-17",
        region: "宜蘭縣",
        owner: "蘇麗華",
        phone: "0955555666",
        status: "退回補件"
    },
    {
        id: "H0015",
        storeName: "毛寶貝寵物店",
        registerDate: "2025-08-19",
        region: "花蓮縣",
        owner: "鄭大明",
        phone: "0966777888",
        status: "已通過"
    },
    {
        id: "H0016",
        storeName: "寵物好朋友",
        registerDate: "2025-08-21",
        region: "台東縣",
        owner: "賴雅文",
        phone: "0977999000",
        status: "已拒絕"
    },
    {
        id: "H0017",
        storeName: "愛心寵物診所",
        registerDate: "2025-08-23",
        region: "澎湖縣",
        owner: "謝志豪",
        phone: "0988111222",
        status: "待審核"
    },
    {
        id: "H0018",
        storeName: "寵物溫馨家",
        registerDate: "2025-08-25",
        region: "金門縣",
        owner: "何美玲",
        phone: "0999333444",
        status: "退回補件"
    },
    {
        id: "H0019",
        storeName: "毛孩健康中心",
        registerDate: "2025-08-27",
        region: "連江縣",
        owner: "魏俊傑",
        phone: "0911555666",
        status: "已通過"
    },
    {
        id: "H0020",
        storeName: "寵物快樂園",
        registerDate: "2025-08-29",
        region: "桃園市",
        owner: "馬志強",
        phone: "0922777888",
        status: "已拒絕"
    }
];

// 根據狀態篩選店家
const pendingStores = computed(() => {
    return stores.filter(store => store.status === selectedStatus.value)
})

const operatingStores = computed(() => {
    return stores.filter(store => store.status === "已通過")
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

// 第二個表格的分頁邏輯（營運中的店家）
const totalPages2 = computed(() => Math.ceil(operatingStores.value.length / pageSize))
const paginatedOperatingStores = computed(() => {
    const start = (currentPage2.value - 1) * pageSize
    return operatingStores.value.slice(start, start + pageSize)
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
            
            <button 
                class="btn" 
                :class="{ 'btn-active': selectedStatus === '待審核' }"
                @click="filterByStatus('待審核')">
                待審核
            </button>
            <button 
                class="btn" 
                :class="{ 'btn-active': selectedStatus === '退回補件' }"
                @click="filterByStatus('退回補件')">
                退回補件
            </button>
            <button 
                class="btn" 
                :class="{ 'btn-active': selectedStatus === '已拒絕' }"
                @click="filterByStatus('已拒絕')">
                已拒絕
            </button>
        </div>

        <div class="storemanage-table-container">
            <Table>
                <template #header>
                    <th>編號</th>
                    <th>店家</th>
                    <th>註冊日期</th>
                    <th>所在地區</th>
                    <th>負責人</th>
                    <th>聯絡電話</th>
                    <th>審核狀況</th>
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

        <!-- 選擇日期 -->
        <label class="storemanage-filter-label">
            註冊日期：
            <input type="date" v-model="selectedDate" class="storemanage-filter-input" />
        </label>

        <div class="storemanage-table-container">
            <Table>
                <template #header>
                    <th>編號</th>
                    <th>店家</th>
                    <th>註冊日期</th>
                    <th>所在地區</th>
                    <th>負責人</th>
                    <th>聯絡電話</th>
                    <th>店家狀況</th>
                    <th>操作</th>
                </template>
                <template #body>
                    <tr v-for="store in paginatedOperatingStores" :key="store.id" class="card-row">
                        <StoreCard :store="store" />
                    </tr>
                </template>
            </Table>

            <Pagination :current-page="currentPage2" :total-pages="totalPages2" @page-change="handlePageChange2" />
        </div>
    </div>


</template>

<style></style>