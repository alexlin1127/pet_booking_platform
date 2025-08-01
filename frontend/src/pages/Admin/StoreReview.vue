
<script setup>
import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { stores } from "../../data/storeData.js";

const route = useRoute();
const router = useRouter();

// 從 URL 參數取得店家 ID
// 使用方式：/store-review?id=H0001&service=grooming
const storeId = computed(() => route.query.id);

// 根據 ID 找到對應的店家資料
const currentStore = computed(() => {
    if (!storeId.value) return null;
    return stores.find(store => store.id === storeId.value) || null;
});

// 取得服務種類
const type = computed(() => route.query.service === "lodging" ? "lodging" : "grooming");

// 依據目前店家服務類型
const hasGrooming = computed(() => currentStore.value?.hasGrooming || false);
const hasLodging = computed(() => currentStore.value?.hasLodging || false);

// 標題
const title = computed(() => type.value === "lodging" ? "店家資料審查" : "店家資料詳情");

// 切換鈕：只有同時有美容和住宿才顯示
const showSwitchBtn = computed(() => hasGrooming.value && hasLodging.value);

// 美容專屬欄位
const showGrooming = computed(() => hasGrooming.value);
// 住宿專屬欄位
const showLodging = computed(() => hasLodging.value);
const showSafety = computed(() => type.value === "lodging" && hasLodging.value);

const imageList = computed(() =>
    type.value === "lodging"
        ? [
            "營業登記資料",
            "特定寵物登記許可證",
            "營業場所文件",
            "申請書與切結書",
            "服務環境/相關證照",
            "消防安全相關照片",
        ]
        : ["服務環境/相關證照", "營業登記資料"]
);
const gridClass = computed(() =>
    type.value === "lodging" ? "sr-grid-3" : "sr-grid-2"
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
        <!-- 當沒有找到店家資料時顯示提示 -->
        <div v-if="!currentStore" class="text-center py-16">
            <h2 class="text-xl font-semibold text-gray-600 mb-4">找不到店家資料</h2>
            <p class="text-gray-500">請確認 URL 中的店家 ID 是否正確</p>
            <p class="text-sm text-gray-400 mt-2">使用方式：?id=H0001&service=grooming</p>
        </div>

        <!-- 當有店家資料時顯示內容 -->
        <div v-else>
            <!-- demo 切換鈕，可刪 -->
            <div class="flex gap-2 mb-4" v-if="showSwitchBtn">
                <button class="sr-btn-outline" @click="setService('grooming')">
                    寵物美容預覽
                </button>
                <button class="sr-btn-outline" @click="setService('lodging')">
                    寵物住宿預覽
                </button>
            </div>

            <!-- 標題 -->
            <h1 class="sr-title">{{ title }}</h1>

            <!-- 基本資訊 -->
            <section>
                <div class="sr-row">
                    <span class="sr-label">店家名稱</span><span class="sr-value">{{ currentStore.storeName }}</span>
                </div>
                <div class="sr-row">
                    <span class="sr-label">負責人姓名</span><span class="sr-value">{{ currentStore.owner }}</span>
                </div>
                <div class="sr-row">
                    <span class="sr-label">店家地址</span><span class="sr-value">{{ currentStore.address }}</span>
                </div>
                <div class="sr-row">
                    <span class="sr-label">聯絡電話</span><span class="sr-value">{{ currentStore.phone }}</span>
                </div>
                <div class="sr-row">
                    <span class="sr-label">信箱</span>
                    <span class="sr-value">{{ currentStore.email }}</span>
                </div>

                <div class="sr-row">
                    <span class="sr-label">提供接送服務</span><span class="sr-value">{{ bullet(currentStore.pickup) }}</span>
                </div>
                <div class="sr-row">
                    <span class="sr-label">提供美容服務</span><span class="sr-value">{{ bullet(currentStore.hasGrooming) }}</span>
                </div>
                <div class="sr-row">
                    <span class="sr-label">提供住宿服務</span><span class="sr-value">{{ bullet(currentStore.hasLodging) }}</span>
                </div>

                <!-- 美容專屬欄位 -->
                <template v-if="showGrooming">
                    <div class="sr-row">
                        <span class="sr-label">服務細項</span><span class="sr-value">{{ currentStore.groomingdetails }}</span>
                    </div>
                    <div class="sr-row">
                        <span class="sr-label">專業證照</span><span class="sr-value">{{ currentStore.certificate }}</span>
                    </div>
                </template>

                <div class="sr-row items-start">
                    <span class="sr-label">店家簡介</span>
                    <p class="sr-value whitespace-pre-line">{{ currentStore.intro }}</p>
                </div>
            </section>

            <!-- 消防安全（住宿版才顯示） -->
            <template v-if="showSafety">
                <div class="sr-row">
                    <span class="sr-label">服務細項</span>
                    <span class="sr-value">{{ currentStore.lodgingdetails }}</span>
                </div>
                <h2 class="sr-subttl">消防安全設備說明(必填)</h2>
                <p class="whitespace-pre-line">{{ currentStore.safetyInstructions }}</p>
            </template>

            <!-- 圖片區 -->
            <div :class="[gridClass, 'mt-12']">
                <div v-for="(title, idx) in imageList" :key="idx" class="space-y-2 text-center">
                    <p class="sr-label w-full text-sm font-medium">{{ title }}</p>
                    <div class="sr-box mx-auto"></div>
                    <!-- 佔位用 -->
                </div>
            </div>

            <!-- 底部按鈕 -->
            <div class="flex flex-col sm:flex-row gap-4 justify-center mt-16">
                <button class="sr-btn sm:w-40" @click="AddQ">加入問題件</button>
                <button class="sr-btn sm:w-40" @click="approve">核准</button>
            </div>
        </div>
    </div>
</template>

<style></style>
