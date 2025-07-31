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
const selectedStatus = ref('首次申請')

const stores = [
    {
        id: "H0001",
        storeName: "寵物樂園",
        registerDate: "2025-07-01",
        address: "花蓮縣花蓮市",
        owner: "王小明",
        services: "寵物美容",
        phone: "0912345678",
        applystatus: "首次申請",
        storestatus: "營業中"
    },
    {
        id: "H0002",
        storeName: "毛孩之家之寵物美容沙龍及住宿",
        registerDate: "2025-07-10",
        address: "新北市板橋區",
        owner: "李小華",
        services: "寵物美容、住宿",
        phone: "0922333444",
        applystatus: "退回補件",
        storestatus: "暫停營業"
    },
    {
        id: "H0004",
        storeName: "毛寶貝寵物醫院",
        registerDate: "2025-07-25",
        address: "台中市西屯區",
        owner: "張美玲",
        services: "寵物醫療",
        phone: "0944555666",
        applystatus: "已通過",
        storestatus: "營業中"
    },
    {
        id: "H0005",
        storeName: "快樂寵物旅館",
        registerDate: "2025-07-28",
        address: "高雄市左營區",
        owner: "林志明",
        services: "寵物住宿",
        phone: "0955777888",
        applystatus: "補件申請",
        storestatus: "營業中"
    },
    {
        id: "H0006",
        storeName: "愛心動物診所",
        registerDate: "2025-08-01",
        address: "台南市安平區",
        owner: "黃美華",
        services: "寵物醫療、美容",
        phone: "0966888999",
        applystatus: "退回補件",
        storestatus: "暫停營業"
    },
    {
        id: "H0007",
        storeName: "寵物天堂",
        registerDate: "2025-08-03",
        address: "基隆市仁愛區",
        owner: "劉志強",
        services: "寵物美容、用品販售",
        phone: "0977111222",
        applystatus: "已通過",
        storestatus: "營業中"
    },
    {
        id: "H0009",
        storeName: "寵愛一生動物醫院",
        registerDate: "2025-08-07",
        address: "苗栗縣頭份市",
        owner: "蔡正忠",
        services: "寵物醫療",
        phone: "0999555666",
        applystatus: "首次申請",
        storestatus: "營業中"
    },
    {
        id: "H0010",
        storeName: "快樂狗狗美容坊",
        registerDate: "2025-08-09",
        address: "彰化縣員林市",
        owner: "許淑芬",
        services: "寵物美容",
        phone: "0911777888",
        applystatus: "退回補件",
        storestatus: "暫停營業"
    },
    {
        id: "H0011",
        storeName: "寵物大本營",
        registerDate: "2025-08-11",
        address: "雲林縣斗六市",
        owner: "陳俊宏",
        services: "寵物住宿、美容",
        phone: "0922999000",
        applystatus: "已通過",
        storestatus: "營業中"
    },
    {
        id: "H0013",
        storeName: "愛寵動物醫院",
        registerDate: "2025-08-15",
        address: "屏東縣屏東市",
        owner: "楊志明",
        services: "寵物醫療、住宿",
        phone: "0944333444",
        applystatus: "補件申請",
        storestatus: "營業中"
    },
    {
        id: "H0014",
        storeName: "寵物樂活館",
        registerDate: "2025-08-17",
        address: "宜蘭縣宜蘭市",
        owner: "蘇麗華",
        services: "寵物美容、用品販售",
        phone: "0955555666",
        applystatus: "退回補件",
        storestatus: "暫停營業"
    },
    {
        id: "H0015",
        storeName: "毛寶貝寵物店",
        registerDate: "2025-08-19",
        address: "花蓮縣吉安鄉",
        owner: "鄭大明",
        services: "寵物用品販售",
        phone: "0966777888",
        applystatus: "已通過",
        storestatus: "營業中"
    },
    {
        id: "H0017",
        storeName: "愛心寵物診所",
        registerDate: "2025-08-23",
        address: "澎湖縣馬公市",
        owner: "謝志豪",
        services: "寵物醫療",
        phone: "0988111222",
        applystatus: "首次申請",
        storestatus: "營業中"
    },
    {
        id: "H0018",
        storeName: "寵物溫馨家",
        registerDate: "2025-08-25",
        address: "金門縣金城鎮",
        owner: "何美玲",
        services: "寵物住宿、美容",
        phone: "0999333444",
        applystatus: "退回補件",
        storestatus: "暫停營業"
    },
    {
        id: "H0019",
        storeName: "毛孩健康中心",
        registerDate: "2025-08-27",
        address: "連江縣南竿鄉",
        owner: "魏俊傑",
        services: "寵物醫療、保健",
        phone: "0911555666",
        applystatus: "已通過",
        storestatus: "營業中"
    }
];

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

        <!-- 選擇日期 -->
        <label class="storemanage-filter-label">
            註冊日期：
            <input type="date" v-model="selectedDate" class="accmanage-filter-input" />
            ~
            <input type="date" v-model="selectedDate" class="accmanage-filter-input" />
        </label>

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