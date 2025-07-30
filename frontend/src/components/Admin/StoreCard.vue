<script setup>
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
    <td>
      <button class="btn">審核</button>
    </td>
</template>

<style></style>