<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import Card from "../../../components/UI/Card.vue";
import ModalBox from "../../../components/UI/ModalBox.vue";
import Switch from "../../../components/UI/Switch.vue";
import { services as staticServices } from "../../../data/services"; //避免和響應式變數撞名
import api from "../../../api/api.js";

const router = useRouter();
const userId = ref(null);

const services = ref([]); // 用於存儲所有服務資料

const getUser = async () => {
  try {
    const response = await api.get("/users/me");
    userId.value = response.data.id;
    console.log("User ID fetched:", userId.value);
  } catch (error) {
    // console.error("Error fetching user data:", error);
  }
};

const getBoardingServices = async () => {
  try {
    const response = await api.get("/store/boarding_services");
    const boardingData = response.data.map((item) => ({
      id: item.id,
      title: item.room_type,
      description: item.introduction,
      price: item.pricings[0].pricing || 0, // 假設取第一個價格
      type: "boarding",
      tags: [item.species],
      bullets: [
        `清潔頻率：${item.cleaning_frequency}`,
        `房間數量：${item.room_count}`,
      ],
      duration: null, // 住宿服務無時長
    }));
    services.value.push(...boardingData);
    console.log("Boarding services fetched:", boardingData);
  } catch (error) {
    console.error("Error fetching boarding services:", error);
  }
};

const getGroomingServices = async () => {
  try {
    const response = await api.get("/store/grooming_services");
    const groomingData = response.data.map((item) => ({
      id: item.id,
      title: item.service_title,
      description: item.introduction,
      price: item.pricings[0].pricing || 0, // 假設取第一個價格
      type: "grooming",
      tags: [item.species], // 假設用固定標籤
      bullets: [`注意事項：${item.notice}`],
      duration: `${item.duration_min} ~ ${item.duration_max} 分鐘`,
    }));
    services.value.push(...groomingData);
    console.log("Grooming services fetched:", groomingData);
  } catch (error) {
    console.error("Error fetching grooming services:", error);
  }
};

onMounted(async () => {
  await getUser();
  await Promise.all([getBoardingServices(), getGroomingServices()]);
});

// Modal 狀態
const showDelete = ref(false); // 新增
const pending = ref(null); // 暫存要刪除的服務資料

// 頁首：true=美容, false=住宿
const isGrooming = ref(true);

// 下拉篩選選項
const tagOptions = ["dog", "cat"];
const selectedTag = ref("全部");

// 操作事件
const onEdit = (id, type) => {
  router.push(`/stores/services/edit/${id}/${type}`);
};
const onDelete = (svc) => {
  //  改成接收整個物件，不是 id
  pending.value = svc; //  存起要刪除的項目
  showDelete.value = true; //  打開 Modal
};

// 新增服務按鈕事件
const handleAddService = () => {
  router.push("/stores/services/add");
};

// Modal 按鈕事件
const onModalAction = async (event) => {
  const action = event?.action;
  console.log("Action triggered:", action);
  console.log("Pending value before action:", pending.value);

  if (action === "confirm" && pending.value) {
    // 先更新前端數據
    services.value = services.value.filter(
      (s) => !(s.id === pending.value.id && s.type === pending.value.type)
    );

    try {
      const endpoint =
        pending.value.type === "grooming"
          ? `/store/grooming_services/${pending.value.id}`
          : `/store/boarding_services/${pending.value.id}`;
      await api.delete(endpoint);
      console.log(`Service with ID ${pending.value.id} deleted successfully.`);
    } catch (error) {
      console.error(
        `Failed to delete service with ID ${pending.value.id}:`,
        error
      );
      // 如果刪除失敗，重新調用 API 獲取最新數據
      if (pending.value.type === "grooming") {
        await getGroomingServices();
      } else {
        await getBoardingServices();
      }
    }
  }

  showDelete.value = false;
  pending.value = null;
};

// 過濾服務清單
const filteredServices = computed(() => {
  const type = isGrooming.value ? "grooming" : "boarding";
  return services.value
    .filter((s) => s.type === type)
    .filter((s) =>
      selectedTag.value === "全部" ? true : s.tags?.includes(selectedTag.value)
    );
});

