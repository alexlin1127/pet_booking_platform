<script setup>
   import { ref } from 'vue'

// ✅ 定義接收的 props
const props = defineProps({
  visible: Boolean,
  infoRows: Array,
  confirmText: { type: String, default: '確認駁回' },       // ✅ 可自訂確認按鈕文字
  cancelText: { type: String, default: '取消駁回' }      // ✅ 可自訂取消按鈕文字
})

// ✅ 定義 emit
const emits = defineEmits(['cancel', 'confirm'])
// ✅ 綁定 textarea 的 v-model
const selectedReason = ref('')
// ✅ emit 點擊取消事件
const onCancel = () => emits('cancel')

// ✅ emit 點擊確認，並回傳選擇的原因
const onConfirm = () => {
  emits('confirm', selectedReason.value)
}
</script>
<template>
   <!-- ✅ 外層 Modal 結構，這是之前漏掉的部分 -->
  <div v-if="visible" class="modal-overlay">
    <div class="modal-content">
      <!-- ✅ 資訊列 -->
      <div v-for="(row, i) in infoRows" :key="i" class="modal-row">
        <div class="modal-label">{{ row[0] }}</div>
        <div class="modal-label">{{ row[1] }}</div>
      </div>

      <!-- ✅ 駁回原因 -->
      <div class="modal-title">駁回原因</div>
      <textarea
        v-model="selectedReason"
        class="w-full h-40 p-4 border border-gray-400 rounded resize-none"
        placeholder="請輸入退件原因"
      ></textarea>

      <!-- ✅ 按鈕列 -->
      <div class="modal-btn-row">
        <button class="modal-btn-cancel" @click="onCancel">{{ cancelText }}</button>
        <button class="modal-btn-confirm" @click="onConfirm">{{ confirmText }}</button>
      </div>
    </div>
  </div>
</template>



<style></style>