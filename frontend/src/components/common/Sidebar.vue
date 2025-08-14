<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '../../api/api.js'

const role = ref("admin")

const getRole = async () => {
    // 登入成功後取得腳色並導向
    try {
        const userRes = await api.get('/users/me');
        role.value = userRes.data.role;
        
    } catch (err) {
        alert('無法取得腳色');
    }
}

const isOpen = ref(true)
const isDesktop = ref(window.matchMedia('(min-width: 1024px)').matches)

const toggleSidebar = () => {
    isOpen.value = !isOpen.value
}

function handleResize() {
    isDesktop.value = window.matchMedia('(min-width: 1024px)').matches
}

onMounted(() => {
    window.addEventListener('resize', handleResize);
    getRole();
})
onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
})

// 新增展開狀態
const showGrooming = ref(false)
const showBoarding = ref(false)
const showManagement = ref(false)
const showAnnouncement = ref(false)
const showService = ref(false)
const showProfile = ref(false)
const showStore = ref(false)
</script>

<template>
    <div v-if="isDesktop" :class="['sidebar', isOpen ? 'sidebar-open' : 'sidebar-collapsed']">
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
            <div v-if="role == 'customers'" class="sidebar-menu-section">
                <RouterLink to="/customers" class="sidebar-link" active-class="sidebar-link-active">首頁</RouterLink>

                <!-- 公告相關 -->
                <div class="sidebar-submenu-group">
                    <div class="sidebar-link" @click="showAnnouncement = !showAnnouncement">公告</div>
                    <template v-if="showAnnouncement">
                        <RouterLink to="/customers/news" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">最新消息</RouterLink>
                    </template>
                </div>

                <!-- 服務與預約相關 -->
                <div class="sidebar-submenu-group">
                    <div class="sidebar-link" @click="showService = !showService">服務與預約</div>
                    <template v-if="showService">
                        <RouterLink to="/customers/orders/grooming" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">查看美容訂單</RouterLink>
                        <RouterLink to="/customers/orders/accommodation" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">查看住宿訂單</RouterLink>
                        <RouterLink to="/customers/orders/history" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">歷史訂單紀錄</RouterLink>
                    </template>
                </div>

                <!-- 店家資訊相關 -->
                <div class="sidebar-submenu-group">
                    <div class="sidebar-link" @click="showStore = !showStore">店家資訊</div>
                    <template v-if="showStore">
                        <RouterLink to="/customers/stores" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">店家資訊</RouterLink>
                        <RouterLink to="/customers/stores/map" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">店家分布</RouterLink>
                    </template>
                </div>

                <!-- 帳號與個人資料相關 -->
                <div class="sidebar-submenu-group">
                    <div class="sidebar-link" @click="showProfile = !showProfile">帳號與個人資料</div>
                    <template v-if="showProfile">
                        <RouterLink to="/customers/profile/settings" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">個人資料設定</RouterLink>
                        <RouterLink to="/customers/profile/favorites" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">收藏/追蹤店家</RouterLink>
                        <RouterLink to="/customers/profile/security" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">帳戶安全性設定</RouterLink>
                    </template>
                </div>
            </div>

            <!-- 店家選單 -->
            <div v-else-if="role == 'stores'" class="sidebar-menu-section">
                <RouterLink to="/stores/dashboard" class="sidebar-link" active-class="sidebar-link-active">首頁</RouterLink>
                <RouterLink to="/stores/addbookings" class="sidebar-link" active-class="sidebar-link-active">新增預約</RouterLink>
                <!-- 預約管理相關 -->
                <div class="sidebar-submenu-group">
                    <div class="sidebar-link" @click="showGrooming = !showGrooming">美容管理</div>
                    <template v-if="showGrooming">
                        <RouterLink to="/stores/grooming-bookings" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">今日美容預約</RouterLink>
                        <RouterLink to="/stores/grooming-bookings/manage" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">待審核預約</RouterLink>
                        <RouterLink to="/stores/grooming-bookings/history" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">歷史訂單紀錄</RouterLink>
                        <RouterLink to="/stores/grooming/watchlists" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">查看觀察名單</RouterLink>
                    </template>
                </div>

                <div class="sidebar-submenu-group">
                    <div class="sidebar-link" @click="showBoarding = !showBoarding">住宿管理</div>
                    <template v-if="showBoarding">
                        <RouterLink to="/stores/boarding-bookings" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">目前住宿總覽</RouterLink>
                        <RouterLink to="/stores/boarding-bookings/manage" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">待審核預約</RouterLink>
                        <RouterLink to="/stores/boarding-bookings/history" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">歷史訂單紀錄</RouterLink>
                        <RouterLink to="/stores/boarding/watchlists" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">查看觀察名單</RouterLink>
                    </template>
                </div>


                <!-- 店家管理相關 -->
                <div class="sidebar-submenu-group">
                    <div class="sidebar-link" @click="showManagement = !showManagement">店家管理</div>
                    <template v-if="showManagement">
                        <RouterLink to="/stores/info/manage" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">店家資訊管理</RouterLink>
                        <RouterLink to="/stores/services/manage" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">服務項目管理</RouterLink>
                        <RouterLink to="/stores/posts/manage" class="sidebar-link sidebar-submenu"
                            active-class="sidebar-link-active">貼文管理</RouterLink>
                    </template>
                </div>
            </div>

            <!-- 管理員選單 -->
            <div v-else class="sidebar-menu-section">
                <RouterLink to="/admin" class="sidebar-link" active-class="sidebar-link-active">首頁</RouterLink>
                <RouterLink to="/admin/stores/manage" class="sidebar-link" active-class="sidebar-link-active">店家帳號審核及管理
                </RouterLink>
                <RouterLink to="/admin/accounts" class="sidebar-link" active-class="sidebar-link-active">帳號管理
                </RouterLink>
                <RouterLink to="/admin/posts" class="sidebar-link" active-class="sidebar-link-active">貼文管理</RouterLink>
            </div>
        </div>
    </div>
</template>