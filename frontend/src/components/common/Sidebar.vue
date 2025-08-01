<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const role = ref("admin")

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
            <!-- 一般用戶選單 -->
            <div v-if="role == 'User'" class="sidebar-menu-section">
                <RouterLink to="/user" class="sidebar-link" active-class="sidebar-link-active">首頁</RouterLink>
                
                <!-- 公告相關 -->
                <div class="sidebar-submenu-group">
                    <RouterLink to="/user/announcement" class="sidebar-link" active-class="sidebar-link-active">公告</RouterLink>
                    <RouterLink to="/user/news" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">最新消息</RouterLink>
                </div>
                
                <!-- 服務與預約相關 -->
                <div class="sidebar-submenu-group">
                    <RouterLink to="/user/service" class="sidebar-link" active-class="sidebar-link-active">服務與預約</RouterLink>
                    <RouterLink to="/user/orders/grooming" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">查看美容訂單</RouterLink>
                    <RouterLink to="/user/orders/accommodation" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">查看住宿訂單</RouterLink>
                    <RouterLink to="/user/orders/history" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">歷史訂單紀錄</RouterLink>
                </div>
                
                <!-- 店家資訊相關 -->
                <div class="sidebar-submenu-group">
                    <RouterLink to="/user/stores" class="sidebar-link" active-class="sidebar-link-active">店家資訊</RouterLink>
                    <RouterLink to="/user/stores/map" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">店家分布</RouterLink>
                </div>
                
                <!-- 帳號與個人資料相關 -->
                <div class="sidebar-submenu-group">
                    <RouterLink to="/user/profile" class="sidebar-link" active-class="sidebar-link-active">帳號與個人資料</RouterLink>
                    <RouterLink to="/user/profile/settings" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">個人資料設定</RouterLink>
                    <RouterLink to="/user/profile/favorites" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">收藏/追蹤店家</RouterLink>
                    <RouterLink to="/user/profile/security" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">帳戶安全性設定</RouterLink>
                </div>
            </div>
            
            <!-- 店家選單 -->
            <div v-else-if="role == 'Shop'" class="sidebar-menu-section">
                <RouterLink to="/shop" class="sidebar-link" active-class="sidebar-link-active">首頁</RouterLink>
                
                <!-- 預約管理相關 -->
                <div class="sidebar-submenu-group">
                    <RouterLink to="/shop/bookings" class="sidebar-link" active-class="sidebar-link-active">預約管理</RouterLink>
                    <RouterLink to="/shop/bookings/grooming" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">查看美容訂單</RouterLink>
                    <RouterLink to="/shop/bookings/accommodation" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">查看住宿訂單</RouterLink>
                    <RouterLink to="/shop/bookings/history" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">歷史訂單紀錄</RouterLink>
                    <RouterLink to="/shop/bookings/risk" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">查看風險訂單</RouterLink>
                </div>
                
                <!-- 店家管理相關 -->
                <div class="sidebar-submenu-group">
                    <RouterLink to="/shop/management" class="sidebar-link" active-class="sidebar-link-active">店家管理</RouterLink>
                    <RouterLink to="/shop/management/info" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">店家資訊管理</RouterLink>
                    <RouterLink to="/shop/management/services" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">服務項目管理</RouterLink>
                    <RouterLink to="/shop/management/posts" class="sidebar-link sidebar-submenu" active-class="sidebar-link-active">貼文管理</RouterLink>
                </div>
            </div>
            
            <!-- 管理員選單 -->
            <div v-else class="sidebar-menu-section">
                <RouterLink to="/admin" class="sidebar-link" active-class="sidebar-link-active">首頁</RouterLink>
                <RouterLink to="/admin/store/manage" class="sidebar-link" active-class="sidebar-link-active">店家帳號審核及管理</RouterLink>
                <RouterLink to="/admin/account" class="sidebar-link" active-class="sidebar-link-active">帳號管理</RouterLink>
                <RouterLink to="/admin/post" class="sidebar-link" active-class="sidebar-link-active">貼文管理</RouterLink>
            </div>
        </div>
    </div>
</template>
