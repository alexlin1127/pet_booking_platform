<template>
  <div class="p-6 space-y-8">
    <h1 class="text-2xl font-bold mb-6">卡片組件使用範例</h1>
    
    <!-- 直向卡片範例 -->
    <section>
      <h2 class="text-xl font-semibold mb-4">直向卡片範例</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- 基本直向卡片 (可點擊) -->
        <Card 
          type="vertical" 
          :clickable="true" 
          :hasButton="false"
          @click="handleCardClick('店家1')"
        >
          <template #icon>
            <div class="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center">
              <svg class="w-12 h-12 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 2L3 7v11a2 2 0 002 2h10a2 2 0 002-2V7l-7-5z"/>
              </svg>
            </div>
          </template>
          
          <template #caption>
            專業寵物美容護理服務
          </template>
          
          <template #title>
            毛毛寵物美容店
          </template>
          
          <template #content>
            <div class="card-info-item">
              <svg fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
              </svg>
              台北市大安區復興南路一段123號
            </div>
            
            <div class="card-info-item">
              <svg fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
              </svg>
              02-2345-6789
            </div>
            
            <div class="card-info-item">
              <svg fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
              週一至週日 09:00-21:00
            </div>
            
            <div class="flex flex-wrap mt-3">
              <span class="card-badge">美容服務</span>
              <span class="card-badge">洗澡服務</span>
            </div>
          </template>
        </Card>
        
        <!-- 有按鈕的直向卡片 -->
        <Card 
          type="vertical" 
          :clickable="false" 
          :hasButton="true"
        >
          <template #icon>
            <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center">
              <svg class="w-12 h-12 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </template>
          
          <template #caption>
            24小時專業寵物住宿服務
          </template>
          
          <template #title>
            愛心寵物旅館
          </template>
          
          <template #content>
            <div class="card-info-item">
              <svg fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
              </svg>
              新北市板橋區中山路二段456號
            </div>
            
            <div class="flex flex-wrap mt-3">
              <span class="card-badge">住宿服務</span>
              <span class="card-badge">24小時監護</span>
            </div>
          </template>
          
          <template #button>
            <button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              立即預約
            </button>
          </template>
        </Card>
      </div>
    </section>
    
    <!-- 橫向卡片範例 -->
    <section>
      <h2 class="text-xl font-semibold mb-4">橫向卡片範例</h2>
      
      <div class="space-y-4 max-w-2xl">
        <!-- 基本橫向卡片 -->
        <Card 
          type="horizontal" 
          :clickable="true" 
          :hasButton="false"
          @click="handleCardClick('店家A')"
        >
          <template #image>
            <img src="/api/placeholder/64/64" alt="店家圖片" class="rounded-md">
          </template>
          
          <template #title>
            快樂寵物診所
          </template>
          
          <template #content>
            <div class="card-info-item">
              <svg fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
              </svg>
              台中市西屯區台灣大道三段789號
            </div>
            <div class="card-info-item">
              <svg fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
              </svg>
              週一至週六 08:00-22:00
            </div>
          </template>
        </Card>
        
        <!-- 有按鈕的橫向卡片 -->
        <Card 
          type="horizontal" 
          :clickable="false" 
          :hasButton="true"
        >
          <template #image>
            <div class="w-full h-full bg-purple-100 rounded-md flex items-center justify-center">
              <svg class="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </template>
          
          <template #title>
            專業寵物訓練中心
          </template>
          
          <template #content>
            <div class="card-info-item">
              <svg fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
              </svg>
              03-1234-5678
            </div>
            <div class="flex flex-wrap">
              <span class="card-badge">行為訓練</span>
              <span class="card-badge">社會化課程</span>
            </div>
          </template>
          
          <template #button>
            <button class="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors">
              查看詳情
            </button>
          </template>
        </Card>
      </div>
    </section>
  </div>
</template>

<script setup>
import Card from '../UI/Card.vue'

const handleCardClick = (storeName) => {
  console.log(`點擊了 ${storeName}`)
  // 這裡可以添加導航邏輯，例如：
  // router.push(`/store/${storeId}`)
}
</script>
