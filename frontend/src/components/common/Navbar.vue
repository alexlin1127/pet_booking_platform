<script setup>
import { ref, computed } from 'vue';
import { RouterLink, useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

// 定義登入狀態
const login = ref(true); // 改為 true 方便測試
const role = ref('stores'); // 可以是 'admin', 'stores', 'customers'

// 手機版選單狀態
const isMobileMenuOpen = ref(false);

// 會員中心折疊狀態
const isMemberSectionOpen = ref(false);

// 計算當前路徑
const currentPath = computed(() => route.path);

// 判斷是否在管理後台
const isAdminPage = computed(() => currentPath.value.startsWith('/admin'));
// 判斷是否在商家後台
const isStorePage = computed(() => currentPath.value.startsWith('/stores'));

// 登出功能
const logout = () => {
  login.value = false;
  role.value = '';
  router.push('/login');
};

// 切換前後台
const toggleBackend = () => {
  if (role.value === 'admin') {
    if (isAdminPage.value) {
      router.push('/');
    } else {
      router.push('/admin');
    }
  } else if (role.value === 'stores') {
    if (isStorePage.value) {
      router.push('/');
    } else {
      router.push('/stores/posts/manage');
    }
  }
};

// 切換手機版選單
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

// 切換會員中心區塊
const toggleMemberSection = () => {
  isMemberSectionOpen.value = !isMemberSectionOpen.value;
};
</script>

<template>
    <nav class="nav">
        <!-- 手機版漢堡選單 -->
        <div class="mobile-menu-btn lg:hidden">
            <button @click="toggleMobileMenu" class="hamburger-btn">
                ☰
            </button>
        </div>

        <!-- 左側 Logo & 名稱 -->
        <div class="navtitle">
            <img src="https://via.placeholder.com/40x40?text=LOGO" alt="Logo" />
            <p>
                <RouterLink to="/" class="brand-link">寵物美容預約平台</RouterLink>
            </p>
        </div>

        <!-- 中間導航選單 (桌面版) - 管理者和店家登入後不顯示，其他身分都顯示 -->
        <div v-if="!login || (role !== 'admin' && role !== 'stores')" class="nav-menu hidden lg:flex ml-auto mr-4">
            <RouterLink to="/" class="nav-link">首頁</RouterLink>
            <RouterLink to="/news" class="nav-link">最新消息</RouterLink>
            <RouterLink to="/stores" class="nav-link">查看店家</RouterLink>
            <RouterLink to="/booking/grooming" class="nav-link">預約美容</RouterLink>
            <RouterLink to="/booking/lodging" class="nav-link">預約住宿</RouterLink>
        </div>

        <!-- 右側用戶區域 -->
        <div class="user-area flex items-center">
            <!-- 用戶問候語 -->
            <div v-if="login" class="user-greeting hidden lg:block">
                <p v-if="role === 'admin'" class="greeting-text">Hi, 管理者</p>
                <p v-else-if="role === 'stores'" class="greeting-text">XX店家</p>
                <p v-else-if="role === 'customers'" class="greeting-text">XX使用者</p>
            </div>

            <!-- 前後台切換按鈕 -->
            <div v-if="login && (role === 'admin' || role === 'stores')" class="backend-toggle">
                <button @click="toggleBackend" class="toggle-btn">
                    <span v-if="role === 'admin'">
                        {{ isAdminPage ? '前台' : '後台' }}
                    </span>
                    <span v-else-if="role === 'stores'">
                        {{ isStorePage ? '前台' : '後台' }}
                    </span>
                </button>
            </div>

            <!-- 會員中心 (僅客戶顯示) -->
            <div v-if="login && role === 'customers'" class="member-center hidden lg:block">
                <div class="dropdown">
                    <button class="dropdown-btn">會員中心</button>
                    <div class="dropdown-menu">
                        <RouterLink to="/member/profile" class="dropdown-item">基本資料</RouterLink>
                        <RouterLink to="/member/pets" class="dropdown-item">毛孩資料</RouterLink>
                        <RouterLink to="/member/bookings" class="dropdown-item">預約紀錄</RouterLink>
                    </div>
                </div>
            </div>

            <!-- 登入/登出按鈕 -->
            <div class="auth-buttons">
                <RouterLink to="/login" v-if="!login">
                    <button class="login-btn">登入</button>
                </RouterLink>
                <button v-else @click="logout" class="logout-btn">登出</button>
            </div>
        </div>

        <!-- 手機版側邊選單 -->
        <div v-show="isMobileMenuOpen" class="mobile-sidebar lg:hidden">
            <!-- 會員中心 (手機版) -->
            <div v-if="login && role === 'customers'" class="mobile-member">
                <button @click="toggleMemberSection" class="mobile-section-title w-full text-left flex justify-between items-center">
                    會員中心
                    <span class="transform transition-transform duration-200" :class="{ 'rotate-180': isMemberSectionOpen }">▼</span>
                </button>
                <div v-show="isMemberSectionOpen" class="mobile-member-links mt-2 space-y-1">
                    <RouterLink to="/member/profile" class="mobile-link" @click="isMobileMenuOpen = false">基本資料</RouterLink>
                    <RouterLink to="/member/pets" class="mobile-link" @click="isMobileMenuOpen = false">毛孩資料</RouterLink>
                    <RouterLink to="/member/bookings" class="mobile-link" @click="isMobileMenuOpen = false">預約紀錄</RouterLink>
                </div>
            </div>
            
            <!-- 主要導航 (手機版) - 只對客戶和未登入用戶顯示 -->
            <div v-if="!login || (role !== 'admin' && role !== 'stores')" class="mobile-nav">
                <RouterLink to="/" class="mobile-link" @click="isMobileMenuOpen = false">首頁</RouterLink>
                <RouterLink to="/news" class="mobile-link" @click="isMobileMenuOpen = false">最新消息</RouterLink>
                <RouterLink to="/stores" class="mobile-link" @click="isMobileMenuOpen = false">查看店家</RouterLink>
                <RouterLink to="/booking/grooming" class="mobile-link" @click="isMobileMenuOpen = false">預約美容</RouterLink>
                <RouterLink to="/booking/lodging" class="mobile-link" @click="isMobileMenuOpen = false">預約住宿</RouterLink>
            </div>
        </div>
    </nav>
</template>


