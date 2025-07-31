<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const isOpen = ref(true)
const toggleSidebar = () => {
    isOpen.value = !isOpen.value
}
</script>

<template>
    <div :class="['sidebar', isOpen ? 'sidebar-open' : 'sidebar-collapsed']">
        <div :class="['functionmenu', isOpen ? 'functionmenu-open' : 'functionmenu-collapsed']" @click="toggleSidebar">
            <p v-if="isOpen" class="sidebar-menu-text">
                <span>功</span><span>能</span><span>選</span><span>單</span>
                <FontAwesomeIcon icon="angle-left" class="sidebar-menu-icon" />
            </p>
            <p v-else class="sidebar-menu-text-collapsed">
                <FontAwesomeIcon icon="angle-right" class="sidebar-menu-icon mb-1" />
                <span>功</span>
                <span>能</span>
                <span>選</span>
                <span>單</span>
            </p>
        </div>
        <div v-if="isOpen" class="sidebar-links">
            <RouterLink to="/Admin" class="sidebar-link">首頁</RouterLink>
            <RouterLink to="/Admin/Store/Manage" class="sidebar-link">店家帳號審核及管理</RouterLink>
            <RouterLink to="/Admin/Account" class="sidebar-link">帳號管理</RouterLink>
            <RouterLink to="/Admin/Post" class="sidebar-link">貼文管理</RouterLink>
        </div>
    </div>
</template>

