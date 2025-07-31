<script setup>
import { RouterLink } from 'vue-router';

defineProps({
  store: Object
});

</script>

<template>
  <td>{{ store.id }}</td>
  <td>{{ store.storeName }}</td>
  <td>{{ store.registerDate }}</td>
  <td>{{ store.region }}</td>
  <td>{{ store.owner }}</td>
  <td>{{ store.phone }}</td>
  <td>{{ store.status }}</td>
  <td v-if="store.status === '待審核'">
    <RouterLink :to="`/Admin/Store/review?id=${store.id}&name=${store.storeName}`">
      <button class="btn">審核</button>
    </RouterLink>
  </td>
  <td v-else>
    <RouterLink :to="`/Admin/Store/details?id=${store.id}&name=${store.storeName}`">
      <button class="btn">店家詳情</button>
    </RouterLink>
  </td>
</template>

<style></style>