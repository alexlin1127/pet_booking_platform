<script setup>
import { ref, computed,onMounted} from "vue";
import Table from "../../../components/UI/Table.vue";
import StoreCard from "./StoreCard.vue";
import Pagination from "../../../components/common/Pagination.vue";
import api from "../../../api/api.js";

const stores = ref([]); // 初始化為空陣列

const storeData = async () => {
  try {
    const res = await api.get("admin/stores");
    console.log(res.data); // 調試 API 響應
    stores.value = Array.isArray(res.data.results) ? res.data.results : []; // 確保 results 為陣列
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
  { label: "退回補件", value: "rechecked" }
];
const selectedType = ref('pending');

// 狀態文字動態顯示
const statusLabel = computed(() => {
  const found = statusOptions.find(opt => opt.value === selectedType.value);
  return found ? found.label : "";
});


const pageSize = 5;
// 第一個表格的分頁邏輯（審核中的店家）
const currentPage1 = ref(1);
// 第二個表格的分頁邏輯（營運中的店家）
const currentPage2 = ref(1);

// 篩選狀態
const selectedStatus = ref("pending");

// 根據狀態篩選店家
const pendingStores = computed(() => {
  return stores.value.filter((store) => store.status === selectedStatus.value);
});

const operatingStores = computed(() => {
  return stores.value.filter((store) => store.status?.trim() === "confirmed");
});

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
          :class="selectedType === opt.value ? 'active' : ''"
          @click="selectedType = opt.value"
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
