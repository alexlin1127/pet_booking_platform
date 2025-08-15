<!-- src/pages/PetInfo.vue -->
<script setup>
import { reactive, ref, onBeforeUnmount} from 'vue'
import { useRouter } from 'vue-router'
import FormTemplate from '@/components/UI/FormTemplate.vue'

const router = useRouter()

/* 假資料（下拉選單選項） */
const genderOptions = [
  { label: '請選擇毛孩的性別', value: '' },
  { label: '男', value: '男' },
  { label: '女', value: '女' },
]
const coatOptions = [
  { label: '請選擇您的毛孩的毛量', value: '' },
  { label: '短毛', value: '短毛' },
  { label: '長毛', value: '長毛' },
]
const sizeOptions = [
  { label: '請選擇您的毛孩的體型', value: '' },
  { label: '小型犬', value: '小型犬' },
  { label: '中型犬', value: '中型犬' },
  { label: '大型犬', value: '大型犬' },
]

/* 表單狀態 */
const form = reactive({
  petType: '狗狗',
  name: '',
  gender: '',
  breed: '',
  coat: '',
  size: '',
  age: '',
  weight: '',
  neutered: '',
  microchipped: '',
  note: '',
  photoFile: null,
  photoPreviewUrl: '',
})

/* 照片上傳 */
const fileInputRef = ref(null)
function pickPhoto() { fileInputRef.value?.click() }
function onFileChange(e) {
  const input = e.target
  const file = input && input.files && input.files[0]
  if (!file) return

  if (form.photoPreviewUrl) URL.revokeObjectURL(form.photoPreviewUrl)
  form.photoFile = file
  form.photoPreviewUrl = URL.createObjectURL(file)
}

onBeforeUnmount(() => {
  if (form.photoPreviewUrl) URL.revokeObjectURL(form.photoPreviewUrl)
})

/* 動作 */
function submit() { alert('表單已送出（示意），之後可接 API') }
function cancel() { router.back() }
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 md:px-6 pb-16 pt-10">
    <!-- 頁面標題（置中；不放在 FormTemplate 內） -->
    <!-- <h1 v-if="" class="cp-title">新增毛孩子基本資料</h1>
    <h1 v-else-if="" class="cp-title">修改毛孩子基本資料</h1> -->

    <!-- 表單主體（使用 FormTemplate；不帶 title） -->
    <FormTemplate>
      <!-- 第一段：基本資料 -->
      <div class="form-group">
        <label>毛孩類別 *</label>
        <div class="radio-row">
          <label class="radio-item">
            <input class="radio-input" type="radio" value="狗狗" v-model="form.petType" />
            <span>狗狗</span>
          </label>
          <label class="radio-item">
            <input class="radio-input" type="radio" value="貓貓" v-model="form.petType" />
            <span>貓貓</span>
          </label>
        </div>
      </div>

      <!-- 2 欄：名字 / 性別 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="form-group">
          <label>毛孩姓名 *</label>
          <input class="form-input" type="text" v-model="form.name" placeholder="請輸入寵物名字" />
        </div>
        <div class="form-group">
          <label>毛孩性別 *</label>
          <select class="form-input" v-model="form.gender">
            <option v-for="opt in genderOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
          </select>
        </div>
      </div>

      <!-- 品種 -->
      <div class="form-group">
        <label>毛孩品種</label>
        <input class="form-input" type="text" v-model="form.breed" placeholder="請輸入您毛孩子的品種" />
      </div>

      <!-- 2 欄：毛量 / 體型 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="form-group">
          <label>毛孩毛量 *</label>
          <select class="form-input" v-model="form.coat">
            <option v-for="opt in coatOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>毛孩體型 *</label>
          <select class="form-input" v-model="form.size">
            <option v-for="opt in sizeOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
          </select>
        </div>
      </div>

      <!-- 2 欄：年齡 / 體重 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="form-group">
          <label>毛孩年齡</label>
          <div class="inline-input">
            <input class="form-input" type="number" min="0" v-model="form.age" placeholder="請輸入您毛孩年齡" />
            <span class="suffix">歲</span>
          </div>
        </div>
        <div class="form-group">
          <label>毛孩體重</label>
          <div class="inline-input">
            <input class="form-input" type="number" min="0" step="0.1" v-model="form.weight" placeholder="請輸入您毛孩的體重" />
            <span class="suffix">kg</span>
          </div>
        </div>
      </div>

      <hr class="divider" />

      <!-- 兩組 Radio：桌機各佔一半，手機直排 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- 已結紮 -->
        <div class="form-group">
          <label>已結紮 *</label>
          <div class="radio-row">
            <label class="radio-item">
              <input class="radio-input" type="radio" value="是" v-model="form.neutered" />
              <span>是</span>
            </label>
            <label class="radio-item">
              <input class="radio-input" type="radio" value="否" v-model="form.neutered" />
              <span>否</span>
            </label>
            <label class="radio-item">
              <input class="radio-input" type="radio" value="不確定" v-model="form.neutered" />
              <span>不確定</span>
            </label>
          </div>
        </div>

        <!-- 已植入晶片 -->
        <div class="form-group">
          <label>已植入晶片 *</label>
          <div class="radio-row">
            <label class="radio-item">
              <input class="radio-input" type="radio" value="是" v-model="form.microchipped" />
              <span>是</span>
            </label>
            <label class="radio-item">
              <input class="radio-input" type="radio" value="否" v-model="form.microchipped" />
              <span>否</span>
            </label>
            <label class="radio-item">
              <input class="radio-input" type="radio" value="不確定" v-model="form.microchipped" />
              <span>不確定</span>
            </label>
          </div>
        </div>
      </div>

      <hr class="divider" />

      <!-- 照片上傳 -->
      <div class="form-group">
        <label>毛孩照片 *</label>
        <div class="photo-row">
          <button type="button" class="upload-btn" @click="pickPhoto">新增圖片</button>
          <input ref="fileInputRef" type="file" accept="image/*" class="hidden" @change="onFileChange" />
          <img v-if="form.photoPreviewUrl" class="photo-preview" :src="form.photoPreviewUrl" alt="預覽圖片" />
        </div>
      </div>

      <!-- 備註 -->
      <div class="form-group">
        <label>備註</label>
        <textarea
          class="form-textarea"
          rows="5"
          v-model="form.note"
          placeholder="請輸入您毛孩是否藥物過敏等其它情況"
        ></textarea>
      </div>
    </FormTemplate>
         <!-- 動作列（與其它頁一致的兩顆按鈕） -->
      <div  class="w-full max-w-xl mx-auto grid grid-cols-2 gap-4 mt-8">
        <button type="button" class="btn btn-ghost" @click="cancelEdit">取消</button>
        <button type="button" class="btn btn-primary" :disabled="isSubmitting" @click="changePassword">確定</button>
      </div>
  </main>
</template>

<style scoped>
/* 頁面標題（你指定的語意化） */
.cp-title { @apply text-3xl md:text-4xl font-bold text-center mb-8; }

/* 分隔線（與你的主題色系一致） */
.divider { @apply my-5 border-t; border-color: #e7ded4; }

/* 單選群組 */
.radio-row  { @apply flex flex-wrap items-center gap-6; }
.radio-item { @apply inline-flex items-center gap-2; }
.radio-input { @apply w-4 h-4; }

/* 內嵌單位（歲／kg） */
.inline-input { @apply flex items-center gap-2; }
.inline-input .suffix { @apply text-sm text-gray-500; }

/* 圖片與上傳 */
.photo-row { @apply flex items-start gap-4; }
.photo-preview { @apply w-28 h-28 object-cover w-24 h-24 ; }
</style>
