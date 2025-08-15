<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../../../api/api.js";

const router = useRouter();

const userId = ref(null);
const pickup = ref(true); //接送服務
const grooming = ref(true); //美容服務
const boarding = ref(false); //住宿服務
const boardingTypes = ref([]); // 住宿類型
const dogLicenseFile = ref(null); // 用於存儲狗狗上傳的圖片文件
const catLicenseFile = ref(null); // 用於存儲貓咪上傳的圖片文件
const dogUploadedFileURL = ref(null); // 用於顯示狗狗上傳圖片的 URL
const catUploadedFileURL = ref(null); // 用於顯示貓咪上傳圖片的 URL

onMounted(async () => {
  try {
    const response = await api.get("/users/me");
    userId.value = response.data.id;
    // console.log("User ID fetched:", userId.value);
  } catch (error) {
    console.error("Error fetching user data:", error);
  }
});

const getServices = async () => {
  try {
    const response = await api.get(`/store/profile/${userId.value}`);
    const data = response.data;

    // 設置預設值
    pickup.value = data.pick_up_service || false;
    grooming.value = data.grooming_service || false;
    boarding.value = data.boarding_service || false;
  } catch (error) {
    console.error("Error fetching services:", error);
  }
};

onMounted(async () => {
  await getServices();
});

const submitForm = async () => {
  if (!pickup.value && !grooming.value && !boarding.value) {
    alert("請至少選擇一項服務！");
    return;
  }

  try {
    const formData = new FormData();
    formData.append("pick_up_service", pickup.value);
    formData.append("grooming_service", grooming.value);
    formData.append("boarding_service", boarding.value);
    formData.append("boarding_pet_type", JSON.stringify(boardingTypes.value));
    formData.append("status", "pending");
    if (dogLicenseFile.value) {
      formData.append("boarding_license_dog_url", dogLicenseFile.value);
    }

    if (catLicenseFile.value) {
      formData.append("boarding_license_cat_url", catLicenseFile.value);
    }

    const response = await api.patch(
      `/store/profile/${userId.value}`,
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
      }
    );

    console.log("表單提交成功：", response.data);
    alert("表單提交成功！");
    router.push("/stores/info/manage");
  } catch (error) {
    console.error("表單提交失敗：", error);
    alert("表單提交失敗，請稍後再試！");
  }
};

const handleCancel = () => {
  router.push("/stores/info/manage");
};

const handleFileUpload = (e, type) => {
  const file = e.target.files[0];
  if (file) {
    const fileURL = URL.createObjectURL(file);
    if (type === "dog") {
      dogLicenseFile.value = file;
      dogUploadedFileURL.value = fileURL; // 儲存狗狗檔案 URL
    } else if (type === "cat") {
      catLicenseFile.value = file;
      catUploadedFileURL.value = fileURL; // 儲存貓咪檔案 URL
    }
  }
};

const triggerFileInput = (type) => {
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.accept = "image/*";
  fileInput.onchange = (e) => handleFileUpload(e, type);
  fileInput.click();
};

const submitLicense = async () => {
  if (!dogLicenseFile.value && !catLicenseFile.value) {
    alert("請選擇要上傳的圖片！");
    return;
  }

  try {
    const formData = new FormData();
    if (dogLicenseFile.value) {
      formData.append("license", dogLicenseFile.value);
    }
    if (catLicenseFile.value) {
      formData.append("license", catLicenseFile.value);
    }

    const response = await api.post(
      `/store/profile/${userId.value}/upload-license`,
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
      }
    );

    console.log("圖片上傳成功：", response.data);
    alert("圖片上傳成功！");
  } catch (error) {
    console.error("圖片上傳失敗：", error);
    alert("圖片上傳失敗，請稍後再試！");
  }
};
</script>

