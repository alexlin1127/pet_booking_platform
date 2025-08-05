import { createRouter, createWebHistory } from "vue-router";
import Home from "../auth/WelcomePage.vue";
import Login from "../auth/Login.vue";
import Register from "../auth/Register.vue";

// 使用者畫面Router
import CustomerRegister from "../pages/Customers/CustomerRegister.vue"

// 商家畫面Router
import StoreRegister from "../pages/Stores/StoreRegister.vue"
import StoreManage from "../pages/Stores/Posts/Postsmanage.vue"
import StorePostProcess from "../pages/Stores/Posts/PostsProcess.vue"
import StorePostView from "../pages/Stores/Posts/PostsView.vue"

// 管理者頁面Router
import Admin from "../pages/Admin/AdminDashboard.vue"
import StoreManagement from "../pages/Admin/Stores/StoreManagement.vue"
import StoreReview from "../pages/Admin/Stores/StoreReview.vue"
import AccountManagement from "../pages/Admin/Account/AccountManagement.vue"
import PostManagement from "../pages/Admin/Posts/PostManagement.vue"
import PostReview from "../pages/Admin/Posts/PostReview.vue";

// 前台頁面Router - 使用正確的路徑
import NewsPage from "../pages/Customers/News.vue";
import StoresPage from "../pages/Customers/StoresView.vue";
import BookingGroomingPage from "../pages/Customers/Booking/Grooming.vue";
import BookingLodgingPage from "../pages/Customers/Booking/Lodging.vue";



const routes = [
    {
        path: "/",
        component: Home,
        meta: { sidebar: false }
    },
    {
        path: "/news",
        component: NewsPage,
        meta: { sidebar: false }
    },
    {
        path: "/stores",
        component: StoresPage,
        meta: { sidebar: false }
    },
    {
        path: "/booking/grooming",
        component: BookingGroomingPage,
        meta: { sidebar: false }
    },
    {
        path: "/booking/lodging",
        component: BookingLodgingPage,
        meta: { sidebar: false }
    },
    {
        path: "/login",
        component: Login,
        meta: { sidebar: false }
    },
    {
        path: "/register",
        component: Register,
        meta: { sidebar: false }
    },
    {
        path: "/register/customers",
        component: CustomerRegister,
        meta: { sidebar: false }
    },

    // 商家頁面路由
    {
        path: "/register/stores/:step",
        component: StoreRegister,
        meta: { sidebar: false }
    },
    {
        path: "/stores/posts/manage",
        component: StoreManage,
        meta: { sidebar: true }
    },
    {
        path: "/stores/posts/add",
        component: StorePostProcess,
        meta: { sidebar: false }
    },
    {
        path: "/stores/posts/edit/:id",
        component: StorePostProcess,
        meta: { sidebar: false }
    },
    {
        path: "/stores/posts/view/:id",
        component: StorePostView,
        meta: { sidebar: false }
    },

    // // 管理者頁面Router
    {
        path: "/admin",
        component: Admin,
        meta: { sidebar: true }
    },
    {
        path: "/admin/stores/manage",
        component: StoreManagement,
        meta: { sidebar: true }
    },
    {
        path: "/admin/stores/:status",
        component: StoreReview,
        meta: { sidebar: false }
    },
    {
        path: "/admin/accounts/:page?",
        component: AccountManagement,
        meta: { sidebar: true }
    },
    {
        path: "/admin/posts",
        component: PostManagement,
        meta: { sidebar: true }
    },
    {
        path: "/admin/posts/:status",
        component: PostReview,
        meta: { sidebar: false }
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;