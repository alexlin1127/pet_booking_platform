<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 房型數據
const roomTypes = [
  {
    id: 1,
    name: '普通房',
    totalRooms: 5,
    availableRooms: 5,
    pet_type: 'dog',
    type:''
  },
  {
    id: 2,
    name: '豪華房',
    totalRooms: 5,
    availableRooms: 5,
    pet_type: 'dog'
  },
  {
    id: 3,
    name: '總統套房',
    totalRooms: 5,
    availableRooms: 5,
    pet_type: 'dog'
  },
  {
    id: 4,
    name: '獨立單間',
    totalRooms: 5,
    availableRooms: 5,
    pet_type: 'cat'
  },
  {
    id: 5,
    name: '雙貓間',
    totalRooms: 5,
    availableRooms: 5,
    pet_type: 'cat'
  },
  {
    id: 6,
    name: '',
    totalRooms: 0,
    availableRooms: 0,
    pet_type: 'cat'
  }
]

// 預約統計數據
const pendingBookings = ref(20)
const recentBookings = ref(32)

// 當前選中的寵物類型
const selectedPetType = ref('狗狗')

const goToPendingBookings = () => {
  router.push('/stores/boarding/pending')
}

const goToRecentBookings = () => {
  router.push('/stores/boarding/recent')
}
</script>
<template>
  <div class="boarding-container">
    <!-- 頁面標題 -->
    <div class="page-header">
      <h1 class="page-title">目前住宿總覽</h1>
      
      <!-- 寵物類型選擇 -->
      <div class="pet-type-selector">
        <label class="pet-type-option">
          <input 
            type="radio" 
            name="petType" 
            value="狗狗" 
            v-model="selectedPetType"
            class="pet-type-radio"
          />
          <span class="pet-type-dot"></span>
          <span class="pet-type-label">狗狗</span>
        </label>
        
        <label class="pet-type-option">
          <input 
            type="radio" 
            name="petType" 
            value="貓貓" 
            v-model="selectedPetType"
            class="pet-type-radio"
          />
          <span class="pet-type-dot"></span>
          <span class="pet-type-label">貓貓</span>
        </label>
      </div>
    </div>

    <!-- 房型卡片網格 -->
    <div class="room-grid">
      <div 
        v-for="room in roomTypes" 
        :key="room.id"
        :class="['room-card', { 'room-card-empty': room.id === 6 }]"
      >
        <div v-if="room.id !== 6" class="room-content">
          <div class="room-header">
            <h3 class="room-title">{{ room.name }}</h3>
          </div>
          <div class="room-body">
            <div class="room-info">
              <span class="room-info-label">店內房間數：</span>
              <span class="room-info-value">{{ room.totalRooms }} 個</span>
            </div>
            <div class="room-info">
              <span class="room-info-label">剩餘空位：</span>
              <span class="room-info-value">{{ room.availableRooms }} 個</span>
            </div>
          </div>
        </div>
        <div v-else class="empty-slot"></div>
      </div>
    </div>

    <!-- 預約統計卡片 -->
    <div class="booking-stats-grid">
      <div class="stats-card" @click="goToPendingBookings">
        <div class="stats-header">
          <h3 class="stats-title">待審核預約</h3>
        </div>
        <div class="stats-body">
          <div class="stats-number">{{ pendingBookings }} 筆</div>
          <button class="stats-button">查看詳情</button>
        </div>
      </div>

      <div class="stats-card" @click="goToRecentBookings">
        <div class="stats-header">
          <h3 class="stats-title">近期預約</h3>
        </div>
        <div class="stats-body">
          <div class="stats-number">{{ recentBookings }} 筆</div>
          <button class="stats-button">查看詳情</button>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped src="../../../../styles/pages/Stores/Booking/Boarding/bk.css"></style>