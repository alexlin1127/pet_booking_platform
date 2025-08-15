<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import Table from "../../../components/UI/Table.vue";
import AccountCard from "./AccountCard.vue";
import Pagination from "../../../components/common/Pagination.vue";
import api from "../../../api/api.js";

// ==================== 路由和分頁設置 ====================
const route = useRoute();
const router = useRouter();
const pageSize = 5;
const currentPage = ref(parseInt(route.params.page) || 1);

// ==================== 資料狀態 ====================
const accounts = ref([]);
const profile = ref([]);

// ==================== 篩選條件 ====================
const selectedStartDate = ref("");
const selectedEndDate = ref("");
const selectedType = ref("");
const dateValidationError = ref("");

// ==================== 日期驗證 ====================
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

// ==================== 資料處理 ====================

// ==================== 資料處理 ====================
// 合併 accounts 和 profile 資料
const mergedAccounts = computed(() => {
  return accounts.value.map((acc) => {
    const profileData = profile.value.find((p) => p.user_id === acc.user_id) || {};
    return {
      id: acc.id,
      user_id: acc.user_id,
      full_name: profileData.full_name || "未知",
      username: acc.username,
      role: acc.role,
      isActive: acc.is_active,
      createdAt: acc.created_at,
    };
  });
});

// ==================== 篩選邏輯 ====================

// ==================== 篩選邏輯 ====================
const filteredAccounts = computed(() => {
  // 先驗證日期範圍
  if (!validateDateRange()) {
    return mergedAccounts.value.filter((acc) => {
      const typeMatch = !selectedType.value || acc.role === selectedType.value;
      return typeMatch;
    });
  }

  return mergedAccounts.value.filter((acc) => {
    // 日期區間篩選
    const accountDate = new Date(acc.createdAt);
    let dateMatch = true;
    
    if (selectedStartDate.value) {
      const startDate = new Date(selectedStartDate.value);
      dateMatch = dateMatch && accountDate >= startDate;
    }
    
    if (selectedEndDate.value) {
      const endDate = new Date(selectedEndDate.value);
      endDate.setHours(23, 59, 59, 999);
      dateMatch = dateMatch && accountDate <= endDate;
    }
    
    const typeMatch = !selectedType.value || acc.role === selectedType.value;
    return dateMatch && typeMatch;
  });
});

// ==================== 篩選操作 ====================
const clearAllFilters = () => {
  selectedStartDate.value = "";
  selectedEndDate.value = "";
  selectedType.value = "";
  dateValidationError.value = "";
};

// ==================== 分頁邏輯 ====================

// ==================== 分頁邏輯 ====================
const totalPages = computed(() => Math.ceil(filteredAccounts.value.length / pageSize));

const paginatedAccounts = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredAccounts.value.slice(start, start + pageSize);
});

const handlePageChange = (page) => {
  currentPage.value = page;
  router.push(`/admin/accounts/${page}`);
};

// ==================== 監聽器 ====================
watch([selectedStartDate, selectedEndDate, selectedType], () => {
  currentPage.value = 1;
  router.push("/admin/accounts/1");
});

// ==================== API 呼叫 ====================

// ==================== API 呼叫 ====================
const getAccounts = async () => {
  try {
    const res = await api.get("users");
    accounts.value = Array.isArray(res.data) ? res.data : [];
    console.log("Accounts data:", accounts.value);
  } catch (error) {
    console.error("Error fetching accounts:", error);
  }
};

const getProfile = async () => {
  try {
    const res = await api.get("customer/profiles");
    profile.value = Array.isArray(res.data) ? res.data : [];
    console.log("Profile data:", profile.value);
  } catch (error) {
    console.error("Error fetching profile:", error);
  }
};

// ==================== 事件處理 ====================
const handleStatusChanged = (userId, newStatus) => {
  const accountIndex = accounts.value.findIndex(acc => acc.id === userId);
  if (accountIndex !== -1) {
    accounts.value[accountIndex].is_active = newStatus;
  }
  console.log(`帳號 ${userId} 狀態已更新為: ${newStatus ? '啟用' : '停用'}`);
};

// ==================== 生命週期 ====================

onMounted(() => {
  getAccounts();
  getProfile();
});
</script>

<template>
  <div class="accmanage-container">
    <h1 class="accmanage-title">帳號管理</h1>

    <div class="accmanage-filters">
      <!-- 選擇帳號類型 -->
      <label class="accmanage-filter-label">
        帳號類型：
        <select v-model="selectedType" class="accmanage-filter-input">
          <option value="">全部</option>
          <option value="admin">管理員</option>
          <option value="store">店家</option>
          <option value="member">一般用戶</option>
        </select>
      </label>
      <!-- 選擇日期區間 -->
      <label class="accmanage-filter-label">
        建立日期：
        <input
          type="date"
          v-model="selectedStartDate"
          class="accmanage-filter-input"
          @change="validateDateRange"
        />
        ~
        <input
          type="date"
          v-model="selectedEndDate"
          class="accmanage-filter-input"
          @change="validateDateRange"
        />
      </label>
      <!-- 日期驗證錯誤訊息 -->
      <span v-if="dateValidationError" class="text-red-500 text-sm">
        {{ dateValidationError }}
      </span>
      <!-- 清空篩選按鈕 -->
      <button 
        v-if="selectedStartDate || selectedEndDate || selectedType"
        @click="clearAllFilters"
        class="accmanage-filter-btn"
      >
        清空篩選
      </button>
    </div>

    <div class="accmanage-table-container">
      <Table>
        <template #header>
          <th>編號</th>
          <th>名字</th>
          <th>帳號</th>
          <th>帳號類型</th>
          <th>帳號狀態</th>
          <th>建立日期</th>
          <th>操作</th>
        </template>
        <template #body>
          <tr
            v-for="acc in paginatedAccounts"
            :key="acc.user_id"
            class="card-row"
          >
            <AccountCard :account="acc" @statusChanged="handleStatusChanged" />
          </tr>
        </template>
      </Table>

      <Pagination
        :current-page="currentPage"
        :total-pages="totalPages"
        @page-change="handlePageChange" 
      />
    </div>
  </div>
</template>

<style scoped src="../../../styles/pages/Admin/Accounts/manage.css"></style>
