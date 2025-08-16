<script setup>
import { ref, computed, onMounted, watch } from "vue";
import Table from "../../../components/UI/Table.vue";
import StoreCard from "./StoreCard.vue";
import Pagination from "../../../components/common/Pagination.vue";
import api from "../../../api/api.js";

const stores = ref([]); // 初始化為空陣列

const storeData = async () => {
  try {
    const res = await api.get("admin/stores");
    console.log(res.data); // 調試 API 響應
    stores.value = Array.isArray(res.data) ? res.data : []; // 確保返回值為陣列
  } catch (err) {
    alert("無法取得店家資料");
    stores.value = []; // 確保失敗時為空陣列
  }
};

onMounted(() => {
  storeData();
});

// 狀態對應表
const statusOptions = [
  { label: "首次申請", value: "pending" },
  { label: "補件申請", value: "repending" },
  { label: "退回補件", value: "rechecked" },
];

// 狀態文字動態顯示
const statusLabel = computed(() => {
  const found = statusOptions.find((opt) => opt.value === selectedStatus.value);
  return found ? found.label : "";
});

const pageSize = 5;
// 第一個表格的分頁邏輯（審核中的店家）
const currentPage1 = ref(1);
// 第二個表格的分頁邏輯（營運中的店家）
const currentPage2 = ref(1);

// 篩選狀態
const selectedStatus = ref("pending");

// 日期篩選條件
const selectedStartDate = ref("");
const selectedEndDate = ref("");

// 日期驗證
const dateValidationError = ref("");

// 驗證日期區間
const validateDateRange = () => {
  if (selectedStartDate.value && selectedEndDate.value) {
    const startDate = new Date(selectedStartDate.value);
    const endDate = new Date(selectedEndDate.value);
    
    if (startDate > endDate) {
      dateValidationError.value = "結束日期不能早於開始日期";
      return false;
    }
  }
  dateValidationError.value = "";
  return true;
};

// 根據狀態篩選店家
const pendingStores = computed(() => {
  return stores.value.filter(
    (store) => store.status?.trim() === selectedStatus.value
  );
});

const operatingStores = computed(() => {
  return stores.value.filter((store) => {
    // 狀態篩選
    const statusMatch = store.status?.trim() === "confirmed";
    
    // 先驗證日期範圍
    if (!validateDateRange()) {
      return statusMatch;
    }
    
    // 日期區間篩選
    let dateMatch = true;
    if (selectedStartDate.value || selectedEndDate.value) {
      const storeDate = new Date(store.created_at || store.registerDate);
      
      if (selectedStartDate.value) {
        const startDate = new Date(selectedStartDate.value);
        dateMatch = dateMatch && storeDate >= startDate;
      }
      
      if (selectedEndDate.value) {
        const endDate = new Date(selectedEndDate.value);
        endDate.setHours(23, 59, 59, 999);
        dateMatch = dateMatch && storeDate <= endDate;
      }
    }
    
    return statusMatch && dateMatch;
  });
});

// 清空日期篩選
const clearDateFilter = () => {
  selectedStartDate.value = "";
  selectedEndDate.value = "";
  dateValidationError.value = "";
};

// 第一個表格的分頁邏輯（審核中的店家）
const totalPages1 = computed(() =>
  Math.ceil(pendingStores.value.length / pageSize)
);
const paginatedPendingStores = computed(() => {
  const start = (currentPage1.value - 1) * pageSize;
  return pendingStores.value.slice(start, start + pageSize);
});

// 第二個表格的分頁邏輯（營運中的店家）
const totalPages2 = computed(() =>
  Math.ceil(operatingStores.value.length / pageSize)
);
const paginatedOperatingStores = computed(() => {
  const start = (currentPage2.value - 1) * pageSize;
  return operatingStores.value.slice(start, start + pageSize);
});

// 分頁處理函數
const handlePageChange1 = (page) => {
  currentPage1.value = page;
};

const handlePageChange2 = (page) => {
  currentPage2.value = page;
};

// 監聽日期篩選條件變更
watch([selectedStartDate, selectedEndDate], () => {
  currentPage2.value = 1; // 重置到第一頁
});
</script>

<template>
  <div class="storemanage-container">
    <h1 class="storemanage-title">店家帳號審核及管理</h1>
    <!-- 狀態切換按鈕 -->
    <div class="storemanage-filter-bar">
      <span class="storemanage-filter-label">{{ statusLabel }}店家列表</span>
      <div class="storemanage-filter-btns">
        <button
          v-for="opt in statusOptions"
          :key="opt.value"
          class="storemanage-filter-btn"
          :class="selectedStatus === opt.value ? 'active' : ''"
          @click="selectedStatus = opt.value"
        >
          {{ opt.label }}
        </button>
      </div>
    </div>

    <div class="storemanage-table-container">
      <Table>
        <template #header>
          <th>店家</th>
          <th>負責人</th>
          <th>聯絡電話</th>
          <th>店址</th>
          <th>服務項目</th>
          <th>註冊日期</th>
          <th>申請狀態</th>
          <th>操作</th>
        </template>
        <template #body>
          <tr
            v-for="store in paginatedPendingStores"
            :key="store.id"
            class="card-row"
          >
            <StoreCard :store="store" />
          </tr>
        </template>
      </Table>
      <Pagination
        :current-page="currentPage1"
        :total-pages="totalPages1"
        @page-change="handlePageChange1"
      />
    </div>
  </div>

  <div class="storemanage-container">
    <h1 class="storemanage-title">營運中</h1>
    
    <!-- 選擇日期區間 -->
    <div class="storemanage-filters">
      <label class="storemanage-filter-label">
        註冊日期：
        <input
          type="date"
          v-model="selectedStartDate"
          class="storemanage-filter-input"
          @change="validateDateRange"
        />
        ~
        <input
          type="date"
          v-model="selectedEndDate"
          class="storemanage-filter-input"
          @change="validateDateRange"
        />
      </label>
      <!-- 日期驗證錯誤訊息 -->
      <span v-if="dateValidationError" class="text-red-500 text-sm">
        {{ dateValidationError }}
      </span>
      <button 
        class="storemanage-filter-btn"
        @click="clearDateFilter"
        v-if="selectedStartDate || selectedEndDate"
      >
        清空篩選
      </button>
    </div>
    <div class="storemanage-table-container">
      <Table>
        <template #header>
          <th>店家</th>
          <th>負責人</th>
          <th>聯絡電話</th>
          <th>店址</th>
          <th>服務項目</th>
          <th>註冊日期</th>
          <th>申請狀態</th>
          <th>操作</th>
        </template>
        <template #body>
          <tr
            v-for="store in paginatedOperatingStores"
            :key="store.id"
            class="card-row"
          >
            <StoreCard :store="store" />
          </tr>
        </template>
      </Table>
      <Pagination
        :current-page="currentPage2"
        :total-pages="totalPages2"
        @page-change="handlePageChange2"
      />
    </div>
  </div>
</template>

<style scoped src="../../../styles/pages/Admin/Stores/storemanage.css"></style>
