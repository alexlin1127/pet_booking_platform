<!-- PetConfirm.vue（只示範跟 Modal 相關的完整可用段落） -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

/* 假資料（頁面上本來在用的） */
const pet = ref({
  name: '小白',
  gender: '女',
  breed: '貴賓犬',
  age: 3,
  weight: 4.5,
  neutered: false,
  microchip: true,
  groomingCount: 0,
  lastGroomingDate: '',
  avatarUrl: 'https://picsum.photos/seed/poodle/640/480'
})

/* ✅ Modal 開關 */
const show = ref(false)
const openModal  = () => { show.value = true }
const closeModal = () => { show.value = false }

/* ✅ 你模板裡用的是 close / confirm，把方法對齊 */
const close   = () => closeModal()
const confirm = () => {
  // TODO：在這裡呼叫你的刪除 API，例如：
  // await api.deletePet(pet.value.id)
  closeModal()
}

/* 其它動作（例如修改） */
const editPet = () => router.push('/login/customers/petinfo')
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 md:px-6 pb-16 pt-10">
    <!-- 標題 + 右側新增 -->
    <div class="mb-8 flex items-center">
      <div class="flex-1"></div>
      <h1 class="pet-title text-center flex-shrink-0">毛孩子基本資料</h1>
      <div class="flex-1 flex justify-end">
        <button type="button" class="pet-action">新增毛孩子</button>
      </div>
    </div>

    <!-- 主卡片（略） -->
    <section class="pet-summary-card">
      <div class="pet-avatar-wrap">
        <img :src="pet.avatarUrl" alt="pet avatar" class="pet-avatar" />
      </div>
      <div class="pet-header">
        <h3 class="pet-name">{{ pet.name || '未命名' }}（{{ pet.gender || '—' }}）</h3>
        <p class="pet-subtitle">
          {{ pet.breed || '—' }} / {{ pet.age || '—' }}歲 / {{ pet.weight || '—' }}kg
        </p>
      </div>
      <div class="pet-badge" :class="pet.neutered ? 'is-ok' : 'is-muted'">
        {{ pet.neutered ? '已結紮' : '未結紮' }}
      </div>
      <div class="pet-badge" :class="pet.microchip ? 'is-ok' : 'is-muted'">
        {{ pet.microchip ? '已植入晶片' : '未植入晶片' }}
      </div>
      <div class="pet-stat">美容次數：{{ pet.groomingCount ?? 0 }}次</div>
      <div class="pet-stat">上次美容日期：{{ pet.lastGroomingDate || '尚未預約' }}</div>

      <!-- 這顆要打開 modal -->
      <button type="button" class="pet-action pet-action--danger" @click="openModal">
        刪除毛孩子
      </button>
      <button type="button" class="pet-action" @click="editPet">
        修改毛孩子
      </button>
    </section>

    <!-- ✅ Modal（不依賴外部元件，show 控制顯示） -->
    <div v-if="show" class="fixed inset-0 z-[9999]">
      <!-- 遮罩 -->
      <div class="fixed inset-0 bg-black/50" @click="close"></div>

      <!-- 置中白底卡片 -->
      <div class="fixed inset-0 flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-[680px] overflow-hidden">
          <!-- Modal 標題列 -->
          <div class="px-6 py-4 border-b flex items-center justify-between">
            <h3 class="text-lg font-semibold">確認刪除該毛孩的紀錄</h3>
            <button class="text-gray-500 hover:text-gray-700 text-xl" @click="close">×</button>
          </div>

          <!-- Modal 內容：⚠️ 這裡用你給的排版 -->
          <div class="p-6">
            <div class="pet-summary-card bolder-0">
              <!-- 照片 -->
              <div class="pet-avatar-wrap">
                <img :src="pet.avatarUrl" alt="pet avatar" class="pet-avatar pointer-events-none" />
              </div>

              <!-- 標頭 -->
              <div class="pet-header">
                <h3 class="pet-name">{{ pet.name || '未命名' }}（{{ pet.gender || '—' }}）</h3>
                <p class="pet-subtitle">
                  {{ pet.breed || '—' }} / {{ pet.age || '—' }}歲 / {{ pet.weight || '—' }}kg
                </p>
              </div>

              <!-- 標籤 -->
              <div class="pet-badge" :class="pet.neutered ? 'is-ok' : 'is-muted'">
                {{ pet.neutered ? '已結紮' : '未結紮' }}
              </div>
              <div class="pet-badge" :class="pet.microchip ? 'is-ok' : 'is-muted'">
                {{ pet.microchip ? '已植入晶片' : '未植入晶片' }}
              </div>

              <!-- 統計 -->
              <div class="pet-stat">美容次數：{{ pet.groomingCount ?? 0 }}次</div>
              <div class="pet-stat">上次美容日期：{{ pet.lastGroomingDate || '尚未預約' }}</div>

              <!-- 動作（照你要求，用 close / confirm 名稱） -->
              <button type="button" class="pet-action" @click="close">取消</button>
              <button type="button" class="pet-action pet-action--danger" @click="confirm">刪除</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
