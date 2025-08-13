<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const form = ref({
  name: '',
  city: '',
  district: '',
  detailAddress: '',
  phone: '',
  hours: '',
  services: '',
  traffic: '',
  description: '',
  fb: '',
  line: '',
  google:''
})
const pickup = ref(true) //接送服務
const grooming = ref(true) //美容服務
const boarding = ref(false) //住宿服務
const boardingTypes = ref([]) // 住宿類型
const imageNote = ref('') // 圖片說明

const submitForm = () => {
  console.log({
    pickup: pickup.value,
    grooming: grooming.value,
    boarding: boarding.value,
    boardingTypes: boardingTypes.value,
    imageNote: imageNote.value
  })
}
//圖片管理區
const fileInput = ref(null) //綁定 HTML <input type="file"> 的 DOM可以用 fileInput.value.click() 來程式化開啟檔案選擇視窗
// 先放幾張示意圖；實務上可從後端讀取
const images = ref([
  'https://images.unsplash.com/photo-1518791841217-8f162f1e1131?q=80&w=600',
  'https://images.unsplash.com/photo-1543466835-00a7907e9de1?q=80&w=400',
  'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=400'
])
const handleFiles = (e) => {
  const files = Array.from(e.target.files || []) //e.target.files檔案選擇視窗中選的檔案列表（FileList）
  if (!files.length) return
  const remain = 9 - images.value.length //圖片上限是 9 張，計算能放幾張
  const toAdd = files.slice(0, remain) //選了很多張，只取可用的數量

  // 轉成本地 URL 預覽；實務上改成上傳後拿回 URL
  toAdd.forEach(f => {
    const url = URL.createObjectURL(f)
    images.value.push(url) //即時渲染
  })
  e.target.value = '' // 允許重選同一批
}
// 刪除圖片
const remove = (index) => {
  images.value.splice(index, 1)
}

//營業時間
/* 時間下拉：每 30 分一格（可改） */
// length: 48 → 代表一天要切成 48 格（因為 24 小時 × 每小時 2 格 = 48）
// i / 2 → 因為每小時有兩格（:00 和 :30），除以 2 就能得到小時數
// Math.floor() → 去掉小數
// String(...).padStart(2, '0') → 小時補 0，讓 9 變成 09
const timeOptions = Array.from({ length: 48 }, (_, i) => {
  const h = String(Math.floor(i / 2)).padStart(2, '0')
  const m = i % 2 ? '30' : '00'
  return `${h} : ${m}`
})

const openTime = ref('09 : 00')
const closeTime = ref('17 : 00')

/* 公休 */
const weekdays = [
  { value: 1, label: '星期一' },
  { value: 2, label: '星期二' },
  { value: 3, label: '星期三' },
  { value: 4, label: '星期四' },
  { value: 5, label: '星期五' },
  { value: 6, label: '星期六' },
  { value: 7, label: '星期日' }
]
const offDays = ref([]) // 例： [1,3,7]

/* 服務項目（標籤）固定清單，用來顯示建議按鈕 */
const serviceOptions = [
  '寵物美容', '美容剪毛', 'SPA護理', '寵物洗澡', '貓咪專區', '造型美容'
]
// 已選中的服務項目（初始值先選 3 個）
const selectedServices = ref(['寵物美容', '美容剪毛', 'SPA護理'])
// 輸入框的文字（用於自訂新增服務項目）
const tagInput = ref('')

const addService = (name) => {
  if (!name) return //名稱是空的，就直接跳出（不新增）
  if (selectedServices.value.length >= 20) return //  如果已達 20 個上限，就不新增
  if (!selectedServices.value.includes(name)) {  // 如果目前還沒有這個項目
    selectedServices.value.push(name)  // 加到已選清單中
  }
}

