<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api/api'
import LineChart from '../../components/UI/LineChart.vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const route = useRoute()
const router = useRouter()


const shopsawaitingreview = ref(3)
const postsawaitingreview = ref(15)
const totalusers = ref(520)
const totalshops = ref(12)

const FurryParentsRegisterWeek = ref(1546)
const FurryParentsRegisterMonth = ref(4567)
const statRange = ref('week') // 'week' 或 'month'

const statLabel = computed(() =>
    statRange.value === 'week' ? '近一週' : '近一月'
)

const FurryParentsRegister = computed(() =>
    statRange.value === 'week' ? FurryParentsRegisterWeek.value : FurryParentsRegisterMonth.value
)

const weekChart = ref([])
const monthChart = ref([])

const getpendingData = async () => {
    try {
        const res = await api.get('/admin/stores/statistics');
        shopsawaitingreview.value = res.data.pending_store_count;
        postsawaitingreview.value = res.data.pending_post_count;
        totalshops.value = res.data.total_store_count;
    } catch (err) {
        alert('無法取得資料');
        return;
    }
}

const getTotalUsers = async () => {
    try {
        const res = await api.get('/users/registered_all');
        totalusers.value = res.data.summary.all.member_count;
        FurryParentsRegisterWeek.value = res.data.summary.last_7_days.store_count;
        FurryParentsRegisterMonth.value = res.data.summary.last_30_days.store_count;
        weekChart.value = res.data.daily_registration_last_7_days.member;
        monthChart.value = res.data.daily_registration_last_30_days.member;
        console.log(weekChart.value, monthChart.value)

    } catch (err) {
        alert('無法取得用戶和店家數量');
        return;
    }
}

const currentChartData = computed(() =>
    statRange.value === 'week' ? weekChart.value : monthChart.value
)

onMounted(() => {
    getpendingData();
    getTotalUsers();
});

</script>

<template>
    <div class="dashboard-container">
        <h1 class="dashboard-title">重要通知</h1>
        
        <!-- 重要通知卡片區域 -->
        <div class="notification-cards">
            <div class="notification-card">
                <div class="card-icon">
                    <FontAwesomeIcon icon="people-group" class="w-8 h-8 text-red-600" />
                </div>
                <div class="card-content">
                    <p class="card-label">待審核店家申請</p>
                    <p class="card-number">{{ shopsawaitingreview }}<span class="card-unit">位</span></p>
                </div>
                <RouterLink to="/admin/stores/manage" class="card-button">
                    審核店家申請
                </RouterLink>
            </div>

            <div class="notification-card">
                <div class="card-icon">
                    <FontAwesomeIcon icon="clipboard-list" class="w-8 h-8 text-red-600" />
                </div>
                <div class="card-content">
                    <p class="card-label">最新貼文待審核</p>
                    <p class="card-number">{{ postsawaitingreview }}<span class="card-unit">篇</span></p>
                </div>
                <RouterLink to="/admin/posts" class="card-button">
                    審核貼文管理
                </RouterLink>
            </div>
        </div>

        <!-- 統計資訊條 -->
        <div class="stats-bar">
            <p class="stats-text">
                目前用戶人數 <span class="stats-number">{{ totalusers }}</span> 人 / 店家 <span class="stats-number">{{ totalshops }}</span> 間
            </p>
        </div>

        <!-- 營運概況 -->
        <div class="operations-section">
            <h2 class="section-title">營運概況</h2>
            
            <div class="chart-container">
                <div class="chart-controls">
                    <button 
                        :class="statRange === 'week' ? 'chart-btn active' : 'chart-btn'" 
                        @click="statRange = 'week'"
                    >
                        近一週
                    </button>
                    <button 
                        :class="statRange === 'month' ? 'chart-btn active' : 'chart-btn'" 
                        @click="statRange = 'month'"
                    >
                        近一月
                    </button>
                </div>
                
                <div class="chart-content">
                    <!-- 左側：數據展示 -->
                    <div class="chart-area">
                        <div class="data-display">
                            <p class="data-title">毛孩爸媽註冊人數</p>
                            <p class="data-number">{{ FurryParentsRegister.toLocaleString() }}</p>
                        </div>
                    </div>
                    
                    <!-- 右側：圖表 -->
                    <div class="chart-area">
                        <LineChart :chartData="currentChartData" :label="statLabel" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped src="../../styles/pages/Admin/admindashboard.css"></style>