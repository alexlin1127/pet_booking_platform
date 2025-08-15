<!-- src/pages/Order.vue -->
<script setup>
import { ref, computed } from 'vue'
import Card from '@/components/UI/Card.vue'
import Switch from '@/components/UI/Switch.vue'

/** 兩隻寵物（狗、貓） */
const pets = ref([
    {
        id: 'p1',
        name: '小白',
        gender: '女',
        breed: '貴賓犬',
        age: 3,
        weight: 4.5,
        neutered: false,
        microchip: true,
        groomingCount: 2,
        lastGroomingDate: '2024-08-15',
        avatarUrl: 'https://picsum.photos/seed/poodle/640/480'
    },
    {
        id: 'p2',
        name: 'AA',
        gender: '女',
        breed: '英國短毛貓',
        age: 2,
        weight: 3.8,
        neutered: true,
        microchip: true,
        groomingCount: 5,
        lastGroomingDate: '2024-07-20',
        avatarUrl: 'https://images.unsplash.com/photo-1511044568932-338cba0ad803?q=80&w=800&auto=format&fit=crop'
    }
])

/** 目前選取的寵物 + 篩選 */
const selectedPetId = ref(pets.value[0].id)
const activePet = computed(() => pets.value.find(p => p.id === selectedPetId.value))

const isGrooming = ref(true)                // Switch 綁定：true=美容, false=住宿
const filterType = computed(() => (isGrooming.value ? 'grooming' : 'boarding'))

