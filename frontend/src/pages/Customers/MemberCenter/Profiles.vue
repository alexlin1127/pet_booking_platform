<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
// ⬇️ 按你的實際路徑修改（你給我的 Form.vue）
import FormTemplate from '../../../components/UI/FormTemplate.vue'

/** 假資料（可換 API） */
const profile = reactive({
  name: '王小明',
  gender: '男',
  phone: '0911111111',
  email: '1@gmail.com',
})

const router = useRouter();

/** 編輯狀態（只控制密碼列是否顯示與底部按鈕群） */
const isEditing = ref(false)

/** 只有密碼可以編輯 */
const password = ref('')
const isSubmitting = ref(false)

function startEdit() {
  password.value = ''
  isEditing.value = true
}
function cancelEdit() {
  password.value = ''
  isEditing.value = false
}
async function changePassword() {
    router.push('/members/profiles/password/change')
}

/** 優惠券（展示用） */
const coupon = reactive({ code: 'sfsd654xv46334', used: false })
const statusText = computed(() => (coupon.used ? '已使用此優惠券' : '尚未使用此優惠券'))
const statusClass = computed(() => (coupon.used ? 'is-used' : 'is-unused'))
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 md:px-6 py-8">
    <h1 class="page-title">會員基本資料</h1>
    <!-- 表單（用 FormTemplate） -->
  <FormTemplate class="mt-6 md:mt-8">
  <!-- ✅ default slot（不加名字，或用 #default 都可以） -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <!-- 姓名（唯讀） -->
    <div class="form-group md:col-span-2">
      <label>姓名</label>
      <input class="form-input" type="text" :value="profile.name" readonly aria-readonly="true" />
    </div>

    <!-- 性別（唯讀 select） -->
    <div class="form-group">
      <label>性別</label>
      <select class="form-input" :value="profile.gender" disabled>
        <option value="男">男</option>
        <option value="女">女</option>
        <option value="其他">其他</option>
      </select>
    </div>

    <!-- 聯絡電話（唯讀） -->
    <div class="form-group">
      <label>聯絡電話</label>
      <input class="form-input" type="tel" :value="profile.phone" readonly aria-readonly="true" />
    </div>

    <!-- Email（唯讀） -->
    <div class="form-group md:col-span-2">
      <label>Email</label>
      <input class="form-input" type="email" :value="profile.email" readonly aria-readonly="true" />
    </div>

    <!-- 只有在編輯狀態時顯示密碼列 -->
    <div v-if="isEditing" class="md:col-span-2">
      <div class="pw-row">
        <label class="pw-label">密碼</label>
        <div class="pw-grid">
          <input class="pw-input" type="password" v-model="password" placeholder="XXXXXXXX" autocomplete="new-password" />
          <button type="button" class="pw-btn" :disabled="isSubmitting" @click="changePassword">變更密碼</button>
        </div>
      </div>
    </div>
  </div>
</FormTemplate>
  <!-- <template #actions> -->
    <div class="action-bar">
      <div v-if="!isEditing" class="flex justify-center">
        <button type="button" class="btn btn-primary px-5 py-2.5" @click="startEdit">變更資料</button>
      </div>
      <div v-else class="w-full max-w-xl mx-auto grid grid-cols-2 gap-4">
        <button type="button" class="btn btn-ghost" @click="cancelEdit">取消</button>
        <button type="button" class="btn btn-primary" :disabled="isSubmitting" @click="changePassword">確定</button>
      </div>
    </div>
  <!-- </template> -->


    <!-- 優惠券卡片（同樣使用 FormTemplate，標題 = 註冊優惠） -->
  <FormTemplate v-if="!isEditing">
    <!-- ✅ default slot -->
    <div class="coupon-card">
      <div class="coupon-title">註冊優惠</div>
      <div class="coupon-code">{{ coupon.code }}</div>
      <div class="coupon-status" :class="statusClass">
        <svg class="icon" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M20.3 5.7a1 1 0 0 1 0 1.4l-9.6 9.6a1 1 0 0 1-1.4 0L3.7 11a1 1 0 1 1 1.4-1.4l4.2 4.2 8.9-8.9a1 1 0 0 1 1.4 0z"/>
        </svg>
        <span>{{ statusText }}</span>
      </div>
    </div>
  </FormTemplate>

  </main>
</template>

<style scoped src="../../../styles/pages/Customers/MemberCenter/profiles.css"></style>