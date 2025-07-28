<script setup>
    import { ref } from 'vue';
    import { RouterLink } from 'vue-router';
    
    // 定義登入狀態
    const login = ref(false);
</script>

<template>
    <nav class="nav">
        <!-- 左側logo & 名字 -->
        <div class="navtitle">
            <img class="" src=""/>
            <p class=" text-base sm:text-2xl">
                <RouterLink to="/">寵旅匠-寵物美容預約平台</RouterLink>
            </p>
        </div>

        <!-- 右側 -->
        <div class="router">
            <RouterLink to="/">首頁</RouterLink>
            <a href="#">最新消息</a>
            <a href="#">店家列表</a>
            <a href="#">預約美容服務</a>
            <a href="#">寵物小學堂</a>
            <RouterLink to="/Login">
                <button class="btn login-btn" v-if="!login">
                    註冊/登入
                </button>
                <button class="btn logout-btn" v-else>
                    登出
                </button>
            </RouterLink>
        </div>
    </nav>
</template>

<style></style>
