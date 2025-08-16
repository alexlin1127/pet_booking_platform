<script setup>
import { ref, computed } from "vue";

const activeTab = ref("grooming");

/* 只改這裡：免金鑰嵌入地圖
   - 改成你的地址：例如 "花蓮市"、"台北 101"、"PetCraft Inn"
   - 或用座標："25.033968,121.564468"
*/
const mapQuery = ref("花蓮市"); // ← 換成你要顯示的位置
const mapSrc = computed(
  () =>
    `https://maps.google.com/maps?q=${encodeURIComponent(
      mapQuery.value
    )}&hl=zh-TW&z=13&output=embed`
);
</script>

<template>
  <div class="home-page">
    <!-- ───────── Hero 區 ────────── -->
    <section class="hero">
      <h1 class="hero-title">為毛孩找到適合的專業美容師<br />及住宿環境</h1>

      <!-- 分頁按鈕（改用 hp-*，避免全站衝突） -->
      <div class="hp-tab-group">
        <button
          class="hp-tab"
          :class="
            activeTab === 'grooming' ? 'hp-tab--solid' : 'hp-tab--outline'
          "
          @click="activeTab = 'grooming'"
        >
          預約美容
        </button>
        <button
          class="hp-tab"
          :class="
            activeTab === 'boarding' ? 'hp-tab--solid' : 'hp-tab--outline'
          "
          @click="activeTab = 'boarding'"
        >
          預約住宿
        </button>
      </div>

      <!-- 裝飾爪印（改用 hp-*，避免全站衝突） -->
      <svg class="hp-paw hp-paw-1" viewBox="0 0 24 24">
        <use href="#icon-paw" />
      </svg>
      <svg class="hp-paw hp-paw-2" viewBox="0 0 24 24">
        <use href="#icon-paw" />
      </svg>
    </section>

    <!-- ───────── 功能卡片 ────────── -->
    <nav class="cards">
      <router-link to="/customers/grooming" class="card">
        <svg class="icon" viewBox="0 0 24 24"><use href="#icon-store" /></svg>
        <span class="label-small">查找優質商家</span>
        <span class="label-big">查看美容</span>
      </router-link>

      <router-link to="/customers/boarding" class="card">
        <svg class="icon" viewBox="0 0 24 24"><use href="#icon-home" /></svg>
        <span class="label-small">安心代付</span>
        <span class="label-big">查看住宿</span>
      </router-link>

      <router-link to="/news" class="card">
        <svg class="icon" viewBox="0 0 24 24"><use href="#icon-paw" /></svg>
        <span class="label-small">解答毛爸媽疑問</span>
        <span class="label-big">最新消息</span>
      </router-link>
    </nav>

    <!-- ───────── Google Map（Vue 綁定 src） ────────── -->
    <section class="map-wrap">
      <iframe
        class="map"
        :src="mapSrc"
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        allowfullscreen
      ></iframe>
    </section>

    <!-- 可自行加入 Footer，如果已有全域 Footer，此區塊可刪 -->
    <!-- <footer class="footer">© 2025 PetCraft Inn</footer> -->
  </div>

  <!-- —— SVG Sprites ——————————————— -->
  <svg xmlns="http://www.w3.org/2000/svg" style="display: none">
    <symbol id="icon-store" viewBox="0 0 24 24">
      <path d="M3 9h18l-1 11H4L3 9zm19-2V5H2v2l1 2h18l1-2z" />
    </symbol>
    <symbol id="icon-home" viewBox="0 0 24 24">
      <path d="M12 3l10 9h-3v9H5v-9H2l10-9z" />
    </symbol>
    <symbol id="icon-paw" viewBox="0 0 24 24">
      <circle cx="4.5" cy="10.5" r="2.5" />
      <circle cx="19.5" cy="10.5" r="2.5" />
      <circle cx="9" cy="4.5" r="2.5" />
      <circle cx="15" cy="4.5" r="2.5" />
      <path
        d="M12 9c3.2 0 5.8 2.6 5.8 5.8S15.2 20.5 12 20.5 6.2 17.9 6.2 14.8 8.8 9 12 9z"
      />
    </symbol>
  </svg>
</template>



<style scoped src="../styles/auth/welcome.css"></style>
