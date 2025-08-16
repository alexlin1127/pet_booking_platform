<script setup>
import { ref, computed } from "vue";

// 產生 00:00~23:45 每 15 分鐘的時段
const timeOptions = Array.from({ length: 24 * 4 }, (_, i) => {
  const h = String(Math.floor(i / 4)).padStart(2, "0");
  const m = String((i % 4) * 15).padStart(2, "0");
  return `${h}:${m}`;
});

const step = ref(1);
const form = ref({
  pet: "",
  pickup: "否",
  roomType: "",
  arrivalDate: "",
  arrivalTime: "",
  departureDate: "",
  departureTime: "",
  pricePlan: "",
  remark: "",
});

const estimatedTotal = computed(() => {
  if (!form.value.pricePlan) return 0;
  return Number(form.value.pricePlan);
});

function submitForm() {
  step.value = 2;
}

function resetForm() {
  step.value = 1;
}
</script>

<template>
  <div class="petstay-page">
    <div class="ps-content">
      <div v-if="step === 1" class="ps-card">
        <div class="ps-title">預約住宿服務</div>
        <form @submit.prevent="submitForm">
          <div class="grid grid-cols-1 gap-6">
            <!-- 選擇毛孩 -->
            <div>
              <label class="ps-label">選擇毛孩</label>
              <select v-model="form.pet" class="ps-select" required>
                <option value="">毛孩資料請先登錄</option>
                <option value="dog1">毛球（小型犬）</option>
                <option value="dog2">乖乖（新犬）</option>
              </select>
            </div>
            <!-- 是否送接服務 -->
            <div>
              <label class="ps-label">是否送接服務</label>
              <div class="flex gap-6 mt-1">
                <label>
                  <input
                    type="radio"
                    class="ps-radio"
                    v-model="form.pickup"
                    value="是"
                  />
                  是
                </label>
                <label>
                  <input
                    type="radio"
                    class="ps-radio"
                    v-model="form.pickup"
                    value="否"
                  />
                  否
                </label>
              </div>
            </div>
            <!-- 預約房型 -->
            <div>
              <label class="ps-label">選擇房型</label>
              <select v-model="form.roomType" class="ps-select" required>
                <option value="">請選擇房型</option>
                <option value="小型犬">小型犬</option>
                <option value="貓咪">貓咪</option>
              </select>
            </div>
            <!-- 到店日期與時間（同一行） -->
            <div class="ps-row">
              <div class="ps-col">
                <label class="ps-label">到店日期</label>
                <input
                  type="date"
                  v-model="form.arrivalDate"
                  class="ps-input"
                  required
                />
              </div>
              <div class="ps-col">
                <label class="ps-label">到店時間</label>
                <select v-model="form.arrivalTime" class="ps-select" required>
                  <option value="">請選擇時間</option>
                  <option
                    v-for="t in timeOptions"
                    :key="'arrive-' + t"
                    :value="t"
                  >
                    {{ t }}
                  </option>
                </select>
              </div>
            </div>
            <!-- 離店日期與時間（同一行） -->
            <div class="ps-row">
              <div class="ps-col">
                <label class="ps-label">離店日期</label>
                <input
                  type="date"
                  v-model="form.departureDate"
                  class="ps-input"
                  required
                />
              </div>
              <div class="ps-col">
                <label class="ps-label">離店時間</label>
                <select v-model="form.departureTime" class="ps-select" required>
                  <option value="">請選擇時間</option>
                  <option
                    v-for="t in timeOptions"
                    :key="'leave-' + t"
                    :value="t"
                  >
                    {{ t }}
                  </option>
                </select>
              </div>
            </div>
            <!-- 優惠方案純展示 -->
            <div>
              <label class="ps-label">優惠方案</label>
              <div class="ps-options-box">
                <ul class="ps-list">
                  <li>每晚 NT$ 1,200</li>
                  <li>長住 3 晚，每晚 NT$ 1,000</li>
                  <li>長住 1 個月，每晚 NT$ 800</li>
                </ul>
              </div>
            </div>
            <!-- 價格方案（如需選擇仍保留你的原欄位） -->
            <div>
              <label class="ps-label">價格方案（如有）</label>
              <select v-model="form.pricePlan" class="ps-select">
                <option value="">請選擇方案</option>
                <option value="1200">每晚 NT$ 1,200</option>
                <option value="1000">長住 3 晚，每晚 NT$ 1,000</option>
                <option value="800">長住 1 個月，每晚 NT$ 800</option>
              </select>
            </div>
            <!-- 備註 -->
            <div>
              <label class="ps-label">備註</label>
              <textarea
                v-model="form.remark"
                class="ps-textarea"
                rows="3"
                placeholder="如需優惠請於此欄填寫"
              ></textarea>
            </div>
          </div>
          <!-- 預估金額顯示 -->
          <div class="ps-total-box">
            本次住宿預估結總金額：<span
              class="font-bold text-lg text-[var(--accent-strong)]"
              >{{ estimatedTotal }} 元</span
            >
          </div>
          <button class="ps-book-btn" type="submit">確認預約</button>
        </form>
      </div>
      <!-- 完成預約畫面 -->
      <div v-else class="ps-finish-wrap">
        <div class="ps-finish-icon">
          <svg viewBox="0 0 24 24" fill="none">
            <circle
              cx="12"
              cy="12"
              r="11"
              stroke="#3bb272"
              stroke-width="2"
              fill="#e4f8ec"
            />
            <path
              d="M7 13l3 3 6-6"
              stroke="#3bb272"
              stroke-width="2.5"
              fill="none"
              stroke-linecap="round"
            />
          </svg>
        </div>
        <div class="ps-finish-title">完成預約</div>
        <div class="ps-finish-sub">感謝您的預約！<br />請等待店家審核</div>
        <button class="ps-finish-wait-btn" disabled>請等待店家審核</button>
        <div class="ps-finish-info-card">
          <div class="ps-finish-info-row"><span>顧客</span><b>王小明</b></div>
          <div class="ps-finish-info-row">
            <span>到店日期</span><b>{{ form.arrivalDate }}（週五）</b>
          </div>
          <div class="ps-finish-info-row">
            <span>到店時間</span><b>{{ form.arrivalTime }}</b>
          </div>
          <div class="ps-finish-info-row">
            <span>離店日期</span><b>{{ form.departureDate }}（週五）</b>
          </div>
          <div class="ps-finish-info-row">
            <span>離店時間</span><b>{{ form.departureTime }}</b>
          </div>
          <div class="ps-finish-info-row"><span>預約天數</span><b>1 天</b></div>
          <div class="ps-finish-info-row">
            <span>預約房間</span><b>{{ form.roomType }}</b>
          </div>
          <div class="ps-finish-info-row">
            <span>聯絡店家</span><b>03-81234567</b>
          </div>
        </div>
        <div class="ps-finish-coupon-card">
          <div class="ps-finish-coupon-label">本次使用註冊優惠</div>
          <div class="ps-finish-coupon-code">sfsd654xv46334</div>
        </div>
        <button class="ps-finish-btn" @click="resetForm">返回</button>
      </div>
    </div>
  </div>
</template>

<style scoped src="../../../styles/pages/Customers/Booking/boarding.css"></style>