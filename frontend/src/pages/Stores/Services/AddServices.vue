<script setup lang="ts">
import { computed, ref, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../../../api/api";

type Mode = "add" | "edit" | "view";
type SrvType = "grooming" | "lodging";
type Pet = "dog" | "cat";

const route = useRoute();
const router = useRouter();

// --- Mode ---
const mode = computed<Mode>(() => {
  const p = route.path;
  if (p.includes("/add")) return "add";
  if (p.includes("/edit")) return "edit";
  return "view";
});

// --- Type & Pet ---
const type = ref<SrvType>((route.params.type as SrvType) || "lodging");
const pet = ref<Pet>((route.params.pet as Pet) || "dog");

// --- Computed flags ---
const lockType = computed(() => mode.value !== "add");
const isView = computed(() => mode.value === "view");
const isLodging = computed(() => type.value === "lodging");

// --- Page title / button text ---
const pageTitle = computed(() => {
  const action =
    mode.value === "add" ? "新增" : mode.value === "edit" ? "修改" : "查看";
  const petText = pet.value === "dog" ? "狗" : "貓";
  const srvText = type.value === "grooming" ? "美容" : "住宿";
  return `${action}${petText}${srvText}服務項目`;
});
const submitText = computed(() => (mode.value === "add" ? "新增" : "完成"));

// --- Lodging reactive object ---
const lodging = reactive({
  cleaning_frequency: "",
  cleaning_note: "", //其他清潔說明
  room_type: "",
  room_count: 0,
  pet_available_amount: 1,
  pricings: [
    {
      _key: cryptoRandom(),
      duration: 1,
      duration_unit: "day",
      pricing: 0,
      overtime_rate: 0,
      overtime_charging: false,
    },
  ],
  introduction: "",
  notice: "",
});

// --- Lodging price functions ---
function addRoomPrice() {
  lodging.pricings.push({
    _key: cryptoRandom(),
    duration: 1,
    duration_unit: "day",
    pricing: 0,
    overtime_rate: 0,
    overtime_charging: false,
  });
}
function removePricing(idx: number) {
  lodging.pricings.splice(idx, 1);
}

// --- Grooming object ---
const grooming = reactive({
  service_title: "",
  introduction: "",
  notice: "",
  pricings: [
    {
      _key: cryptoRandom(),
      fur_amount: "none",
      pet_size: "small",
      grooming_duration: 0, // 以分鐘為單位
      hours: 0, // 新增小時屬性
      mins: 0, // 新增分鐘屬性
      pricing: 0,
    },
  ],
});
function addChargeRow() {
  grooming.pricings.push({
    _key: cryptoRandom(),
    fur_amount: "none",
    pet_size: "small",
    grooming_duration: 0,
    hours: 0,
    mins: 0,
    pricing: 0,
  });
}
function removeChargeRow(idx: number) {
  grooming.pricings.splice(idx, 1);
}

// --- Utilities ---
function cryptoRandom() {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

function goBack() {
  router.back();
}

// 定義 cleaning_frequency 中文
const cleaningFrequencyMap = {
  weekly: "每週一次",
  biweekly: "每兩週一次",
  halfmonth: "每半月一次",
  other: "其他",
};

// --- Submit function ---
async function submit() {
  const payload = isLodging.value
    ? {
        species: pet.value,
        cleaning_frequency:
          lodging.cleaning_frequency === "other"
            ? lodging.cleaning_note
            : cleaningFrequencyMap[lodging.cleaning_frequency],
        room_type: lodging.room_type,
        room_count: lodging.room_count,
        pet_available_amount: lodging.pet_available_amount,
        introduction: lodging.introduction,
        notice: lodging.notice,
        pricings: lodging.pricings.map((p) => ({
          duration: p.duration,
          duration_unit: p.duration_unit,
          pricing: p.pricing,
          overtime_rate: p.overtime_rate,
          overtime_charging: p.overtime_charging,
        })),
      }
    : {
        species: pet.value,
        service_title: grooming.service_title,
        introduction: grooming.introduction,
        notice: grooming.notice,
        pricings: grooming.pricings.map((r) => ({
          fur_amount: r.fur_amount,
          pet_size: r.pet_size,
          grooming_duration: r.hours * 60 + r.mins, // 計算總分鐘數
          pricing: r.pricing,
        })),
      };

  try {
    const apiPath = isLodging.value
      ? "/store/boarding_services"
      : "/store/grooming_services";
    const response = await api.post(apiPath, payload);
    console.log("API response:", response.data);
    router.back();
  } catch (error) {
    console.error("API error:", error);
    alert("提交失敗，請稍後再試。");
  }
}
</script>
<template>
  <div class="storeservices-page">
    <div class="ss-container">
      <h1 class="block-title">{{ pageTitle }}</h1>

      <!-- 基本：毛孩類別、服務項目 -->
      <section class="ss-card">
        <div class="ss-card-inner">
          <!-- 毛孩類別 -->
          <label class="ss-label">毛孩類別 *</label>
          <div class="ss-radio-group">
            <label>
              <input
                class="ss-radio"
                type="radio"
                value="dog"
                v-model="pet"
                :disabled="isView"
              />
              狗狗
            </label>
            <label>
              <input
                class="ss-radio"
                type="radio"
                value="cat"
                v-model="pet"
                :disabled="isView"
              />
              貓貓
            </label>
          </div>

          <!-- 服務項目 -->
          <div class="mt-4">
            <label class="ss-label">服務項目 *</label>
            <div class="ss-radio-group">
              <label>
                <input
                  class="ss-radio"
                  type="radio"
                  value="grooming"
                  v-model="type"
                  :disabled="lockType || isView"
                />
                美容
              </label>
              <label>
                <input
                  class="ss-radio"
                  type="radio"
                  value="lodging"
                  v-model="type"
                  :disabled="lockType || isView"
                />
                住宿
              </label>
            </div>
          </div>
        </div>
      </section>

      <!-- Lodging：清潔與消毒 + 房型設定 + 住宿介紹 -->
      <template v-if="isLodging">
        <!-- 清潔與消毒 -->
        <section class="ss-card">
          <div class="ss-card-inner">
            <label class="ss-label">清潔與消毒 *</label>
            <div class="ss-radio-group">
              <label>
                <input
                  class="ss-radio"
                  type="radio"
                  value="weekly"
                  v-model="lodging.cleaning_frequency"
                  :disabled="isView"
                />
                每週清潔
              </label>
              <label>
                <input
                  class="ss-radio"
                  type="radio"
                  value="biweekly"
                  v-model="lodging.cleaning_frequency"
                  :disabled="isView"
                />
                每兩週清潔
              </label>
              <label>
                <input
                  class="ss-radio"
                  type="radio"
                  value="halfmonth"
                  v-model="lodging.cleaning_frequency"
                  :disabled="isView"
                />
                每半月清潔
              </label>
              <label class="ss-line">
                <input
                  class="ss-radio"
                  type="radio"
                  value="other"
                  v-model="lodging.cleaning_frequency"
                  :disabled="isView"
                />
                其他
                <input
                  class="ss-input is-name"
                  placeholder="請輸入內容"
                  v-model="lodging.cleaning_note"
                  :disabled="isView || lodging.cleaning_frequency !== 'other'"
                />
              </label>
            </div>

            <!-- 房型名稱 + 房間數 -->
            <div class="ss-line">
              <div class="unit">房型名稱</div>
              <input
                class="ss-input is-name"
                placeholder="請輸入內容"
                v-model="lodging.room_type"
                :disabled="isView"
              />

              <div class="unit">房間數數量</div>
              <button
                class="ss-mini"
                @click="lodging.room_count--"
                :disabled="isView || lodging.room_count <= 0"
              >
                -
              </button>
              <input
                class="ss-input is-count"
                v-model.number="lodging.room_count"
                type="number"
                min="0"
                :disabled="isView"
              />
              <button
                class="ss-mini"
                @click="lodging.room_count++"
                :disabled="isView"
              >
                +
              </button>
              <div class="unit">間</div>
              <div class="unit">可容納寵物數量</div>
              <input
                class="ss-input is-count"
                v-model.number="lodging.pet_available_amount"
                type="number"
                min="0"
                :disabled="isView"
              />
              <div class="unit">隻</div>
            </div>
          </div>
        </section>

        <!-- 價格設定 -->
        <section class="ss-card">
          <div class="ss-card-inner">
            <label class="ss-label">價格設定 *</label>

            <div
              v-for="(price, idx) in lodging.pricings"
              :key="price._key"
              class="ss-row"
            >
              <div class="ss-line">
                <div class="unit unit-strong">價格設定</div>
                <div class="unit">住</div>
                <input
                  class="ss-input is-count"
                  type="number"
                  min="1"
                  v-model.number="price.duration"
                  :disabled="isView"
                />
                <select
                  class="ss-select is-count"
                  v-model="price.duration_unit"
                  :disabled="isView"
                >
                  <option value="day">天</option>
                  <option value="month">月</option>
                </select>

                <div class="unit">每晚價格：</div>
                <input
                  class="ss-input is-price"
                  type="number"
                  min="0"
                  placeholder="金額"
                  v-model.number="price.pricing"
                  :disabled="isView"
                />
                <div class="unit">元</div>
              </div>

              <div class="ss-line">
                <div class="unit unit-strong">超時收費 *</div>
                <div class="unit">每小時：</div>
                <input
                  class="ss-input is-price"
                  type="number"
                  min="0"
                  placeholder="金額"
                  v-model.number="price.overtime_rate"
                  :disabled="isView || price.overtime_charging"
                />
                <div class="unit">元</div>

                <label class="ss-line">
                  <input
                    class="ss-checkbox"
                    type="checkbox"
                    v-model="price.overtime_charging"
                    :disabled="isView"
                  />
                  不加收
                </label>
              </div>

              <button
                v-if="!isView"
                class="ss-icon-btn"
                title="刪除價格"
                @click="removePricing(idx)"
              >
                ×
              </button>
            </div>

            <div class="ss-line" v-if="!isView">
              <button class="btn-primary" @click="addRoomPrice">
                新增價格
              </button>
            </div>
          </div>
        </section>

        <!-- 住宿介紹 -->
        <section class="ss-card">
          <div class="ss-card-inner">
            <label class="ss-label">住宿介紹 *</label>
            <textarea
              class="ss-textarea"
              v-model="lodging.introduction"
              :disabled="isView"
            ></textarea>
          </div>
        </section>
        <!-- 注意事項 -->
        <section class="ss-card">
          <div class="ss-card-inner">
            <label class="ss-label">注意事項</label>
            <textarea
              class="ss-textarea"
              v-model="lodging.notice"
              :disabled="isView"
            ></textarea>
          </div>
        </section>
      </template>

      <!-- Grooming：服務細項 + 收費標準 + 服務簡介 + 注意事項 -->
      <template v-else>
        <section class="ss-card">
          <div class="ss-card-inner">
            <label class="ss-label">服務細項 *</label>
            <div class="ss-line">
              <input
                class="ss-input is-name"
                placeholder="請輸入更新的服務 / 服務名稱"
                v-model="grooming.service_title"
                :disabled="isView"
              />
            </div>
          </div>
        </section>

        <section class="ss-card">
          <div class="ss-card-inner">
            <label class="ss-label">收費標準 *</label>

            <div class="ss-dashed">
              <div class="ss-group-title">設定收費標準</div>

              <div
                v-for="(row, idx) in grooming.pricings"
                :key="row._key"
                class="ss-row"
              >
                <div class="ss-line">
                  <div class="unit">請選擇寵物毛量、體型、服務時長及價格</div>

                  <select
                    class="ss-select is-count"
                    v-model="row.fur_amount"
                    :disabled="isView"
                  >
                    <option value="none">無毛</option>
                    <option value="short">短毛</option>
                    <option value="medium">中毛</option>
                    <option value="long">長毛</option>
                  </select>

                  <select
                    class="ss-select is-count"
                    v-model="row.pet_size"
                    :disabled="isView"
                  >
                    <option value="small">小型</option>
                    <option value="medium">中型</option>
                    <option value="large">大型</option>
                  </select>

                  <input
                    class="ss-input is-count"
                    type="number"
                    min="0"
                    v-model.number="row.hours"
                    :disabled="isView"
                  />
                  <div class="unit">時</div>
                  <input
                    class="ss-input is-count"
                    type="number"
                    min="0"
                    v-model.number="row.mins"
                    :disabled="isView"
                  />
                  <div class="unit">分</div>

                  <div class="unit">價格：</div>
                  <input
                    class="ss-input is-price"
                    type="number"
                    min="0"
                    placeholder="金額"
                    v-model.number="row.pricing"
                    :disabled="isView"
                  />
                  <div class="unit">元</div>
                </div>

                <button
                  v-if="!isView"
                  class="ss-icon-btn"
                  title="刪除"
                  @click="removeChargeRow(idx)"
                >
                  ×
                </button>
              </div>

              <div class="ss-line" v-if="!isView">
                <button class="btn-ghost" @click="addChargeRow">新增</button>
              </div>
            </div>
          </div>
        </section>

        <section class="ss-card">
          <div class="ss-card-inner">
            <label class="ss-label">服務簡介 *</label>
            <textarea
              class="ss-textarea"
              placeholder="請輸入服務簡介"
              v-model="grooming.introduction"
              :disabled="isView"
            ></textarea>
          </div>
        </section>

        <section class="ss-card">
          <div class="ss-card-inner">
            <label class="ss-label">注意事項</label>
            <textarea
              class="ss-textarea"
              placeholder="請輸入注意事項"
              v-model="grooming.notice"
              :disabled="isView"
            ></textarea>
          </div>
        </section>
      </template>

      <!-- 底部按鈕 -->
      <div class="btn-area">
        <button class="btn-ghost" @click="goBack">
          {{ isView ? "返回" : "取消" }}
        </button>
        <button class="btn-primary" v-if="!isView" @click="submit">
          {{ submitText }}
        </button>
      </div>
    </div>
  </div>
</template>
