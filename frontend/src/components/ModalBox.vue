<script setup>
   import { ref } from 'vue'

// ✅ 定義接收的 props
const props = defineProps({
  visible: Boolean,
  infoRows: Array,
  reasons: Array,
  confirmText: { type: String, default: '確認駁回' },       // ✅ 可自訂確認按鈕文字
  cancelText: { type: String, default: '取消駁回' }      // ✅ 可自訂取消按鈕文字
})

// ✅ 定義 emit
const emits = defineEmits(['cancel', 'confirm'])

// ✅ 定義下拉選單的選擇值
const selectedReason = ref('')

// ✅ emit 點擊取消事件
const onCancel = () => emits('cancel')

// ✅ emit 點擊確認，並回傳選擇的原因
const onConfirm = () => {
  emits('confirm', selectedReason.value)
}
</script>
<template>
     <div v-if="visible" class="modal-overlay">
    <div class="modal-content">
      <!-- 資訊列 顯示 infoRows 每一列資料 -->
      <div v-for="(row, i) in infoRows" :key="i" class="modal-row">
        <div class="modal-label">{{ row[0] }}</div>
        <div class="modal-label">{{ row[1] }}</div>
      </div>

      <!-- 駁回原因 -->
      <div class="modal-title">駁回原因</div>
      <select v-model="selectedReason" class="modal-select">
        <option disabled value="">請選擇原因</option>
        <option v-for="(r, i) in reasons" :key="i" :value="r">{{ r }}</option>
      </select>

      <!-- 按鈕列 -->
      <div class="modal-btn-row">
        
        <button class="modal-btn-confirm" @click="onConfirm">{{ confirmText }}</button>
        <button class="modal-btn-cancel" @click="onCancel">{{ cancelText }}</button>
      </div>
    </div>
  </div>
  
</template>



<style></style>