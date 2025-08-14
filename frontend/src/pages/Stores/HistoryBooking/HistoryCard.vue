<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import { bookings } from '../../../data/bookingfakedata'
import ModalBox from '../../../components/UI/ModalBox.vue'

const props = defineProps({
    history: Object
});

const showWatchListModal = ref(false)

function openWatchListModal() {
    showWatchListModal.value = true
}

function closeWatchListModal() {
    showWatchListModal.value = false
}

function confirmAddToWatchList() {
    const idx = bookings.findIndex(b => b.id === props.history.id)
    if (idx !== -1) {
        bookings[idx] = { ...bookings[idx], blacklist: true }
    }
    showWatchListModal.value = false
}

function addToWatchList() {
    openWatchListModal()
}
</script>

<template>
    <td>{{ history.id }}</td>
    <td>{{ history.customer_name }}</td>
    <td>{{ history.phone }}</td>
    <td>{{ history.pet_name }}</td>
    <td>{{ history.pet_type }}</td>
    <td>{{ history.booking_date }}</td>
    <td>{{ history.service_type }}</td>
    <td>{{ history.status }}</td>
    <td v-if="history.status === '已完成'">
        <RouterLink :to="`/stores/bookingshistory/details?id=${history.id}`">
            <button class="history-btn">訂單詳情</button>
        </RouterLink>
        <button class="history-btn">備註</button>
        <button class="history-btn" :disabled="history.blacklist === true" @click="addToWatchList">
            {{ history.blacklist === true ? '已列入觀察' : '列入觀察' }}
        </button>
    </td>

    <!-- 列入觀察確認 Modal -->
    <ModalBox
        :visible="showWatchListModal"
        title="確認列入觀察名單"
        :buttons="[
            { text: '取消', action: 'cancel', variant: 'cancel', class: 'history-modal-btn-cancel' },
            { text: '確認列入', action: 'confirm', variant: 'primary', class: 'history-modal-btn-confirm' }
        ]"
        @close="closeWatchListModal"
        @button-click="(action) => {
            if (action === 'cancel') closeWatchListModal()
            if (action === 'confirm') confirmAddToWatchList()
        }"
        width="max-w-md"
    >
        <template #default>
            <div class="history-modal-content">
                <p class="history-modal-text">確定要將此訂單列入觀察名單嗎？</p>
                <div class="history-modal-details">
                    <p><strong>訂單編號：</strong>{{ history.id }}</p>
                    <p><strong>客戶姓名：</strong>{{ history.customer_name }}</p>
                    <p><strong>寵物姓名：</strong>{{ history.pet_name }}</p>
                    <p><strong>服務類型：</strong>{{ history.service_type }}</p>
                </div>
            </div>
        </template>
    </ModalBox>
</template>

<style>
.history-modal-content {
    padding: 16px 0;
}

.history-modal-text {
    margin-bottom: 16px;
    font-size: 16px;
    color: #374151;
}

.history-modal-details {
    background-color: #f9fafb;
    padding: 12px;
    border-radius: 8px;
    border-left: 4px solid #3b82f6;
}

.history-modal-details p {
    margin: 4px 0;
    font-size: 14px;
    color: #6b7280;
}

.history-modal-details strong {
    color: #374151;
}

.history-modal-btn-cancel {
    background-color: #f3f4f6;
    color: #374151;
    border: 1px solid #d1d5db;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
}

.history-modal-btn-cancel:hover {
    background-color: #e5e7eb;
}

.history-modal-btn-confirm {
    background-color: #3b82f6;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
}

.history-modal-btn-confirm:hover {
    background-color: #2563eb;
}
</style>