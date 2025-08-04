<script setup>

import { ref, computed } from 'vue'
import FormTemplate from '../../components/UI/FormTemplate.vue'

// 表單資料
const account = ref('')
const password = ref('')
const confirmPassword = ref('')
const agreePrivacy = ref(false)

// 帳號驗證：不可有特殊符號、不可中文，可純英文或英文+數字，4字元以上
const isAccountValid = computed(() => {
  // 僅允許英文或英文+數字，長度4以上
  const accountRegex = /^[A-Za-z][A-Za-z0-9]{3,}$/
  // 不可有中文
  const hasChinese = /[\u4e00-\u9fa5]/.test(account.value)
  return accountRegex.test(account.value) && !hasChinese
})

// 密碼驗證：8字元以上，可純英文、純數字或英文+數字，不可有中文或特殊符號
const isPasswordValid = computed(() => {
  // 僅允許英文或數字，至少8字元
  const passwordRegex = /^[A-Za-z\d]{8,}$/
  // 不可有中文
  const hasChinese = /[\u4e00-\u9fa5]/.test(password.value)
  return passwordRegex.test(password.value) && !hasChinese
})

// 確認密碼是否相同
const isConfirmPasswordValid = computed(() => {
  return password.value === confirmPassword.value && password.value !== ''
})

// 按鈕是否可點選
const isDisabled = computed(() => {
  return !agreePrivacy.value || !isAccountValid.value || !isPasswordValid.value || !isConfirmPasswordValid.value
})

const handleSubmit = () => {
  // 這裡可加上後端帳號重複驗證的 API 呼叫
  console.log('註冊成功')
}

</script>

<template>
    <div class="customers-register-page">
        <FormTemplate @submit="handleSubmit">
            <h1 class="text-4xl text-center font-bold">毛主人註冊</h1>
            <div>
                <div class="mb-4">
                    <label class="customers-register-label">姓名 *</label>
                    <input type="text" class="customers-register-input" placeholder="請輸入您的姓名">
                </div>
                <div class="mb-4">
                    <label class="customers-register-label">帳號 *</label>
                    <input type="text" class="customers-register-input" v-model="account" placeholder="請輸入帳號名稱（至少4字元）">
                    <p v-if="account && !isAccountValid" class="customers-register-error">帳號僅能為英文或英文+數字，且不可有特殊符號或中文，至少4字元</p>
                </div>
                <div class="mb-4">
                    <label class="customers-register-label">密碼 *</label>
                    <input type="password" class="customers-register-input" v-model="password" placeholder="請輸入密碼（至少8字元）">
                    <p v-if="password && !isPasswordValid" class="customers-register-error">密碼必須至少8字元，僅限英文或數字，不可有特殊符號或中文</p>
                </div>
                <div class="mb-4">
                    <label class="customers-register-label">確認密碼 *</label>
                    <input type="password" class="customers-register-input" v-model="confirmPassword" placeholder="請重新輸入密碼">
                    <p v-if="confirmPassword && !isConfirmPasswordValid" class="customers-register-error">密碼不一致</p>
                </div>
                <div class="mb-4">
                    <label class="customers-register-label">Email *</label>
                    <input type="text" class="customers-register-input" placeholder="請輸入您的Email　">
                </div>
                <div class="mb-4">
                    <label class="customers-register-label">聯絡電話 </label>
                    <input type="tel" class="customers-register-input" placeholder="（非必填）　請輸入您的電話">
                </div>
            </div>
            <div class="mb-4 text-center">
                <label>
                    <input type="checkbox" class="cursor-pointer" v-model="agreePrivacy" />
                    我同意隱私政策相關規範
                </label>
            </div>
            <template #actions>
                <div class="flex justify-center w-full">
                  <button type="submit" class="form-customers-register-btn md:w-auto w-full" :disabled="isDisabled">
                      同意註冊
                  </button>
                </div>
            </template>
        </FormTemplate>
        <!-- 社群登入卡片 -->
        <div class="flex flex-col gap-4 mt-8 items-center w-full max-w-xs mx-auto">
            <button class="customers-register-social-card customers-register-social-card--line">
                <FontAwesomeIcon icon="fa-brands fa-line" class="w-5 h-5" />
                <span class="flex-1 text-center">Line 註冊</span>
            </button>
            <button class="customers-register-social-card customers-register-social-card--google">
                <FontAwesomeIcon icon="fa-brands fa-google" class="w-5 h-5" />
                <span class="flex-1 text-center">Google 註冊</span>
            </button>
            <button class="customers-register-social-card customers-register-social-card--facebook">
                <FontAwesomeIcon icon="fa-brands fa-facebook-f" class="w-5 h-5" />
                <span class="flex-1 text-center">Facebook 註冊</span>
            </button>
        </div>
    </div>
</template>