<script setup>
import { computed } from 'vue'
import { bookings } from '../../../../data/bookingfakedata'
import Card from '../../../../components/UI/Card.vue'
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


// 訂單顏色（依customer_name分配，同顧客同色）- 更豐富的顏色搭配
const orderColors = [
    '#dc2626', '#16a34a', '#2563eb', '#ea580c', '#7c3aed', '#db2777', 
    '#059669', '#ca8a04', '#9333ea', '#e11d48', '#0d9488', '#c2410c',
    '#7c2d12', '#166534', '#1e3a8a', '#78350f', '#581c87', '#9f1239'
]
const getBookingColor = (booking) => {
    if (!booking) return '#b8895a'
    // 使用顧客名稱的hash來分配顏色，確保同顧客同色
    const customerHash = booking.customer_name.split('').reduce((hash, char) => hash + char.charCodeAt(0), 0)
    return orderColors[customerHash % orderColors.length]
}

// Modal 狀態
import { ref as vueRef, onMounted, nextTick } from 'vue'
const showModal = vueRef(false)
const modalBooking = vueRef(null)
const bookingScheduleRef = vueRef(null)

const openModal = (booking) => {
    modalBooking.value = booking
    showModal.value = true
}
const closeModal = () => {
    showModal.value = false
}

// 自動滾動到當前時間
const scrollToCurrentTime = () => {
    const now = new Date()
    const currentHour = now.getHours()
    const currentMinute = now.getMinutes()
    
    // 計算當前時間對應的時間軸位置
    let targetTimeSlot = null
    let targetIndex = -1
    
    // 找到最接近當前時間的時間格
    for (let i = 0; i < timeSlots.length; i++) {
        const slot = timeSlots[i]
        const [hour, minute] = slot.label.split(':').map(Number)
        
        if (hour < currentHour || (hour === currentHour && minute <= currentMinute)) {
            targetTimeSlot = slot
            targetIndex = i
        } else {
            break
        }
    }
    
    // 如果找到目標時間，滾動到該位置
    if (targetIndex >= 0 && bookingScheduleRef.value) {
        nextTick(() => {
            const scheduleElement = bookingScheduleRef.value
            const timeSlotWidth = scheduleElement.scrollWidth / timeSlots.length
            const scrollPosition = targetIndex * timeSlotWidth - 100 // 往左偏移一點，讓當前時間不會太靠邊
            
            scheduleElement.scrollTo({
                left: Math.max(0, scrollPosition),
                behavior: 'smooth'
            })
        })
    }
}

