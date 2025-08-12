<script setup>
import { computed } from 'vue'
import { bookings } from '../../../data/bookingfakedata'
import Card from '../../../components/UI/Card.vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const pendingCount = computed(() =>
    bookings.filter(b => b.status === '待審核' && b.service_type === '美容').length
)
const reviewedCount = computed(() =>
    bookings.filter(b => b.status === '已審核' && b.service_type === '美容').length
)

function goToPending() {
    router.push({ name: 'Grooming', hash: '#pending' }).then(() => {
        setTimeout(() => {
            const element = document.getElementById('pending')
            if (element) {
                const elementPosition = element.offsetTop
                const offsetPosition = elementPosition - 100 // 向上偏移 100px
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                })
            }
        }, 100)
    })
}
function goToRecent() {
    router.push({ name: 'Grooming', hash: '#recent' }).then(() => {
        setTimeout(() => {
            const element = document.getElementById('recent')
            if (element) {
                const elementPosition = element.offsetTop
                const offsetPosition = elementPosition - 100 // 向上偏移 100px
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                })
            }
        }, 100)
    })
}
// 1. 產生時間軸（09:00~20:00，每半小時一格，但只顯示整點主線）
const timeSlots = []
for (let h = 9; h <= 20; h++) {
    timeSlots.push({ label: `${h.toString().padStart(2, '0')}:00`, isHalf: false })
    if (h !== 20) timeSlots.push({ label: `${h.toString().padStart(2, '0')}:30`, isHalf: true })
}


// 2. 取得今天日期
const today = new Date().toISOString().slice(0, 10)

// 3. 過濾出今日已審核美容預約
const todayBookings = computed(() =>
    bookings.filter(b => b.service_type === '美容' && b.booking_date === today && b.status === '已審核')
)

// 4. 取得今日所有顧客名稱（不重複）
const customers = computed(() =>
    [...new Set(todayBookings.value.map(b => b.customer_name))]
)

// 5. 將預約資料轉為時程表用格式
function parseTime(str) {
    // 支援 09:00-11:00、10:30-12:00、單一時間
    if (!str) return null
    if (str.includes('-')) {
        const [start, end] = str.split('-')
        return { start, end }
    } else {
        return { start: str, end: null }
    }
}


// 訂單顏色（依customer_name分配，同顧客同色）
const orderColors = [
    '#b8895a', '#b87333', '#c97b63', '#a67c52', '#c9a063', '#b88a5a', '#b87399', '#a6a652', '#c963a0', '#63b8c9'
]
const getBookingColor = (booking) => {
    if (!booking) return '#b8895a'
    // 使用顧客名稱的hash來分配顏色，確保同顧客同色
    const customerHash = booking.customer_name.split('').reduce((hash, char) => hash + char.charCodeAt(0), 0)
    return orderColors[customerHash % orderColors.length]
}

// Modal 狀態
import { ref as vueRef } from 'vue'
const showModal = vueRef(false)
const modalBooking = vueRef(null)
const openModal = (booking) => {
    modalBooking.value = booking
    showModal.value = true
}
const closeModal = () => {
    showModal.value = false
}

// 計算預約方塊的 left/width，精確對齊到時間線條
const getBookingPosition = (booking) => {
    const t = parseTime(booking.booking_time)
    if (!t) return { left: '0%', width: '0%' }

    // 找到開始和結束時間在 timeSlots 中的索引
    const startIndex = timeSlots.findIndex(slot => slot.label === t.start)
    let endIndex = t.end ? timeSlots.findIndex(slot => slot.label === t.end) : startIndex + 3

    if (startIndex === -1) return { left: '0%', width: '0%' }

    // 如果沒有找到結束時間，使用預設長度
    if (endIndex === -1 && t.end) {
        console.warn(`結束時間 ${t.end} 不在時間軸範圍內`)
        endIndex = startIndex + 3 // 預設1.5小時
    }

    // 關鍵修正：預約方塊應該從開始時間線條開始，到結束時間線條結束
    // 每個時間格寬度：100% / timeSlots總數
    const totalSlots = timeSlots.length
    const slotWidth = 100 / totalSlots

    // 開始位置：對齊到開始時間的線條位置（格子中央）
    const startLinePosition = (startIndex + 0.5) * slotWidth

    // 結束位置：對齊到結束時間的線條位置（格子中央）
    const endLinePosition = (endIndex + 0.5) * slotWidth

    // 預約方塊的位置和寬度
    const leftPercent = startLinePosition
    const widthPercent = endLinePosition - startLinePosition

    // 調試日志
    console.log(`${booking.pet_name}: ${t.start}-${t.end}, startIdx:${startIndex}, endIdx:${endIndex}, left:${leftPercent.toFixed(1)}%, width:${widthPercent.toFixed(1)}%`)

    return {
        left: `${Math.max(leftPercent, 0)}%`,
        width: `${Math.max(widthPercent, 2)}%` // 最小寬度2%確保可見
    }
}

