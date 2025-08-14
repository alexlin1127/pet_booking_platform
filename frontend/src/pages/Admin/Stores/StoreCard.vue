<script setup>
import { RouterLink } from "vue-router";

defineProps({
  store: Object,
});
</script>

<template>
  <td>{{ store.store_name }}</td>
  <td>{{ store.owner_name }}</td>
  <td>{{ store.phone }}</td>
  <td>
    {{ store.address.county }}{{ store.address.district
    }}{{ store.address.detail }}
  </td>
  <td>
    <ul>
      <li v-for="item in store.service_item" :key="item">{{ item }}</li>
    </ul>
  </td>
  <td>{{ new Date(store.created_at).toLocaleDateString() }}</td>
  <td>
    {{
      store.status === "pending"
        ? "待審核"
        : store.status === "confirmed"
        ? "已審核"
        : store.status
    }}
  </td>
  <td>
    <RouterLink :to="`/admin/stores/details/${store.id}`">
      <button class="btn">查看詳情</button>
    </RouterLink>
  </td>
</template>

<style></style>
