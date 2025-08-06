<script setup>
import { ref, computed } from 'vue'

// ✅ 定義接收的 props
const props = defineProps({
  visible: Boolean,
  title: String,                    // Modal 標題
  infoRows: Array,                  // 資訊列表 [['標籤', '內容'], ...]
  inputFields: Array,               // 輸入欄位配置
  textareaFields: Array,            // 文字區域配置
  buttons: Array,                   // 按鈕配置
  width: { type: String, default: 'max-w-md' },    // Modal 寬度
  showCloseButton: { type: Boolean, default: true } // 是否顯示關閉按鈕
})

// ✅ 定義 emit
const emits = defineEmits(['close', 'button-click'])

// ✅ 儲存輸入欄位的值
const inputValues = ref({})
const textareaValues = ref({})

// ✅ 檢查是否有取消按鈕
const hasCancelButton = computed(() => {
  return props.buttons?.some(button => 
    button.action === 'cancel' || 
    button.text?.includes('取消') || 
    button.text?.includes('關閉')
  )
})

// ✅ 初始化輸入欄位的值
if (props.inputFields) {
  props.inputFields.forEach(field => {
    inputValues.value[field.key] = field.defaultValue || ''
  })
}

if (props.textareaFields) {
  props.textareaFields.forEach(field => {
    textareaValues.value[field.key] = field.defaultValue || ''
  })
}

// ✅ 關閉 Modal
const closeModal = () => {
  emits('close')
}

// ✅ 處理按鈕點擊
const handleButtonClick = (button) => {
  // 收集所有輸入的資料
  const formData = {
    inputs: inputValues.value,
    textareas: textareaValues.value
  }
  
  emits('button-click', {
    action: button.action,
    data: formData,
    button: button
  })
  
  // 如果按鈕設定為點擊後關閉，則關閉 Modal
  if (button.closeOnClick !== false) {
    closeModal()
  }
}
</script>

<template>
  <!-- ✅ Modal 覆蓋層 -->
  <div v-if="visible" class="modal-overlay" @click.self="closeModal">
    <div :class="['modal-content', width]">
      
      <!-- ✅ Modal 標題與關閉按鈕 -->
      <div class="modal-header" v-if="title || (showCloseButton && !hasCancelButton)">
        <h3 v-if="title" class="modal-title-text">{{ title }}</h3>
        <button v-if="showCloseButton && !hasCancelButton" @click="closeModal" class="modal-close-btn">X</button>
      </div>

      <!-- ✅ 資訊列表 -->
      <div v-if="infoRows && infoRows.length" class="modal-info-section">
        <div v-for="(row, i) in infoRows" :key="i" class="modal-row">
          <div class="modal-label">{{ row[0] }}</div>
          <div class="modal-value">{{ row[1] }}</div>
        </div>
      </div>

      <!-- ✅ 輸入欄位 -->
      <div v-if="inputFields && inputFields.length" class="modal-input-section">
        <div v-for="field in inputFields" :key="field.key" class="modal-field">
          <div class="modal-field-input">
            <label v-if="field.label" class="modal-field-label-input">{{ field.label }}</label>
            <input
              v-model="inputValues[field.key]"
              :type="field.type || 'text'"
              :placeholder="field.placeholder"
              :required="field.required"
              :maxlength="field.maxlength"
              :class="['modal-input', field.class]"
            />
          </div>
          <small v-if="field.hint" class="modal-field-hint">{{ field.hint }}</small>
        </div>
      </div>

      <!-- ✅ 文字區域欄位 -->
      <div v-if="textareaFields && textareaFields.length" class="modal-textarea-section">
        <div v-for="field in textareaFields" :key="field.key" class="modal-field">
          <div class="modal-field-textarea">
            <label v-if="field.label" class="modal-field-label-textarea">{{ field.label }}</label>
            <textarea
              v-model="textareaValues[field.key]"
              :placeholder="field.placeholder"
              :required="field.required"
              :maxlength="field.maxlength"
              :rows="field.rows || 4"
              :class="['modal-textarea', field.class]"
            ></textarea>
          </div>
          <small v-if="field.hint" class="modal-field-hint">{{ field.hint }}</small>
        </div>
      </div>

      <!-- ✅ 按鈕區域 -->
      <div v-if="buttons && buttons.length" class="modal-buttons">
        <button
          v-for="button in buttons"
          :key="button.action"
          @click="handleButtonClick(button)"
          :class="['modal-btn', button.class]"
          :disabled="button.disabled"
        >
          {{ button.text }}
        </button>
      </div>
      
    </div>
  </div>
</template>



<style></style>