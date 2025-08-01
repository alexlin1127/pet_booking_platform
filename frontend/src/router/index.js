import { createRouter, createWebHistory } from "vue-router";
import Home from "../auth/WelcomePage.vue";
import Login from "../auth/Login.vue";
import Register from "../auth/Register/Register.vue";
// 使用者註冊畫面Router
import CustomerRegister from "../auth/Register/CustomerRegister.vue"
// 商家註冊畫面Router
import StoreRegister from "../auth/Register/StoreRegister.vue"

// 管理者頁面Router
import Admin from "../pages/Admin/AdminDashboard.vue"
import StoreManagement from "../pages/Admin/Stores/StoreManagement.vue"
import StoreReview from "../pages/Admin/Stores/StoreReview.vue"
import AccountManagement from "../pages/Admin/Account/AccountManagement.vue"
import PostManagement from "../pages/Admin/Posts/PostManagement.vue"
import PostReview from "../pages/Admin/Posts/PostReview.vue";



const routes = [
    {
        path: "/",
        component: Home,
        meta: { sidebar: true }
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
    {
        path: "/register/stores/:step",
        component: StoreRegister,
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