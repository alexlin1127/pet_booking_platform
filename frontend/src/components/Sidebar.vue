<script setup>

import { ref } from 'vue'
const isOpen = ref(true)
const toggleSidebar = () => {
    isOpen.value = !isOpen.value
}
</script>

<template>
    <div :class="['sidebar', isOpen ? 'sidebar-open' : 'sidebar-collapsed']">
        <div :class="['functionmenu', isOpen ? 'functionmenu-open' : 'functionmenu-collapsed']" @click="toggleSidebar">
            <p v-if="isOpen" class="sidebar-menu-text">
                功能選單
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
        <div>
            <RouterLink>
                <slot name="sidebar-link"></slot>
            </RouterLink>
        </div>
    </div>
</template>

