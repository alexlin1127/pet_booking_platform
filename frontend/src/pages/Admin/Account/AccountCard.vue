<script setup>
import { ref } from "vue";
import api from "../../../api/api.js";

const props = defineProps({
  account: Object,
});

const emit = defineEmits(["statusChanged"]);

const showResetModal = ref(false);
const newPassword = ref("");

function openResetModal() {
  showResetModal.value = true;
}
function closeResetModal() {
  showResetModal.value = false;
  newPassword.value = "";
}
function confirmReset() {
  // 這裡可串 API
  alert("新密碼：" + newPassword.value);
  closeResetModal();
}
const toggleStatus = async () => {
  try {
    console.log("Toggling status for account:", props.account);
    console.log("Account ID:", props.account.id);
    console.log("Current isActive:", props.account.isActive);
    console.log("Will set is_active to:", !props.account.isActive);
    
    const res = await api.patch(`users/${props.account.id}`, {
      is_active: !props.account.isActive,
    });
    
    console.log("API response:", res);
    
    if (res.status === 200) {
      // 立即更新本地狀態
      props.account.isActive = !props.account.isActive;
      // 通知父組件狀態已變更
      emit("statusChanged", props.account.id, props.account.isActive);
    }
  } catch (error) {
    console.error("Error toggling status:", error);
    console.error("Error response:", error.response);
    console.error("Error status:", error.response?.status);
    console.error("Error data:", error.response?.data);
    alert(`狀態更新失敗：${error.response?.data?.detail || error.message}`);
  }
};
</script>

<template>
  <td>{{ props.account.user_id }}</td>
  <td>{{ props.account.full_name }}</td>
  <td>{{ props.account.username }}</td>
  <td>
    <span v-if="props.account.role === 'admin'">管理員</span>
    <span v-else-if="props.account.role === 'store'">店家</span>
    <span v-else-if="props.account.role === 'member'">一般用戶</span>
    <span v-else>未知角色</span>
  </td>
  <td>{{ props.account.isActive ? "啟用" : "停用" }}</td>
  <td>{{ new Date(props.account.createdAt).toLocaleDateString() }}</td>
  <td class="btn-td">
    <button class="acc-btn acc-btn-solid" @click="openResetModal">
      重設密碼
    </button>
    <button class="acc-btn acc-btn-outline" @click="toggleStatus">
      {{ props.account.isActive ? "停用" : "啟用" }}
    </button>
  </td>

  <Teleport to="body">
    <div
      v-if="showResetModal"
      class="acc-modal-mask"
      @click.self="closeResetModal"
    >
      <div class="acc-modal-box">
        <div class="acc-modal-title">重設密碼</div>
        <div class="acc-modal-row">
          <span class="acc-modal-label">編號</span>
          <span class="acc-modal-value">{{ props.account.user_id }}</span>
        </div>
        <div class="acc-modal-row">
          <span class="acc-modal-label">名字</span>
          <span class="acc-modal-value">{{ props.account.full_name }}</span>
        </div>
        <div class="acc-modal-row">
          <span class="acc-modal-label">帳號</span>
          <span class="acc-modal-value">{{ props.account.username }}</span>
        </div>
        <div class="acc-modal-row">
          <span class="acc-modal-label">密碼</span>
          <input
            v-model="newPassword"
            type="text"
            class="acc-modal-input"
            placeholder="請輸入新密碼"
          />
        </div>
        <div class="acc-modal-btns">
          <button @click="closeResetModal" class="acc-modal-btn-outline">
            取消
          </button>
          <button @click="confirmReset" class="acc-modal-btn">確認</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped src="../../../styles/pages/Admin/Accounts/card.css"></style>
