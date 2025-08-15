<script setup>
import { ref } from 'vue'
import { storesinfo } from '@/data/storeinfo' // 路徑依你的專案結構調整
// const storesinfo = ref(storeinfo.value)
</script>
<template>
  <section class="store-section">
    <!-- 標題與操作按鈕 -->
    <!-- 店名與地址 -->
    <div class="store-info">
       <div class="flex flex-col md:flex-row md:justify-between md:items-center">
      <h2 class="store-title">
        {{ storesinfo.name }}</h2>
      <p class="store-address"><FontAwesomeIcon :icon="['fas','location-dot']" class="mr-1" />
      {{ storesinfo.address }}</p>
       </div>
        <div class="flex gap-3 mt-4 justify-center">
        <button class="btn-outline flex-1">返回</button>
        <button class="btn-outline flex-1">店家貼文</button>
         <button class="btn-outline flex-1">服務項目</button>
      </div>
    
    </div>

    <!-- 輪播圖 -->
    <div class="store-carousel">
      <!-- 模擬圖片區塊 -->
      <div class="carousel-image"></div>
      <div class="carousel-dots">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
    </div>

    <!-- 四格資訊 -->
    <div class="store-quick-info">
      <div class="info-card">
        <h3 class="font-bold text-xl">聯絡電話</h3>
        <p>{{ storesinfo.phone }}</p>
      </div>
      <div class="info-card">
        <h3 class="font-bold text-xl">營業時間</h3>
        <p>{{ storesinfo.hours }}</p>
      </div>
      <div class="info-card">
        <h3 class="font-bold text-xl">有接送服務</h3>
        <p>{{ storesinfo.pickup ? '提供專車接送服務' : '否' }}</p>
      </div>
      <div class="info-card">
        <h3 class="font-bold text-xl">交通資訊</h3>
        <p>{{ storesinfo.traffic }}</p>
      </div>
    </div>

    <!-- 服務項目 -->
    <div class="store-services">
      <h3 class="section-subtitle font-bold text-xl">服務項目</h3>
      <div class="service-tags">
        <span class="tag">SPA護理</span>
        <span class="tag">美容剪毛</span>
        <span class="tag">住宿服務</span>
        <span class="tag">寵物洗澡</span>
        <span class="tag">寵物洗澡</span>
        <span class="tag">寵物洗澡</span>
      </div>
    </div>

    <!-- 店家簡介 -->
    <div class="store-description">
      <h3 class="section-subtitle font-bold text-xl mb-4">店家簡介</h3>
      <p>{{ storesinfo.description }}</p>

    </div>


 <!-- icon 區塊：只要其中任何一個有值才顯示整區 -->
    <div
  class="store-social-icons flex items-center gap-4"
  v-if="storesinfo.line || storesinfo.fb || storesinfo.google"
>
<!-- _blank點擊連結時 在新分頁開啟網址 rel避免安全漏洞 -->
  <a
    v-if="storesinfo.line"
    :href="storesinfo.line"
    target="_blank"  
    rel="noopener"
    aria-label="LINE"
    class="icon"
  >
    <FontAwesomeIcon :icon="['fab', 'line']" class="text-green-500" />
  </a>

  <a
    v-if="storesinfo.fb"
    :href="storesinfo.fb"
    target="_blank"
    rel="noopener"
    aria-label="Facebook"
    class="icon"
  >
    <FontAwesomeIcon :icon="['fab', 'facebook-f']" class="text-blue-600" />
  </a>

  <a
    v-if="storesinfo.google"
    :href="storesinfo.google"
    target="_blank"
    rel="noopener"
    aria-label="Google Maps"
    class="icon"
  >
    <FontAwesomeIcon :icon="['fab', 'google']" class="text-red-500" />
  </a>
</div>
  </section>
</template>
<style scoped src="@/styles/pages/Stores/storesinfo.css"></style>