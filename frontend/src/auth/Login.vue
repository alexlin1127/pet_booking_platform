<script setup>
import { ref, onMounted } from 'vue'
import FormTemplate from '../components/UI/FormTemplate.vue'
import api from '../api/api.js'
import { useRouter, RouterLink } from 'vue-router'

const router = useRouter()

// 表單資料
const password = ref('')
const username = ref('')
const captchaInput = ref('')
const captchaCode = ref('')
const captchaCanvas = ref(null)
const captchaInputRef = ref(null)

// 響應式驗證碼圖寬度
const captchaCanvasWidth = ref(80);
function updateCaptchaWidth() {
    if (window.innerWidth >= 768) {
        captchaCanvasWidth.value = 120;
    } else {
        captchaCanvasWidth.value = 80;
    }
}
// 產生四位數字驗證碼
function generateCaptcha() {
    captchaCode.value = Math.floor(1000 + Math.random() * 9000).toString();
    drawCaptcha();
}
// 畫驗證碼到 canvas
function drawCaptcha() {
    if (!captchaCanvas.value) return;
    const ctx = captchaCanvas.value.getContext('2d');
    ctx.clearRect(0, 0, captchaCanvasWidth.value, 32);
    // 背景
    ctx.fillStyle = '#f3f4f6';
    ctx.fillRect(0, 0, captchaCanvasWidth.value, 32);
    // 驗證碼文字
    ctx.font = 'bold 24px Arial';
    ctx.fillStyle = '#2563eb';
    ctx.textBaseline = 'middle';
    // 置中顯示
    const textWidth = ctx.measureText(captchaCode.value).width;
    ctx.fillText(captchaCode.value, (captchaCanvasWidth.value - textWidth) / 2, 16);
    // 干擾線
    for (let i = 0; i < 3; i++) {
        ctx.strokeStyle = `rgba(30,64,175,${0.2 + Math.random() * 0.5})`;
        ctx.beginPath();
        ctx.moveTo(Math.random() * captchaCanvasWidth.value, Math.random() * 32);
        ctx.lineTo(Math.random() * captchaCanvasWidth.value, Math.random() * 32);
        ctx.stroke();
    }
}
onMounted(() => {
    updateCaptchaWidth();
    window.addEventListener('resize', updateCaptchaWidth);
    generateCaptcha();
    // 進入畫面時若 ref 綁定已完成，立即畫一次
    setTimeout(() => { drawCaptcha(); }, 0);
});

const handleSubmit = async () => {
    // 僅允許 4 位數字
    if (!/^[0-9]{4}$/.test(captchaInput.value)) {
        alert('請輸入 4 位數字驗證碼');
        captchaInput.value = '';
        captchaInputRef.value && captchaInputRef.value.focus();
        return;
    }
    if (captchaInput.value !== captchaCode.value) {
        alert('驗證碼錯誤，請重新輸入');
        generateCaptcha();
        captchaInput.value = '';
        captchaInputRef.value && captchaInputRef.value.focus();
        return;
    }
    // 其餘登入/註冊流程
    try {
        const res = await api.post('/token', {
            username: username.value,
            password: password.value
        });
        localStorage.setItem('access_token', res.data.access);
    } catch (err) {
        alert('帳號或密碼錯誤');
        return;
    }
    // 登入成功後取得角色並導向
    try {
        const userRes = await api.get('/users/me');
        const role = userRes.data.role;
        
        if (role === 'admin') {
            console.log('用戶角色:', role);
            router.push('/admin');
        } else if (role === 'store') {
            router.push('/stores/dashboard');
        } else {
            router.push('/');
        }
        alert('驗證碼正確，登入成功');
    } catch (err) {
        alert('登入成功但取得用戶資料失敗');
    }
}

</script>

<template>
    <div class="login-page">
        <FormTemplate @submit="handleSubmit">
            <h1 class="text-4xl text-center font-bold">登入 / 註冊</h1>
            <div>
                <div class="mb-4">
                    <label class="login-label">帳號 ：</label>
                    <input type="text" class="login-input" v-model="username" placeholder="請輸入帳號名稱">
                </div>
                <div class="mb-4">
                    <label class="login-label">密碼 ：</label>
                    <input type="password" class="login-input" v-model="password" placeholder="請輸入密碼">
                </div>
                <div class="mb-4">
                    <label class="login-label">驗證碼 ：</label>
                    <div class="flex items-center gap-2">
                        <input type="text" inputmode="numeric" pattern="[0-9]*" class="login-input flex-1 no-spinner"
                            v-model="captchaInput" ref="captchaInputRef" maxlength="4" autocomplete="off"
                            placeholder="請輸入驗證碼" />
                        <canvas ref="captchaCanvas" :width="captchaCanvasWidth" height="32"
                            class="rounded border cursor-pointer select-none" @click="generateCaptcha"
                            title="點擊可刷新驗證碼"></canvas>
                    </div>
                </div>
            </div>
            <div class="mb-4 text-end">
                <RouterLink to="/password/forgot">忘記密碼</RouterLink>
            </div>
            <template #actions>
                <div class="login-actions">
                    <RouterLink to="/register" class="form-login-btn text-center">
                        註冊新帳戶
                    </RouterLink>
                    <button type="submit" class="form-login-btn text-center">
                        登入
                    </button>
                </div>
            </template>
        </FormTemplate>
        <!-- 社群登入卡片 -->
        <div class="flex flex-col gap-4 mt-8 items-center w-full max-w-xs mx-auto">
            <button
                class="login-social-card bg-green-500 text-white font-bold flex items-center px-6 py-3 rounded-lg shadow hover:bg-green-600 transition w-full">
                <FontAwesomeIcon icon="fa-brands fa-line" class="w-5 h-5" />
                <span class="flex-1 text-center">Line 登入</span>
            </button>
            <button
                class="login-social-card bg-white text-gray-800 font-bold flex items-center px-6 py-3 rounded-lg shadow border hover:bg-gray-100 transition w-full">
                <FontAwesomeIcon icon="fa-brands fa-google" class="w-5 h-5" />
                <span class="flex-1 text-center">Google 登入</span>
            </button>
            <button
                class="login-social-card bg-blue-600 text-white font-bold flex items-center px-6 py-3 rounded-lg shadow hover:bg-blue-700 transition w-full">
                <FontAwesomeIcon icon="fa-brands fa-facebook-f" class="w-5 h-5" />
                <span class="flex-1 text-center">Facebook 登入</span>
            </button>
        </div>
    </div>
</template>

<style scoped src="../styles/auth/login.css"></style>