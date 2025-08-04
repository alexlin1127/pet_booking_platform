<script setup>
import { ref } from 'vue'
import FormTemplate from '../../../components/UI/FormTemplate.vue'

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
        <h1 class="addposts-title">新增貼文</h1>
        <FormTemplate @submit="handleSubmit">
            <div class="addposts-form-content">
                <div>
                    <label class="addposts-label">服務項目</label>
                    <div class="addposts-radio-group">
                        <label class="addposts-radio-item"><input type="radio" name="service" value="美容" class="mr-1" />
                            美容</label>
                        <label class="addposts-radio-item"><input type="radio" name="service" value="住宿" class="mr-1" />
                            住宿</label>
                    </div>
                </div>
                <div>
                    <label class="addposts-label">標籤</label>
                    <div class="addposts-checkbox-grid">
                        <label class="addposts-checkbox-item"><input type="checkbox" value="毛孩日常" class="mr-1" />
                            毛孩日常</label>
                        <label class="addposts-checkbox-item"><input type="checkbox" value="毛孩美容" class="mr-1" />
                            毛孩美容</label>
                        <label class="addposts-checkbox-item"><input type="checkbox" value="毛孩造型" class="mr-1" />
                            毛孩造型</label>
                        <label class="addposts-checkbox-item"><input type="checkbox" value="毛孩保養" class="mr-1" />
                            毛孩保養</label>
                        <label class="addposts-checkbox-item"><input type="checkbox" value="毛孩知識" class="mr-1" />
                            毛孩知識</label>
                        <label class="addposts-checkbox-item">
                            <input type="checkbox" value="其他" class="mr-1" v-model="otherChecked" /> 其他
                            <input v-if="otherChecked" v-model="otherText" type="text" placeholder="請輸入"
                                class="ml-2 border-b border-gray-400 focus:border-blue-500 outline-none w-24 bg-transparent text-sm" />
                        </label>
                    </div>
                </div>
                <div>
                    <label class="addposts-label">標題</label>
                    <input type="text" placeholder="請填寫標題" class="addposts-input" />
                </div>
                <div>
                    <label class="addposts-label">內容</label>
                    <textarea placeholder="請填寫內容" class="addposts-textarea"></textarea>
                </div>
                <div>
                    <label class="addposts-label">圖片</label>
                    <div class="addposts-upload-area">
                        <button type="button" class="addposts-upload-btn">新增圖片</button>
                    </div>
                    <!-- 圖片預覽區塊（有圖片時才顯示，這裡用靜態假資料示意） -->
                    <div v-if="images && images.length" class="addposts-image-preview">
                        <div v-for="img in images" :key="img" class="addposts-image-placeholder">{{ img }}</div>
                    </div>
                </div>
            </div>
            <div class="addposts-button-group">
                <button type="button" class="addposts-cancel-btn">取消</button>
                <button type="submit" class="addposts-submit-btn">送出審核</button>
            </div>
        </FormTemplate>
    </div>
</template>