/** 歷史資料（依寵物分組） */
const groomingHistoryByPet = ref({
    p1: [
        { id: 1, store: 'a店家', date: '2024-08-15', service: 'SPA', price: 2400, status: '已完成', cover: 'https://images.unsplash.com/photo-1558944351-c0a5456a6cbe?q=80&w=800&auto=format&fit=crop' },
        { id: 2, store: 'b店家', date: '2024-07-20', service: '剪指甲', price: 1800, status: '已完成', cover: 'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=800&auto=format&fit=crop' }
    ],
    p2: [
        { id: 3, store: 'c店家', date: '2024-07-20', service: 'SPA', price: 1600, status: '已完成', cover: 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?q=80&w=800&auto=format&fit=crop' }
    ]
})

const boardingHistoryByPet = ref({
    p1: [
        { id: 11, store: 'a店家', date: '2024-08-15', service: 'SPA', price: 2400, status: '已完成', cover: 'https://images.unsplash.com/photo-1507149833265-60c372daea22?q=80&w=800&auto=format&fit=crop' }
    ],
    p2: [] // 貓沒有住宿紀錄
})

/** 依目前寵物＋篩選取得清單 */
const histories = computed(() => {
    const pid = selectedPetId.value
    return isGrooming.value
        ? (groomingHistoryByPet.value[pid] || [])
        : (boardingHistoryByPet.value[pid] || [])
})

/** 說明文字（會依寵物/篩選/是否有清單變化） */
const descForCurrent = computed(() =>
    isGrooming.value
        ? '查看這隻寵物的美容基本資料與歷史紀錄'
        : '查看這隻寵物在住宿的基本資料與歷史狀況'
)

const historyDesc = computed(() =>
    histories.value.length === 0
        ? '尚無服務紀錄'
        : (isGrooming.value
            ? '查看您過往的美容預約店家與服務狀況'
            : '查看您過往的住宿預約店家與入住狀況')
)

function pickPet(id) { selectedPetId.value = id }
</script>

<template>
    <div class="container-block">
        <!-- 預約紀錄 -->
        <section class="section-block">
            <h2 class="page-title">預約紀錄</h2>
            <p class="section-subtitle text-left">{{ descForCurrent }}</p>

            <!-- 上方寵物卡片 -->
            <div class="grid-pets">
                <div v-for="p in pets" :key="p.id" class="tap-card cursor-pointer" role="button" tabindex="0"
                    :aria-pressed="p.id === selectedPetId" @click="pickPet(p.id)" @keydown.enter.prevent="pickPet(p.id)"
                    @keydown.space.prevent="pickPet(p.id)">
                    <Card type="vertical" :hasButton="false" :clickable="true" class="pet-summary-card"
                        :class="p.id === selectedPetId ? 'pet-summary--active' : ''">
                        <!-- 原本的 #icon / #title / #content 保持不變 -->
                        ...


                        <!-- 左側縮圖 -->
                        <template #icon>
                            <div class="pet-card__avatar">
                                <img :src="p.avatarUrl" alt="avatar" />
                            </div>
                        </template>

                        <!-- 同一行：姓名（性別） + 規格 -->
                        <template #title>
                            <div class="pet-card__titleLine">
                                <h3 class="pet-card__name">{{ p.name }}（{{ p.gender }}）</h3>
                                <div class="pet-card__spec">
                                    <span>{{ p.breed }}</span>
                                    <span>/ {{ p.age }}歲</span>
                                    <span class="spec-weight"> / {{ p.weight }}kg</span>
                                </div>
                            </div>
                        </template>

                        <template #content>
                            <div class="pet-card__bullets">
                                <!-- 第1列，第1欄 -->
                                <span class="bullet">{{ p.neutered ? '已結紮' : '未結紮' }}</span>
                                <!-- 第1列，第2欄 -->
                                <span class="bullet">{{ p.microchip ? '已植晶片' : '未植晶片' }}</span>

                                <!-- 第2列：依篩選切換 -->
                                <template v-if="isGrooming">
                                    <!-- 第2列，第1欄 -->
                                    <span class="bullet">美容次數：{{ p.groomingCount }}次</span>
                                    <!-- 第2列，第2欄 -->
                                    <span class="bullet">上次預約日期：{{ p.lastGroomingDate || '尚未預約' }}</span>
                                </template>
                                <template v-else>
                                    <span class="bullet">住宿次數：{{ (boardingHistoryByPet[p.id] || []).length }}次</span>
                                    <span class="bullet">最近一次：{{ (boardingHistoryByPet[p.id] || [])[0]?.date || '尚未預約'
                                        }}</span>
                                </template>
                            </div>
                        </template>
                    </Card>
                </div>
            </div>

        </section>

        <!-- 歷史預約紀錄 -->
        <section class="section-block">
            <h2 class="page-title">歷史預約紀錄</h2>
            <p class="section-subtitle text-left">{{ historyDesc }}</p>

            <!-- 篩選（靠左、文字在兩側） -->
            <div class="filter-row">
                <span class="filter-label">美容</span>
                <Switch :model-value="!isGrooming" @update:model-value="val => isGrooming = !val" size="md" />
                <span class="filter-label">住宿</span>
            </div>

            <!-- 有紀錄才渲染卡片，沒有就只顯示上面的「尚無服務紀錄」 -->
            <div v-if="histories.length > 0" class="grid-history">
                <Card v-for="item in histories" :key="`${filterType}-${item.id}`" type="horizontal" :hasButton="true"
                    :clickable="true" class="history-card">
                    <!-- ✅ 改這裡：用 #image 才會進到 .card-image -->
                    <template #image>
                        <img :src="item.cover" alt="" />
                    </template>

                    <!-- 第一行：左=頭貼(由 Card 放在左側)+店名+服務；右=狀態 -->
                    <template #title>
                        <div class="history-card__titleRow">
                            <div class="history-card__leftGroup">
                                <span class="store-name">{{ item.store }}</span>
                                <span v-if="item.service" class="service-chip">{{ item.service }}</span>
                            </div>
                            <span class="status-chip">{{ item.status }}</span>
                        </div>
                    </template>

                    <!-- 第二行：左=服務時間；右=金額 -->
                    <template #content>
                        <div class="history-card__contentRow">
                            <span class="history-card__time">服務時間：{{ item.date }}</span>
                            <span class="history-card__price">NT$ {{ item.price.toLocaleString() }}</span>
                        </div>
                    </template>
                </Card>
            </div>
        </section>
    </div>
</template>
