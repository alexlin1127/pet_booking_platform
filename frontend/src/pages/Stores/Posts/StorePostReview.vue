<!-- src/pages/Admin/PostReview.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ModalBox from '../../../components/UI/ModalBox.vue'
import { postreview } from '@/data/postreview.js'

const route = useRoute()
const router = useRouter()

const postId = ref('')
const title = ref('')
const content = ref([])
const imgSrc = ref(postreview.imgSrc)

const show = ref(false)
const infoRows = ref([])

/** 初始化：優先 /stores/Posts/PostReview/:id，其次相容 query */
onMounted(() => {
  const paramId = route.params.id
  if (paramId) postId.value = String(paramId)

  const q = route.query
  title.value = q?.title ? decodeURIComponent(q.title) : postreview.title

  if (q?.content) {
    try {
      const decoded = decodeURIComponent(q.content)
      content.value = JSON.parse(decoded)
    } catch {
      content.value = [decodeURIComponent(q.content)]
    }
  } else {
    content.value = postreview.content
  }

  imgSrc.value = q?.imgSrc || postreview.imgSrc
  const storeName = q?.storeName ? decodeURIComponent(q.storeName) : postreview.store
  infoRows.value = [
    ['編號', postId.value || postreview.id],
    ['店家名稱', storeName],
    ['標題', title.value]
  ]
})

/** 駁回彈窗按鈕事件 */
const handleButtonClick = (event) => {
  if (event.action === 'cancel') {
    show.value = false
    return
  }
  if (event.action === 'confirm') {
    const reason = event.data?.textareas?.reason || ''
    const payload = { postId: postId.value || postreview.id, reason }
    console.log('模擬送出 API 資料：', payload)
    alert('已成功駁回貼文')
    show.value = false
  }
}
const editPost = () => {
  // 這裡放編輯邏輯或跳轉，例如：
  // router.push(`/stores/posts/edit/${postId.value}`)
  console.log('go edit')
}
/** 返回（避免回到同頁，建議回列表或上一頁） */
const goBack = () => router.push('/stores/store-management') // 或 router.back()
const approve = () => alert('已核准貼文')
</script>

<template>
  <div class="page-layout">
    <main class="page-main">
      <!-- 新增：圖片上方的按鈕列 -->
      <div class="flex justify-end gap-3 mb-2">
        <button class="btn-back" @click="goBack">返回</button>
        <button class="btn-back" @click="editPost">編輯</button>
      </div>
      <img :src="imgSrc" alt="封面圖" class="article-img" />
      <h1 class="article-title">{{ title }}</h1>

      <div class="article-content">
        <p v-for="(para, idx) in content" :key="idx">{{ para }}</p>
      </div>

      <!-- <div class="article-buttons">
        <button class="btn-back" @click="goBack">返回</button>
        <button class="btn-addQ" @click="show = true">加入問題件</button>
        <button class="btn-check" @click="approve">核准</button>
      </div> -->
    </main>
  </div>

  <ModalBox
    :visible="show"
    title="貼文駁回"
    :infoRows="infoRows"
    :textareaFields="[
      { key: 'reason', label: '駁回原因（限200字內）', placeholder: '請輸入退件原因', rows: 5, maxlength: 200, required: true }
    ]"
    :buttons="[
      { text: '取消', action: 'cancel', class: 'modal-btn-cancel' },
      { text: '確認並通知店家', action: 'confirm', class: 'modal-btn-danger' }
    ]"
    @close="show = false"
    @button-click="handleButtonClick"
  />
</template>
