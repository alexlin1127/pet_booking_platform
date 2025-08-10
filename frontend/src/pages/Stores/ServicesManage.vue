<script setup>
import Card from '@/components/UI/Card.vue'
import { services } from '@/data/service.js'

const onEdit = (id) => console.log('edit', id)
const onDelete = (id) => console.log('delete', id)
</script>

<template>
  <div class="service-page">
    <div class="service-header">
      <h1 class="service-title-page">服務項目管理</h1>
      <button class="svc-btn svc-btn-primary">新增服務</button>
    </div>

    <section class="space-y-10">
      <Card
        v-for="s in services"
        :key="s.id"
        type="vertical"
        :hasButton="true"               
        :clickable="false"              
        class="service-card"            
      >
        <template #title>
          <h3 class="service-item-title">
            {{ s.title }} <span class="service-price">NT${{ s.price }}</span>
          </h3>
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
