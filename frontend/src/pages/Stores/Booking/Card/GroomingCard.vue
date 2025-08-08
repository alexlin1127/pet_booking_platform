<script setup>
import { RouterLink } from 'vue-router';

defineProps({
    grooming: Object
});
</script>

<template>
    <td>
      <FontAwesomeIcon v-if="grooming.note && grooming.note.trim() !== ''" icon="fa-solid fa-bookmark" />
    </td>
    <td>{{ grooming.id }}</td>
    <td>{{ grooming.customer_name }}</td>
    <td>{{ grooming.phone }}</td>
    <td>{{ grooming.pet_name }}</td>
    <td>{{ grooming.pet_type }}</td>
    <td>{{ grooming.booking_date }}</td>
    <td>{{ grooming.booking_time }}</td>
    <td>{{ grooming.status }}</td>

    <td v-if="grooming.status === '待審核'">
        <RouterLink :to="`/stores/grooming-booking/review?id=${grooming.id}`">
            <button class="grooming-btn">審核</button>
        </RouterLink>
        <button class="grooming-btn">取消</button>
    </td>
    <td v-else-if="grooming.status === '已審核'">
        <RouterLink :to="`/stores/grooming-booking/review?id=${grooming.id}`">
            <button class="grooming-btn">詳情</button>
        </RouterLink>
        <button class="grooming-btn">取消</button>
        <button class="grooming-btn">已完成</button>
    </td>
    <td v-else>
        <RouterLink :to="`/stores/grooming-booking/details?id=${grooming.id}`">
            <button class="grooming-btn">訂單詳情</button>
        </RouterLink>
        <button class="grooming-btn">備註</button>
        <button class="grooming-btn">列入觀察</button>
    </td>
</template>

<style></style>