/* 新增：把服務物件轉成 ModalBox 需要的 infoRows 二維陣列 */
const buildInfoRows = (svc) => {
  if (!svc) return [];
  const bullets = (svc.bullets ?? []).map((b) => `• ${b}`).join("\n"); // 用換行與項目符號
  const tags = (svc.tags ?? []).join("、");
  return [
    ["項目", svc.title],
    ["價格", `NT$ ${svc.price}`],
    ["說明", svc.description],
    ["注意事項", bullets],
    ["服務時間", svc.duration],
    ["標籤", tags],
  ];
};
/* 新增：把服務物件轉成 ModalBox 需要的 infoRows 二維陣列  */
</script>

<template>
  <div class="service-page">
    <div class="service-header">
      <h1 class="service-title-page">服務項目管理</h1>
      <button class="svc-btn svc-btn-primary" @click="handleAddService">
        新增服務
      </button>
    </div>
    <!-- 美容 / 住宿 切換 -->
    <div class="flex items-center">
      <span class="mr-2 text-sm">美容</span>
      <Switch v-model="isGrooming" size="md" />
      <span class="ml-2 text-sm">住宿</span>
      <!-- 篩選服務 下拉 -->
      <span class="ml-2 text-sm py-2">篩選服務</span>
      <select v-model="selectedTag" class="select-filter ml-4">
        <option v-for="opt in tagOptions" :key="opt" :value="opt">
          {{ opt === "dog" ? "犬" : "貓" }}
        </option>
      </select>
    </div>
    <section class="space-y-10">
      <Card
        v-for="s in filteredServices"
        :key="s.id"
        type="vertical"
        :hasButton="true"
        :clickable="false"
        class="service-card"
      >
        <!-- 不要 icon：若卡片本身會渲染空容器，就用 CSS 隱藏；或保留此具名 slot 覆蓋 -->
        <template #icon><template v-if="false" /></template>

        <template #title>
          <div class="flex items-center justify-between">
            <h3 class="service-item-title">
              {{ s.title }} <span class="service-price">NT${{ s.price }}</span>
            </h3>
          </div>
        </template>

        <template #content>
          <p class="service-desc">{{ s.description }}</p>

          <ul class="service-bullets">
            <li v-for="b in s.bullets" :key="b">{{ b }}</li>
          </ul>

          <div class="service-meta">
            <div v-if="isGrooming" class="service-duration">
              施作時間：{{ s.duration }}
            </div>
            <div class="service-tags">
              <span v-for="t in s.tags" :key="t" class="service-tag">{{
                t
              }}</span>
            </div>
          </div>
        </template>

        <template #button>
          <div class="service-actions">
            <button class="svc-btn svc-btn-outline" @click="onDelete(s)">
              刪除服務
            </button>
            <button class="svc-btn svc-btn-solid" @click="onEdit(s.id, s.type)">
              修改內容
            </button>
          </div>
        </template>
      </Card>
    </section>
    <!-- 刪除確認 Modal -->
    <ModalBox
      :visible="showDelete"
      :title="'確認刪除該服務'"
      :buttons="[
        {
          text: '取消',
          action: 'cancel',
          variant: 'cancel',
          class: 'svc-btn svc-btn-outline w-20',
        },
        {
          text: '確認',
          action: 'confirm',
          variant: 'danger',
          class: 'svc-btn svc-btn-solid gap-6',
        },
      ]"
      @close="
        () => {
          showDelete = false;
          pending = null;
        }
      "
      @button-click="onModalAction"
      width="max-w-2xl"
    >
      <!-- ⬇⬇⬇ 這段是新的 slot：照圖示排版 ⬇⬇⬇ -->
      <template #default>
        <div v-if="pending" class="del-preview">
          <!-- 服務名稱 ＆ 價格（左右對齊） -->
          <div class="flex items-center justify-between">
            <div class="service-item-title">
              {{ pending.title
              }}<span class="service-price">NT${{ pending.price }}</span>
            </div>
          </div>

          <!-- 服務描述 -->
          <div class="svc-desc">
            <p>{{ pending.description }}</p>
          </div>

          <!-- 注意事項：黑色圓點 -->
          <ul class="service-bullets">
            <li v-for="(b, i) in pending.bullets" :key="b">{{ b }}</li>
          </ul>

          <!-- 服務時間（灰字） -->
          <div class="service-duration mt-2 mb-2">
            服務時間：約 {{ pending.duration }}
          </div>

          <!-- 標籤（膠囊） -->
          <div class="service-tags justify-start">
            <span v-for="(t, i) in pending.tags" :key="i" class="service-tag">{{
              t
            }}</span>
          </div>
        </div>
      </template>
    </ModalBox>
  </div>
</template>
