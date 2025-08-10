<script setup>
import { ref, computed } from 'vue'
import Card from '@/components/UI/Card.vue'
import Switch from '@/components/UI/Switch.vue'
import { services } from '@/data/service.js'

// 頁首：true=美容, false=住宿
const isGrooming = ref(true)

// 下拉篩選選項
const tagOptions = ['全部', '短毛', '長毛', '犬', '貓'] // 依你的資料調整
const selectedTag = ref('全部')

// 操作事件
const onEdit   = id => console.log('edit', id)
const onDelete = id => console.log('delete', id)

// 過濾服務清單
const filteredServices = computed(() => {
  const type = isGrooming.value ? 'boarding' : 'grooming' // 依資料實際欄位修改
  return services
    .filter(s => s.type === type)
    .filter(s => selectedTag.value === '全部' ? true : s.tags?.includes(selectedTag.value))
})
</script>

<template>
  <div class="service-page">
    <div class="service-header">
      <h1 class="service-title-page">服務項目管理</h1>
      <button class="svc-btn svc-btn-primary">新增服務</button>
    </div>
    <!-- 美容 / 住宿 切換 -->
      <div class="flex items-center">
        <span class="mr-2 text-sm">美容</span>
        <Switch v-model="isGrooming" size="md" />
        <span class="ml-2 text-sm">住宿</span>
      <!-- 篩選服務 下拉 -->
      <span class="ml-2 text-sm py-2">篩選服務</span>
      <select
        v-model="selectedTag"  class="select-filter ml-4">
        <option v-for="opt in tagOptions"  :key="opt" :value="opt">{{ opt }}</option>
      </select>
      </div>

      <!-- 篩選服務 下拉
      <select
        v-model="selectedTag"
        class="border border-[#d8c9b8] rounded px-2 py-1 text-sm bg-white"
      >
        <option v-for="opt in tagOptions"  :key="tag" :value="tag">{{ tag }}</option>
      </select> -->
    

    <section class="space-y-10">
      <Card
        v-for="s in filteredServices"
        :key="s.id"
        type="vertical"
        :hasButton="true"
        :clickable="false"
        class="service-card"
      >
        <!-- 不要 icon：若卡片本身會渲染空容器，就用 CSS 隱藏；或保留此具名 slot 覆蓋 -->
        <template #icon><template v-if="false" /></template>

        <template #title>
          <div class="flex items-center justify-between">
            <h3 class="service-item-title">
              {{ s.title }} <span class="service-price">NT${{ s.price }}</span>
            </h3>
          </div>
        </template>

        <template #content>
          <p class="service-desc">{{ s.description }}</p>

          <ul class="service-bullets">
            <li v-for="b in s.bullets" :key="b">{{ b }}</li>
          </ul>

          <div class="service-meta">
            <div class="service-duration">施作時間：{{ s.duration }}</div>
            <div class="service-tags">
              <span v-for="t in s.tags" :key="t" class="service-tag">{{ t }}</span>
            </div>
          </div>
        </template>

        <template #button>
          <div class="service-actions">
            <button class="svc-btn svc-btn-outline" @click="onDelete(s.id)">刪除服務</button>
            <button class="svc-btn svc-btn-solid" @click="onEdit(s.id)">修改內容</button>
          </div>
        </template>
      </Card>
    </section>
  </div>
</template>
