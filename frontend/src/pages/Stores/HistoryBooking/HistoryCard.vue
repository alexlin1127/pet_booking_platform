<script setup>
import { RouterLink } from 'vue-router';

defineProps({
    history: Object
});
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
        <button class="history-btn">列入觀察</button>
    </td>
</template>

<style></style>