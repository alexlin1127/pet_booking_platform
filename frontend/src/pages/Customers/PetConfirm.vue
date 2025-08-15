<!-- PetConfirm.vue（修正版） -->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

/** 1) 狀態 */
const isEdit = computed(() => route.params.mode === 'edit')
const isLoading = ref(false)

/** 2) 從後端取回的寵物資料（預設 null = 尚未有資料） */
const pet = ref(null) // 測空狀態時保持 null

/* 假資料（開發用：註解這段就能看到「尚無任何資料」） */
 pet.value = {
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
   }

/** 3) 安全代理（提供預設值，避免模板報錯） */
const defaultAvatar = 'https://placehold.co/350x350?text=No+Photo'
const p = computed(() => ({
  avatarUrl: pet.value?.avatarUrl || defaultAvatar,
  name: pet.value?.name || '未命名',
  gender: pet.value?.gender ?? '—',
  breed: pet.value?.breed ?? '—',
  age: pet.value?.age ?? '—',
  weight: pet.value?.weight ?? '—',
  neutered: !!pet.value?.neutered,
  microchip: !!pet.value?.microchip,
  groomingCount: pet.value?.groomingCount ?? 0,
  lastGroomingDate: pet.value?.lastGroomingDate || '尚未預約'
}))

/** 4) 是否有實質資料（空物件/null => false） */
const hasPetData = computed(() => {
  if (!pet.value) return false
  return Object.values(pet.value).some(v => v !== '' && v !== null && v !== undefined)
})

/** 5) 編輯模式：模擬載入資料（請換成你的 API） */
onMounted(async () => {
  if (!isEdit.value) return
  isLoading.value = true
  try {
    // const data = await api.get('/pets/:id')
    const data = pet.value // 這裡示範直接吃上方假資料；註解時為 null
    pet.value = data
  } finally {
    isLoading.value = false
  }
})

/** 6) Modal 控制 */
const show = ref(false)
const openModal  = () => { if (!hasPetData.value) return; show.value = true }
const closeModal = () => { show.value = false }
const close   = () => closeModal()
const confirm = () => {
  // TODO：呼叫刪除 API，例如：await api.deletePet(pet.value.id)
  closeModal()
}

/** 7) 路由跳轉（用 name + params） */
const editPet = () => router.push({ name: 'PetInfo', params: { mode: 'edit' } })
const createPet = () => router.push({ name: 'PetInfo', params: { mode: 'create' } })
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 md:px-6 pb-16 pt-10">
    <!-- 標題 + 右側新增 -->
    <div class="mb-8 flex items-center">
      <div class="flex-1"></div>
      <h1 class="pet-title text-center flex-shrink-0">毛孩子基本資料</h1>
      <div class="flex-1 flex justify-end">
        <button type="button" class="pet-action" @click="createPet">新增毛孩子</button>
      </div>
    </div>

    <!-- 1) 編輯模式 + 讀取中 -->
    <div v-if="isEdit && isLoading" class="text-center py-10">
      讀取中…
    </div>

    <!-- 2) 無資料（不論 create 或 edit，都顯示空狀態；需要限定 edit 再加 isEdit） -->
    <div v-else-if="!hasPetData" class="text-center py-10">
      <p class="mb-4 text-gray-600 text-lg">尚無任何資料</p>
    </div>

    <!-- 3) 有資料才顯示卡片 -->
    <section v-else class="pet-summary-card">
      <div class="pet-avatar-wrap">
        <img :src="p.avatarUrl" alt="pet avatar" class="pet-avatar" />
      </div>

      <div class="pet-header">
        <h3 class="pet-name">{{ p.name }}（{{ p.gender }}）</h3>
        <p class="pet-subtitle">
          {{ p.breed }} / {{ p.age }}歲 / {{ p.weight }}kg
        </p>
      </div>

      <div class="pet-badge" :class="p.neutered ? 'is-ok' : 'is-muted'">
        {{ p.neutered ? '已結紮' : '未結紮' }}
      </div>
      <div class="pet-badge" :class="p.microchip ? 'is-ok' : 'is-muted'">
        {{ p.microchip ? '已植入晶片' : '未植入晶片' }}
      </div>

      <div class="pet-stat">美容次數：{{ p.groomingCount }}次</div>
      <div class="pet-stat">上次美容日期：{{ p.lastGroomingDate }}</div>

      <button type="button" class="pet-action pet-action--danger" @click="openModal">
        刪除毛孩子
      </button>
      <button type="button" class="pet-action" @click="editPet">
        修改毛孩子
      </button>
    </section>

    <!-- Modal（只有有資料時才會顯示） -->
    <div v-if="show && hasPetData" class="fixed inset-0 z-[9999]">
      <div class="fixed inset-0 bg-black/50" @click="close"></div>
      <div class="fixed inset-0 flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-[680px] overflow-hidden">
          <div class="flex items-center justify-center mt-4 py-4">
            <h3 class="pet-title text-center flex-shrink-0">確認刪除該毛孩的紀錄</h3>
          </div>
          <div class="p-6">
            <div class="pet-modal-card">
              <div class="pet-avatar-wrap">
                <img :src="p.avatarUrl" alt="pet avatar" class="pet-avatar pointer-events-none" />
              </div>
              <div class="pet-header">
                <h3 class="pet-name">{{ p.name }}（{{ p.gender }}）</h3>
                <p class="pet-subtitle text-left">
                  {{ p.breed }} / {{ p.age }}歲 / {{ p.weight }}kg
                </p>
              </div>
              <div class="pet-badge" :class="p.neutered ? 'is-ok' : 'is-muted'">
                {{ p.neutered ? '已結紮' : '未結紮' }}
              </div>
              <div class="pet-badge" :class="p.microchip ? 'is-ok' : 'is-muted'">
                {{ p.microchip ? '已植入晶片' : '未植入晶片' }}
              </div>
              <div class="pet-stat">美容次數：{{ p.groomingCount }}次</div>
              <div class="pet-stat">上次美容日期：{{ p.lastGroomingDate }}</div>
              <button type="button" class="pet-action" @click="close">取消</button>
              <button type="button" class="pet-action pet-action--danger" @click="confirm">刪除</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
