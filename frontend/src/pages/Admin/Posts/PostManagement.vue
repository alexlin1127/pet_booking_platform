<script setup>
import { ref, computed, onMounted, watch } from "vue";
import Table from "../../../components/UI/Table.vue";
import PostCard from "./PostCard.vue";
import Pagination from "../../../components/common/Pagination.vue";
import api from "../../../api/api.js";

const pageSize = 5; // 每頁顯示5個

// 第一個表格的分頁邏輯（審核中的貼文）
const currentPage1 = ref(1);

// 第二個表格的分頁邏輯（營運中的貼文）
const currentPage2 = ref(1);

// 篩選狀態
const selectedStatus = ref("pending");

const posts = ref([]); // 初始化為空陣列
const getPosts = async () => {
  try {
    const res = await api.get("admin/posts");
    posts.value = Array.isArray(res.data) ? res.data : [];
    console.log(res.data); // 調試 API 響應
  } catch (err) {
    alert("無法取得貼文資料");
    posts.value = []; // 確保失敗時為空陣列
  }
};

onMounted(() => {
  getPosts();
});

// 根據狀態篩選貼文
const pendingPosts = computed(() => {
  return posts.value.filter((post) => post.status === selectedStatus.value);
});

const approvedPosts = computed(() => {
  return posts.value.filter((post) => post.status === "confirmed");
});

// 篩選按鈕處理函數
const filterByStatus = (status) => {
  selectedStatus.value = status;
  currentPage1.value = 1; // 重置到第一頁
};

// 第一個表格的分頁邏輯（待審核的貼文）
const totalPages1 = computed(
  () => Math.ceil(pendingPosts.value.length / pageSize) || 1
);
const paginatedPendingPosts = computed(() => {
  const start = (currentPage1.value - 1) * pageSize;
  return pendingPosts.value.slice(start, start + pageSize);
});

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

// 篩選邏輯
const filteredApprovedPosts = computed(() => {
  // 先驗證日期範圍
  if (!validateDateRange()) {
    return approvedPosts.value;
  }

  return approvedPosts.value.filter((post) => {
    const postDate = new Date(post.created_at);
    let dateMatch = true;
    
    if (selectedStartDate.value) {
      const startDate = new Date(selectedStartDate.value);
      dateMatch = dateMatch && postDate >= startDate;
    }
    
    if (selectedEndDate.value) {
      const endDate = new Date(selectedEndDate.value);
      endDate.setHours(23, 59, 59, 999);
      dateMatch = dateMatch && postDate <= endDate;
    }
    
    return dateMatch;
  });
});

// 清空篩選
const clearDateFilter = () => {
  selectedStartDate.value = "";
  selectedEndDate.value = "";
  dateValidationError.value = "";
};

// 分頁邏輯
const totalPages2 = computed(
  () => Math.ceil(filteredApprovedPosts.value.length / pageSize) || 1
);
const paginatedApprovedPosts = computed(() => {
  const start = (currentPage2.value - 1) * pageSize;
  return filteredApprovedPosts.value.slice(start, start + pageSize);
});

// 分頁處理函數
const handlePageChange1 = (page) => {
  currentPage1.value = page;
};

const handlePageChange2 = (page) => {
  currentPage2.value = page;
};

// 監聽篩選條件變更
watch([selectedStartDate, selectedEndDate], () => {
  currentPage2.value = 1; // 重置到第一頁
});
</script>

<template>
  <div class="postmanage-container">
    <h1 class="postmanage-title">貼文管理</h1>

    <div class="postmanage-filter">
      <div class="postmanage-filter-label">
        <p>
          {{
            selectedStatus === "pending"
              ? "待審核貼文列表"
              : "退回補件貼文列表"
          }}
        </p>
      </div>

      <button
        class="postmanage-filter-btn"
        :class="{ active: selectedStatus === 'pending' }"
        @click="filterByStatus('pending')"
      >
        待審核
      </button>
      <button
        class="postmanage-filter-btn"
        :class="{ active: selectedStatus === 'rechecked' }"
        @click="filterByStatus('rechecked')"
      >
        退回補件
      </button>
    </div>

    <div class="postmanage-table-container">
      <Table>
        <template #header>
          <th>貼文ID</th>
          <th>店家名稱</th>
          <th>發布日期</th>
          <th>標題</th>
          <th>審核狀況</th>
          <th>操作</th>
        </template>
        <template #body>
          <tr
            v-for="post in paginatedPendingPosts"
            :key="post.id"
            class="card-row"
          >
            <PostCard :post="post" />
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

  <div class="postmanage-container">
    <h1 class="postmanage-title">已通過貼文</h1>

    <!-- 選擇日期區間 -->
    <div class="postmanage-filters">
      <label class="postmanage-filter-label">
        發布日期：
        <input
          type="date"
          v-model="selectedStartDate"
          class="postmanage-filter-input"
          @change="validateDateRange"
        />
        ~
        <input
          type="date"
          v-model="selectedEndDate"
          class="postmanage-filter-input"
          @change="validateDateRange"
        />
      </label>
      <!-- 日期驗證錯誤訊息 -->
      <span v-if="dateValidationError" class="text-red-500 text-sm">
        {{ dateValidationError }}
      </span>
      <button 
        class="postmanage-filter-btn"
        @click="clearDateFilter"
        v-if="selectedStartDate || selectedEndDate"
      >
        清空篩選
      </button>
    </div>

    <div class="postmanage-table-container">
      <Table>
        <template #header>
          <th>貼文ID</th>
          <th>店家名稱</th>
          <th>發布日期</th>
          <th>標題</th>
          <th>審核狀況</th>
          <th>操作</th>
        </template>
        <template #body>
          <tr
            v-for="post in paginatedApprovedPosts"
            :key="post.id"
            class="card-row"
          >
            <PostCard :post="post" />
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

<style scoped src="../../../styles/pages/Admin/Posts/postmanage.css"></style>
