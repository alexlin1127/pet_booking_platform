import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
// 使用者註冊畫面Router
import UserRegister from "../pages/Users/Register.vue"
// 商家註冊畫面Router
import ShopRegister from "../pages/Shops/Register.vue"
// 管理者頁面Router
import Admin from "../pages/Admin/Index.vue"
import StoreManagement from "../pages/Admin/StoreManagement.vue"
import StoreReview from "../pages/Admin/StoreReview.vue"
import AccountManagement from "../pages/Admin/AccountManagement.vue"
import PostManagement from "../pages/Admin/PostManagement.vue"



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
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;