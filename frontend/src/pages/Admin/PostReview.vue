<!-- src/pages/Admin/PostReview.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import ModalBox from '../../components/ModalBox.vue'
// import axios from 'axios' // 若未來要打真 API

const route = useRoute()

const postId = ref('')
const title = ref('')
const content = ref([])
const imgSrc = ref('https://images.unsplash.com/photo-1601758228041-f3b2795255f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80') // 預設封面圖

const show = ref(false)
const infoRows = ref([])


//  模擬從 API 拿資料（日後這段只要換成 axios.get()）
onMounted(() => {
  // 從路由查詢參數獲取資料
  const routePostId = route.query.id
  const routeTitle = route.query.title
  const routeContent = route.query.content
  const routeStoreName = route.query.storeName
  
  // 如果有路由參數就使用，否則使用假資料
  if (routePostId && routeTitle) {
    postId.value = routePostId
    title.value = decodeURIComponent(routeTitle)
    
    // 處理 content - 如果有傳遞就使用，否則使用預設內容
    if (routeContent) {
      try {
        const decodedContent = decodeURIComponent(routeContent)
        content.value = JSON.parse(decodedContent)
      } catch {
        content.value = [decodeURIComponent(routeContent)]
      }
    } else {
      content.value = getDefaultContent()
    }
    
    // 將資料轉為 modal 可用格式
    infoRows.value = [
      ['編號', routePostId],
      ['店家名稱', routeStoreName ? decodeURIComponent(routeStoreName) : '毛星球寵物美容館'],
      ['標題', decodeURIComponent(routeTitle)]
    ]
  } else {
    // 假資料備用
    const res = {
      id: '001',
      store: '毛星球寵物美容館',
      title: '今天的店裡超熱鬧！三位新朋友來洗香香'
    }
    postId.value = res.id
    title.value = res.title
    content.value = getDefaultContent()
    
    infoRows.value = [
      ['編號', res.id],
      ['店家名稱', res.store],
      ['標題', res.title]
    ]
  }
})

// 預設內容函數，避免重複程式碼
const getDefaultContent = () => [
  '今天我們迎接了三位可愛的新朋友洗澡洗香香：米克斯「肉肉」、黃金獵犬組合「阿吉」與「阿豆」，還有常常來報到的哈士奇爆毛王「哈丁」！',
  '牠們一進門就吸引不少目光，一開始都有點害羞，但在熟悉的美容師帶領與香香的洗毛小浴缸下，很快就放下不安，用呆萌、歡樂、無辜的表情征服大家。',
  '最後的吹乾與造型，「肉肉」和「阿吉」都超配合，不只變得超帥氣，還紛紛搖尾巴向工作人員撒嬌。而哈丁雖然狂掉毛，本店美容師還是迅速處理完畢，毛量不減，帥度破表！',
  '若你家毛孩也需要香香洗澡，或想看看更多可愛瞬間，記得追蹤我們的社群平台唷！如果想預約洗澡，可以直接透過下方按鈕快速前往預約頁！'
]

const handleButtonClick = (event) => {
  if (event.action === 'cancel') {
    show.value = false
  } else if (event.action === 'confirm') {
    const reason = event.data.textareas.reason || ''
    console.log('收到駁回原因：', reason)

    // 模擬發送駁回資料給後端
    const payload = {
      postId: postId.value, 
      reason: reason
    }

    console.log('模擬送出 API 資料：', payload)
    // await axios.post('/api/posts/reject', payload) // 正式使用時啟用

    alert('已成功駁回貼文')
    show.value = false
  }
}


</script>

<template>
  <!-- 整頁結構，外層負責佈局 -->
  <div class="page-layout">
    <main class="page-main">
      <img :src="imgSrc" alt="封面圖" class="article-img" />
      <h1 class="article-title">{{ title }}</h1>
      <div class="article-content">
        <p v-for="(para, idx) in content" :key="idx">{{ para }}</p>
      </div>
      <div class="article-buttons" v-if="route.path === '/admin/post/review'">
        <RouterLink to="/admin/post" class="btn-back">返回</RouterLink>
        <button class="btn-addQ" @click="show = true">加入問題件</button>
        <button class="btn-check">核准</button>
      </div>
      <div class="article-buttons" v-else-if="route.path === '/admin/post/details'">
        <RouterLink to="/admin/post" class="btn-back">返回</RouterLink>
      </div>
    </main>
  </div>

  <ModalBox
    :visible="show"
    title="貼文駁回"
    :infoRows="infoRows"
    :textareaFields="[
      {
        key: 'reason',
        label: '駁回原因（限200字內）',
        placeholder: '請輸入退件原因',
        rows: 5,
        maxlength: 200,
        required: true
      }
    ]"
    :buttons="[
      {
        text: '取消',
        action: 'cancel',
        class: 'modal-btn-cancel'
      },
      {
        text: '確認並通知店家',
        action: 'confirm',
        class: 'modal-btn-danger'
      }
    ]"
    @close="show = false"
    @button-click="handleButtonClick"
  />
</template>