onMounted(() => {
    // 組件掛載後自動滾動到當前時間
    setTimeout(() => {
        scrollToCurrentTime()
    }, 100) // 稍微延遲確保DOM完全渲染
})


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
    <div class="grooming-booking-container">
        <!-- 標題 -->
        <div class="title-header">
            <h1>今日美容預約</h1>
        </div>
        <!-- 預約時程表 -->
        <div class="booking-schedule" ref="bookingScheduleRef">
            <!-- 時間表頭 -->
            <div class="schedule-header">
                <div class="time-header">顧客</div>
                <template v-for="(slot, idx) in timeSlots" :key="slot.label">
                    <div class="time-slot">
                        <span v-if="!slot.isHalf">{{ slot.label }}</span>
                        <!-- 只顯示整點主線 -->
                        <div v-if="!slot.isHalf" class="full-hour-line"></div>
                    </div>
                </template>
            </div>

            <!-- 顧客預約行 -->
            <div v-for="customer in customers" :key="customer" class="customer-row">
                <!-- 顧客名稱 -->
                <div class="customer-name">
                    {{ customer }}
                </div>

                <!-- 時間軸區域 -->
                <div class="time-axis-area">
                    <!-- 時間格子與線條 -->
                    <template v-for="(slot, timeIndex) in timeSlots" :key="slot.label">
                        <div class="time-cell">
                            <!-- 只顯示整點主線 -->
                            <div v-if="!slot.isHalf" class="full-hour-line"></div>
                        </div>
                    </template>

                    <!-- 訂單方塊層（絕對定位，僅限於時間軸區域內） -->
                    <div class="booking-blocks-layer">
                        <template v-for="booking in todayBookings.filter(b => b.customer_name === customer)"
                            :key="booking.id">
                            <div class="booking-item"
                                :style="{
                                    left: getBookingPosition(booking).left,
                                    width: getBookingPosition(booking).width,
                                    backgroundColor: getBookingColor(booking)
                                }" @click="openModal(booking)">
                                <div class="booking-item-text">{{ booking.pet_name }}{{ booking.note ? ', ' +
                                    booking.note : '' }}</div>
                                <div class="booking-item-time">{{ booking.booking_time }}</div>
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
                <div class="grooming-stats-title-wrapper">
                    <span class="grooming-stats-title">近期預約</span>
                </div>
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
        <div class="modal-overlay">
            <div class="booking-receipt-modal">
                <button class="modal-close" @click="closeModal">×</button>
                
                <!-- 顧客資訊標題 -->
                <div class="customer-header">
                    <h2 class="customer-title">顧客 {{ modalBooking?.customer_name }}</h2>
                </div>
                
                <div class="receipt-content" v-if="modalBooking">
                    <!-- 上半部：左右分欄 -->
                    <div class="top-section">
                        <!-- 左側資訊 -->
                        <div class="left-section">
                            <div class="info-row">
                                <span class="label">聯絡電話：</span>
                                <span class="value">{{ modalBooking.phone || '0911111111' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">寵物名字：</span>
                                <span class="value">{{ modalBooking.pet_name }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">寵物種類：</span>
                                <span class="value">{{ modalBooking.pet_type || '臘腸犬' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">寵物體型：</span>
                                <span class="value">{{ modalBooking.pet_size || '小型' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">顧客備註：</span>
                                <span class="value">{{ modalBooking.note || '寵物對某些洗劑過敏，請使用低敏感型產品' }}</span>
                            </div>
                        </div>

                        <!-- 右側訂單資訊 -->
                        <div class="right-section">
                            <h3 class="section-title">訂單資訊</h3>
                            <div class="order-info">
                                <div class="info-row">
                                    <span class="label">預約服務：</span>
                                    <span class="value">{{ modalBooking.service_type || '美容' }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">預約日期：</span>
                                    <span class="value">{{ modalBooking.booking_date }} (週五)</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">預約時間：</span>
                                    <span class="value">{{ modalBooking.booking_time }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 下半部：兩個區塊左右分欄 -->
                    <div class="bottom-section">
                        <!-- 左側店家備註 -->
                        <div class="store-notes-section">
                            <h3 class="section-title">店家備註</h3>
                            <textarea 
                                class="store-notes-input" 
                                placeholder="請輸入備註"
                                rows="4"
                            ></textarea>
                        </div>

                        <!-- 右側服務項目明細 -->
                        <div class="service-details-section">
                            <h3 class="section-title">服務項目明細</h3>
                            <div class="service-grid">
                                <div class="service-row">
                                    <span class="service-label">服務項目：</span>
                                    <span class="service-value">洗澡清潔</span>
                                </div>
                                <div class="service-row">
                                    <span class="service-label">說明：</span>
                                    <span class="service-value">包含洗毛、吹乾、清潔耳朵</span>
                                </div>
                                <div class="service-row">
                                    <span class="service-label">訂單金額：</span>
                                    <span class="service-value">NT$800</span>
                                </div>
                                <div class="service-row">
                                    <span class="service-label">預計時間：</span>
                                    <span class="service-value">約45分</span>
                                </div>
                                <div class="service-row">
                                    <span class="service-label">是否接送：</span>
                                    <span class="service-value">是</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 按鈕區域 -->
                    <div class="action-buttons">
                        <button class="btn-secondary" @click="closeModal">返回</button>
                        <button class="btn-primary">儲存</button>
                    </div>
                </div>
            </div>
        </div>
    </template>
</template>

<style scoped src="../../../../styles/pages/Stores/Booking/Grooming/bk.css"></style>

