<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Card from '../../components/UI/Card.vue'

const route = useRoute()
const router = useRouter()

const shopsawaitingreview = ref(3)
const postsawaitingreview = ref(15)
const totalusers = ref(520)
const totalshops = ref(12)

const FurryParentsRegister = ref(1546)
const statRange = ref('week') // 'week' 或 'month'

const statLabel = computed(() =>
    statRange.value === 'week' ? '近一週' : '近一月'
)
</script>

<template>
    <h1 class="storemanage-title">重要通知</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 my-4 gap-2">
        <Card type="vertical" :hasButton="true">
            <template #icon>
                <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center"></div>
            </template>
            <template #title>
                <p>待審核店家申請</p>
            </template>
            <template #count>
                <p class="countshop">{{ shopsawaitingreview }} 位</p>
            </template>
            <template #button>
                <RouterLink to="/admin/store/manage" class="button">審核店家申請</RouterLink>
            </template>
        </Card>
        <Card type="vertical" :hasButton="true">
            <template #icon>
                <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                    <svg class="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>
            </template>
            <template #title>
                <p>最新貼文待審核</p>
            </template>
            <template #button>
                <RouterLink to="/admin/post" class="button">審核貼文管理</RouterLink>
            </template>
            <template #count>
                <p class="countpost">
                    <span>{{ postsawaitingreview }}</span>位
                </p>
            </template>
        </Card>
    </div>
    <hr />

    <div class="w-full  bg-gray-200 text-3xl text-center py-4 my-3">
        <p>目前總用戶人數 <span class="num text-lime-600">{{ totalusers }}</span> 人 / 店家 <span class="num text-lime-600">{{ totalshops }} </span> 間</p>
    </div>

    <hr />
    <div>
        <h1 class="storemanage-title">營運概況</h1>
        <div class="bg-white rounded-lg shadow-md p-6 mt-4">
            <div class="flex gap-4 mb-6">
                <button :class="statRange === 'week' ? 'bg-lime-300' : 'bg-lime-100'" @click="statRange = 'week'"
                    class="px-4 py-2 text-lime-700 rounded-lg font-semibold hover:bg-lime-200 transition">近一週</button>
                <button :class="statRange === 'month' ? 'bg-lime-300' : 'bg-lime-100'" @click="statRange = 'month'"
                    class="px-4 py-2 text-lime-700 rounded-lg font-semibold hover:bg-lime-200 transition">近一月</button>
            </div>  
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
                <!-- 左半邊：數字區 -->
                <div class="flex flex-col items-center justify-center">
                    <p class="text-lg text-gray-600 mb-2">{{ statLabel }}毛孩爸媽註冊人數</p>
                    <p class="text-4xl font-bold">{{ FurryParentsRegister }}</p>
                    <p class="text-sm text-gray-400 mt-2">統計區間：近一週 / 近一月</p>
                </div>
                <!-- 右半邊：圖表區 -->
                <div class="flex items-center justify-center h-32 bg-gray-50 rounded-lg border border-gray-200">
                    <span class="text-gray-400">（這裡預留折線圖）</span>
                </div>
            </div>
        </div>
    </div>
</template>
<style></style>
