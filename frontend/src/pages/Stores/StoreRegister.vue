<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import FormTemplate from '../../components/UI/FormTemplate.vue'

const route = useRoute()
const router = useRouter()
const currentStep = computed(() => route.params.step)

const nextStep = () => {
  const next = parseInt(currentStep.value) + 1
  router.push(`/register/stores/${next}`)
}

const quickRegister = () => {
  // 快速註冊邏輯（僅註冊帳號）
  console.log('快速註冊帳號')
  // 這裡可以加入快速註冊的 API 呼叫
  alert('帳號註冊成功！')
}

// 動態計算標題
const formTitle = computed(() => {
  return currentStep.value == '1' ? '店家註冊申請' : '填寫店家基本資料'
})

const form = ref({
  storeName: "",
  ownerName: "",
  city: "",
  district: "",
  address: "",
  email: "",
  services: [], // 服務項目 ['grooming', 'boarding']
  bookingType: "", // 單筆/多筆預約
  groomerCount: "", // 美容師人數
  boardingTypes: [], // 住宿類型 ['dog', 'cat']
  pickupService: "", // 接送服務
});

/* ---------- 縣市/行政區 ---------- */
const cities = [
  {
    value: "花蓮縣",
    districts: ["花蓮市", "吉安鄉", "新城鄉", "玉里鎮"],
  },
];

const selectedCity = computed(
  () => cities.find((c) => c.value === form.value.city)?.districts ?? []
);

/* ---------- 檔案上傳 ---------- */
const files = ref({
  license: [],
  dogLicense: [],
  catLicense: [],
});

function onPick(key, e) {
  files.value[key] = Array.from(e.target.files ?? []).map((f) => ({
    name: f.name,
    size: f.size,
    url: URL.createObjectURL(f),
    file: f,
  }));
}

function viewFile(key) {
  if (files.value[key] && files.value[key][0]) {
    window.open(files.value[key][0].url, '_blank');
  }
}

/* ---------- 送出 ---------- */
function submit() {
  const required = [
    "storeName",
    "ownerName",
    "city",
    "district",
    "address",
    "email",
  ];
  const missed = required.filter((k) => !form.value[k]);
  if (missed.length) {
    alert("請填寫完整必填欄位");
    return;
  }
  console.log("payload =>", { ...form.value, files: files.value });
  alert("已送出審核！");
  router.push("/admin/stores/manage");
}
</script>

