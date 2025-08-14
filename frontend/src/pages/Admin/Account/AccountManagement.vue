<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import Table from "../../../components/UI/Table.vue";
import AccountCard from "./AccountCard.vue";
import Pagination from "../../../components/common/Pagination.vue";
import api from "../../../api/api.js";

const route = useRoute();
const router = useRouter();

const pageSize = 5;
const currentPage = ref(parseInt(route.params.page) || 1);

const accounts = ref([]);
const profile = ref([]);

// 篩選條件
const selectedDate = ref("");
const selectedType = ref("");

// 合併 accounts 和 profile 資料
const mergedAccounts = computed(() => {
  return accounts.value.map((acc) => {
    const profileData =
      profile.value.find((p) => p.user_id === acc.user_id) || {};
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

// 篩選邏輯
const filteredAccounts = computed(() => {
  return mergedAccounts.value.filter((acc) => {
    const dateMatch =
      !selectedDate.value || acc.createdAt.startsWith(selectedDate.value);
    const typeMatch = !selectedType.value || acc.role === selectedType.value;
    return dateMatch && typeMatch;
  });
});

// 分頁邏輯
const totalPages = computed(() =>
  Math.ceil(filteredAccounts.value.length / pageSize)
);
const paginatedAccounts = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredAccounts.value.slice(start, start + pageSize);
});

const handlePageChange = (page) => {
  currentPage.value = page;
  router.push(`/admin/accounts/${page}`);
};

// 當篩選條件變更時，重置到第一頁
watch([selectedDate, selectedType], () => {
  currentPage.value = 1;
  router.push("/admin/accounts/1");
});

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

// 處理狀態變更事件
const handleStatusChanged = (userId, newStatus) => {
  // 更新 accounts 資料中的對應項目
  const accountIndex = accounts.value.findIndex(acc => acc.id === userId);
  if (accountIndex !== -1) {
    accounts.value[accountIndex].is_active = newStatus;
  }
  console.log(`帳號 ${userId} 狀態已更新為: ${newStatus ? '啟用' : '停用'}`);
};

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
      <!-- 選擇日期 -->
      <label class="accmanage-filter-label">
        建立日期：
        <input
          type="date"
          v-model="selectedDate"
          class="accmanage-filter-input"
        />
        ~
        <input
          type="date"
          v-model="selectedDate"
          class="accmanage-filter-input"
        />
      </label>
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
