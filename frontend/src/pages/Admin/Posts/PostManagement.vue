<script setup>
import { ref, computed } from 'vue'
import Table from "../../../components/UI/Table.vue"
import PostCard from "./PostCard.vue";
import Pagination from "../../../components/common/Pagination.vue"

const pageSize = 5 // 每頁顯示5個

// 第一個表格的分頁邏輯（審核中的店家）
const currentPage1 = ref(1)

// 第二個表格的分頁邏輯（營運中的店家）
const currentPage2 = ref(1)

// 篩選狀態
const selectedStatus = ref('待審核')

const posts = [
    {
        id: "P0001",
        storeName: "寵物樂園",
        publishDate: "2025-07-01",
        title: "夏日寵物保養小貼士",
        content: [
        "今天我們迎接了三位可愛的新朋友洗澡洗香香：米克斯「肉肉」、黃金獵犬組合「阿吉」與「阿豆」，還有常常來報到的哈士奇爆毛王「哈丁」！",
        "牠們一進門就吸引不少目光，一開始都有點害羞，但在熟悉的美容師帶領與香香的洗毛小浴缸下，很快就放下不安，用呆萌、歡樂、無辜的表情征服大家。",
        "最後的吹乾與造型，「肉肉」和「阿吉」都超配合，不只變得超帥氣，還紛紛搖尾巴向工作人員撒嬌。而哈丁雖然狂掉毛，本店美容師還是迅速處理完畢，毛量不減，帥度破表！",
        "若你家毛孩也需要香香洗澡，或想看看更多可愛瞬間，記得追蹤我們的社群平台唷！如果想預約洗澡，可以直接透過下方按鈕快速前往預約頁！"],
        status: "待審核"
    },
    {
        id: "P0002",
        storeName: "毛孩之家寵物美容",
        publishDate: "2025-07-05",
        title: "新開幕優惠活動",
        content: "慶祝新店開幕，洗剪吹套餐8折優惠...",
        status: "退回補件"
    },
    {
        id: "P0003",
        storeName: "寵物小棧",
        publishDate: "2025-07-08",
        title: "寵物訓練課程招生",
        content: "專業寵物行為訓練師指導...",
        status: "已拒絕"
    },
    {
        id: "P0004",
        storeName: "毛寶貝寵物醫院",
        publishDate: "2025-07-12",
        title: "疫苗接種提醒",
        content: "提醒各位飼主定期為寵物接種疫苗...",
        status: "已通過"
    },
    {
        id: "P0005",
        storeName: "快樂寵物旅館",
        publishDate: "2025-07-15",
        title: "暑假住宿優惠方案",
        content: "暑假期間寵物住宿享有特別優惠...",
        status: "待審核"
    },
    {
        id: "P0006",
        storeName: "愛心動物診所",
        publishDate: "2025-07-18",
        title: "寵物健康檢查重要性",
        content: "定期健康檢查是維護寵物健康的關鍵...",
        status: "退回補件"
    },
    {
        id: "P0007",
        storeName: "寵物天堂",
        publishDate: "2025-07-22",
        title: "新品上市 - 天然飼料",
        content: "引進歐洲進口天然無添加飼料...",
        status: "已通過"
    },
    {
        id: "P0008",
        storeName: "毛毛小屋",
        publishDate: "2025-07-25",
        title: "寵物美容技巧分享",
        content: "在家也能幫毛孩做基礎美容...",
        status: "已拒絕"
    },
    {
        id: "P0009",
        storeName: "寵愛一生動物醫院",
        publishDate: "2025-07-28",
        title: "急診服務公告",
        content: "24小時急診服務，為您的毛孩守護健康...",
        status: "待審核"
    },
    {
        id: "P0010",
        storeName: "快樂狗狗美容坊",
        publishDate: "2025-08-01",
        title: "夏季造型特輯",
        content: "涼爽可愛的夏季造型，讓毛孩清爽一夏...",
        status: "退回補件"
    },
    {
        id: "P0011",
        storeName: "寵物大本營",
        publishDate: "2025-08-05",
        title: "寵物用品大特價",
        content: "全館寵物用品7折起，數量有限...",
        status: "已通過"
    },
    {
        id: "P0012",
        storeName: "毛孩寵物旅館",
        publishDate: "2025-08-08",
        title: "旅館設施介紹",
        content: "舒適安全的住宿環境，專業的照護服務...",
        status: "已拒絕"
    },
    {
        id: "P0013",
        storeName: "愛寵動物醫院",
        publishDate: "2025-08-12",
        title: "寵物肥胖問題探討",
        content: "如何判斷寵物是否過重及減重方法...",
        status: "待審核"
    },
    {
        id: "P0014",
        storeName: "寵物樂活館",
        publishDate: "2025-08-15",
        title: "寵物瑜珈課程開班",
        content: "和毛孩一起做瑜珈，增進親密關係...",
        status: "退回補件"
    },
    {
        id: "P0015",
        storeName: "毛寶貝寵物店",
        publishDate: "2025-08-18",
        title: "秋季保養品推薦",
        content: "換季時節，為毛孩選擇適合的保養品...",
        status: "已通過"
    },
    {
        id: "P0016",
        storeName: "寵物好朋友",
        publishDate: "2025-08-22",
        title: "寵物攝影服務",
        content: "專業寵物攝影，留下美好回憶...",
        status: "已拒絕"
    },
    {
        id: "P0017",
        storeName: "愛心寵物診所",
        publishDate: "2025-08-25",
        title: "老年寵物照護指南",
        content: "高齡寵物的特殊照護需求與注意事項...",
        status: "待審核"
    },
    {
        id: "P0018",
        storeName: "寵物溫馨家",
        publishDate: "2025-08-28",
        title: "寵物心理健康重要性",
        content: "關注毛孩的心理健康，營造快樂環境...",
        status: "退回補件"
    },
    {
        id: "P0019",
        storeName: "毛孩健康中心",
        publishDate: "2025-09-01",
        title: "營養補充品介紹",
        content: "為不同年齡的寵物選擇合適的營養品...",
        status: "已通過"
    },
    {
        id: "P0020",
        storeName: "寵物快樂園",
        publishDate: "2025-09-05",
        title: "中秋節寵物注意事項",
        content: "中秋節期間需要注意的寵物安全事項...",
        status: "已拒絕"
    }
];

