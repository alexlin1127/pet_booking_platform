<script setup>
import { ref } from 'vue'

const pickup = ref(true)
const grooming = ref(true)
const boarding = ref(false)
const boardingTypes = ref([])
const imageNote = ref('')

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
  <section class="max-w-2xl mx-auto p-6 bg-white shadow rounded">
    <h1 class="text-2xl font-bold mb-6">服務開通</h1>

    <!-- 基本服務開關 -->
    <form @submit.prevent="submitForm" class="space-y-6">
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

    <!-- 按鈕區 -->
    <div class="form-actions">
      <button type="button" class="btn-secondary">取消並返回</button>
      <button type="submit" class="btn-primary">送出並儲存</button>
    </div>
  </form>
  </section>
</template>
<style scoped src="@/styles/pages/Stores/openservice.css"></style>

