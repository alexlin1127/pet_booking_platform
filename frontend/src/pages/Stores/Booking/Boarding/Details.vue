<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

// 預約詳情資料
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
  pickup_delivery: false,
  store_note: ''
});

// 歷史預約紀錄
const historyBookings = ref([]);

// 載入狀態
const isLoading = ref(false);

// 從 URL 查詢參數獲取預約 ID
const bookingId = route.query.id;

onMounted(() => {
  loadBookingDetails();
  loadHistoryBookings();
});

const loadBookingDetails = async () => {
  if (!bookingId) {
    console.error('沒有提供預約 ID');
    return;
  }

  isLoading.value = true;
  
  try {
    // TODO: 替換為實際的 API 調用
    // const response = await fetch(`/api/boarding-bookings/${bookingId}`);
    // const data = await response.json();
    // booking.value = data;
    
    // 模擬資料
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
      pickup_delivery: true,
      store_note: ''
    };
    
  } catch (error) {
    console.error('載入預約詳情失敗:', error);
  } finally {
    isLoading.value = false;
  }
};

const loadHistoryBookings = async () => {
  try {
    // TODO: 替換為實際的 API 調用
    // const response = await fetch(`/api/customers/${booking.value.customer_id}/boarding-history`);
    // const data = await response.json();
    // historyBookings.value = data;
    
    // 模擬歷史紀錄資料
    historyBookings.value = [
      {
        id: 1,
        booking_date: '2025/06/09',
        service_type: '住宿',
        room_type: '普通房',
        stay_duration: '1天',
        price: 800,
        store_note: '小型犬，容易緊張但可控制'
      },
      {
        id: 2,
        booking_date: '2025/06/02',
        service_type: '住宿',
        room_type: '普通房',
        stay_duration: '1天',
        price: 1200,
        store_note: '小型犬，容易緊張但可控制\n配合度佳，洗澡完成高\n下次可嘗試縮短修毛時間'
      }
    ];
    
  } catch (error) {
    console.error('載入歷史紀錄失敗:', error);
  }
};

const goBack = () => {
  router.go(-1);
};

// 格式化日期顯示
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
  const weekday = weekdays[date.getDay()];
  return `${dateStr} (週${weekday})`;
};

// 滾動到上一個記錄
const scrollToPrevious = () => {
  const container = document.querySelector('.history-container');
  container.scrollLeft -= 400;
};

// 滾動到下一個記錄
const scrollToNext = () => {
  const container = document.querySelector('.history-container');
  container.scrollLeft += 400;
};
</script>

<template>
  <div class="details-container">
    <div class="details-card">
      <!-- 載入狀態 -->
      <div v-if="isLoading" class="loading-state">
        <p>載入中...</p>
      </div>
      
      <!-- 主要內容 -->
      <div v-else>
        <!-- 顧客資訊卡片 -->
        <div class="customer-header">
          <h2 class="customer-title">顧客 {{ booking.customer_name }}</h2>
          <button @click="goBack" class="back-btn">返回前頁</button>
        </div>
        
        <div class="content-grid">
          <!-- 左側：顧客詳細資訊 -->
          <div class="left-section">
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
            
            <!-- 店家備註 -->
            <div class="store-note-section">
              <h3>店家備註</h3>
              <textarea 
                v-model="booking.store_note"
                placeholder="請輸入備註"
                class="store-note-textarea"
                readonly
              ></textarea>
            </div>
          </div>
          
          <!-- 右側：訂單資訊與服務明細 -->
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
            </div>
            
            <!-- 服務項目明細 -->
            <div class="service-detail-section">
              <h3>服務項目明細</h3>
              <div class="info-row">
                <label>服務項目：</label>
                <span>{{ booking.service_type }}</span>
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
                <label>預約天數：</label>
                <span>{{ booking.stay_duration }}</span>
              </div>
              <div class="info-row">
                <label>是否接送：</label>
                <span>{{ booking.pickup_delivery ? '是' : '否' }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 歷史預約紀錄 -->
        <div class="history-section">
          <h3 class="history-title">查看歷史預約紀錄</h3>
          
          <div class="history-wrapper">
            <button @click="scrollToPrevious" class="scroll-btn scroll-left">&lt;</button>
            
            <div class="history-container">
              <div 
                v-for="history in historyBookings" 
                :key="history.id"
                class="history-card"
              >
                <!-- 預約資訊 -->
                <div class="history-info">
                  <h4>預約資訊</h4>
                  <p>預約日期：{{ formatDate(history.booking_date) }}</p>
                </div>
                
                <!-- 服務項目明細 -->
                <div class="history-service">
                  <h4>服務項目明細</h4>
                  <p>服務項目：{{ history.service_type }}</p>
                  <p>預約房型：{{ history.room_type }}</p>
                  <p>預約天數：{{ history.stay_duration }}</p>
                  <p>訂單金額：NT${{ history.price }}</p>
                </div>
                
                <!-- 店家備註 -->
                <div class="history-note">
                  <h4>店家備註</h4>
                  <p>{{ history.store_note }}</p>
                </div>
              </div>
            </div>
            
            <button @click="scrollToNext" class="scroll-btn scroll-right">&gt;</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped src="../../../../styles/pages/Stores/Booking/Boarding/details.css"></style>