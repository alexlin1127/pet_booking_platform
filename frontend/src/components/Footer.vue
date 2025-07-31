<script setup>
import { ref } from 'vue'

const role = ref('admin')
</script>
<template>
    <footer class="footer">
        <Router-link to="">聯繫我們</Router-link>
        <Router-link to="">隱私權政策</Router-link>
        <Router-link to="">服務條款</Router-link>
        <Router-link to="" v-if="role !== 'admin'">寵物QA</Router-link>
        <Router-link to="" v-if="role !== 'admin'">使用手冊</Router-link>
        <Router-link to="">寵物美容預約平台.版權所有.</Router-link>
    </footer>
</template>



<style scoped></style>
