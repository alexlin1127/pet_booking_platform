<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router';
import FormTemplate from '../components/UI/FormTemplate.vue';

const route = useRoute();
const router = useRouter();

// 狀態判斷：根據路由顯示第一頁或第二頁
const isFirstPage = computed(() => route.path === '/password/forgot');
const isSecondPage = computed(() => route.path === '/password/change');

// 第一頁欄位
const email = ref('')
const verificationCode = ref('')
const emailCheckStatus = ref('') // 'exists', 'not-exists', ''
const isEmailValid = computed(() => email.value.trim().length > 0)
const isEmailExists = computed(() => emailCheckStatus.value === 'exists')
const isEmailNotExists = computed(() => emailCheckStatus.value === 'not-exists')

// 第二頁欄位
const password = ref('')
const confirmPassword = ref('')

// 密碼驗證：8字元以上，可純英文、純數字或英文+數字，不可有中文或特殊符號
const isPasswordValid = computed(() => {
        const passwordRegex = /^[A-Za-z\d]{8,}$/
        const hasChinese = /[\u4e00-\u9fa5]/.test(password.value)
        return passwordRegex.test(password.value) && !hasChinese
})

// 確認密碼是否相同
const isConfirmPasswordValid = computed(() => {
        return password.value === confirmPassword.value && password.value !== ''
})

// 驗證 Email 是否存在於資料庫
function verifyEmail() {
    if (!isEmailValid.value) return;
    
    // TODO: 串接後端 API 驗證 email 是否存在
    // 目前模擬：test@example.com 存在，其他不存在
    if (email.value === 'test@example.com') {
        emailCheckStatus.value = 'exists';
    } else {
        emailCheckStatus.value = 'not-exists';
    }
}

function handleSubmit(e) {
    e.preventDefault();
    if (isFirstPage.value) {
        // 檢查 email 是否已驗證且存在
        if (!isEmailExists.value) {
            alert('請先驗證Email');
            return;
        }
        
        // 檢查驗證碼是否正確（去除空格）
        const trimmedCode = verificationCode.value.trim();
        console.log('輸入的驗證碼:', trimmedCode); // 除錯用
        if (trimmedCode !== '1234') {
            alert('驗證碼不正確');
            return;
        }
        
        // 驗證通過，跳轉到第二頁
        router.push('/password/change');
    } else if (isSecondPage.value) {
        // 驗證密碼
        if (!isPasswordValid.value || !isConfirmPasswordValid.value) return;
        // TODO: 串接 API
        alert('密碼已變更');
    }
}
</script>

<template>
    <div class="forgot-password-page">
        <FormTemplate @submit="handleSubmit">
            <h1 class="text-4xl text-center font-bold">忘記密碼</h1>
            <div v-if="isFirstPage">
                <label class="forgot-password-label">請輸入E-mail</label>
                <div class="mb-4 flex gap-2 items-center">
                    <input type="email" class="forgot-password-input" v-model="email" placeholder="請輸入您的E-mail">
                    <button type="button" class="form-forgot-password-btn text-center" @click="verifyEmail">驗證Email</button>
                </div>
                <p v-if="isEmailNotExists" class="forgot-password-error">Email不存在</p>
                <p v-if="!isEmailValid && email === ''" class="forgot-password-error">Email為必填</p>
                
                <label class="forgot-password-label">驗證碼</label>
                <div class="mb-4">
                    <input type="text" class="forgot-password-input" v-model="verificationCode" placeholder="請輸入您的驗證碼">
                </div>
            </div>

            <div v-if="isSecondPage">
                <div class="mb-4">
                    <label class="change-password-label">新密碼</label>
                    <input type="password" class="change-password-input" v-model="password" placeholder="XXXXXXXX">
                    <p v-if="password && !isPasswordValid" class="change-password-error">密碼必須至少8字元，僅限英文或數字，不可有特殊符號或中文</p>
                    <p v-if="!isPasswordValid && password === ''" class="change-password-error">密碼為必填</p>
                </div>
                <div class="mb-4">
                    <label class="change-password-label">再次輸入新密碼</label>
                    <input type="password" class="change-password-input" v-model="confirmPassword" placeholder="XXXXXXXX">
                    <p v-if="confirmPassword && !isConfirmPasswordValid" class="change-password-error">密碼不一致</p>
                    <p v-if="!isConfirmPasswordValid && confirmPassword === ''" class="change-password-error">確認密碼為必填</p>
                </div>
            </div>

            <template #actions>
                <div class="forgot-password-actions">
                    <RouterLink to="/login" class="cancel-forgot-password-btn text-center">取消</RouterLink>
                    <button v-if="isFirstPage" type="button" class="form-forgot-password-btn text-center" @click="handleSubmit">前往變更</button>
                    <button v-if="isSecondPage" type="submit" class="form-forgot-password-btn text-center">確認變更</button>
                </div>
            </template>
        </FormTemplate>
    </div>
</template>

<style scoped src="../styles/auth/forgotpassword.css"></style>