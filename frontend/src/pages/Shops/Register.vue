<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import FormTemplate from '../../components/FormTemplate.vue'

const route = useRoute()
const router = useRouter()
const currentStep = computed(() => route.params.step)

const agreePrivacy = ref(false)
const isDisabled = computed(() => {
  // 第二步才需要勾選隱私政策
  return currentStep.value == '2' && !agreePrivacy.value
})

const nextStep = () => {
  const next = parseInt(currentStep.value) + 1
  router.push(`/Register/Shops/${next}`)
}

const submitForm = () => {
  // 送出審核邏輯
  console.log('送出審核')
}

// 動態計算標題和按鈕文字
const formTitle = computed(() => {
  return currentStep.value == '1' ? '店家註冊申請' : '填寫店家基本資料'
})

const buttonText = computed(() => {
  return currentStep.value == '1' ? '下一步' : '送出審核'
})

const handleSubmit = () => {
  if (currentStep.value == '1') {
    nextStep()
  }
  else {
    submitForm()
  }
}
</script>

<template>
  <div class="shops-page min-h-screen bg-gray-50 py-8">
    <FormTemplate :title="formTitle" @submit="handleSubmit">
      <!-- 第一步表單內容 -->
      <div v-if="currentStep == '1'">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">商家名稱</label>
          <input type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">聯絡電話</label>
          <input type="tel"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
      </div>

      <!-- 第二步表單內容 -->
      <div v-else-if="currentStep == '2'">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">商家地址</label>
          <textarea
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="3"></textarea>
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">營業時間</label>
          <input type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
        <div class="mb-4 text-center">
          <label>
            <input type="checkbox" class="cursor-pointer" v-model="agreePrivacy" />
            我同意隱私政策
          </label>
        </div>
      </div>
      <template #actions>
        <button type="submit" class="form-regist-btn" :disabled="isDisabled">
          {{ buttonText }}
        </button>
      </template>
    </FormTemplate>
  </div>
</template>