<template>
  <div class="w-full px-4 md:px-8 lg:px-16 py-6 max-w-screen-xl mx-auto">
    <!-- 頁面標題 -->
    <h1 class="page-title">服務開通</h1>

    <!-- 表單：只包基本服務開關 -->
    <form @submit.prevent="submitForm" class="space-y-6">
      <section class="card">
        <!-- 接送服務 -->
        <fieldset class="form-group">
          <legend class="form-group-label mb-1">接送服務</legend>
          <div class="form-radio-group">
            <label class="form-radio">
              <input type="radio" v-model="pickup" :value="true" />
              <span>是</span>
            </label>
            <label class="form-radio">
              <input type="radio" v-model="pickup" :value="false" />
              <span>否</span>
            </label>
          </div>
        </fieldset>

        <!-- 美容服務 -->
        <fieldset class="form-group">
          <legend class="form-group-label">美容服務</legend>
          <div class="form-radio-group">
            <label class="form-radio">
              <input type="radio" v-model="grooming" :value="true" />
              <span>是</span>
            </label>
            <label class="form-radio">
              <input type="radio" v-model="grooming" :value="false" />
              <span>否</span>
            </label>
          </div>
        </fieldset>

        <!-- 住宿服務 -->
        <fieldset class="form-group">
          <legend class="form-group-label">住宿服務</legend>
          <div class="form-radio-group">
            <label class="form-radio">
              <input type="radio" v-model="boarding" :value="true" />
              <span>是</span>
            </label>
            <label class="form-radio">
              <input type="radio" v-model="boarding" :value="false" />
              <span>否</span>
            </label>
          </div>
        </fieldset>

        <!-- 住宿類型 -->
        <div v-if="boarding" class="boarding-type-block">
          <label class="field-label">寵物住宿類型</label>
          <div class="boarding-type-checkboxes">
            <label class="boarding-type-option">
              <input type="checkbox" v-model="boardingTypes" value="狗狗" />
              <span>狗狗</span>
            </label>
            <label class="boarding-type-option">
              <input type="checkbox" v-model="boardingTypes" value="貓咪" />
              <span>貓咪</span>
            </label>
          </div>
        </div>
      </section>
    </form>

    <!-- 登記證上傳：獨立卡片 -->
    <section
      v-if="boardingTypes.includes('狗狗') || boardingTypes.includes('貓咪')"
      class="card mt-6"
    >
      <h2 class="section-subtitle">
        特定寵物業登記許可證 <span class="required">*</span>
      </h2>

      <div v-if="boardingTypes.includes('狗狗')" class="license-upload-block">
        <label class="license-label">狗狗特定寵物業登記許可證</label>
        <button type="button" class="btn" @click="triggerFileInput('dog')">
          上傳狗狗證明
        </button>
      </div>

      <div v-if="boardingTypes.includes('貓咪')" class="license-upload-block">
        <label class="license-label">貓咪特定寵物業登記許可證</label>
        <button type="button" class="btn" @click="triggerFileInput('cat')">
          上傳貓咪證明
        </button>
      </div>

      <!-- 顯示上傳的圖片 -->
      <div v-if="dogUploadedFileURL" class="uploaded-image-preview">
        <h3 class="preview-title">上傳的狗狗證明圖片：</h3>
        <img
          :src="dogUploadedFileURL"
          alt="Uploaded Dog Image"
          class="uploaded-image"
        />
      </div>

      <div v-if="catUploadedFileURL" class="uploaded-image-preview">
        <h3 class="preview-title">上傳的貓咪證明圖片：</h3>
        <img
          :src="catUploadedFileURL"
          alt="Uploaded Cat Image"
          class="uploaded-image"
        />
      </div>
    </section>

    <!-- 按鈕列（在最底、容器內） -->
    <div class="btn-row">
      <button type="button" class="btn btn-secondary" @click="handleCancel">
        取消並返回
      </button>
      <button type="button" class="btn btn-primary" @click="submitForm()">
        送出審核
      </button>
    </div>
  </div>
</template>