<template>
  <div class="shops-page min-h-screen bg-gray-50 py-8">
    <FormTemplate :title="formTitle" @submit="handleSubmit">
      <!-- 第一步表單內容 -->
      <div v-if="currentStep == '1'">
        <div class="mb-4">
          <label class="storereview-label">帳號 *</label>
          <input type="tel" class="storereview-input">
        </div>
        <div class="mb-4">
          <label class="storereview-label">密碼 *</label>
          <input type="password" class="storereview-input">
        </div>
        <div class="mb-4">
          <label class="storereview-label">確認密碼 *</label>
          <input type="password" class="storereview-input">
        </div>
      </div>

      <!-- 第二步表單內容 -->
      <div v-else-if="currentStep == '2'">
        <div class="storereview-container">
          <form class="storereview-form" @submit.prevent="submit">
            <!-- 1. 店家名稱／負責人 -->
            <div class="storereview-form-row">
              <div>
                <label class="storereview-label">貴店名稱 *</label>
                <input v-model="form.storeName" type="text" class="storereview-input" placeholder="請輸入貴店名稱" required />
              </div>
              <div>
                <label class="storereview-label">負責人姓名 *</label>
                <input v-model="form.ownerName" type="text" class="storereview-input" placeholder="請輸入負責人姓名" required />
              </div>
            </div>

            <!-- 2. 所在地 -->
            <div>
              <label class="storereview-label">貴店地址 *</label>
              <div class="storereview-address-row">
                <select v-model="form.city" class="storereview-input-cites" required>
                  <option value="" disabled>縣市</option>
                  <option v-for="c in cities" :key="c.value" :value="c.value">
                    {{ c.value }}
                  </option>
                </select>
                <select v-model="form.district" :disabled="!form.city" class="storereview-input-townships" required>
                  <option value="" disabled>鄉鎮市區</option>
                  <option v-for="d in selectedCity" :key="d" :value="d">
                    {{ d }}
                  </option>
                </select>
                <input v-model="form.address" type="text" class="storereview-input storereview-address-input" placeholder="請輸入詳細地址" required />
              </div>
            </div>

            <!-- 3. 信箱 -->
            <div>
              <label class="storereview-label">信箱 *</label>
              <input v-model="form.email" type="email" class="storereview-input" placeholder="請輸入信箱" required />
            </div>

            <!-- 服務項目（可複選） -->
            <div>
              <p class="storereview-label storereview-label-service">服務項目（可複選） *</p>
              <div class="storereview-checkbox-row">
                <label class="storereview-checkbox-label">
                  <input v-model="form.services" type="checkbox" value="grooming" class="storereview-radio" />
                  <span>美容</span>
                </label>
                <label class="storereview-checkbox-label">
                  <input v-model="form.services" type="checkbox" value="boarding" class="storereview-radio" />
                  <span>住宿</span>
                </label>
              </div>
            </div>

            <!-- 美容相關欄位 -->
            <template v-if="form.services.includes('grooming')">
              <div class="storereview-grooming-row">
                <div>
                  <span class="storereview-label mb-2">同一時段允許單筆或多筆預約 *</span>
                  <div class="storereview-pickup-row">
                    <label class="storereview-checkbox-label">
                      <input v-model="form.bookingType" type="radio" value="single" class="storereview-radio" />
                      <span>單筆</span>
                    </label>
                    <label class="storereview-checkbox-label">
                      <input v-model="form.bookingType" type="radio" value="multiple" class="storereview-radio" />
                      <span>多筆</span>
                    </label>
                  </div>
                </div>
                <div class="storereview-groomer-count-row">
                  <label class="storereview-label mb-0 mr-2">店內美容師人數 *</label>
                  <select v-model="form.groomerCount" class="storereview-input-cites" required>
                    <option value="" disabled>請選擇</option>
                    <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
                  </select>
                </div>
                <!-- 是否接送 -->
                <div>
                  <p class="storereview-label mb-2">是否提供接送服務 *</p>
                  <div class="storereview-pickup-row">
                    <label class="storereview-checkbox-label">
                      <input v-model="form.pickupService" type="radio" value="yes" class="storereview-radio" />
                      <span>是</span>
                    </label>
                    <label class="storereview-checkbox-label">
                      <input v-model="form.pickupService" type="radio" value="no" class="storereview-radio" />
                      <span>否</span>
                    </label>
                  </div>
                </div>
              </div>
            </template>

            <!-- 住宿相關欄位 -->
            <template v-if="form.services.includes('boarding')">
              <div>
                <p class="storereview-label mb-2">寵物住宿類型（可複選） *</p>
                <div class="storereview-checkbox-row">
                  <label class="storereview-checkbox-label">
                    <input v-model="form.boardingTypes" type="checkbox" value="dog" class="storereview-radio" />
                    <span>狗狗</span>
                  </label>
                  <label class="storereview-checkbox-label">
                    <input v-model="form.boardingTypes" type="checkbox" value="cat" class="storereview-radio" />
                    <span>貓咪</span>
                  </label>
                </div>
              </div>

              <!-- 狗狗證照 -->
              <div v-if="form.boardingTypes.includes('dog')" class="storereview-license-row">
                <label class="storereview-label mb-0">特定寵物業許可證(狗) *</label>
                <input ref="dogLicenseInput" type="file" accept="image/*" class="hidden"
                  @change="(e) => onPick('dogLicense', e)" />
                <button type="button" class="upload-img-btn" @click="$refs.dogLicenseInput.click()">上傳圖片</button>
              </div>
              <template v-if="form.boardingTypes.includes('dog') && files.dogLicense && files.dogLicense.length">
                <div class="storereview-file-row">
                  <span>{{ files.dogLicense[0].name }}</span>
                  <button type="button" class="underline text-blue-600" @click="viewFile('dogLicense')">查看</button>
                </div>
              </template>
              
              <!-- 貓咪證照 -->
              <div v-if="form.boardingTypes.includes('cat')" class="storereview-license-row">
                <label class="storereview-label mb-0">特定寵物業許可證(貓) *</label>
                <input ref="catLicenseInput" type="file" accept="image/*" class="hidden"
                  @change="(e) => onPick('catLicense', e)" />
                <button type="button" class="upload-img-btn" @click="$refs.catLicenseInput.click()">上傳圖片</button>
              </div>
              <template v-if="form.boardingTypes.includes('cat') && files.catLicense && files.catLicense.length">
                <div class="storereview-file-row">
                  <span>{{ files.catLicense[0].name }}</span>
                  <button type="button" class="underline text-blue-600" @click="viewFile('catLicense')">查看</button>
                </div>
              </template>
            </template>

            <!-- 營業登記 -->
            <div class="storereview-license-row">
              <label class="storereview-label mb-0">營業登記資料</label>
              <input ref="licenseInput" type="file" accept="image/*" class="hidden"
                @change="(e) => onPick('license', e)" />
              <button type="button" class="upload-img-btn" @click="$refs.licenseInput.click()">上傳圖片</button>
            </div>

            <template v-if="files.license && files.license.length">
              <div class="storereview-file-row">
                <span>{{ files.license[0].name }}</span>
                <button type="button" class="underline text-blue-600" @click="viewFile('license')">查看</button>
              </div>
            </template>
          </form>
        </div>
      </div>

      <template #actions>
        <template v-if="currentStep != '2'">
          <div class="store-regist-btn-row">
            <button type="button" class="store-regist-btn" @click="quickRegister">
              快速註冊帳號
            </button>
            <button type="button" class="store-regist-btn" @click="nextStep">
              繼續填寫基本資訊
            </button>
          </div>
        </template>
        <template v-else>
          <div class="store-regist-btn-center-row">
            <button type="submit" class="store-regist-btn-center">
              送出審核
            </button>
          </div>
        </template>
      </template>
    </FormTemplate>
  </div>
</template>