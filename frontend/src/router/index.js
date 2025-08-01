import { createRouter, createWebHistory } from "vue-router";
import Home from "../auth/WelcomePage.vue";
import Login from "../auth/Login.vue";
import Register from "../auth/Register/Register.vue";
// 使用者註冊畫面Router
import UserRegister from "../pages/Customers/Index.vue"
// 商家註冊畫面Router
import ShopRegister from "../pages/Stores/StoresDashboard.vue"
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
        path: "/register/users",
        component: UserRegister,
        meta: { sidebar: false }
    },
    {
        path: "/register/shops/:step",
        component: ShopRegister,
        meta: { sidebar: false }
    },

    // // 管理者頁面Router
    {
        path: "/admin",
        component: Admin,
        meta: { sidebar: true }
    },
    {
        path: "/admin/store/manage",
        component: StoreManagement,
        meta: { sidebar: true }
    },
    {
        path: "/admin/store/:status",
        component: StoreReview,
        meta: { sidebar: false }
    },
    {
        path: "/admin/account/:page?",
        component: AccountManagement,
        meta: { sidebar: true }
    },
    {
        path: "/admin/post",
        component: PostManagement,
        meta: { sidebar: true }
    },
    {
        path: "/admin/post/:status",
        component: PostReview,
        meta: { sidebar: false }
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;