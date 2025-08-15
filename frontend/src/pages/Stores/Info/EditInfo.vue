<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
import api from "../../../api/api.js";

const userId = ref(null);

onMounted(async () => {
  try {
    const response = await api.get("/users/me");
    userId.value = response.data.id;
    console.log("User ID fetched:", userId.value);
  } catch (error) {
    // console.error("Error fetching user data:", error);
  }
});

const form = ref({
  name: "",
  address: { county: "", district: "", detail: "" },
  phone: "",
  hours: "",
  services: "",
  traffic_info: "",
  description: "",
  facebook_link: "",
  line_link: "",
  google_map_link: "",
});
const pick_up_service = ref(true); //接送服務
const grooming_service = ref(true); //美容服務
const boarding_service = ref(false); //住宿服務
const boarding_pet_type = ref([]); // 住宿類型
const imageNote = ref(""); // 圖片說明
const imagesToUpload = ref([]); // 用於存儲待上傳的圖片文件
const heroImage = ref(null); // 用於存儲封面圖片

const submitForm = () => {
  console.log({
    pick_up_service: pick_up_service.value,
    grooming_service: grooming_service.value,
    boarding_service: boarding_service.value,
    boarding_pet_type: boarding_pet_type.value,
    imageNote: imageNote.value,
  });
};
//圖片管理區
const fileInput = ref(null); //綁定 HTML <input type="file"> 的 DOM可以用 fileInput.value.click() 來程式化開啟檔案選擇視窗
// 圖片區
const images = ref([]);
const handleFiles = (e) => {
  const files = Array.from(e.target.files || []);
  if (!files.length) return;

  const remain = 9 - imagesToUpload.value.length; // 限制圖片數量
  const toAdd = files.slice(0, remain);

  toAdd.forEach((file) => {
    const url = URL.createObjectURL(file);
    images.value.push(url); // 即時渲染圖片
    imagesToUpload.value.push(file); // 存入待上傳的圖片文件
  });

  // 將第一張圖片的 URL 存為 hero_image
  if (images.value.length > 0) {
    form.value.hero_image = images.value[0];
  }

  e.target.value = ""; // 清空檔案選擇器
};

//營業時間
/* 時間下拉：每 30 分一格（可改） */
/* length: 48 → 代表一天要切成 48 格（因為 24 小時 × 每小時 2 格 = 48）
  i / 2 → 因為每小時有兩格（:00 和 :30），除以 2 就能得到小時數
  Math.floor() → 去掉小數
  String(...).padStart(2, '0') → 小時補 0，讓 9 變成 09
*/
const timeOptions = Array.from({ length: 48 }, (_, i) => {
  const h = String(Math.floor(i / 2)).padStart(2, "0");
  const m = i % 2 ? "30" : "00";
  return `${h} : ${m}`;
});

const daily_opening_time = ref("09 : 00");
const daily_closing_hours = ref("17 : 00");

/* 公休 */
const weekdays = [
  { value: "星期一", label: "星期一" },
  { value: "星期二", label: "星期二" },
  { value: "星期三", label: "星期三" },
  { value: "星期四", label: "星期四" },
  { value: "星期五", label: "星期五" },
  { value: "星期六", label: "星期六" },
  { value: "星期日", label: "星期日" },
];
const close_day = ref([]); // 例： [1,3,7]

/* 服務項目（標籤）固定清單，用來顯示建議按鈕 */
const serviceOptions = [
  "寵物美容",
  "美容剪毛",
  "SPA護理",
  "寵物洗澡",
  "貓咪專區",
  "造型美容",
];

const selectedServices = ref([]);
// 輸入框的文字（用於自訂新增服務項目）
const tagInput = ref("");

const addService = (name) => {
  if (!name) return; //名稱是空的，就直接跳出（不新增）
  if (selectedServices.value.length >= 20) return; //  如果已達 20 個上限，就不新增
  if (!selectedServices.value.includes(name)) {
    // 如果目前還沒有這個項目
    selectedServices.value.push(name); // 加到已選清單中
  }
};

const addFromInput = () => {
  const val = tagInput.value.trim(); // 去掉輸入前後的空白
  if (!val) return; // 如果輸入是空的，就不新增
  addService(val); // 新增到已選清單selectedServices
  tagInput.value = ""; // 新增後清空輸入框
};
// 移除指定索引的服務項目
const removeService = (idx) => selectedServices.value.splice(idx, 1);

const formatTime = (time) => {
  return time.replace(/\s/g, ""); // 移除空格，確保格式為 hh:mm
};

