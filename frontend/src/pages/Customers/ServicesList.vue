<script setup>
import { ref, computed } from 'vue'
import '@/styles/pages/Stores/service.css'
import { useRouter } from 'vue-router'
import Card from '@/components/UI/Card.vue'
import Switch from '@/components/UI/Switch.vue'
import { services as staticServices } from '@/data/service.js' //避免和響應式變數撞名

// 響應式服務清單（用假資料做副本，刪除時不會影響原檔）
const services = ref([...staticServices]) // ⬅️ 新增

// 頁首：true=美容, false=住宿
const isGrooming = ref(true)

// 下拉篩選選項
const tagOptions = ['全部', '短毛', '長毛', '犬', '貓'] // 依你的資料調整
const selectedTag = ref('全部')

const router = useRouter()


// 過濾服務清單
const filteredServices = computed(() => {
  const type = isGrooming.value ? 'grooming' : 'boarding' // 依資料實際欄位修改
  return (services.value ?? [])  //修正：要用 services.value
    .filter(s => s.type === type || (type === 'boarding' && s.type === 'lodging'))
    .filter(s => selectedTag.value === '全部' ? true : s.tags?.includes(selectedTag.value))
})
// 立即預約（未登入先註解；依 type 分流）
const order = (svc) => {
  const type = isGrooming.value ? 'grooming' : 'boarding'
  const path = type === 'grooming' ? '/booking/grooming' : '/booking/lodging'
 router.push({ path, query: { id: svc.id, from: 'services' } })
}



/* ⬇⬇⬇ 新增：把服務物件轉成 ModalBox 需要的 infoRows 二維陣列 ⬇⬇⬇ */
const buildInfoRows = (svc) => {
  if (!svc) return []
  const bullets = (svc.bullets ?? []).map(b => `• ${b}`).join('\n') // 用換行與項目符號
  const tags    = (svc.tags ?? []).join('、')
  return [
    ['項目', svc.title],
    ['價格', `NT$ ${svc.price}`],
    ['說明', svc.description],
    ['注意事項', bullets],
    ['服務時間', svc.duration],
    ['標籤', tags],
  ]
}
/* ⬆⬆⬆ 新增：把服務物件轉成 ModalBox 需要的 infoRows 二維陣列 ⬆⬆⬆ */
// 返回
const goBack = () => router.push('/news')




</script>

<template>
  <div class="service-page">
    <div class="service-header">
      <h1 class="service-title-page">服務項目</h1>
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
             <button class="svc-btn svc-btn-outline" @click="goBack">返回</button>
            <button class="svc-btn svc-btn-solid" @click="order(s)">立即預約</button>
          </div>
        </template>
      </Card>
    </section>
  </div>
</template>
