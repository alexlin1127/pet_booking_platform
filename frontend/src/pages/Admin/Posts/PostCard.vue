<script setup>
import { RouterLink } from "vue-router";

defineProps({
  post: Object,
});
</script>

<template>
  <td>{{ post.id }}</td>
  <td>{{ post.store_name }}</td>
  <td>{{ post.created_at }}</td>
  <td>{{ post.title }}</td>
  <td>
    {{
      post.status === "pending"
        ? "待審核"
        : post.status === "rechecked"
        ? "退回補件"
        : post.status === "confirmed"
        ? "已審核"
        : "未知狀態"
    }}
  </td>
  <td v-if="post.status === 'pending'">
    <RouterLink
      :to="`/admin/posts/review?id=${post.id}&title=${encodeURIComponent(
        post.title
      )}&store_name=${encodeURIComponent(post.store_name)}`"
    >
      <button class="btn">查看並審核</button>
    </RouterLink>
  </td>
  <td v-else>
    <RouterLink
      :to="`/admin/posts/details?id=${post.id}&title=${encodeURIComponent(
        post.title
      )}&store_name=${encodeURIComponent(post.store_name)}`"
    >
      <button class="btn">店家詳情</button>
    </RouterLink>
  </td>
</template>

<style></style>
