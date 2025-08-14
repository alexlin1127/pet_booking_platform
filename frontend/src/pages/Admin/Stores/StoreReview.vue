<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../../../api/api.js";

const route = useRoute();
const router = useRouter();

// 從 URL 參數取得店家 ID
const storeId = computed(() => route.params.id);
// console.log(storeId.value);
// 根據 ID 調用 API 獲取店家詳細資料
const currentStore = ref(null);

async function fetchStoreDetails() {
  if (!storeId.value) return;
  try {
    const response = await api.get(`/admin/stores/${storeId.value}`);
    currentStore.value = response.data;
    console.log(currentStore.value);
  } catch (error) {
    console.error(error);
  }
}

onMounted(() => {
  fetchStoreDetails();
});

// 取得服務種類
const type = computed(() => {
  return route.query.service === "boarding" ? "boarding" : "grooming";
});

// 標題
const title = computed(() => {
  if (currentStore.value?.status === "pending") {
    return "店家資料審查";
  } else if (currentStore.value?.status === "confirmed") {
    return "店家資料詳情";
  }
  return "店家資料"; // 預設標題
});

// 切換鈕：只有同時有美容和住宿才顯示
// const showSwitchBtn = computed(() => hasGrooming.value && hasBoarding.value);

// 美容專屬欄位
// const showGrooming = computed(() => hasGrooming.value);
// 住宿專屬欄位
// const showBoarding = computed(() => hasBoarding.value);
// const showSafety = computed(
// () => type.value === "boarding" && hasBoarding.value;
// );

const imageList = computed(() => {
  const baseImages = [
    { title: "營業登記資料", url: currentStore.value?.business_licences_url },
  ];

  if (currentStore.value?.boarding_service) {
    if (
      Array.isArray(currentStore.value?.boarding_pet_type) &&
      currentStore.value.boarding_pet_type.includes("dog")
    ) {
      baseImages.push({
        title: "特定寵物登記許可證(狗狗)",
        url: currentStore.value?.boarding_license_dog_url,
      });
    }
    if (
      Array.isArray(currentStore.value?.boarding_pet_type) &&
      currentStore.value.boarding_pet_type.includes("cat")
    ) {
      baseImages.push({
        title: "特定寵物登記許可證(貓咪)",
        url: currentStore.value?.boarding_license_cat_url,
      });
    }
  }

  return baseImages;
});
const gridClass = computed(() =>
  type.value === "boarding" ? "sr-grid-3" : "sr-grid-2"
);

const bullet = (val) => (val ? "● 是   ○ 否" : "○ 是   ● 否");
function AddQ() {
  alert("加入問題件！");
}
function approve() {
  alert("核准完成！");
}
function setService(svc) {
  router.replace({ query: { ...route.query, service: svc } });
}
</script>

<template>
  <div class="sr-container max-w-4xl mx-auto">
    <!-- 當有店家資料時顯示內容 -->
    <div v-if="currentStore">
      <!-- demo 切換鈕，可刪 -->
      <div class="flex gap-2 mb-4" v-if="showSwitchBtn">
        <button class="sr-btn-outline" @click="setService('grooming')">
          寵物美容預覽
        </button>
        <button class="sr-btn-outline" @click="setService('boarding')">
          寵物住宿預覽
        </button>
      </div>

      <!-- 標題 -->
      <h1 class="sr-title">{{ title }}</h1>

      <!-- 基本資訊 -->
      <section>
        <div class="sr-row">
          <span class="sr-label">店家名稱</span
          ><span class="sr-value">{{ currentStore.store_name }}</span>
        </div>
        <div class="sr-row">
          <span class="sr-label">負責人姓名</span
          ><span class="sr-value">{{ currentStore.owner_name }}</span>
        </div>
        <div class="sr-row">
          <span class="sr-label">店家地址</span
          ><span class="sr-value"
            >{{ currentStore.address.county }}{{ currentStore.address.district
            }}{{ currentStore.address.detail }}</span
          >
        </div>
        <div class="sr-row">
          <span class="sr-label">聯絡電話</span
          ><span class="sr-value">{{ currentStore.phone }}</span>
        </div>
        <div class="sr-row">
          <span class="sr-label">信箱</span>
          <span class="sr-value">{{ currentStore.email }}</span>
        </div>

        <div class="sr-row">
          <span class="sr-label">提供接送服務</span
          ><span class="sr-value">{{
            bullet(currentStore.pick_up_service)
          }}</span>
        </div>
        <div class="sr-row">
          <span class="sr-label">提供美容服務</span
          ><span class="sr-value">{{
            bullet(currentStore.grooming_service)
          }}</span>
        </div>
        <div class="sr-row">
          <span class="sr-label">提供住宿服務</span
          ><span class="sr-value">{{
            bullet(currentStore.boarding_service)
          }}</span>
        </div>
        <div class="sr-row">
          <span class="sr-label">同一時段允許單筆或多筆預約</span
          ><span class="sr-value">{{
            bullet(currentStore.grooming_single_appointment)
          }}</span>
        </div>
        <div class="sr-row">
          <span class="sr-label">店內美容師人數</span>
          <span class="sr-value">{{ currentStore.staff_number }}</span>
        </div>
      </section>

      <!-- 圖片區 -->
      <div :class="[gridClass, 'mt-12']">
        <div
          v-for="(image, idx) in imageList"
          :key="idx"
          class="space-y-2 text-center"
        >
          <p class="sr-label w-full text-sm font-medium">{{ image.title }}</p>
          <div class="sr-box mx-auto">
            <img
              v-if="image.url"
              :src="image.url"
              :alt="image.title"
              class="w-full h-auto object-contain"
            />
            <!-- 佔位用 -->
          </div>
        </div>
      </div>

      <!-- 底部按鈕 -->
      <div
        v-if="currentStore.status === 'pending'"
        class="flex flex-col sm:flex-row gap-4 justify-center mt-16"
      >
        <button class="sr-btn sm:w-40" @click="AddQ">加入問題件</button>
        <button class="sr-btn sm:w-40" @click="approve">核准</button>
      </div>
      <div
        v-if="currentStore.status === 'confirmed'"
        class="flex flex-col sm:flex-row gap-4 justify-center mt-16"
      >
        <RouterLink :to="`/admin/stores/manage`">
          <button type="button" class="sr-btn sm:w-40">返回</button>
        </RouterLink>
      </div>
    </div>
    <!-- 當沒有找到店家資料時顯示提示 -->
    <div v-else="!currentStore" class="text-center py-16">
      <h2 class="text-xl font-semibold text-gray-600 mb-4">找不到店家資料</h2>
      <p class="text-gray-500">請確認 URL 中的店家 ID 是否正確</p>
    </div>
  </div>
</template>

<style></style>