//確認修改送出
const updateStoreInfo = async () => {
  // 表單驗證
  if (
    !form.value.name ||
    !form.value.phone ||
    !form.value.address.county ||
    !form.value.address.district ||
    !form.value.address.detail
  ) {
    alert("請填寫完整的店家資訊！");
    return;
  }

  try {
    const formData = new FormData();

    // 一般欄位
    formData.append("name", form.value.name);
    formData.append("phone", form.value.phone);
    formData.append("address", JSON.stringify(form.value.address)); // 物件要轉成字串
    formData.append("traffic_info", form.value.traffic_info);
    formData.append("description", form.value.description);
    formData.append("facebook_link", form.value.facebook_link);
    formData.append("line_link", form.value.line_link);
    formData.append("google_map_link", form.value.google_map_link);

    // 服務選項
    formData.append("pick_up_service", pick_up_service.value);
    formData.append("grooming_service", grooming_service.value);
    formData.append("boarding_service", boarding_service.value);
    formData.append(
      "boarding_pet_type",
      JSON.stringify(
        boarding_pet_type.value.length ? boarding_pet_type.value : null
      )
    );

    // 營業時間 & 公休
    formData.append("daily_opening_time", formatTime(daily_opening_time.value));
    formData.append(
      "daily_closing_hours",
      formatTime(daily_closing_hours.value)
    );
    formData.append("close_day", JSON.stringify(close_day.value));

    // 服務項目
    formData.append("service_item", JSON.stringify(selectedServices.value));
    // 圖片
    imagesToUpload.value.forEach((file) => {
      formData.append("images", file); // 後端 getlist('images') 可以抓到
    });

    formData.append("hero_img", heroImage.value);

    // 清晰區分已有圖片和新上傳圖片，並加入日誌檢查
    console.log("準備附加到 FormData 的圖片資料：");

    // 附加已有圖片的 URL
    images.value.forEach((url, index) => {
      if (
        !imagesToUpload.value.some((file) => URL.createObjectURL(file) === url)
      ) {
        formData.append(`existing_images[${index}]`, url);
        console.log(`附加已有圖片 URL: existing_images[${index}] = ${url}`);
      }
    });

    // 附加新上傳的圖片文件
    imagesToUpload.value.forEach((file, index) => {
      formData.append(`new_images[${index}]`, file);
      console.log(`附加新圖片文件: new_images[${index}] = ${file.name}`);
    });

    // 發送請求
    const response = await api.patch(
      `/store/profile/${userId.value}`,
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
      }
    );

    console.log("店家資訊更新成功：", response.data);
    router.push("/stores/info/manage");
  } catch (error) {
    console.error("店家資訊更新失敗：", error);
    alert("更新失敗，請稍後再試！");
  }
};

onMounted(async () => {
  try {
    const response = await api.get(`/store/profile/${userId.value}`);
    const data = response.data;

    // 提取 hero_image 和圖片 URL
    if (data.images) {
      images.value = data.images.map((img) => img.image_url);
      console.log("提取的圖片 URL：", images.value);
    } else {
      console.log("沒有圖片資料");
    }
    // 填充表單資料
    form.value.name = data.store_name || "";
    form.value.address = data.address || {
      county: "",
      district: "",
      detail: "",
    };
    form.value.phone = data.phone || "";
    form.value.traffic_info = data.traffic_info || "";
    form.value.description = data.description || "";
    form.value.facebook_link = data.facebook_link || "";
    form.value.line_link = data.line_link || "";
    form.value.google_map_link = data.google_map_link || "";
    // 填充其他資料
    pick_up_service.value = data.pick_up_service || false;
    grooming_service.value = data.grooming_service || false;
    boarding_service.value = data.boarding_service || false;
    boarding_pet_type.value = data.boarding_pet_type || [];

    daily_opening_time.value = data.daily_opening_time
      ? data.daily_opening_time.slice(0, 5).replace(":", " : ")
      : "09 : 00";
    daily_closing_hours.value = data.daily_closing_hours
      ? data.daily_closing_hours.slice(0, 5).replace(":", " : ")
      : "17 : 00";

    // 初始化公休日期
    close_day.value = data.close_day || [];

    selectedServices.value = data.service_item || [];

    console.log("店家資訊已載入：", data);
  } catch (error) {
    console.error("無法載入店家資訊：", error);
  }
});
</script>

