<script setup>
import { useRouter } from "vue-router";
import { ref, computed, onMounted } from "vue";
import api from "../../../api/api.js";

const userId = ref(null);

onMounted(async () => {
  try {
    const response = await api.get("/users/me");
    userId.value = response.data.id;
    // console.log("User ID fetched:", userId.value);
  } catch (error) {
    console.error("Error fetching user data:", error);
  }
});

const storesinfo = ref({});

const fetchStoreInfo = async () => {
  try {
    const response = await api.get(`/store/profile/${userId.value}`);
    const data = response.data;

    // Format time fields to remove seconds
    if (data.daily_opening_time) {
      data.daily_opening_time = data.daily_opening_time.slice(0, 5);
    }
    if (data.daily_closing_hours) {
      data.daily_closing_hours = data.daily_closing_hours.slice(0, 5);
    }

    storesinfo.value = data;
    console.log("Store info fetched:", storesinfo.value);
  } catch (error) {
    console.error("Error fetching store info:", error);
  }
};

onMounted(fetchStoreInfo);

const router = useRouter();
</script>
<template>
  <section class="store-section">
    <!-- 標題與操作按鈕 -->
    <div class="store-header">
      <h1 class="store-title">店家資訊</h1>
      <div class="store-actions">
        <button class="btn-outline" @click="router.push('/stores/info/edit')">
          修改資料
        </button>
        <button class="btn-black" @click="router.push('/stores/openservices')">
          變更服務
        </button>
      </div>
    </div>
    <!-- 店家審核狀態 -->
    <h2 class="store-status">
      <FontAwesomeIcon :icon="['fas', 'sync-alt']" />
      <span v-if="storesinfo.status === 'pending'">審核中</span>
      <span v-else-if="storesinfo.status === 'confirmed'">已通過</span>
      <span v-else-if="storesinfo.status === 'rechecked'">退回補件</span>
    </h2>

    <!-- 店名與地址 -->
    <div class="store-info">
      <div class="flex flex-col md:flex-row md:justify-between md:items-center">
        <h2 class="store-name">
          <FontAwesomeIcon :icon="['fas', 'circle']" />
          {{ storesinfo.store_name }}
        </h2>
        <p class="store-address" v-if="storesinfo.address">
          <FontAwesomeIcon :icon="['fas', 'location-dot']" class="mr-1" />
          {{ storesinfo.address.county }}{{ storesinfo.address.district
          }}{{ storesinfo.address.detail }}
        </p>
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
        <p>
          {{ storesinfo.daily_opening_time }} -
          {{ storesinfo.daily_closing_hours }}
        </p>
      </div>
      <div class="info-card">
        <h3 class="font-bold text-xl">有接送服務</h3>
        <p>{{ storesinfo.pick_up_service ? "有" : "否" }}</p>
      </div>
      <div class="info-card">
        <h3 class="font-bold text-xl">交通資訊</h3>
        <p>{{ storesinfo.traffic_info }}</p>
      </div>
    </div>

    <!-- 服務項目 -->
    <div class="store-services">
      <h3 class="section-subtitle font-bold text-xl">服務項目</h3>
      <div
        v-for="service in storesinfo.service_item"
        :key="service"
        class="service-tags"
      >
        <span class="tag">{{ service }}</span>
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
