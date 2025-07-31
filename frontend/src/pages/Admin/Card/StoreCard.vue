<script setup>
import { RouterLink } from 'vue-router';

defineProps({
  store: Object
});

</script>

<template>
  <td>{{ store.storeName }}</td>
  <td>{{ store.owner }}</td>
  <td>{{ store.phone }}</td>
  <td>{{ store.address }}</td>
  <td v-if="store.applystatus !=='已通過'">
    {{ store.services }}
  </td>
  <td v-else>
    {{ store.storestatus }}
  </td>
  <td>{{ store.registerDate }}</td>
  <td v-if="store.applystatus !=='已通過'">
    {{ store.applystatus }}
  </td>
  <td v-if="store.applystatus === '首次申請'">
    <RouterLink :to="`/admin/store/review?id=${store.id}&name=${store.storeName}`">
      <button class="btn">審核</button>
    </RouterLink>
  </td>
  <td v-else-if="store.applystatus === '補件申請'">
    <RouterLink :to="`/admin/store/review?id=${store.id}&name=${store.storeName}`">
      <button class="btn">重新審核</button>
    </RouterLink>
  </td>
  <td v-else>
    <RouterLink :to="`/admin/store/details?id=${store.id}&name=${store.storeName}`">
      <button class="btn">店家詳情</button>
    </RouterLink>
  </td>
</template>

<style></style>