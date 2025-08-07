<script setup>
import { ref } from 'vue'

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
  line: ''
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
</script>
<template>
  <section class="max-w-4xl mx-auto p-6 bg-white shadow rounded space-y-6">
    <h1 class="text-2xl font-bold">修改本店資訊</h1>
<form @submit.prevent="submitForm" class="space-y-6">
    <!-- 店家照片 -->
    
      <div class="flex flex-col mb-6">
      <label class="block font-semibold mb-2">店家照片</label>
      <button class="mt-2 px-4 py-1 bg-black text-white text-sm rounded">新增圖片</button>
      </div>
      <div class="grid grid-cols-4 gap-2">
        <div v-for="n in 8" :key="n" class="aspect-[4/3] bg-gray-200"></div>
      </div>
      <!-- <button class="mt-2 px-4 py-1 bg-black text-white text-sm rounded">新增圖片</button> -->
    

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
    <div>
      <label class="block font-semibold mb-1">營業時間</label>
      <input type="text" v-model="form.hours" placeholder="例：週一～週日 10:00~19:00（週日休息）" class="form-input w-full" />
    </div>

    <!-- 服務項目 -->
    <div>
      <label class="block font-semibold mb-1">服務項目</label>
      <input type="text" v-model="form.services" placeholder="例：寵物洗澡、美容剪毛、SPA護理、貓咪專區" class="form-input w-full" />
    </div>

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

    <!-- FB連結 -->
    <div>
      <label class="block font-semibold mb-1">FB連結</label>
      <input type="text" v-model="form.fb" class="form-input w-full" placeholder="請提供官方FB網址" />
    </div>

    <!-- LINE連結 -->
    <div>
      <label class="block font-semibold mb-1">LINE連結</label>
      <input type="text" v-model="form.line" class="form-input w-full" placeholder="請提供官方LINE網址" />
    </div>

    <!-- 按鈕列 -->
    <div class="flex justify-center pt-6 space-x-8">
      <button class="px-6 py-4 bg-black text-white rounded">取消並返回</button>
      <button class="px-6 py-4 bg-black text-white rounded">確認修改</button>
    </div>
    </form>
  </section>
</template>


<style scoped>
.form-input, .form-select, .form-textarea {
  @apply border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400;
}
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .boarding-type-block {
    @apply border p-4 rounded;
  }

  .boarding-type-label {
    @apply block font-medium mb-2;
  }

  .boarding-type-checkboxes {
    @apply flex gap-4;
  }

  .boarding-type-option {
    @apply inline-flex items-center;
  }

  .license-upload-block {
    @apply border p-4 rounded flex items-center gap-2;
  }

  .license-label {
    @apply block font-medium;
  }

  .upload-btn {
    @apply bg-black text-white px-4 py-2 rounded hover:bg-gray-800;
  }

  .form-actions {
    @apply flex flex-col items-center gap-4 mt-6;
  }

  /* .btn-secondary {
    @apply w-full bg-gray-200 text-black py-2 rounded hover:bg-gray-300;
  }

  .btn-primary {
    @apply w-full bg-black text-white py-2 rounded hover:bg-gray-800;
  } */
}

</style>
