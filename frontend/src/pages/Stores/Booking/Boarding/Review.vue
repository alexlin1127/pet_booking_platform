<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

// 預約資料
const booking = ref({
  id: null,
  customer_name: '',
  phone: '',
  pet_name: '',
  pet_type: '',
  last_grooming_date: '',
  customer_note: '',
  service_type: '',
  booking_date: '',
  check_in_date: '',
  check_out_date: '',
  stay_duration: '',
  room_type: '',
  price: 0,
  pickup_delivery: false
});

// 店家備註
const storeNote = ref('');

// 從 URL 查詢參數獲取預約 ID
const bookingId = route.query.id;

onMounted(() => {
  // 模擬從 API 獲取預約資料
  loadBookingData();
});

const loadBookingData = () => {
  // 這裡應該調用 API 獲取實際資料
  // 目前使用模擬資料
  booking.value = {
    id: bookingId,
    customer_name: '張小玲',
    phone: '0911111111',
    pet_name: '毛毛',
    pet_type: '布偶貓',
    last_grooming_date: '2025/04/10',
    customer_note: '寵物對某些洗劑過敏，請使用敏感型產品',
    service_type: '住宿',
    booking_date: '2025/08/01',
    check_in_date: '2025/08/01',
    check_out_date: '2025/08/02',
    stay_duration: '1天',
    room_type: '單間房',
    price: 800,
    pickup_delivery: true
  };
};

const goBack = () => {
  router.go(-1);
};

const confirmBooking = () => {
  // 這裡應該調用 API 確認預約
  console.log('確認預約:', {
    bookingId: booking.value.id,
    storeNote: storeNote.value
  });
  
  // 確認後返回上一頁
  alert('預約已確認！');
  router.go(-1);
};

// 格式化日期顯示
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
  const weekday = weekdays[date.getDay()];
  return `${dateStr} (週${weekday})`;
};
</script>

<template>
  <div class="review-container">
    <div class="review-card">
      <!-- 標題 -->
      <h1 class="page-title">審核預約</h1>
      
      <!-- 顧客資訊卡片 -->
      <div class="customer-card">
        <h2 class="customer-title">顧客 {{ booking.customer_name }}</h2>
      </div>
      
      <div class="content-grid">
        <!-- 左側：顧客詳細資訊 -->
        <div class="left-section">
          <div class="customer-info-section">
            <div class="info-row">
              <label>聯絡電話：</label>
              <span>{{ booking.phone }}</span>
            </div>
            <div class="info-row">
              <label>寵物名字：</label>
              <span>{{ booking.pet_name }}</span>
            </div>
            <div class="info-row">
              <label>寵物種類：</label>
              <span>{{ booking.pet_type }}</span>
            </div>
            <div class="info-row">
              <label>上次洗澡：</label>
              <span>{{ booking.last_grooming_date }}</span>
            </div>
            <div class="info-row">
              <label>顧客備註：</label>
              <span>{{ booking.customer_note }}</span>
            </div>
          </div>
          
          <!-- 店家備註 -->
          <div class="store-note-section">
            <h3>店家備註</h3>
            <textarea 
              v-model="storeNote"
              placeholder="請輸入備註"
              class="store-note-textarea"
            ></textarea>
          </div>
        </div>
        
        <!-- 右側：訂單資訊 -->
        <div class="right-section">
          <!-- 訂單資訊 -->
          <div class="order-info-section">
            <h3>訂單資訊</h3>
            <div class="info-row">
              <label>預約服務：</label>
              <span>{{ booking.service_type }}</span>
            </div>
            <div class="info-row">
              <label>預約日期：</label>
              <span>{{ formatDate(booking.booking_date) }}</span>
            </div>
            <div class="info-row">
              <label>預約時間：</label>
              <span>{{ booking.stay_duration }}</span>
            </div>
            <div class="info-row">
              <label>入住時間：</label>
              <span>{{ booking.check_in_date }}</span>
            </div>
            <div class="info-row">
              <label>退房時間：</label>
              <span>{{ booking.check_out_date }}</span>
            </div>
            <div class="info-row">
              <label>預約房型：</label>
              <span>{{ booking.room_type }}</span>
            </div>
            <div class="info-row">
              <label>訂單金額：</label>
              <span>NT${{ booking.price }}</span>
            </div>
            <div class="info-row">
              <label>是否接送：</label>
              <span>{{ booking.pickup_delivery ? '是' : '否' }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 按鈕區域 -->
      <div class="button-group">
        <button @click="goBack" class="btn-secondary">返回前頁</button>
        <button @click="confirmBooking" class="btn-primary">確認預約</button>
      </div>
    </div>
  </div>
</template>

<style scoped src="../../../../styles/pages/Stores/Booking/Grooming/review.css"></style>
