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
    <span v-if="store.grooming_service">美容</span>
    <span v-if="store.grooming_service && store.boarding_service"> / </span>
    <span v-if="store.boarding_service">住宿</span>
  </td>
  <td>{{ new Date(store.created_at).toLocaleDateString() }}</td>
  <td>
    {{
      store.status === "pending"
        ? "首次申請"
        : store.status === "repending"
          ? "補件申請"
          : store.status === "rechecked"
            ? "退回補件"
            : store.status === "confirmed"
              ? "營業中"
              : store.status
    }}
  </td>
  <td>
    <RouterLink :to="`/admin/stores/details/${store.id}`">
      <button class="storecard-btn">
        {{
          store.status === "pending"
            ? "查看並審核"
            : store.status === "repending"
              ? "重新審核"
              : store.status === "rechecked"
                ? "查看詳情"
                : store.status === "confirmed"
                  ? "查看"
                  : "查看"
        }}
      </button>
    </RouterLink>
  </td>
</template>

<style scoped src="../../../styles/pages/Admin/Stores/card.css"></style>