const addFromInput = () => {
  const val = tagInput.value.trim() // 去掉輸入前後的空白
  if (!val) return // 如果輸入是空的，就不新增
  addService(val) // 新增到已選清單selectedServices
  tagInput.value = ''  // 新增後清空輸入框
}
// 移除指定索引的服務項目
const removeService = (idx) => selectedServices.value.splice(idx, 1)
</script>
<template>
  <div class="w-full px-4 md:px-8 lg:px-16 py-6 max-w-screen-xl mx-auto">
 <!-- ✅ 標題在外面 -->
    <h1 class="page-title">修改本店資訊</h1>
   <!-- ✅ 表單卡片（框線在這裡） -->
    <section class="form-card">
      <form @submit.prevent="submitForm" class="space-y-6">
    <!-- 店家照片 -->
      <section class="photos-section">
        <div class="photos-header">
          <label class="photos-title block font-semibold mb-1">店家照片</label>
          <!-- 上傳按鈕（隱藏 input） -->
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            multiple
            class="hidden"
            @change="handleFiles"
          />
          <button type="button" class="upload-btn"  @click="fileInput.click()">
            新增圖片
          </button>
        </div>

        

        <!-- 圖片格子 -->
        <ul class="photo-grid">
          <!-- 封面（第一張） -->
          <li v-if="images.length" class="photo-card cover-card">
            <img :src="images[0]" alt="封面" class="photo-img" />
            <span class="cover-badge">封面</span>
            <span class="cover-tip">此張將作為店家頁面的封面圖</span>
            <button type="button" class="photo-delete" @click="remove(0)">×</button>
          </li>

          <!-- 其餘縮圖 -->
          <li
            v-for="(src, idx) in images.slice(1)"
            :key="src + idx"
            class="photo-card"
          >
            <img :src="src" class="photo-img" />
            <button
              type="button"
              class="photo-delete"
              @click="remove(idx + 1)"
              aria-label="刪除圖片"
            >
              ×
            </button>
          </li>

          <!-- 佔位上傳卡（未達上限時顯示） -->
          <li
            v-if="images.length < 9"
            class="photo-card placeholder-card"
            @click="fileInput.click()"
          >
            <span class="placeholder-plus">＋</span>
            <span class="placeholder-text">新增圖片</span>
          </li>
        </ul>
      </section>
        

        <!-- 店家名稱 -->
        <div>
          <label class="block font-semibold mb-1">店家名稱</label>
          <input type="text" v-model="form.name" placeholder="請輸入店家名稱" class="form-input w-full" />
        </div>

        <!-- 地址 -->
        <div>
          <label class="block font-semibold mb-1">地址</label>
          <div class="flex gap-2">
            <select v-model="form.city" class="form-select w-1/4">
              <option disabled selected>市</option>
            </select>
            <select v-model="form.district" class="form-select w-1/4">
              <option disabled selected>區</option>
            </select>
            <input type="text" v-model="form.detailAddress" class="form-input flex-1" placeholder="請輸入詳細地址" />
          </div>
        </div>

        <!-- 電話 -->
        <div>
          <label class="block font-semibold mb-1">電話</label>
          <input type="text" v-model="form.phone" placeholder="請輸入店家電話" class="form-input w-full" />
        </div>

    <!-- 營業時間 -->
      <section class="space-y-4">
        <div class="form-row">
          <label class="field-label">營業時間</label>
          <div class="time-row">
            <span class="time-label">開始營業時間：</span>
            <select v-model="openTime" class="time-select">
              <option v-for="t in timeOptions" :key="'open-'+t" :value="t">{{ t }}</option>
            </select>

            <span class="mx-2">~</span>

            <span class="time-label">結束營業時間：</span>
            <select v-model="closeTime" class="time-select">
              <option v-for="t in timeOptions" :key="'close-'+t" :value="t">{{ t }}</option>
            </select>
          </div>
        </div>

        <!-- 公休時間 -->
        <div class="form-row">
          <label class="field-label">公休時間</label>
          <div class="days-row">
            <label v-for="d in weekdays" :key="d.value" class="day-item">
              <input
                type="checkbox"
                class="day-checkbox"
                :value="d.value"
                v-model="offDays"
              />
              <span>{{ d.label }}</span>
            </label>
          </div>
        </div>

        <!-- 服務項目 -->
        <div class="form-row">
          <label class="field-label">服務項目</label>

          <!-- 已選標籤 + 輸入框 -->
          <div class="service-wrap">
            <div class="service-input">
              <!-- 已選標籤 -->
              <span
                v-for="(tag, i) in selectedServices"
                :key="tag + i"
                class="tag-chip"
              >
                {{ tag }}
                <button type="button" class="tag-x" @click="removeService(i)">×</button>
              </span>

              <!-- 文字輸入（Enter 新增） -->
              <input
                v-model.trim="tagInput"
                class="tag-text"
                type="text"
                placeholder="輸入服務並按 Enter"
                @keydown.enter.prevent="addFromInput"
              />
            </div>
          </div>

          <!-- 建議清單（點一下加入） -->
          <div class="service-suggest">
            <button
              v-for="s in serviceOptions"
              :key="s"
              type="button"
              class="suggest-chip"
              @click="addService(s)"
              :disabled="selectedServices.includes(s)"
            >
              {{ s }}
            </button>
          </div>
        </div>
  </section>
    
  

    <!-- 交通 -->
    <div>
      <label class="block font-semibold mb-1">交通</label>
      <input type="text" v-model="form.traffic" placeholder="例：捷運站步行5分鐘，附近有收費停車場" class="form-input w-full" />
    </div>

    <!-- 接送、美容、住宿服務（你已完成） -->
     <!-- 基本服務開關 -->
    
      <!-- 接送服務 -->
      <fieldset class="space-y-2">
        <legend class="font-semibold">接送服務</legend>
        <label class="inline-flex items-center mr-4">
          <input type="radio" v-model="pickup" :value="true" class="form-radio" />
          <span class="ml-2">是</span>
        </label>
        <label class="inline-flex items-center">
          <input type="radio" v-model="pickup" :value="false" class="form-radio" />
          <span class="ml-2">否</span>
        </label>
      </fieldset>

      <!-- 美容服務 -->
      <fieldset class="space-y-2">
        <legend class="font-semibold">美容服務</legend>
        <label class="inline-flex items-center mr-4">
          <input type="radio" v-model="grooming" :value="true" class="form-radio" />
          <span class="ml-2">是</span>
        </label>
        <label class="inline-flex items-center">
          <input type="radio" v-model="grooming" :value="false" class="form-radio" />
          <span class="ml-2">否</span>
        </label>
      </fieldset>

      <!-- 住宿服務 -->
      <fieldset class="space-y-2">
        <legend class="font-semibold">住宿服務</legend>
        <label class="inline-flex items-center mr-4">
          <input type="radio" v-model="boarding" :value="true" class="form-radio" />
          <span class="ml-2">是</span>
        </label>
        <label class="inline-flex items-center">
          <input type="radio" v-model="boarding" :value="false" class="form-radio" />
          <span class="ml-2">否</span>
        </label>
      </fieldset>

     <!-- 住宿類型 -->
    <div v-if="boarding" class="boarding-type-block">
      <label class="boarding-type-label">寵物住宿類型</label>
      <div class="boarding-type-checkboxes">
        <label class="boarding-type-option">
          <input type="checkbox" v-model="boardingTypes" value="狗狗" />
          <span>狗狗</span>
        </label>
        <label class="boarding-type-option">
          <input type="checkbox" v-model="boardingTypes" value="貓咪" />
          <span>貓咪</span>
        </label>
      </div>
    </div>

    <!-- 狗狗登記證 -->
    <div v-if="boardingTypes.includes('狗狗')" class="license-upload-block">
      <label class="license-label">狗狗特定寵物業登記許可證</label>
      <button type="button" class="upload-btn">上傳狗狗證明</button>
    </div>

    <!-- 貓咪登記證 -->
    <div v-if="boardingTypes.includes('貓咪')" class="license-upload-block">
      <label class="license-label">貓咪特定寵物業登記許可證</label>
      <button type="button" class="upload-btn">上傳貓咪證明</button>
    </div>
    <!-- 店家簡介 -->
    <div>
      <label class="block font-semibold mb-1">店家簡介</label>
      <textarea v-model="form.description" rows="8" placeholder="請輸入店家簡介內容" class="form-textarea w-full"></textarea>
    </div>

    <!-- LINE連結 -->
    <div>
      <label class="block font-semibold mb-1">LINE連結</label>
      <input type="url" v-model.trim="form.line" class="form-input w-full" placeholder="請提供官方LINE網址" />
    </div>
    
    <!-- FB連結 -->
    <div>
      <label class="block font-semibold mb-1">FB連結</label>
      <input type="url" v-model.trim="form.fb" class="form-input w-full" placeholder="請提供官方FB網址" />
    </div>

    <!-- google連結 -->
    <div>
      <label class="block font-semibold mb-1">Google地圖連結</label>
      <input type="url" v-model.trim="form.google" class="form-input w-full" placeholder="請提供官方Google地圖網址" />
    </div>    
    <!-- 按鈕列 -->
    </form>
  </section>
    <div class="flex justify-center pt-6 space-x-8">
      <button class="btn" @click="router.push('/stores/info/manage')">取消並返回</button>
      <button class="btn">確認修改</button>
    </div>
  </div>
</template>