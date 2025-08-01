<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: Number,
  totalPages: Number
})

defineEmits(['page-change'])

const visiblePages = computed(() => {
  // 總是顯示3個頁碼
  if (props.totalPages <= 3) {
    // 如果總頁數不超過3頁，顯示全部
    const pages = []
    for (let i = 1; i <= props.totalPages; i++) {
      pages.push(i)
    }
    return pages
  }
  
  let start, end
  if (props.currentPage <= 2) {
    // 在前面時顯示 1,2,3
    start = 1
    end = 3
  } else if (props.currentPage >= props.totalPages - 1) {
    // 在後面時顯示最後3頁
    start = props.totalPages - 2
    end = props.totalPages
  } else {
    // 在中間時顯示當前頁前後各1頁
    start = props.currentPage - 1
    end = props.currentPage + 1
  }
  
  const pages = []
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})
</script>

<template>
  <div class="pagination-container">
    <button @click="$emit('page-change', 1)" :disabled="currentPage === 1" 
            class="pagination-btn">
      至最前
    </button>
    <button @click="$emit('page-change', currentPage - 1)" :disabled="currentPage === 1"
            class="pagination-btn">
      上一頁
    </button>
    
    <button v-for="page in visiblePages" :key="page"
            @click="$emit('page-change', page)"
            :class="['pagination-btn', page === currentPage ? 'pagination-btn-active' : '']">
      {{ page }}
    </button>
    
    <button @click="$emit('page-change', currentPage + 1)" :disabled="currentPage === totalPages"
            class="pagination-btn">
      下一頁
    </button>
    <button @click="$emit('page-change', totalPages)" :disabled="currentPage === totalPages"
            class="pagination-btn">
      至最後
    </button>
  </div>
</template>