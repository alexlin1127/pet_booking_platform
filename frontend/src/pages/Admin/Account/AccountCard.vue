<script setup>
import { ref } from 'vue';
defineProps({
  acc: Object
});

const showResetModal = ref(false);
const newPassword = ref('');

function openResetModal() {
  showResetModal.value = true;
}
function closeResetModal() {
  showResetModal.value = false;
  newPassword.value = '';
}
function confirmReset() {
  // 這裡可串 API
  alert('新密碼：' + newPassword.value);
  closeResetModal();
}
function toggleStatus() {
  // 串接 API: 切換 acc.status
  // 例如 axios.post('/api/account/toggle', { id: acc.id })
  // 實際串接後可根據回傳結果更新 acc.status
}
</script>


<template>
  <td>{{ acc.id }}</td>
  <td>{{ acc.name }}</td>
  <td>{{ acc.account }}</td>
  <td>{{ acc.type }}</td>
  <td>{{ acc.status }}</td>
  <td>{{ acc.createdAt }}</td>
  <td class="btn-td">
    <button class="acc-btn acc-btn-solid" @click="openResetModal">重設密碼</button>
    <button class="acc-btn acc-btn-outline" @click="toggleStatus">{{ acc.status === '啟用' ? '停用' : '啟用' }}</button>

    <!-- 重設密碼 Modal -->
    <div v-if="showResetModal" class="acc-modal-mask">
      <div class="acc-modal-box">
        <div class="acc-modal-title">重設密碼</div>
        <div class="acc-modal-row">
          <span class="acc-modal-label">編號</span>
          <span class="acc-modal-value">{{ acc.id }}</span>
        </div>
        <div class="acc-modal-row">
          <span class="acc-modal-label">店家名稱</span>
          <span class="acc-modal-value">{{ acc.store }}</span>
        </div>
        <div class="acc-modal-row">
          <span class="acc-modal-label">名字</span>
          <span class="acc-modal-value">{{ acc.name }}</span>
        </div>
        <div class="acc-modal-row">
          <span class="acc-modal-label">帳號</span>
          <span class="acc-modal-value">{{ acc.account }}</span>
        </div>
        <div class="acc-modal-row">
          <span class="acc-modal-label">密碼</span>
          <input v-model="newPassword" type="text" class="acc-modal-input" placeholder="請輸入新密碼" />
        </div>
        <div class="acc-modal-btns">
          <button @click="closeResetModal" class="acc-modal-btn-outline">取消</button>
          <button @click="confirmReset" class="acc-modal-btn">確認</button>
        </div>
      </div>
    </div>
  </td>
</template>

<style scoped src="../../../styles/pages/Admin/Accounts/card.css"></style>