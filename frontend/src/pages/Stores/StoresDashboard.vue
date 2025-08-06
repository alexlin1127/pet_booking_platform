<script setup>
import Card from '../../components/UI/Card.vue';
import { ref, computed } from 'vue';

// 時間週期選擇
const selectedPeriod = ref('week');

// 模擬數據
const stats = ref({
  week: {
    revenue: 28650,
    avgOrderValue: 1850,
    customers: 89,
    services: 156,
    occupancyRate: 78
  },
  month: {
    revenue: 125400,
    avgOrderValue: 1920,
    customers: 342,
    services: 658,
    occupancyRate: 82
  }
});

// 待審核數據
const pendingData = ref({
  grooming: 12,
  boarding: 8,
  posts: 5
});

// 熱門服務排行
const popularServices = ref([
  '洗澡清潔服務',
  '剪毛造型服務',
  '指甲修剪服務',
  '毛髮護理服務',
  '寵物 SPA 服務'
]);

// 房間使用狀況
const roomStatus = ref([
  { id: 'A', customer: '張小玲', pet: '白白', time: '14:00 - 16:00', occupied: true },
  { id: 'B', customer: '李大明', pet: '黑黑', time: '15:30 - 18:00', occupied: true },
  { id: 'C', customer: null, pet: null, time: null, occupied: false },
  { id: 'D', customer: '王小美', pet: '花花', time: '09:00 - 12:00', occupied: true },
  { id: 'E', customer: null, pet: null, time: null, occupied: false },
  { id: 'F', customer: '陳大華', pet: '咪咪', time: '16:00 - 19:00', occupied: true }
]);

// 計算屬性
const currentStats = computed(() => stats.value[selectedPeriod.value]);
const periodText = computed(() => selectedPeriod.value === 'week' ? '本週' : '本月');

// 方法
const handlePendingClick = (type) => {
  // 導航到對應的審核頁面
  console.log(`前往${type}審核頁面`);
};
</script>
<template>
  <div class="stores-dashboard">
    <div class="dashboard-header">
      <div class="period-selector">
        <button :class="['period-btn', { active: selectedPeriod === 'week' }]" @click="selectedPeriod = 'week'">
          過去一週
        </button>
        <button :class="['period-btn', { active: selectedPeriod === 'month' }]" @click="selectedPeriod = 'month'">
          過去一月
        </button>
      </div>
    </div>

    <!-- 營收統計區域 -->
    <div class="stats-section">
      <Card type="vertical" :clickable="false" class="revenue-card">
        <template #title><span class="card-title">營業收入</span></template>
        <template #content><span class="card-content">NT$ {{ currentStats.revenue.toLocaleString() }}</span></template>
        <template #anno><span class="card-anno">{{ periodText }}收入</span></template>
        <template #title2><span class="card-title2">平均客單價</span></template>
        <template #content2><span class="card-content2">NT$ {{ currentStats.avgOrderValue.toLocaleString()
            }}</span></template>
      </Card>

      <Card type="vertical" :clickable="false" class="customer-card">
        <template #title><span class="card-title">服務客戶</span></template>
        <template #content><span class="card-content">{{ currentStats.customers }} 位</span></template>
        <template #anno><span class="card-anno">{{ periodText }}客戶數</span></template>
        <template #title2><span class="card-title2">服務次數</span></template>
        <template #content2><span class="card-content2">{{ currentStats.services }} 次</span></template>
      </Card>

      <Card type="vertical" :clickable="false" class="metrics-card">
        <template #title>經營指標</template>
        <template #content>
          <div class="occupancy-info">
            <span class="label">空間使用率</span>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: currentStats.occupancyRate + '%' }"></div>
            </div>
            <span class="percentage">{{ currentStats.occupancyRate }}%</span>
          </div>
        </template>
      </Card>
    </div>

    <!-- 服務排行與空間狀況 -->
    <div class="service-space-section">
      <Card type="vertical" :clickable="false" class="ranking-card">
        <template #title>熱門排行榜</template>
        <template #content>
          <div class="ranking-list">
            <div v-for="(service, index) in popularServices" :key="index" class="ranking-item">
              <span class="rank">
                <template v-if="index === 0">👑</template>{{ index + 1 }}.
              </span>
              <span class="service-name">{{ service }}</span>
            </div>
          </div>
        </template>
      </Card>

      <Card type="vertical" :clickable="false" class="space-card">
        <template #title>空間使用狀況</template>
        <template #content>
          <div class="rooms-grid">
            <Card v-for="room in roomStatus" :key="room.id" type="vertical" :clickable="false"
              :class="['room-card', { 'occupied': room.occupied, 'vacant': !room.occupied }]">
              <template #title>{{ room.id }}房</template>
              <template #content v-if="room.occupied">
                <div class="room-time mb-2 text-center text-gray-500 text-sm">{{ room.time }}</div>
                <div class="room-info">
                  <div class="room-row">
                    <span class="room-label">顧客：</span>
                    <span class="room-value">{{ room.customer }}</span>
                  </div>
                  <div class="room-row">
                    <span class="room-label">毛孩：</span>
                    <span class="room-value">{{ room.pet }}</span>
                  </div>
                </div>
              </template>
              <template #content v-else>
                <div class="vacant-info">現為空房</div>
              </template>
            </Card>
          </div>
        </template>
      </Card>
    </div>

    <!-- 待審核項目 -->
    <div class="pending-section">
      <Card type="vertical" :clickable="true" :hasButton="true" class="pending-card grooming"
        @click="handlePendingClick('grooming')">
        <template #title>
          <span>待審核預約<br class="hidden md:inline">（美容）</span>
        </template>
        <template #content>{{ pendingData.grooming }} 筆</template>
        <template #button>
          <button class="pending-btn">前往審核</button>
        </template>
      </Card>

      <Card type="vertical" :clickable="true" :hasButton="true" class="pending-card boarding"
        @click="handlePendingClick('boarding')">
        <template #title>
          <span>待審核預約<br class="hidden md:inline">（住宿）</span>
        </template>
        <template #content>{{ pendingData.boarding }} 筆</template>
        <template #button>
          <button class="pending-btn">前往審核</button>
        </template>
      </Card>

      <Card type="vertical" :clickable="true" :hasButton="true" class="pending-card posts"
        @click="handlePendingClick('posts')">
        <template #title>待審核貼文<br class="hidden md:inline">（美容、住宿）</template>
        <template #content>{{ pendingData.posts }} 則</template>
        <template #button>
          <button class="pending-btn">前往審核</button>
        </template>
      </Card>
    </div>
  </div>
</template>
