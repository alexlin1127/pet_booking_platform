<script setup>
import { ref } from "vue";
import api from "../../../api/api.js";
defineProps({
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
    const res = await api.patch(`users/${account.id}`, {
      is_active: !account.isActive,
    });
    if (res.status === 200) {
      emit("statusChanged");
    }
  } catch (error) {
    console.error("Error toggling status:", error);
  }
};
</script>

<template>
  <td>{{ account.user_id }}</td>
  <td>{{ account.full_name }}</td>
  <td>{{ account.username }}</td>
  <td>
    <span v-if="account.role === 'admin'">管理員</span>
    <span v-else-if="account.role === 'store'">店家</span>
    <span v-else-if="account.role === 'member'">一般用戶</span>
    <span v-else>未知角色</span>
  </td>
  <td>{{ account.isActive ? "啟用" : "停用" }}</td>
  <td>{{ new Date(account.createdAt).toLocaleDateString() }}</td>
  <td class="btn-td">
    <button class="acc-btn acc-btn-solid" @click="openResetModal">
      重設密碼
    </button>
    <button class="acc-btn acc-btn-outline" @click="toggleStatus">
      {{ account.isActive ? "停用" : "啟用" }}
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
          <span class="acc-modal-value">{{ account.user_id }}</span>
        </div>
        <div class="acc-modal-row">
          <span class="acc-modal-label">名字</span>
          <span class="acc-modal-value">{{ account.full_name }}</span>
        </div>
        <div class="acc-modal-row">
          <span class="acc-modal-label">帳號</span>
          <span class="acc-modal-value">{{ account.username }}</span>
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
