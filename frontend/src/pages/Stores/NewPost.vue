<script setup>
import { ref } from 'vue'
import FormTemplate from '@/components/UI/FormTemplate.vue'

function handleSubmit() {
    console.log('提交貼文！')
    // 做驗證或送 API
}

const otherChecked = ref(false)
const otherText = ref("")

// 圖片預覽假資料
const images = ref([]) // 之後可改為圖片檔案陣列
</script>

<template>
  <div class="addposts-container">
    <!-- ✅ 框線外的頁面標題 -->
    <h1 class="addposts-title">新增貼文</h1>

    <!-- ✅ 不改 FormTemplate，但把它的標題留空；並把 actions slot 留空 -->
    <FormTemplate :title="''" @submit="handleSubmit">
      <div class="addposts-form-content">
        <!-- 服務項目 -->
        <div class="form-group">
          <label class="form-group-label">服務項目</label>
          <div class="addposts-radio-group">
            <label class="addposts-radio-item">
              <input type="radio" name="service" value="美容" class="mr-1" /> 美容
            </label>
            <label class="addposts-radio-item">
              <input type="radio" name="service" value="住宿" class="mr-1" /> 住宿
            </label>
          </div>
        </div>

        <!-- 標籤 -->
        <div class="form-group">
          <label class="form-group-label">標籤</label>
          <div class="addposts-checkbox-grid">
            <label class="addposts-checkbox-item">
              <input type="checkbox" value="毛孩日常" class="mr-1" /> 毛孩日常
            </label>
            <label class="addposts-checkbox-item">
              <input type="checkbox" value="毛孩美容" class="mr-1" /> 毛孩美容
            </label>
            <label class="addposts-checkbox-item">
              <input type="checkbox" value="毛孩造型" class="mr-1" /> 毛孩造型
            </label>
            <label class="addposts-checkbox-item">
              <input type="checkbox" value="毛孩保養" class="mr-1" /> 毛孩保養
            </label>
            <label class="addposts-checkbox-item">
              <input type="checkbox" value="毛孩知識" class="mr-1" /> 毛孩知識
            </label>
            <label class="addposts-checkbox-item">
              <input type="checkbox" value="其他" class="mr-1" v-model="otherChecked" /> 其他
              <input
                v-if="otherChecked"
                v-model="otherText"
                type="text"
                placeholder="請輸入"
                class="ml-2 border-b border-gray-400 focus:border-blue-500 outline-none w-24 bg-transparent text-sm"
              />
            </label>
          </div>
        </div>

        <!-- 標題 -->
        <div class="form-group">
          <label class="form-group-label">標題</label>
          <input type="text" placeholder="請填寫標題" class="addposts-input" />
        </div>

        <!-- 內容 -->
        <div class="form-group">
          <label class="form-group-label">內容</label>
          <textarea placeholder="請填寫內容" class="addposts-textarea"></textarea>
        </div>

        <!-- 圖片 -->
        <div class="form-group">
          <label class="form-group-label">圖片</label>
          <div class="addposts-upload-area">
            <button type="button" class="addposts-upload-btn">新增圖片</button>
          </div>

          <!-- 圖片預覽（可選） -->
          <div v-if="images && images.length" class="addposts-image-preview">
            <div v-for="img in images" :key="img" class="addposts-image-placeholder">{{ img }}</div>
          </div>
        </div>
      </div>

      <!-- 不放 actions，讓 Template 的 actions 區保持空的（下面有自訂的按鈕列） -->
      <template #actions></template>
    </FormTemplate>

    <!-- ✅ 框線外的按鈕列（跟你的截圖同位置） -->
    <div class="addposts-button-group">
      <button type="button" class="addposts-cancel-btn">取消</button>
      <button type="button" class="addposts-submit-btn" @click="handleSubmit">新增</button>
    </div>
  </div>
</template>

<style src="@/styles/pages/Admin/Stores/newpost.css" scoped></style>