</script>

<template>
    <div class="grooming-booking-container pt-6 pr-6 pl-6 bg-gray-50 mb-8">
        <!-- 標題 -->
        <div class="title-header bg-amber-200 text-center py-4 rounded-lg mb-6">
            <h1 class="text-2xl font-bold text-amber-900">今日美容預約</h1>
        </div>
        <!-- 預約時程表 -->
        <div class="booking-schedule bg-white rounded-lg shadow-lg overflow-x-auto">
            <!-- 時間表頭 -->
            <div class="schedule-header grid desktop-grid">
                <div class="time-header p-3 font-semibold text-gray-800 bg-gray-100">顧客</div>
                <template v-for="(slot, idx) in timeSlots" :key="slot.label">
                    <div class="time-slot text-center font-medium text-gray-700 relative flex flex-col items-center justify-end"
                        style="padding: 0; height: 48px; background: none;">
                        <span v-if="!slot.isHalf" style="font-size: 1.1rem; margin-bottom: 2px;">{{ slot.label }}</span>
                        <!-- 只顯示整點主線 -->
                        <div v-if="!slot.isHalf" class="full-hour-line"
                            style="position: absolute; left: 50%; top: 100%; transform: translateX(-50%);"></div>
                    </div>
                </template>
            </div>

            <!-- 顧客預約行 -->
            <div v-for="customer in customers" :key="customer"
                class="customer-row relative border-b border-gray-200 hover:bg-gray-50 desktop-grid">
                <!-- 顧客名稱 -->
                <div class="customer-name p-4 border-r border-gray-300 bg-gray-50 font-medium text-gray-800">
                    {{ customer }}
                </div>

                <!-- 時間軸區域 -->
                <div class="time-axis-area relative h-20"
                    :style="{ display: 'grid', gridTemplateColumns: `repeat(${timeSlots.length}, 1fr)`, gridColumn: '2 / -1' }">
                    <!-- 時間格子與線條 -->
                    <template v-for="(slot, timeIndex) in timeSlots" :key="slot.label">
                        <div class="time-cell relative" style="padding: 0; background: none;">
                            <!-- 只顯示整點主線 -->
                            <div v-if="!slot.isHalf" class="full-hour-line"
                                style="position: absolute; left: 50%; top: 0; height: 100%; transform: translateX(-50%); z-index: 0;">
                            </div>
                        </div>
                    </template>

                    <!-- 訂單方塊層（絕對定位，僅限於時間軸區域內） -->
                    <div class="booking-blocks-layer"
                        style="position: absolute; left: 0; right: 0; top: 0; bottom: 0; z-index: 2; pointer-events: none;">
                        <template v-for="booking in todayBookings.filter(b => b.customer_name === customer)"
                            :key="booking.id">
                            <div class="booking-item absolute flex flex-col items-center justify-center font-medium shadow-sm text-white text-xs cursor-pointer"
                                :style="{
                                    left: getBookingPosition(booking).left,
                                    width: getBookingPosition(booking).width,
                                    top: '6px',
                                    bottom: '6px',
                                    backgroundColor: getBookingColor(booking),
                                    borderRadius: '8px',
                                    padding: '4px 6px',
                                    minHeight: '60px',
                                    pointerEvents: 'auto'
                                }" @click="openModal(booking)">
                                <div class="text-center font-semibold">{{ booking.pet_name }}{{ booking.note ? ', ' +
                                    booking.note : '' }}</div>
                                <div class="text-center text-xs opacity-90 mt-1">{{ booking.booking_time }}</div>
                            </div>
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </div>



    <!-- 待審核項目 -->
    <div class="grooming-stats-container">
        <Card class="grooming-stats-card" type="vertical" :clickable="false" :hasButton="true">
            <template #title>
                <div class="grooming-stats-title-wrapper"><span class="grooming-stats-title">待審核預約</span></div>
            </template>
            <template #content>
                <span class="grooming-stats-count">{{ pendingCount }} 筆</span>
            </template>
            <template #button>
                <button class="grooming-stats-btn" @click="goToPending">查看詳情</button>
            </template>
        </Card>
        <Card class="grooming-stats-card" :clickable="false" :hasButton="true">
            <template #title>
                <div class="grooming-stats-title-wrapper"><span class="grooming-stats-title">近期預約</span></div>
            </template>
            <template #content>
                <span class="grooming-stats-count">{{ reviewedCount }} 筆</span>
            </template>
            <template #button>
                <button class="grooming-stats-btn" @click="goToRecent">查看詳情</button>
            </template>
        </Card>
    </div>

    <!-- ModalBox -->
    <template v-if="showModal">
        <div class="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg shadow-lg p-8 min-w-[300px] max-w-[90vw] relative">
                <button class="absolute top-2 right-2 text-gray-400 hover:text-gray-700 text-xl"
                    @click="closeModal">×</button>
                <h2 class="text-lg font-bold mb-4">預約詳細資訊</h2>
                <div v-if="modalBooking">
                    <div class="mb-2"><b>顧客：</b>{{ modalBooking.customer_name }}</div>
                    <div class="mb-2"><b>寵物：</b>{{ modalBooking.pet_name }}</div>
                    <div class="mb-2"><b>服務時間：</b>{{ modalBooking.booking_time }}</div>
                    <div class="mb-2"><b>備註：</b>{{ modalBooking.note || '無' }}</div>
                    <div class="mb-2"><b>狀態：</b>{{ modalBooking.status }}</div>
                </div>
            </div>
        </div>
    </template>
