<script setup>
import { RouterLink } from 'vue-router';

defineProps({
    boarding: Object
});
</script>

<template>
     <td>
      <FontAwesomeIcon v-if="boarding.note && boarding.note.trim() !== ''" icon="fa-solid fa-bookmark" />
    </td>
    <td>{{ boarding.id }}</td>
    <td>{{ boarding.customer_name }}</td>
    <td>{{ boarding.phone }}</td>
    <td>{{ boarding.pet_name }}</td>
    <td>{{ boarding.pet_type }}</td>
    <td>{{ boarding.booking_date }}</td>
    <td>{{ boarding.room_type }}</td>
    <td>{{ boarding.status }}</td>
    <td v-if="boarding.status === '已審核'">
        <RouterLink :to="`/stores/boarding-booking/review?id=${boarding.id}`">
            <button class="boarding-btn">詳情</button>
        </RouterLink>
        <button class="boarding-btn">取消</button>
        <button class="boarding-btn">已完成</button>
    </td>
</template>

<style></style>