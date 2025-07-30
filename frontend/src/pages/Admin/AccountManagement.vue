<script setup>
import Table from "../../components/Table.vue"
import AccountCard from "../../components/Admin/AccountCard.vue";

const accounts = [
  {
    id: "A0001",
    type: "管理員",
    name: "王小明",
    account: "admin001",
    store: "寵物樂園",
    status: "啟用",
    createdAt: "2025-07-01"
  },
  {
    id: "S0002",
    type: "店家",
    name: "李小華",
    account: "shop002",
    store: "毛孩之家",
    status: "停用",
    createdAt: "2025-07-10"
  },
  {
    id: "U0003",
    type: "一般用戶",
    name: "陳大仁",
    account: "user003",
    store: "寵物小棧",
    status: "啟用",
    createdAt: "2025-07-20"
  }
];
</script>

<template>
    <div>
        <h1>帳號管理</h1>
    </div>
    
    <div>
        <Table>
            <template #header>
                <th>編號</th>
                <th>帳號類型</th>
                <th>名字</th>
                <th>帳號</th>
                <th>所屬店家</th>
                <th>帳號狀態</th>
                <th>建立日期</th>
                <th>功能</th>
                <th>操作</th>
            </template>
            <template #body>
                <tr v-for="acc in accounts" :key="acc.id" class="card-row">
                    <AccountCard :acc="acc" />
                </tr>
            </template>
        </Table>
    </div>

</template>

<style>
table {
  border-spacing: 0 12px;
}
.card-row {
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s;
}
.card-row:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.2);
}
.card-row td {
  padding: 16px 16px;
  border: none;
}
</style>