<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../../../api/api.js";

const router = useRouter();
const pickup = ref(true); //接送服務
const grooming = ref(true); //美容服務
const boarding = ref(false); //住宿服務
const boardingTypes = ref([]); // 住宿類型
const imageNote = ref(""); // 圖片說明

const submitForm = () => {
  console.log({
    pickup: pickup.value,
    grooming: grooming.value,
    boarding: boarding.value,
    boardingTypes: boardingTypes.value,
    imageNote: imageNote.value,
  });
};

const handleCancel = () => {
  router.push("/stores/info/manage");
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
        <button type="button" class="btn">上傳狗狗證明</button>
      </div>

      <div v-if="boardingTypes.includes('貓咪')" class="license-upload-block">
        <label class="license-label">貓咪特定寵物業登記許可證</label>
        <button type="button" class="btn">上傳貓咪證明</button>
      </div>
    </section>

    <!-- 按鈕列（在最底、容器內） -->
    <div class="btn-row">
      <button type="button" class="btn btn-secondary" @click="handleCancel">
        取消並返回
      </button>
      <button type="button" class="btn btn-primary">送出審核</button>
    </div>
  </div>
</template>
