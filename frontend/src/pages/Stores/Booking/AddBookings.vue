<script setup>
// 美容用：依寵物類型切換下拉選單內容
const dogBreedOptions = [
    '小型犬（10kg以下）',
    '中型犬（20kg以下）',
    '大型犬（30kg以下）',
    '超過30kg請與店家聯繫'
]
const catBreedOptions = [
    '短毛',
    '長毛'
]
import { ref, computed } from 'vue'

// 頁面模式：'form' | 'success'
const mode = ref('form')

// 表單數據
const form = ref({
    service: 'grooming', // 'grooming' | 'boarding'
    customerName: '',
    phone: '',
    petName: '',
    petType: '',
    breed: '',
    groomingService: '',
    date: new Date(),
    time: '',
    memo: '',
    // 住宿專用
    breedSize: '小型犬',
    startDate: '',
    startTime: '09:30',
    endDate: '',
    endTime: '18:00',
})

// 時間段選擇
const period = ref('am')

// 日曆相關
const calendar = ref({
    year: new Date().getFullYear(),
    month: new Date().getMonth()
})

// 完成頁面摘要
const summary = ref({})

// 方法
const switchService = (service) => {
    form.value.service = service
}

const prevMonth = () => {
    if (calendar.value.month === 0) {
        calendar.value.month = 11
        calendar.value.year--
    } else {
        calendar.value.month--
    }
}

const nextMonth = () => {
    if (calendar.value.month === 11) {
        calendar.value.month = 0
        calendar.value.year++
    } else {
        calendar.value.month++
    }
}

// 生成日曆格子
const calendarCells = computed(() => {
    const cells = []
    const year = calendar.value.year
    const month = calendar.value.month
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    // 當月第一天是星期幾 (0=星期日, 1=星期一...)
    const firstDay = new Date(year, month, 1).getDay()
    // 當月有幾天
    const daysInMonth = new Date(year, month + 1, 0).getDate()

    // 補前面空格（上個月的日期）
    const prevMonth = month === 0 ? 11 : month - 1
    const prevYear = month === 0 ? year - 1 : year
    const daysInPrevMonth = new Date(prevYear, prevMonth + 1, 0).getDate()

    for (let i = firstDay - 1; i >= 0; i--) {
        const d = new Date(prevYear, prevMonth, daysInPrevMonth - i)
        d.setHours(0, 0, 0, 0)
        cells.push({
            date: d,
            muted: true
        })
    }

    // 當月日期
    for (let day = 1; day <= daysInMonth; day++) {
        const d = new Date(year, month, day)
        d.setHours(0, 0, 0, 0)
        cells.push({
            date: d,
            muted: d < today
        })
    }

    return cells
})

const isSameDate = (date1, date2) => {
    return date1.getFullYear() === date2.getFullYear() &&
        date1.getMonth() === date2.getMonth() &&
        date1.getDate() === date2.getDate()
}

const selectDate = (cell) => {
    if (!cell.muted) {
        form.value.date = cell.date
    }
}

// 時間段顯示
const shownSlots = computed(() => {
    const slots = []
    if (period.value === 'am') {
        for (let h = 9; h <= 12; h++) {
            slots.push({
                time: `${h.toString().padStart(2, '0')}:00`,
                label: `${h.toString().padStart(2, '0')}:00`,
                disabled: false
            })
            if (h < 12) {
                slots.push({
                    time: `${h.toString().padStart(2, '0')}:30`,
                    label: `${h.toString().padStart(2, '0')}:30`,
                    disabled: false
                })
            }
        }
    } else {
        for (let h = 13; h <= 17; h++) {
            slots.push({
                time: `${h.toString().padStart(2, '0')}:00`,
                label: `${h.toString().padStart(2, '0')}:00`,
                disabled: false
            })
            if (h < 17) {
                slots.push({
                    time: `${h.toString().padStart(2, '0')}:30`,
                    label: `${h.toString().padStart(2, '0')}:30`,
                    disabled: false
                })
            }
        }
    }
    return slots
})

// 價格計算
const groomingPrice = computed(() => {
    if (form.value.groomingService === '洗澡清潔、手部基礎') return 800
    if (form.value.groomingService === '洗澡清潔 + 剪毛造型') return 1200
    return 0
})

const boardingPrice = computed(() => {
    if (!form.value.startDate || !form.value.endDate) return 0
    const start = new Date(form.value.startDate)
    const end = new Date(form.value.endDate)
    // 需包含入住當天，離店不算
    const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24))
    if (days < 1) return 0
    if (days >= 30) {
        return days * 600
    } else if (days >= 7) {
        return days * 850
    } else if (days >= 3) {
        return days * 1000
    } else {
        return days * 1200
    }
})