// 根據狀態篩選貼文
const pendingPosts = computed(() => {
    return posts.filter(post => post.status === selectedStatus.value)
})

const approvedPosts = computed(() => {
    return posts.filter(post => post.status === "已通過")
})

// 篩選按鈕處理函數
const filterByStatus = (status) => {
    selectedStatus.value = status
    currentPage1.value = 1 // 重置到第一頁
}

// 第一個表格的分頁邏輯（待審核的貼文）
const totalPages1 = computed(() => Math.ceil(pendingPosts.value.length / pageSize))
const paginatedPendingPosts = computed(() => {
    const start = (currentPage1.value - 1) * pageSize
    return pendingPosts.value.slice(start, start + pageSize)
})

// 第二個表格的分頁邏輯（已通過的貼文）
const totalPages2 = computed(() => Math.ceil(approvedPosts.value.length / pageSize))
const paginatedApprovedPosts = computed(() => {
    const start = (currentPage2.value - 1) * pageSize
    return approvedPosts.value.slice(start, start + pageSize)
})

// 分頁處理函數
const handlePageChange1 = (page) => {
    currentPage1.value = page
}

const handlePageChange2 = (page) => {
    currentPage2.value = page
}
</script>

<template>
    <div class="postmanage-container">
        <h1 class="postmanage-title">貼文管理</h1>

        <div class="postmanage-filters">
            <div class="storemanage-list">
                <p>{{ selectedStatus }}貼文列表</p>
            </div>

            <button class="btn" :class="{ 'btn-active': selectedStatus === '待審核' }" @click="filterByStatus('待審核')">
                待審核
            </button>
            <button class="btn" :class="{ 'btn-active': selectedStatus === '退回補件' }" @click="filterByStatus('退回補件')">
                退回補件
            </button>
        </div>

        <div class="storemanage-table-container">
            <Table>
                <template #header>
                    <th>貼文ID</th>
                    <th>店家名稱</th>
                    <th>發布日期</th>
                    <th>標題</th>
                    <th>審核狀況</th>
                    <th>操作</th>
                </template>
                <template #body>
                    <tr v-for="post in paginatedPendingPosts" :key="post.id" class="card-row">
                        <PostCard :post="post" />
                    </tr>
                </template>
            </Table>

            <Pagination :current-page="currentPage1" :total-pages="totalPages1" @page-change="handlePageChange1" />
        </div>
    </div>

    <div class="storemanage-container">
        <h1 class="storemanage-title">已通過貼文</h1>

        <!-- 選擇日期 -->
        <label class="storemanage-filter-label">
            發布日期：
            <input type="date" v-model="selectedDate" class="accmanage-filter-input" />
            ~
            <input type="date" v-model="selectedDate" class="accmanage-filter-input" />
        </label>

        <div class="storemanage-table-container">
            <Table>
                <template #header>
                    <th>貼文ID</th>
                    <th>店家名稱</th>
                    <th>發布日期</th>
                    <th>標題</th>
                    <th>審核狀況</th>
                    <th>操作</th>
                </template>
                <template #body>
                    <tr v-for="post in paginatedApprovedPosts" :key="post.id" class="card-row">
                        <PostCard :post="post" />
                    </tr>
                </template>
            </Table>

            <Pagination :current-page="currentPage2" :total-pages="totalPages2" @page-change="handlePageChange2" />
        </div>
    </div>


</template>

<style></style>