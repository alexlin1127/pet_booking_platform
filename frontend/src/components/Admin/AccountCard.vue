<script setup>
defineProps({
  acc: Object
});
</script>

<template>
    <td>{{ acc.id }}</td>
    <td>{{ acc.type}}</td>
    <td>{{ acc.name }}</td>
    <td>{{ acc.account }}</td>
    <td>{{ acc.store }}</td>
    <td>{{ acc.status }}</td>
    <td>{{ acc.createdAt }}</td>
    <td class="btn-td">
      <button class="btn">重設密碼</button>
      <button class="btn">刪除</button>
    </td>
</template>

<style></style>