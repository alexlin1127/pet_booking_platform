<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { posts } from '../../../data/postsfakedata'
import FormTemplate from '../../../components/UI/FormTemplate.vue'
import '../../../styles/pages/Stores/Posts/postsprocess.css'

const router = useRouter()
const route = useRoute()

// 判斷是否為編輯模式
const isEditMode = computed(() => route.path.includes('/edit/'))
const postId = computed(() => route.params.id)

// 表單資料
const formData = ref({
    service: '',
    tags: [],
    title: '',
    content: '',
    images: []
})

const otherChecked = ref(false)
const otherText = ref("")

// 圖片預覽假資料
const images = ref([]) // 之後可改為圖片檔案陣列

// 載入編輯資料
onMounted(() => {
    console.log('🔍 onMounted 執行，isEditMode:', isEditMode.value, 'postId:', postId.value)
    if (isEditMode.value && postId.value) {
        const post = posts.find(p => String(p.id) === String(postId.value))
        console.log('🔍 找到的貼文:', post)
        if (post) {
            formData.value.title = post.title
            formData.value.content = post.content
            formData.value.service = post.tag === '寵物美容' ? '美容' : '住宿'
            // 這裡可以根據需求設定其他欄位
            images.value = post.images || []
        }
    }
})

function handleSubmit() {
    console.log('🚀 handleSubmit 被呼叫')
    if (isEditMode.value) {
        console.log('更新貼文！', formData.value)
        // 做編輯驗證或送 API
    } else {
        console.log('提交貼文！', formData.value)
        // 做新增驗證或送 API
    }
}

function goToManage() {
    router.push('/stores/posts/manage')
}
</script>

<template>
    <div class="addposts-container">
        <FormTemplate :title="isEditMode ? '編輯貼文' : '新增貼文'" @submit="handleSubmit">
            <div class="addposts-form-content">
                <div>
                    <label class="addposts-label">服務項目</label>
                    <div class="addposts-radio-group">
                        <label class="addposts-radio-item"><input type="radio" name="service" value="美容" v-model="formData.service" class="mr-1" />
                            美容</label>
                        <label class="addposts-radio-item"><input type="radio" name="service" value="住宿" v-model="formData.service" class="mr-1" />
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
                    <input type="text" placeholder="請填寫標題" v-model="formData.title" class="addposts-input" />
                </div>
                <div>
                    <label class="addposts-label">內容</label>
                    <textarea placeholder="請填寫內容" v-model="formData.content" class="addposts-textarea"></textarea>
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
            
            <template #actions>
                <div class="addposts-button-group">
                    <button type="button" class="addposts-cancel-btn" @click="goToManage">取消</button>  
                    <button type="submit" :class="isEditMode ? 'editposts-submit-btn' : 'addposts-submit-btn'">
                        {{ isEditMode ? '完成編輯' : '送出審核' }}
                    </button>
                </div>
            </template>
        </FormTemplate>
    </div>
</template>