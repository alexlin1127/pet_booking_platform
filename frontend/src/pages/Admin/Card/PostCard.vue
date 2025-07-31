<script setup>
import { RouterLink } from 'vue-router';

defineProps({
  post:Object
});

</script>

<template>
  <td>{{ post.id }}</td>
  <td>{{ post.storeName }}</td>
  <td>{{ post.publishDate }}</td>
  <td>{{ post.title }}</td>
  <td>{{ post.status }}</td>
  <td v-if="post.status === '待審核'">
    <RouterLink :to="`/admin/post/review?id=${post.id}&title=${post.title}`">
      <button class="btn">查看並審核</button>
    </RouterLink>
  </td>
  <td v-else>
    <RouterLink :to="`/admin/post/details?id=${post.id}&title=${post.title}`">
      <button class="btn">店家詳情</button>
    </RouterLink>
  </td>
</template>

<style></style>