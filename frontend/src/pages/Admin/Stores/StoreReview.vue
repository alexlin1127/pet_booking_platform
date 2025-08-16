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

// modal 狀態
const showModal = ref(false);
const rejectReason = ref("");

function AddQ() {
  showModal.value = true;
}
function closeModal() {
  showModal.value = false;
  rejectReason.value = "";
}
const confirmReject = async () => {
  try {
    const res = await api.patch(`/admin/stores/${storeId.value}`, {
      status: "rechecked",
      reject_content: rejectReason.value,
    });
    alert("退件原因已更新：" + rejectReason.value);
    closeModal();
  } catch (error) {
    console.error("更新失敗", error);
    alert("更新失敗，請稍後再試");
  }
  router.push("/admin/stores/manage");
};
const approve = async () => {
  try {
    const res = await api.patch(`/admin/stores/${storeId.value}`, {
      status: "confirmed",
    });
    alert("核准完成！");
  } catch (error) {
    console.error("核准失敗", error);
    alert("核准失敗，請稍後再試");
  }
  router.push("/admin/stores/manage");
};
function setService(svc) {
  router.replace({ query: { ...route.query, service: svc } });
}
function back() {
  router.push("/admin/stores/manage");
}
</script>

<template>
  <div class="sr-main-container">
    <!-- 當有店家資料時顯示內容 -->
    <div v-if="currentStore">
      <!-- demo 切換鈕，可刪 -->
      <div class="sr-switch-bar" v-if="showSwitchBtn">
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
      <div :class="[gridClass, 'sr-image-list']">
        <div v-for="(image, idx) in imageList" :key="idx" class="sr-image-item">
          <p class="sr-image-title">{{ image.title }}</p>
          <div class="sr-image-box">
            <img
              v-if="image.url"
              :src="image.url"
              :alt="image.title"
              class="sr-image-img"
            />
            <!-- 佔位用 -->
          </div>
        </div>
      </div>

      <!-- 退件原因 -->
      <div v-if="currentStore.status === 'rechecked'" class="sr-reject-content">
        <h3 class="sr-reject-title">退件原因</h3>
        <p class="sr-reject-text">{{ currentStore.reject_content }}</p>
      </div>

      <!-- 底部按鈕 -->
      <div v-if="currentStore.status === 'pending'" class="sr-bottom-btns">
        <button class="sr-btn sm:w-40" @click="back">返回</button>
        <button class="sr-btn sm:w-40" @click="AddQ">加入問題件</button>
        <button class="sr-btn sm:w-40" @click="approve">核准</button>
      </div>

      <!-- Modal 退件原因 -->
      <div v-if="showModal" class="sr-modal-mask">
        <div class="sr-modal-box">
          <div class="sr-modal-close">
            <button @click="closeModal">×</button>
          </div>
          <div class="sr-modal-row">
            <div class="sr-modal-label">店家編號</div>
            <div class="sr-modal-label">
              {{ currentStore.store_id || "0000" }}
            </div>
          </div>
          <div class="sr-modal-row">
            <div class="sr-modal-label">店家名稱</div>
            <div class="sr-modal-label">{{ currentStore.store_name }}</div>
          </div>
          <div class="sr-modal-row">
            <div class="sr-modal-label">負責人姓名</div>
            <div class="sr-modal-label">{{ currentStore.owner_name }}</div>
          </div>
          <div class="sr-modal-title">退件原因</div>
          <textarea
            v-model="rejectReason"
            placeholder="請輸入退件原因"
            rows="4"
            class="sr-modal-textarea"
          ></textarea>
          <div class="sr-modal-btns">
            <button @click="closeModal" class="sr-modal-btn-outline">
              返回
            </button>
            <button @click="confirmReject" class="sr-modal-btn">確定</button>
          </div>
        </div>
      </div>
      <div v-if="currentStore.status === 'confirmed'" class="sr-bottom-btns">
        <RouterLink :to="`/admin/stores/manage`">
          <button type="button" class="sr-btn sm:w-40">返回</button>
        </RouterLink>
      </div>
    </div>

    <!-- 當沒有找到店家資料時顯示提示 -->
    <div v-else="!currentStore" class="sr-notfound">
      <h2 class="sr-notfound-title">找不到店家資料</h2>
      <p class="sr-notfound-desc">請確認 URL 中的店家 ID 是否正確</p>
    </div>
  </div>
</template>

<style scoped src="../../../styles/pages/Admin/Stores/storereview.css"></style>
