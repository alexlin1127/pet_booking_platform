<!-- src/pages/Auth/ChangePassword.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import FormTemplate from '@/components/UI/FormTemplate.vue' // 依實際路徑調整

const router = useRouter()

// 表單狀態
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

// UI 狀態
const submitting = ref(false)
const errorMsg = ref('')

// 返回上一頁
function goBack() {
  router.back()
}

// 基本驗證
function validate() {
  errorMsg.value = ''
  if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
    errorMsg.value = '請完整填寫所有欄位'
    return false
  }
  if (newPassword.value.length < 8) {
    errorMsg.value = '新密碼至少需 8 碼'
    return false
  }
  if (newPassword.value !== confirmPassword.value) {
    errorMsg.value = '兩次輸入的新密碼不一致'
    return false
  }
  if (newPassword.value === oldPassword.value) {
    errorMsg.value = '新密碼不可與原始密碼相同'
    return false
  }
  return true
}

// 送出
async function submit() {
  if (!validate()) return
  try {
    submitting.value = true
    // TODO: 換成你的 API
    // await api.changePassword({ oldPassword: oldPassword.value, newPassword: newPassword.value })
    await new Promise(r => setTimeout(r, 600))
    alert('密碼已變更成功')
    router.back()
  } catch (e) {
    errorMsg.value = '變更失敗，請稍後再試'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 md:px-6 py-8">
     <h1 class="cp-title">變更密碼</h1>
    <!-- ✅ 使用 FormTemplate：標題 + default slot(表單) + actions slot(按鈕列) -->
    <FormTemplate>
      <!-- default slot：表單內容 -->
      <template #default>
        <div class="grid grid-cols-1 gap-4">
          <div class="form-group">
            <label>原始密碼</label>
            <input
              class="form-input themed-input"
              type="password"
              v-model="oldPassword"
              placeholder="XXXXXXXX"
              autocomplete="current-password"
            />
          </div>

          <div class="form-group">
            <label>新密碼</label>
            <input
              class="form-input themed-input"
              type="password"
              v-model="newPassword"
              placeholder="XXXXXXXX"
              autocomplete="new-password"
            />
          </div>

          <div class="form-group">
            <label>再次輸入新密碼</label>
            <input
              class="form-input themed-input"
              type="password"
              v-model="confirmPassword"
              placeholder="XXXXXXXX"
              autocomplete="new-password"
            />
          </div>

          <p v-if="errorMsg" class="text-sm text-red-500">{{ errorMsg }}</p>
        </div>
      </template>

      <!-- actions slot：底部按鈕列（與你會員頁一致的寬度/樣式） -->
      <template #actions>
        <div class="w-full max-w-xl mx-auto grid grid-cols-2 gap-4">
          <button type="button" class="btn-ghost-theme" @click="goBack">返回</button>
          <button
            type="button"
            class="btn-primary-theme"
            :disabled="submitting"
            @click="submit"
          >
            確認變更
          </button>
        </div>
      </template>
    </FormTemplate>
  </main>
</template>

<style scoped>
 .cp-title  { @apply text-3xl md:text-4xl font-bold text-center mb-8; }

/* 讓 input 與你站內主題一致（邊框 #5c4636、focus 光暈 #d8c9b8） */
.themed-input {
  @apply w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2;
  border-color: #5c4636;
  --tw-ring-color: #d8c9b8;
}

/* 主題按鈕（與你會員頁相同視覺） */
.btn-primary-theme {
  @apply inline-flex items-center justify-center rounded-md px-5 py-2.5 text-sm font-medium text-white transition-colors;
  background-color: #cda372;          /* 暖棕金 */
}
.btn-primary-theme:hover { background-color: #b98f60; }
.btn-primary-theme:disabled { @apply opacity-60 cursor-not-allowed; }

.btn-ghost-theme {
  @apply inline-flex items-center justify-center rounded-md px-5 py-2.5 text-sm font-medium transition-colors bg-white border;
  border-color: #d8c9b8;
  color: #5c4636;
}
.btn-ghost-theme:hover { @apply bg-amber-50; }
</style>
