<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import FormTemplate from '../../components/FormTemplate.vue'

const route = useRoute()

const agreePrivacy = ref(false)
const isDisabled = computed(() => {
    return !agreePrivacy.value
})

const submitForm = () => {
    console.log('確認註冊')
}

// 動態計算標題和按鈕文字
const formTitle = ref("毛主人註冊")
const buttonText = ref("確認註冊")
const handleSubmit = () => submitForm()
</script>

<template>
    <div class="shops-page min-h-screen bg-gray-50 py-8">
        <FormTemplate :title="formTitle" @submit="handleSubmit">
            <div class="mb-4">
                <label class="shops-label name">姓名（必填）</label>
                <input type="text" class="shops-input" placeholder="請填上您的姓名" required>
            </div>
            <div class="mb-4">
                <label class="shops-label account">帳號（必填）</label>
                <input type="tel" class="shops-input" placeholder="請輸入您的電話" required>
            </div>
            <div class="mb-4">
                <label class="shops-label password">密碼（必填）</label>
                <input type="text" class="shops-input" placeholder="請輸入密碼" required>
            </div>
            <div class="mb-4">
                <label class="shops-label checkpassword">確認密碼（必填）</label>
                <input type="text" class="shops-input" placeholder="請再次輸入密碼" required>
            </div>
            <div class="mb-4">
                <label class="shops-label localcall">聯絡市話（選填）</label>
                <input type="text" class="shops-input">
            </div>
            <div class="mb-4 text-center">
                <label>
                    <input type="checkbox" class="cursor-pointer" v-model="agreePrivacy" />
                    我同意隱私政策
                </label>
            </div>
            <template #actions>
                <button type="submit" class="form-regist-btn" :disabled="isDisabled">
                    {{ buttonText }}
                </button>
            </template>
        </FormTemplate>
    </div>
</template>