<template>
  <div class="w-full px-4 md:px-8 lg:px-16 py-6 max-w-screen-xl mx-auto">
    <!-- 標題在外面 -->
    <h1 class="page-title">修改本店資訊</h1>
    <!-- 表單卡片（框線在這裡） -->
    <section class="form-card">
      <form @submit.prevent="submitForm" class="space-y-6">
        <!-- 店家照片 -->
        <section class="photos-section">
          <div class="photos-header">
            <label class="photos-title block font-semibold mb-1"
              >店家照片</label
            >
            <!-- 上傳按鈕（隱藏 input） -->
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              multiple
              class="hidden"
              @change="handleFiles"
            />
            <button type="button" class="upload-btn" @click="fileInput.click()">
              新增圖片
            </button>
          </div>

          <!-- 圖片格子 -->
          <ul class="photo-grid">
            <!-- 封面（第一張） -->
            <li v-if="images.length" class="photo-card cover-card">
              <img :src="images[0]" alt="封面" class="photo-img" />
              <span class="cover-badge">封面</span>
              <span class="cover-tip">此張將作為店家頁面的封面圖</span>
              <button type="button" class="photo-delete" @click="remove(0)">
                ×
              </button>
            </li>

            <!-- 其餘縮圖 -->
            <li
              v-for="(src, idx) in images.slice(1)"
              :key="src + idx"
              class="photo-card"
            >
              <img :src="src" class="photo-img" />
              <button
                type="button"
                class="photo-delete"
                @click="remove(idx + 1)"
                aria-label="刪除圖片"
              >
                ×
              </button>
            </li>

            <!-- 佔位上傳卡（未達上限時顯示） -->
            <li
              v-if="images.length < 9"
              class="photo-card placeholder-card"
              @click="fileInput.click()"
            >
              <span class="placeholder-plus">＋</span>
              <span class="placeholder-text">新增圖片</span>
            </li>
          </ul>
        </section>

        <!-- 店家名稱 -->
        <div>
          <label class="block font-semibold mb-1">店家名稱</label>
          <input type="text" v-model="form.name" class="form-input w-full" />
        </div>

        <!-- 地址 -->
        <div>
          <label class="block font-semibold mb-1">地址</label>
          <div class="flex gap-2">
            <input
              v-model="form.address.county"
              class="form-select w-1/4"
              placeholder="請輸入縣市"
            />
            <input
              v-model="form.address.district"
              class="form-select w-1/4"
              placeholder="請輸入區域"
            />
            <input
              type="text"
              v-model="form.address.detail"
              class="form-input flex-1"
              placeholder="請輸入詳細地址"
            />
          </div>
        </div>

        <!-- 電話 -->
        <div>
          <label class="block font-semibold mb-1">電話</label>
          <input type="text" v-model="form.phone" class="form-input w-full" />
        </div>

        <!-- 營業時間 -->
        <section class="space-y-4">
          <div class="form-row">
            <label class="field-label">營業時間</label>
            <div class="time-row">
              <span class="time-label">開始營業時間：</span>
              <select v-model="daily_opening_time" class="time-select">
                <option v-for="t in timeOptions" :key="'open-' + t" :value="t">
                  {{ t }}
                </option>
              </select>

              <span class="mx-2">~</span>

              <span class="time-label">結束營業時間：</span>
              <select v-model="daily_closing_hours" class="time-select">
                <option v-for="t in timeOptions" :key="'close-' + t" :value="t">
                  {{ t }}
                </option>
              </select>
            </div>
          </div>

          <!-- 公休時間 -->
          <div class="form-row">
            <label class="field-label">公休時間</label>
            <div class="days-row">
              <label v-for="d in weekdays" :key="d.value" class="day-item">
                <input
                  type="checkbox"
                  class="day-checkbox"
                  :value="d.value"
                  v-model="close_day"
                />
                <span>{{ d.label }}</span>
              </label>
            </div>
          </div>

          <!-- 服務項目 -->
          <div class="form-row">
            <label class="field-label">服務項目</label>

            <!-- 已選標籤 + 輸入框 -->
            <div class="service-wrap">
              <div class="service-input">
                <!-- 已選標籤 -->
                <span
                  v-for="(tag, i) in selectedServices"
                  :key="tag + i"
                  class="tag-chip"
                >
                  {{ tag }}
                  <button type="button" class="tag-x" @click="removeService(i)">
                    ×
                  </button>
                </span>

                <!-- 文字輸入（Enter 新增） -->
                <input
                  v-model.trim="tagInput"
                  class="tag-text"
                  type="text"
                  placeholder="輸入服務並按 Enter"
                  @keydown.enter.prevent="addFromInput"
                />
              </div>
            </div>

            <!-- 建議清單（點一下加入） -->
            <div class="service-suggest">
              <button
                v-for="s in serviceOptions"
                :key="s"
                type="button"
                class="suggest-chip"
                @click="addService(s)"
                :disabled="selectedServices.includes(s)"
              >
                {{ s }}
              </button>
            </div>
          </div>
        </section>

        <!-- 交通 -->
        <div>
          <label class="block font-semibold mb-1">交通</label>
          <input
            type="text"
            v-model="form.traffic_info"
            class="form-input w-full"
          />
        </div>

        <!-- 接送、美容、住宿服務（你已完成） -->
        <!-- 基本服務開關 -->

        <!-- 接送服務 -->
        <fieldset class="space-y-2">
          <legend class="font-semibold">接送服務</legend>
          <label class="inline_link-flex items-center mr-4">
            <input
              type="radio"
              v-model="pick_up_service"
              :value="true"
              class="form-radio"
            />
            <span class="ml-2">是</span>
          </label>
          <label class="inline_link-flex items-center">
            <input
              type="radio"
              v-model="pick_up_service"
              :value="false"
              class="form-radio"
            />
            <span class="ml-2">否</span>
          </label>
        </fieldset>

        <!-- 美容服務 -->
        <fieldset class="space-y-2">
          <legend class="font-semibold">美容服務</legend>
          <label class="inline_link-flex items-center mr-4">
            <input
              type="radio"
              v-model="grooming_service"
              :value="true"
              class="form-radio"
            />
            <span class="ml-2">是</span>
          </label>
          <label class="inline_link-flex items-center">
            <input
              type="radio"
              v-model="grooming_service"
              :value="false"
              class="form-radio"
            />
            <span class="ml-2">否</span>
          </label>
        </fieldset>

        <!-- 住宿服務 -->
        <fieldset class="space-y-2">
          <legend class="font-semibold">住宿服務</legend>
          <label class="inline_link-flex items-center mr-4">
            <input
              type="radio"
              v-model="boarding_service"
              :value="true"
              class="form-radio"
            />
            <span class="ml-2">是</span>
          </label>
          <label class="inline_link-flex items-center">
            <input
              type="radio"
              v-model="boarding_service"
              :value="false"
              class="form-radio"
            />
            <span class="ml-2">否</span>
          </label>
        </fieldset>

        <!-- 住宿類型 -->
        <div v-if="boarding_service" class="boarding_service-type-block">
          <label class="boarding_service-type-label">寵物住宿類型</label>
          <div class="boarding_service-type-checkboxes">
            <label class="boarding_service-type-option">
              <input type="checkbox" v-model="boarding_pet_type" value="狗狗" />
              <span>狗狗</span>
            </label>
            <label class="boarding_service-type-option">
              <input type="checkbox" v-model="boarding_pet_type" value="貓咪" />
              <span>貓咪</span>
            </label>
          </div>
        </div>

        <!-- 狗狗登記證 -->
        <div
          v-if="boarding_pet_type.includes('狗狗')"
          class="license-upload-block"
        >
          <label class="license-label">狗狗特定寵物業登記許可證</label>
          <button type="button" class="upload-btn">上傳狗狗證明</button>
        </div>

        <!-- 貓咪登記證 -->
        <div
          v-if="boarding_pet_type.includes('貓咪')"
          class="license-upload-block"
        >
          <label class="license-label">貓咪特定寵物業登記許可證</label>
          <button type="button" class="upload-btn">上傳貓咪證明</button>
        </div>
        <!-- 店家簡介 -->
        <div>
          <label class="block font-semibold mb-1">店家簡介</label>
          <textarea
            v-model="form.description"
            rows="8"
            placeholder="請輸入店家簡介內容"
            class="form-textarea w-full"
          ></textarea>
        </div>

        <!-- line連結 -->
        <div>
          <label class="block font-semibold mb-1">line連結</label>
          <input
            type="url"
            v-model.trim="form.line_link"
            class="form-input w-full"
          />
        </div>

        <!-- FB連結 -->
        <div>
          <label class="block font-semibold mb-1">FB連結</label>
          <input
            type="url"
            v-model.trim="form.facebook_link"
            class="form-input w-full"
          />
        </div>

        <!-- google連結 -->
        <div>
          <label class="block font-semibold mb-1">Google地圖連結</label>
          <input
            type="url"
            v-model.trim="form.google_map_link"
            class="form-input w-full"
          />
        </div>
        <!-- 按鈕列 -->
      </form>
    </section>
    <div class="flex justify-center pt-6 space-x-8">
      <button class="btn" @click="router.push('/stores/info/manage')">
        取消並返回
      </button>
      <button class="btn" @click="updateStoreInfo">確認修改</button>
    </div>
  </div>
</template>
