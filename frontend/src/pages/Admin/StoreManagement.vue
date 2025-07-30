<script setup>
import Table from "../../components/Table.vue"
import StoreCard from "../../components/Admin/StoreCard.vue";

const stores = [
  {
    id: "H0001",
    storeName: "寵物樂園",
    registerDate: "2025-07-01",
    region: "台北市",
    owner: "王小明",
    phone: "0912345678",
    status: "待審核"
  },
  {
    id: "H0002",
    storeName: "毛孩之家之寵物美容沙龍及住宿",
    registerDate: "2025-07-10",
    region: "新北市",
    owner: "李小華",
    phone: "0922333444",
    status: "待審核"
  },
  {
    id: "H0003",
    storeName: "寵物小棧",
    registerDate: "2025-07-20",
    region: "桃園市",
    owner: "陳大仁",
    phone: "0933222111",
    status: "待審核"
  }
];
</script>

<template>
    <div>
        <h1>店家審核及管理</h1>
    </div>
    
    <div>
        <Table>
            <template #header>
                <th>編號</th>
                <th>店家</th>
                <th>註冊日期</th>
                <th>所在地區</th>
                <th>負責人</th>
                <th>聯絡電話</th>
                <th>審核狀況</th>
                <th>操作</th>
            </template>
            <template #body>
                <tr v-for="store in stores" :key="store.id" class="card-row">
                    <StoreCard :store="store" />
                </tr>
            </template>
        </Table>
    </div>

</template>

<style></style>