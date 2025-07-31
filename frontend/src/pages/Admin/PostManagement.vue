<!-- src/pages/Admin/PostManagerment.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import ModalBox from '@/components/ModalBox.vue'
// 內容先用假資料
const title = ref('今天的店裡超熱鬧！三位新朋友來洗香香')
const content = ref([
  '今天我們迎接了三位可愛的新朋友洗澡洗香香：米克斯「肉肉」、黃金獵犬組合「阿吉」與「阿豆」，還有常常來報到的哈士奇爆毛王「哈丁」！',
  '牠們一進門就吸引不少目光，一開始都有點害羞，但在熟悉的美容師帶領與香香的洗毛小浴缸下，很快就放下不安，用呆萌、歡樂、無辜的表情征服大家。',
  '最後的吹乾與造型，「肉肉」和「阿吉」都超配合，不只變得超帥氣，還紛紛搖尾巴向工作人員撒嬌。而哈丁雖然狂掉毛，本店美容師還是迅速處理完畢，毛量不減，帥度破表！',
  '若你家毛孩也需要香香洗澡，或想看看更多可愛瞬間，記得追蹤我們的社群平台唷！如果想預約洗澡，可以直接透過下方按鈕快速前往預約頁！'
])
const show = ref(false)
const infoRows = ref([])  //  將 infoRows 定義為 ref，方便從 API 更新
const reasonList = ['資料錯誤', '資格不符', '系統異常']

//  模擬從 API 拿資料（日後這段只要換成 axios.get()）
onMounted(() => {
  // 假資料模擬後端返回格式
  const res = {
    id: 'A1001',
    name: '王小明',
    account: 'ming123',
    store: '貓狗城堡'
  }

  // 將資料轉為 modal 可用格式（之後換後端資料也只需改這裡）
  infoRows.value = [
    ['編號', res.id],
    ['名字', res.name],
    ['帳號', res.account],
    ['所屬店家', res.store]
  ]
})

const handleConfirm = (reason) => {
  alert(`選擇駁回原因：${reason}`)
  show.value = false
}
</script>

<template>
<!-- ✅ 整頁結構，外層負責佈局 -->
 <div class="page-layout">
    <main class="page-main">
      <img :src="imgSrc" alt="封面圖" class="article-img" />
      <h1 class="article-title">{{ title }}</h1>
      <div class="article-content">
        <p v-for="(para, idx) in content" :key="idx">{{ para }}</p>
      </div>
      <div class="article-buttons">
        <button class="btn-secondary">返回首頁</button>
        <button class="btn-primary" @click="show = true">立即預約</button>
      </div>
    </main>
  </div>

  <!-- 按鈕區 -->
  <!-- <div class="flex justify-center gap-4">
    <button class="bg-gray-300 text-black px-6 py-2 rounded hover:bg-gray-400">返回首頁</button>
    <button @click="show = true" class="bg-blue-500 text-white px-4 py-2 rounded">立即預約</button>
  </div> -->
<!-- </main> -->
<!-- </div> -->

    <!-- <button @click="show = true" class="bg-blue-500 text-white px-4 py-2 rounded">打開 Modal</button> -->

    <ModalBox
      :visible="show"
      :infoRows="infoRows"
      :reasons="reasonList"
      cancelText="取消駁回"
      confirmText="確認駁回"
      @cancel="show = false"
      @confirm="handleConfirm"
    />
  <!-- </div> -->
</template>