</template>

<style scoped>
.grooming-stats-container {
    display: flex;
    align-items: stretch;
}

.grooming-stats-card {
    flex: 1 1 340px;
    margin: 0 1.5rem 2.2rem 1.5rem;
    border-radius: 18px;
    background: #fff;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    align-items: stretch;
    padding: 0;
}

.grooming-stats-count {
    display: block;
    font-size: 2.3rem;
    font-weight: bold;
    color: #3d3326;
    text-align: center;
    margin: 2.8rem 0 2.2rem 0;
}

.grooming-stats-title-wrapper {
    width: 100%;
    display: block;
}

.grooming-stats-title {
    display: block;
    width: 100%;
    background: #c7a47b;
    color: #fff;
    font-size: 2.1rem;
    font-weight: bold;
    text-align: center;
    border-radius: 16px 16px 0 0;
    padding: 1.1rem 0 0.7rem 0;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: background 0.2s;
}

.grooming-stats-btn:hover {
    background: #a7895a;
}

@media (min-width: 768px) {
    .grooming-stats-container {
        flex-direction: row;
        gap: 0;
        align-items: stretch;
    }
}

.grooming-booking-container {
    font-family: 'Microsoft JhengHei', sans-serif;
}

/* 響應式 Grid 佈局 */
.desktop-grid {
    display: grid;
    grid-template-columns: 120px repeat(23, 1fr);
    /* 桌機：適中顧客欄 + 23個時間格 */
}

.time-cell {
    min-height: 64px;
    position: relative;
    padding: 0;
    background: none;
}

.time-axis-area {
    min-height: 80px;
    position: relative;
}

.full-hour-line {
    width: 2px;
    height: 100%;
    background: #b8895a;
    opacity: 1;
    border-radius: 2px;
    z-index: 0;
}

.booking-item {
    transition: all 0.2s ease;
    cursor: pointer;
}

.booking-item:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.customer-name {
    writing-mode: horizontal-tb;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* 響應式設計 */
@media (max-width: 1279px) {

    /* 平板及以下：允許水平滑動 */
    .desktop-grid {
        grid-template-columns: 100px repeat(23, minmax(60px, 1fr));
    }

    .booking-schedule {
        overflow-x: auto;
        min-width: 1000px;
        max-width: 100vw;
        box-sizing: border-box;
    }

    .grooming-booking-container {
        max-width: 100vw;
        overflow-x: hidden;
    }

    .booking-item {
        font-size: 10px;
        padding: 2px 4px;
    }
}

@media (max-width: 768px) {

    /* 手機：更緊湊的佈局 */
    .grooming-booking-container {
        padding: 1rem;
    }

    .desktop-grid {
        grid-template-columns: 80px repeat(23, minmax(50px, 1fr));
    }

    .booking-item {
        font-size: 9px;
        padding: 1px 2px;
        min-height: 50px;
    }

    .time-slot {
        font-size: 12px;
        padding: 8px 4px;
    }
}

@media (min-width: 1280px) {

    /* 桌機及以上：無需滑動，適中的顧客欄 */
    .booking-schedule {
        overflow-x: visible;
    }

    .desktop-grid {
        grid-template-columns: 120px repeat(23, 1fr);
    }
}
/* grooming-booking-container 最少預留4格顧客高度，並可自動延展 */
.grooming-booking-container {
    font-family: 'Microsoft JhengHei', sans-serif;
}

/* 讓顧客行自動延展，最少4格 */
.customer-row {
    min-height: 96px;
}

.booking-schedule {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
}
</style>