const resetForm = () => {
    Object.assign(form.value, {
        service: 'grooming',
        customerName: '',
        phone: '',
        petName: '',
        petType: '',
        breed: '',
        groomingService: '',
        date: new Date(),
        time: '',
        memo: '',
        breedSize: '小型犬',
        startDate: '',
        startTime: '09:30',
        endDate: '',
        endTime: '18:00',
    })
}

const submitForm = () => {
    // 驗證表單
    if (!form.value.customerName || !form.value.phone || !form.value.petName) {
        alert('請填寫完整資料')
        return
    }

    // 設定摘要
    summary.value = {
        type: form.value.service,
        customerName: form.value.customerName,
        petName: form.value.petName,
        ...form.value
    }

    // 切換到完成頁
    mode.value = 'success'
}

// 住宿房型選項依犬種動態顯示
const dogRoomOptions = computed(() => {
    switch (form.value.breedSize) {
        case '小型犬':
            return [
                { value: '精緻房', label: '精緻房（15kg以下中型犬可入住）' },
            ];
        case '中型犬':
            return [
                { value: '精緻房', label: '精緻房（15kg以下中型犬可入住）' },
                { value: '豪華房', label: '豪華房（25kg以下大型犬可入住）' },
            ];
        case '大型犬':
            return [
                { value: '豪華房', label: '豪華房（25kg以下大型犬可入住）' },
                { value: '總統套房', label: '總統套房（大型犬以上皆可入住）' },
            ];
        case '30公斤以上':
            return [
                { value: '總統套房', label: '總統套房（大型犬以上皆可入住）' },
            ];
        default:
            return [];
    }
});

const catRoomCountMap = {
    '典雅房': [1, 2],
    '華貴房': [1, 2, 3],
    '尊榮房': [1, 2, 3, 4, 5],
};
const catCountOptions = computed(() => {
    const room = form.value.roomType;
    return (catRoomCountMap[room] || []).map(n => ({ value: String(n), label: `${n}隻` }));
});
</script>

