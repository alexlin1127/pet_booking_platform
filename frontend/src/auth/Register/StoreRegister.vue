<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import FormTemplate from '../../components/UI/FormTemplate.vue'
// import ModalBox from '../../components/UI/ModalBox.vue'

const route = useRoute()
const router = useRouter()
const currentStep = computed(() => route.params.step)
const status = computed(() => route.params.status ?? "pending");

const agreePrivacy = ref(false)
const isDisabled = computed(() => {
  // 第二步才需要勾選隱私政策
  return currentStep.value == '2' && !agreePrivacy.value
})

const nextStep = () => {
  const next = parseInt(currentStep.value) + 1
  router.push(`/register/shops/${next}`)
}

const submitForm = () => {
  // 送出審核邏輯
  console.log('送出審核')
}

// 動態計算標題和按鈕文字
const formTitle = computed(() => {
  return currentStep.value == '1' ? '店家註冊申請' : '填寫店家基本資料'
})

const buttonText = computed(() => {
  return currentStep.value == '1' ? '下一步' : '送出審核'
})

const handleSubmit = () => {
  if (currentStep.value == '1') {
    nextStep()
  }
  else {
    submitForm()
  }
}


const form = ref({
  storeName: "",
  ownerName: "",
  city: "",
  district: "",
  address: "",
  businessId: "",
  provideOnsite: "no",
  services: [],
  otherService: "",
  intro: "",
  serviceNotes: "",
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

/* ---------- 服務項目 ---------- */
const serviceLeft = ["洗澡", "美容剪毛", "指甲修剪", "清潔護理", "接送服務"];
const serviceRight = [
  "造型染色",
  "深層護理／SPA",
  "寵物旅館（寄宿）",
  "幼犬照護",
];

/* ---------- 檔案上傳（示範） ---------- */
const files = ref({
  exterior: [],
  license: [],
  serviceShots: [],
  traffic: [],
  priceList: [],
});
function onPick(key, e) {
  files.value[key] = Array.from(e.target.files ?? []).map((f) => ({
    name: f.name,
    size: f.size,
  }));
}

/* ---------- 送出 ---------- */
function submit() {
  const required = [
    "storeName",
    "ownerName",
    "city",
    "district",
    "address",
    "businessId",
  ];
  const missed = required.filter((k) => !form.value[k]);
  if (missed.length) {
    alert("請填寫完整必填欄位");
    return;
  }
  console.log("payload =>", { ...form.value, files: files.value });
  alert("已送出審核！");
  router.push("/Admin/Store/Manage");
}
</script>

<template>
  <div class="shops-page min-h-screen bg-gray-50 py-8">
    <FormTemplate :title="formTitle" @submit="handleSubmit">
      <!-- 第一步表單內容 -->
      <div v-if="currentStep == '1'">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">帳號 *</label>
          <input type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">密碼 *</label>
          <input type="tel"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">確認密碼 *</label>
          <input type="tel"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
      </div>

      <!-- 第二步表單內容 -->
      <div v-else-if="currentStep == '2'">
        <div class="storereview-container">
          <form class="mx-auto max-w-2xl space-y-8" @submit.prevent="submit">
            <!-- 1. 店家名稱／負責人 -->
            <div class="grid grid-cols-1 gap-6">
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
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <select v-model="form.city" class="storereview-input" required>
                  <option value="" disabled>請選擇縣市</option>
                  <option v-for="c in cities" :key="c.value" :value="c.value">
                    {{ c.value }}
                  </option>
                </select>
                <select v-model="form.district" :disabled="!form.city" class="storereview-input" required>
                  <option value="" disabled>請選擇區域</option>
                  <option v-for="d in selectedCity" :key="d" :value="d">
                    {{ d }}
                  </option>
                </select>
                <input v-model="form.address" type="text" class="storereview-input" placeholder="請輸入詳細地址" required />
              </div>
            </div>

            <!-- 3. 地址 / 統編 -->
            <div>
              <label class="storereview-label">信箱 *</label>
              <input v-model="form.email" type="email" class="storereview-input" placeholder="請輸入詳細地址" required />
            </div>
            <div>
              <label class="storereview-label">營業登記事號（或統編） *</label>
              <input v-model="form.businessId" type="text" class="storereview-input" placeholder="例：12345678"
                required />
            </div>

            <!-- 4. 是否到府 -->
            <div>
              <p class="storereview-label mb-2">是否提供到府服務 *</p>
              <div class="flex items-center gap-6">
                <label class="inline-flex items-center gap-2">
                  <input v-model="form.provideOnsite" type="radio" value="yes" class="storereview-radio" />
                  <span>是</span>
                </label>
                <label class="inline-flex items-center gap-2">
                  <input v-model="form.provideOnsite" type="radio" value="no" class="storereview-radio" />
                  <span>否</span>
                </label>
              </div>
            </div>

            <div>
              <p class="storereview-label mb-2">服務項目（可複選） *</p>
              <div class="flex items-center gap-6">
                <label class="inline-flex items-center gap-2">
                  <input v-model="form.provideOnsite" type="radio" value="yes" class="storereview-radio" />
                  <span>美容</span>
                </label>
                <label class="inline-flex items-center gap-2">
                  <input v-model="form.provideOnsite" type="radio" value="no" class="storereview-radio" />
                  <span>住宿</span>
                </label>
              </div>
            </div>




            <!-- 5. 服務內容 -->
            <div>
              <p class="storereview-label mb-3">服務內容（可複選） *</p>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-10 gap-y-3">
                <label v-for="s in serviceLeft" :key="s" class="inline-flex items-center gap-2">
                  <input type="checkbox" class="storereview-checkbox" :value="s" v-model="form.services" />
                  <span>{{ s }}</span>
                </label>
                <label v-for="s in serviceRight" :key="s" class="inline-flex items-center gap-2">
                  <input type="checkbox" class="storereview-checkbox" :value="s" v-model="form.services" />
                  <span>{{ s }}</span>
                </label>

                <!-- 其他 -->
                <div class="sm:col-span-2 flex items-center gap-2">
                  <label class="inline-flex items-center gap-2">
                    <input type="checkbox" class="storereview-checkbox" value="其他" v-model="form.services" />
                    <span>其他</span>
                  </label>
                  <input v-model="form.otherService" type="text" class="storereview-input flex-1"
                    placeholder="請填寫其他服務" />
                </div>
              </div>
            </div>

            <!-- 6. 簡介 / 備註 -->
            <div>
              <label class="storereview-label">店家簡介</label>
              <textarea v-model="form.intro" rows="5" class="storereview-textarea"
                placeholder="請輸入 200 字以內簡介"></textarea>
            </div>
            <div>
              <label class="storereview-label">提供更多服務說明</label>
              <textarea v-model="form.serviceNotes" rows="5" class="storereview-textarea"
                placeholder="注意事項、加價規則、接送範圍…"></textarea>
            </div>

            <!-- 7. 上傳區塊 -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <p class="storereview-label mb-2">店舖外觀照</p>
                <input type="file" class="storereview-input" multiple @change="(e) => onPick('exterior', e)" />
                <ul class="mt-2 text-sm text-gray-600 space-y-1">
                  <li v-for="f in files.exterior" :key="f.name">• {{ f.name }}</li>
                </ul>
              </div>

              <div>
                <p class="storereview-label mb-2">營業登記／執照</p>
                <input type="file" class="storereview-input" multiple @change="(e) => onPick('license', e)" />
                <ul class="mt-2 text-sm text-gray-600 space-y-1">
                  <li v-for="f in files.license" :key="f.name">• {{ f.name }}</li>
                </ul>
              </div>

              <div>
                <p class="storereview-label mb-2">服務項目照片</p>
                <input type="file" class="storereview-input" multiple @change="(e) => onPick('serviceShots', e)" />
                <ul class="mt-2 text-sm text-gray-600 space-y-1">
                  <li v-for="f in files.serviceShots" :key="f.name">
                    • {{ f.name }}
                  </li>
                </ul>
              </div>

              <div>
                <p class="storereview-label mb-2">交通／位置資訊</p>
                <input type="file" class="storereview-input" multiple @change="(e) => onPick('traffic', e)" />
                <ul class="mt-2 text-sm text-gray-600 space-y-1">
                  <li v-for="f in files.traffic" :key="f.name">• {{ f.name }}</li>
                </ul>
              </div>

              <div class="sm:col-span-2">
                <p class="storereview-label mb-2">服務價目表（圖或 PDF）</p>
                <input type="file" class="storereview-input" multiple @change="(e) => onPick('priceList', e)" />
                <ul class="mt-2 text-sm text-gray-600 space-y-1">
                  <li v-for="f in files.priceList" :key="f.name">• {{ f.name }}</li>
                </ul>
              </div>
            </div>

            <!-- 8. 送出 -->
            <div class="pt-4">
              <button type="submit" class="storereview-btn w-full sm:w-40">
                送出審核
              </button>
            </div>
          </form>
        </div>

        <div class="mb-4 text-center">
          <label>
            <input type="checkbox" class="cursor-pointer" v-model="agreePrivacy" />
            我同意隱私政策
          </label>
        </div>
      </div>
      <template #actions>
        <button type="submit" class="form-regist-btn" :disabled="isDisabled">
          {{ buttonText }}
        </button>
      </template>
    </FormTemplate>
  </div>
</template>