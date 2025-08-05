<script setup>
import { RouterLink, useRouter } from 'vue-router';
import Card from '../components/UI/Card.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

const router = useRouter();

const goBack = () => {
  router.push('/login');
};
</script>

<template>
    <div class="register-page">
        <h1 class="register-title">選擇註冊身分</h1>
        
        <!-- 卡片容器 - 響應式佈局 -->
        <div class="register-cards-container">
            
            <!-- 左卡片 - 毛孩家長 -->
            <RouterLink to="/register/customers" class="register-card-link">
                <Card type="vertical" class="register-card register-group">
                    <template #icon>
                        <div class="register-icon register-icon-blue">
                            <FontAwesomeIcon icon="fa-solid fa-calendar" />
                        </div>
                    </template>
                    
                    <template #caption>
                        <p class="register-caption">幫毛孩預約服務</p>
                    </template>
                    
                    <template #title>
                        <h3 class="register-card-title register-title-blue">毛孩家長</h3>
                    </template>
                </Card>
            </RouterLink>
            
            <!-- 右卡片 - 店家夥伴 -->
            <RouterLink to="/register/stores/1" class="register-card-link">
                <Card type="vertical" class="register-card register-group">
                    <template #icon>
                        <div class="register-icon register-icon-green">
                            <FontAwesomeIcon icon="fa-solid fa-handshake" />
                        </div>
                    </template>
                    
                    <template #caption>
                        <p class="register-caption">經營毛孩服務</p>
                    </template>
                    
                    <template #title>
                        <h3 class="register-card-title register-title-green">店家夥伴</h3>
                    </template>
                </Card>
            </RouterLink>
            
        </div>
        
        <!-- 返回按鈕 -->
        <button @click="goBack" class="register-back-btn">
            返回
        </button>
    </div>
</template>

<style scoped>
/* 樣式已移至 styles/auth/login.css */
</style>