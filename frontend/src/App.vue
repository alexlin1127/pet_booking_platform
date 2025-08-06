<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/common/Navbar.vue'
import Footer from './components/common/Footer.vue'
import Sidebar from './components/common/Sidebar.vue'

const route = useRoute()
const showSidebar = computed(() => route.meta.sidebar !== false)
</script>

<template>
  <Navbar/>

  <div class="main-container">
    <main class="main-content">
      <Sidebar v-if="showSidebar" />
      <div class="content-area">
        <RouterView />
      </div>
    </main>
  </div>

  <Footer/>
</template>

<style scoped></style>
