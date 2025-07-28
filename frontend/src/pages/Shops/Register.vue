<script setup>
import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const router = useRouter()
const currentStep = computed(() => route.params.step)

const nextStep = () => {
  const next = parseInt(currentStep.value) + 1
  router.push(`/Register/Shops/${next}`)
}
</script>

<template>
  <div v-if="currentStep == '1'">
    <!-- 第一步內容 -->
    <p>這是第一個畫面</p>
    <button @click="nextStep">下一步</button>
  </div>
  <div v-else-if="currentStep == '2'">
    <!-- 第二步內容 -->
    <p>這是第二個畫面</p>
  </div>
</template>