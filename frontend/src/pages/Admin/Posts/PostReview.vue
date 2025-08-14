<!-- src/pages/Admin/PostReview.vue -->
<script setup>
import { ref, onMounted } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";
import ModalBox from "../../../components/UI/ModalBox.vue";
import api from "../../../api/api.js";

const route = useRoute();
const router = useRouter();

const postId = ref("");
const title = ref("");
const content = ref([]);
const imgSrc = ref("");

const show = ref(false);
const infoRows = ref([]);

const getPostDetail = async () => {
  try {
    const res = await api.get(`/admin/posts/${postId.value}`);
    const post = res.data;
    console.log("取得貼文詳細資料：", post);
    // 更新資料
    title.value = post.title;
    content.value = [post.content]; // 假設 content 是單一字串，包裝成陣列以便渲染
    imgSrc.value = post.image_url || imgSrc.value; // 如果有圖片 URL，則使用

    // 更新 infoRows
    infoRows.value = [
      ["編號", post.id],
      ["店家名稱", post.store_name],
      ["標題", post.title],
    ];
  } catch (error) {
    console.error("無法取得貼文詳細資料：", error);
    alert("無法取得貼文詳細資料，請稍後再試。");
  }
};

onMounted(() => {
  // 從路由查詢參數獲取資料
  const routePostId = route.query.id;

  if (routePostId) {
    postId.value = routePostId;
    getPostDetail(); // 呼叫 API 獲取貼文詳細資料
  } else {
    alert("無法取得貼文 ID，請返回重試。");
    router.push("/admin/posts");
  }
});

const handleButtonClick = async (event) => {
  if (event.action === "cancel") {
    show.value = false;
  } else if (event.action === "confirm") {
    const reason = event.data.textareas.reason || "";
    console.log("收到駁回原因：", reason);

    // 模擬發送駁回資料給後端
    const payload = {
      status: "rechecked",
      reject_content: reason,
    };

    console.log("模擬送出 API 資料：", payload);
    await api.patch(`/admin/posts/${postId.value}`, payload); // 正式使用時啟用

    alert("已成功駁回貼文");
    show.value = false;
    router.push("/admin/posts"); // 駁回後返回貼文列表
  }
};

const confirmPost = async () => {
  const payload = {
    status: "confirmed",
  };
  try {
    await api.patch(`/admin/posts/${postId.value}`, payload);

    alert("已成功核准貼文");
    show.value = false;
    router.push("/admin/posts");
  } catch (err) {
    console.error("無法核准貼文：", err);
    alert("無法核准貼文，請稍後再試。");
  }
};
</script>

<template>
  <!-- 整頁結構，外層負責佈局 -->
  <div class="page-layout">
    <main class="page-main">
      <img :src="imgSrc" alt="封面圖" class="article-img" />
      <h1 class="article-title">{{ title }}</h1>
      <div class="article-content">
        <p v-for="(para, idx) in content" :key="idx">{{ para }}</p>
      </div>
      <div class="article-buttons" v-if="route.path === '/admin/posts/review'">
        <RouterLink to="/admin/posts" class="btn-back">返回</RouterLink>
        <button class="btn-addQ" @click="show = true">加入問題件</button>
        <button class="btn-check" @click="confirmPost">核准</button>
      </div>
      <div
        class="article-buttons"
        v-else-if="route.path === '/admin/posts/details'"
      >
        <RouterLink to="/admin/posts" class="btn-back">返回</RouterLink>
      </div>
    </main>
  </div>

  <ModalBox
    :visible="show"
    title="貼文駁回"
    :infoRows="infoRows"
    :textareaFields="[
      {
        key: 'reason',
        label: '駁回原因（限200字內）',
        placeholder: '請輸入退件原因',
        rows: 5,
        maxlength: 200,
        required: true,
      },
    ]"
    :buttons="[
      {
        text: '取消',
        action: 'cancel',
        class: 'modal-btn-cancel',
      },
      {
        text: '確認並通知店家',
        action: 'confirm',
        class: 'modal-btn-danger',
      },
    ]"
    @close="show = false"
    @button-click="handleButtonClick"
  />
</template>
