<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Table from "../../../components/UI/Table.vue"
import AccountCard from "./AccountCard.vue"
import Pagination from "../../../components/common/Pagination.vue"

const route = useRoute()
const router = useRouter()

const pageSize = 5
const currentPage = ref(parseInt(route.params.page) || 1)

// 篩選條件
const selectedDate = ref('')
const selectedType = ref('')

// 篩選邏輯
const filteredAccounts = computed(() => {
    return accounts.filter(acc => {
        const dateMatch = !selectedDate.value || acc.createdAt === selectedDate.value
        const typeMatch = !selectedType.value || acc.type === selectedType.value
        return dateMatch && typeMatch
    })
})

// 分頁邏輯
const totalPages = computed(() => Math.ceil(filteredAccounts.value.length / pageSize))
const paginatedAccounts = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    return filteredAccounts.value.slice(start, start + pageSize)
})

const handlePageChange = (page) => {
    currentPage.value = page
    router.push(`/admin/accounts/${page}`)
}

// 當篩選條件變更時，重置到第一頁
watch([selectedDate, selectedType], () => {
    currentPage.value = 1
    router.push('/admin/accounts/1')
})

const accounts = [
    {
        id: "A0001",
        type: "管理員",
        name: "王小明",
        account: "admin001",
        store: "--",
        status: "啟用",
        createdAt: "2025-07-01"
    },
    {
        id: "S0002",
        type: "店家",
        name: "李小華",
        account: "shop002",
        store: "毛孩之家",
        status: "停用",
        createdAt: "2025-07-10"
    },
    {
        id: "U0003",
        type: "一般用戶",
        name: "陳大仁",
        account: "user003",
        store: "寵物小棧",
        status: "啟用",
        createdAt: "2025-07-20"
    },
    {
        id: "S0004",
        type: "店家",
        name: "林美麗",
        account: "shop004",
        store: "毛寶貝寵物醫院",
        status: "啟用",
        createdAt: "2025-07-25"
    },
    {
        id: "U0005",
        type: "一般用戶",
        name: "張志明",
        account: "user005",
        store: "快樂寵物旅館",
        status: "停用",
        createdAt: "2025-07-28"
    },
    {
        id: "A0006",
        type: "管理員",
        name: "劉小芳",
        account: "admin006",
        store: "愛心動物醫院",
        status: "啟用",
        createdAt: "2025-07-30"
    },
    {
        id: "S0007",
        type: "店家",
        name: "吳大明",
        account: "shop007",
        store: "寵物美容坊",
        status: "啟用",
        createdAt: "2025-07-31"
    },
    {
        id: "U0008",
        type: "一般用戶",
        name: "黃小玲",
        account: "user008",
        store: "寵物樂園",
        status: "啟用",
        createdAt: "2025-08-01"
    },
    {
        id: "S0009",
        type: "店家",
        name: "蔡志偉",
        account: "shop009",
        store: "毛孩天堂",
        status: "停用",
        createdAt: "2025-08-02"
    },
    {
        id: "U0010",
        type: "一般用戶",
        name: "許美華",
        account: "user010",
        store: "寵物小棧",
        status: "啟用",
        createdAt: "2025-08-03"
    },
    {
        id: "A0011",
        type: "管理員",
        name: "楊志強",
        account: "admin011",
        store: "動物之家",
        status: "啟用",
        createdAt: "2025-08-04"
    }, {
        id: "A0011",
        type: "管理員",
        name: "楊志強",
        account: "admin011",
        store: "動物之家",
        status: "啟用",
        createdAt: "2025-08-04"
    }, {
        id: "A0011",
        type: "管理員",
        name: "楊志強",
        account: "admin011",
        store: "動物之家",
        status: "啟用",
        createdAt: "2025-08-04"
    }, {
        id: "A0011",
        type: "管理員",
        name: "楊志強",
        account: "admin011",
        store: "動物之家",
        status: "啟用",
        createdAt: "2025-08-04"
    }, {
        id: "A0011",
        type: "管理員",
        name: "楊志強",
        account: "admin011",
        store: "動物之家",
        status: "啟用",
        createdAt: "2025-08-04"
    }, {
        id: "A0011",
        type: "管理員",
        name: "楊志強",
        account: "admin011",
        store: "動物之家",
        status: "啟用",
        createdAt: "2025-08-04"
    }, {
        id: "A0011",
        type: "管理員",
        name: "楊志強",
        account: "admin011",
        store: "動物之家",
        status: "啟用",
        createdAt: "2025-08-04"
    }, {
        id: "A0011",
        type: "管理員",
        name: "楊志強",
        account: "admin011",
        store: "動物之家",
        status: "啟用",
        createdAt: "2025-08-04"
    }, {
        id: "A0011",
        type: "管理員",
        name: "楊志強",
        account: "admin011",
        store: "動物之家",
        status: "啟用",
        createdAt: "2025-08-04"
    },
];
</script>



<template>
    
    <div class="accmanage-container">
        <h1 class="accmanage-title">帳號管理</h1>

        <div class="accmanage-filters">
            <!-- 選擇帳號類型 -->
            <label class="accmanage-filter-label">
                帳號類型：
                <select v-model="selectedType" class="accmanage-filter-input">
                    <option value="">全部</option>
                    <option value="管理員">管理員</option>
                    <option value="店家">店家</option>
                    <option value="一般用戶">一般用戶</option>
                </select>
            </label>
            <!-- 選擇日期 -->
            <label class="accmanage-filter-label">
                建立日期：
                <input type="date" v-model="selectedDate" class="accmanage-filter-input" />
                ~
                <input type="date" v-model="selectedDate" class="accmanage-filter-input" />
            </label>
        </div>

        <div class="accmanage-table-container">
            <Table>
                <template #header>
                    <th>編號</th>
                    <th>名字</th>
                    <th>帳號</th>
                    <th>帳號類型</th>
                    <th>帳號狀態</th>
                    <th>建立日期</th>
                    <th>操作</th>
                </template>
                <template #body>
                    <tr v-for="acc in paginatedAccounts" :key="acc.id" class="card-row">
                        <AccountCard :acc="acc" />
                    </tr>
                </template>
            </Table>

            <Pagination :current-page="currentPage" :total-pages="totalPages" @page-change="handlePageChange" />
        </div>
    </div>
</template>

<style scoped src="../../../styles/pages/Admin/Accounts/manage.css"></style>