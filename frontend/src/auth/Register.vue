<script setup>
import { RouterLink } from 'vue-router';
import Card from '../components/UI/Card.vue';
</script>

<template>
    <h1 class="text-4xl text-center font-bold">選擇註冊身分</h1>
    <!-- 左<Card /> -->
    <!-- 右<Card/> -->
    <RouterLink to="/register/customers">使用者註冊</RouterLink>
    <RouterLink to="/register/stores/1">商家註冊</RouterLink>
</template>
<style></style>