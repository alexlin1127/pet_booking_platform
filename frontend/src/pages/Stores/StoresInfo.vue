<script></script>
<template>
  <section class="store-section">
    <!-- 標題與操作按鈕 -->
    <div class="store-header">
      <h1 class="store-title">店家資訊</h1>
      <div class="store-actions">
        <button class="btn-outline">修改資料</button>
        <button class="btn-black">變更服務</button>
      </div>
    </div>

    <!-- 店名與地址 -->
    <div class="store-info">
      <h2 class="store-name">🐾 毛寶貝寵物美容沙龍</h2>
      <p class="store-address">📍 花蓮縣花蓮市 XXXXXXXXX</p>
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
        <h3>聯絡電話</h3>
        <p>02-1234-5678</p>
      </div>
      <div class="info-card">
        <h3>營業時間</h3>
        <p>週一～週六10:00–19:00</p>
      </div>
      <div class="info-card">
        <h3>有接送服務</h3>
        <p>提供專車接送服務</p>
      </div>
      <div class="info-card">
        <h3>交通資訊</h3>
        <p>靠近某某捷運站，附近有停車場</p>
      </div>
    </div>

    <!-- 服務項目 -->
    <div class="store-services">
      <h3 class="section-subtitle">服務項目</h3>
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
      <h3 class="section-subtitle">店家簡介</h3>
      <p>我們專為海內外飼主們設計舒適、安全、溫馨的住宿空間，讓每位毛孩在主人不在身邊時，依然能受到最用心的照料...</p>
      <ul class="features-list">
        <li>獨立空間設計</li>
        <li>專業照護團隊</li>
        <li>每日回報服務</li>
        <li>活動及互動時間</li>
        <li>依需求設施改變</li>
      </ul>
    </div>

    <!-- 公告欄 -->
    <div class="store-alert">
      <p>重要通知：8/20 本店休息一天，請提早安排您的寵物住宿預約。感謝理解與支持！</p>
    </div>

    <!-- icon 區塊 -->
    <div class="store-social-icons">
      <i class="icon bi bi-facebook"></i>
      <i class="icon bi bi-line"></i>
      <i class="icon bi bi-instagram"></i>
      <i class="icon bi bi-google"></i>
    </div>
  </section>
</template>
<style scoped src="@/styles/pages/Stores/storesinfo.css"></style>