<template>
    <!-- 表單頁 -->
    <section v-if="mode === 'form'" class="storeappointment-container storeappointment-page">
        <h1 class="storeappointment-title">新增預約</h1>

        <!-- tabs -->
        <div class="storeappointment-tab-wrap">
            <button :class="['storeappointment-tab', form.service === 'grooming' && 'storeappointment-tab-active']"
                @click="switchService('grooming')">
                美容
            </button>
            <button :class="['storeappointment-tab', form.service === 'boarding' && 'storeappointment-tab-active']"
                @click="switchService('boarding')">
                住宿
            </button>
        </div>

        <!-- 卡片內容 -->
        <div class="sa-card">
            <div class="sa-card-inner space-y-6">
                <!-- 共用欄位 -->
                <div class="grid md:grid-cols-2 gap-5">
                    <div>
                        <label class="storeappointment-label">顧客姓名</label>
                        <input class="storeappointment-input" v-model="form.customerName" placeholder="請輸入完整姓名" />
                    </div>
                    <div>
                        <label class="storeappointment-label">顧客電話（手機）</label>
                        <input class="storeappointment-input" v-model="form.phone" placeholder="請輸入電話" />
                    </div>
                    <div>
                        <label class="storeappointment-label">毛孩姓名</label>
                        <input class="storeappointment-input" v-model="form.petName" placeholder="請輸入毛孩姓名" />
                    </div>
                    <div>
                        <label class="storeappointment-label">毛孩類別</label>
                        <div class="flex items-center gap-6 pt-2">
                            <label class="inline-flex items-center gap-2"><input type="radio"
                                    class="storeappointment-radio" value="狗" v-model="form.petType" />寵物狗</label>
                            <label class="inline-flex items-center gap-2"><input type="radio"
                                    class="storeappointment-radio" value="貓" v-model="form.petType" />寵物貓</label>
                        </div>
                    </div>
                </div>

                <!-- 美容專屬 -->
                <template v-if="form.service === 'grooming'">
                    <div class="grid md:grid-cols-2 gap-5">
                        <div v-if="form.petType === '狗'">
                            <label class="storeappointment-label">毛孩種類</label>
                            <select class="storeappointment-select" v-model="form.breed">
                                <option value="">請選擇毛孩種類</option>
                                <option v-for="opt in dogBreedOptions" :key="opt">{{ opt }}</option>
                            </select>
                        </div>
                        <div v-else-if="form.petType === '貓'">
                            <label class="storeappointment-label">毛孩種類</label>
                            <select class="storeappointment-select" v-model="form.breed">
                                <option value="">請選擇毛孩種類</option>
                                <option v-for="opt in catBreedOptions" :key="opt">{{ opt }}</option>
                            </select>
                        </div>
                        <div v-else>
                            <label class="storeappointment-label">毛孩種類</label>
                            <select class="storeappointment-select" disabled>
                                <option>請先選擇寵物類別</option>
                            </select>
                        </div>
                        <div>
                            <label class="storeappointment-label">選擇服務項目</label>
                            <select class="storeappointment-select" v-model="form.groomingService">
                                <option value="">請選擇美容項目</option>
                                <option>洗澡清潔、手部基礎</option>
                                <option>洗澡清潔 + 剪毛造型</option>
                            </select>
                        </div>
                    </div>

                    <!-- 時間選擇 -->
                    <div>
                        <h3 class="block-title text-center">選擇預約時間</h3>
                        <div class="timepicker-details">
                            <div class="timepicker-summary">
                                <span class="font-bold">{{ calendar.year }}年{{ calendar.month + 1 }}月</span>
                                <div class="flex gap-3">
                                    <button class="storeappointment-tab px-3 w-auto" @click="prevMonth">‹</button>
                                    <button class="storeappointment-tab px-3 w-auto" @click="nextMonth">›</button>
                                </div>
                            </div>
                            <div class="timepicker-calendar">
                                <div class="calendar-head">
                                    <div class="calendar-title text-gray-600">一 二 三 四 五 六 日</div>
                                </div>
                                <div class="calendar-grid">
                                    <template v-for="(cell, i) in calendarCells" :key="i">
                                        <div :class="['calendar-cell', cell.muted && 'muted', isSameDate(cell.date, form.date) && 'active']"
                                            @click="selectDate(cell)">
                                            {{ cell.date.getDate() }}
                                        </div>
                                    </template>
                                </div>

                                <div class="time-period-row">
                                    <button :class="['time-period', period === 'am' && 'time-period-active']"
                                        @click="period = 'am'">上午</button>
                                    <button :class="['time-period', period === 'pm' && 'time-period-active']"
                                        @click="period = 'pm'">下午</button>
                                </div>

                                <div class="time-grid">
                                    <button v-for="t in shownSlots" :key="t.time"
                                        :class="['time-slot', t.disabled && 'disabled', form.time === t.time && 'active']"
                                        :disabled="t.disabled" @click="form.time = t.time">
                                        {{ t.label }}
                                    </button>
                                </div>

                                <div class="subtotal">
                                    本次美容預估總金額：<span class="font-semibold">{{ groomingPrice.toLocaleString() }}</span>
                                </div>
                            </div>
                        </div>

                        <div class="mt-5">
                            <label class="storeappointment-label">客服備註</label>
                            <textarea class="storeappointment-textarea" v-model="form.memo"
                                placeholder="請輸入備註"></textarea>
                        </div>
                    </div>
                </template>

                <!-- 住宿專屬 -->
                <template v-else>
                    <div class="grid md:grid-cols-2 gap-5">
                        <div v-if="form.petType === '狗'">
                            <label class="storeappointment-label">毛孩種類</label>
                            <select class="storeappointment-select" v-model="form.breedSize">
                                <option value="小型犬">小型犬（10kg以下）</option>
                                <option value="中型犬">中型犬（20kg以下）</option>
                                <option value="大型犬">大型犬（30kg以下）</option>
                                <option value="30公斤以上">30kg以上</option>
                            </select>
                        </div>
                        <div v-if="form.petType === '狗'">
                            <label class="storeappointment-label">選擇房型</label>
                            <select class="storeappointment-select" v-model="form.roomType">
                                <option v-for="opt in dogRoomOptions" :key="opt.value" :value="opt.value">{{ opt.label
                                    }}</option>
                            </select>
                        </div>
                        <div v-if="form.petType === '貓'">
                            <label class="storeappointment-label">選擇房型</label>
                            <select class="storeappointment-select" v-model="form.roomType">
                                <option value="典雅房">典雅房（可入住1-2隻）</option>
                                <option value="華貴房">華貴房（可入住1-3隻）</option>
                                <option value="尊榮房">尊榮房（可入住1-5隻）</option>
                            </select>
                        </div>
                        <div v-if="form.petType === '貓'">
                            <label class="storeappointment-label">選擇入住數量</label>
                            <select class="storeappointment-select" v-model="form.catCount">
                                <option v-for="opt in catCountOptions" :key="opt.value" :value="opt.value">{{ opt.label
                                    }}</option>
                            </select>
                        </div>

                        <div>
                            <label class="storeappointment-label">到店日期</label>
                            <input type="date" class="storeappointment-input" v-model="form.startDate" />
                        </div>
                        <div>
                            <label class="storeappointment-label">到店時間</label>
                            <select class="storeappointment-select" v-model="form.startTime">
                                <option>09:30</option>
                                <option>10:00</option>
                                <option>10:30</option>
                                <option>11:00</option>
                            </select>
                        </div>

                        <div>
                            <label class="storeappointment-label">離店日期</label>
                            <input type="date" class="storeappointment-input" v-model="form.endDate" />
                        </div>
                        <div>
                            <label class="storeappointment-label">離店時間</label>
                            <select class="storeappointment-select" v-model="form.endTime">
                                <option>18:00</option>
                                <option>17:30</option>
                                <option>17:00</option>
                            </select>
                        </div>
                    </div>

                    <div>
                        <label class="storeappointment-label">優惠方案</label>
                        <div class="sa-card border mt-1">
                            <div class="sa-card-inner text-sm leading-7">
                                • 每晚 NT$ 1,200<br />
                                • 長住三晚以上，每晚 NT$ 1,000<br />
                                • 長住七晚以上，每晚 NT$ 850<br />
                                • 長住一個月以上，每晚 NT$ 600
                            </div>
                        </div>
                    </div>

                    <div>
                        <label class="storeappointment-label">備註</label>
                        <textarea class="storeappointment-textarea" v-model="form.memo" placeholder="無"></textarea>
                    </div>

                    <div class="subtotal">
                        本次住宿預估總金額：<span class="font-semibold">{{ boardingPrice.toLocaleString() }}</span>
                    </div>
                </template>

                <!-- 動作列 -->
                <div class="btn-row">
                    <button class="btn-ghost" @click="resetForm">取消預約</button>
                    <button class="btn-primary" @click="submitForm">送出預約</button>
                </div>
            </div>
        </div>
    </section>

    <!-- 完成頁（美容 & 住宿 通用） -->
    <section v-else class="storeappointment-container">
        <div class="success-wrap">
            <div class="success-icon">✓</div>
            <div class="success-title">完成預約</div>

            <div class="success-card">
                <div class="success-body">
                    <div class="success-row">
                        <div class="success-label">顧客</div>
                        <div class="success-value">
                            {{ summary.customerName || '王小明' }}
                        </div>
                    </div>
                    <template v-if="summary.type === 'grooming'">
                        <div class="success-row">
                            <div class="success-label">預約日期</div>
                            <div class="success-value">
                                {{ summary.date ? new Date(summary.date).toLocaleDateString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit', weekday: 'short' }) : '' }}
                            </div>
                        </div>
                        <div class="success-row">
                            <div class="success-label">預約時間</div>
                            <div class="success-value">
                                {{ summary.time ? summary.time : '' }}
                            </div>
                        </div>
                        <div class="success-row">
                            <div class="success-label">服務項目</div>
                            <div class="success-value">
                                {{ summary.groomingService }}
                            </div>
                        </div>
                    </template>

                    <template v-if="summary.type === 'boarding'">
                        <div class="success-row">
                            <div class="success-label">到店日期</div>
                            <div class="success-value">
                                {{ summary.startDate ? new Date(summary.startDate).toLocaleDateString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit', weekday: 'short' }) : '' }}
                            </div>
                        </div>
                        <div class="success-row">
                            <div class="success-label">到店時間</div>
                            <div class="success-value">
                                {{ summary.startTime }}
                            </div>
                        </div>
                        <div class="success-row">
                            <div class="success-label">離店日期</div>
                            <div class="success-value">
                                {{ summary.endDate ? new Date(summary.endDate).toLocaleDateString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit', weekday: 'short' }) : '' }}
                            </div>
                        </div>
                        <div class="success-row">
                            <div class="success-label">離店時間</div>
                            <div class="success-value">
                                {{ summary.endTime }}
                            </div>
                        </div>
                        <div class="success-row">
                            <div class="success-label">預約天數</div>
                            <div class="success-value">
                                {{ summary.startDate && summary.endDate ? Math.ceil((new Date(summary.endDate) - new Date(summary.startDate)) / (1000*60*60*24)) : '' }}天
                            </div>
                        </div>
                        <div class="success-row">
                            <div class="success-label">預約房型</div>
                            <div class="success-value">
                                {{ summary.roomType }}
                            </div>
                        </div>
                    </template>

                    <div class="back-row">
                        <button class="btn-back" @click="resetForm(); mode = 'form'">返回</button>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped src="../../../styles/pages/Stores/Booking/addbookings.css"></style>