/* eslint-disable prettier/prettier */
import { createRouter, createWebHistory } from "vue-router";
<<<<<<< Updated upstream
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
=======

/* ─── 認證 / 共用 ─────────────────────────────── */
import Home from "../auth/WelcomePage.vue";
import Login from "../auth/Login.vue";
import Register from "../auth/Register.vue";

/* ─── 前台（顧客）畫面 ─────────────────────────── */
import NewsPage from "../pages/Customers/News.vue";
import StoresPage from "../pages/Customers/StoresView.vue";
import BookingGroomingPage from "../pages/Customers/Booking/Grooming.vue";
import BookingLodgingPage from "../pages/Customers/Booking/Lodging.vue";
import CustomerRegister from "../pages/Customers/CustomerRegister.vue";
>>>>>>> Stashed changes

/* ─── 商家畫面 ─────────────────────────────────── */
import StoreRegister from "../pages/Stores/StoreRegister.vue";
import StoreManage from "../pages/Stores/Posts/Postsmanage.vue";
import StorePostProcess from "../pages/Stores/Posts/PostsProcess.vue";
import StorePostView from "../pages/Stores/Posts/PostsView.vue";

/* ★ 商家預約畫面（共用新增／編輯／查看） */
import StoreAppointment from "../pages/Stores/StoreAppointment.vue";

/* ★ 新增：商家服務畫面（共用新增／編輯／查看） */
import StoreServices from "../pages/Stores/StoreServices.vue";

/* ─── 管理者畫面 ───────────────────────────────── */
import Admin from "../pages/Admin/AdminDashboard.vue";
import StoreManagement from "../pages/Admin/Stores/StoreManagement.vue";
import StoreReview from "../pages/Admin/Stores/StoreReview.vue";
import AccountManagement from "../pages/Admin/Account/AccountManagement.vue";
import PostManagement from "../pages/Admin/Posts/PostManagement.vue";
import PostReview from "../pages/Admin/Posts/PostReview.vue";

/* ─────────────────────────────────────────────── */

const routes = [
<<<<<<< Updated upstream
    {
        path: "/",
        component: Home,
        meta: { sidebar: true }
    },
    {
        path: "/Login",
        component: Login,
    },
    {
        path: "/Register",
        component: Register,
    },
    {
        path: "/Register/Users",
        component: UserRegister,
    },
    {
        path: "/Register/Shops/:step",
        component: ShopRegister,
    },

    // // 管理者頁面Router
    {
        path: "/Admin",
        component: Admin,
        meta: { sidebar: true }
    },
    {
        path: "/Admin/Store/Manage",
        component: StoreManagement,
        meta: { sidebar: true }
    },
    {
        path: "/Admin/Store/Review",
        component: StoreReview,
    },
    {
        path: "/Admin/Account",
        component: AccountManagement,
        meta: { sidebar: true }
    },
    {
        path: "/Admin/Post",
        component: PostManagement,
        meta: { sidebar: true }
    },
=======
  /* ===== 公用 ===== */
  { path: "/", component: Home, meta: { sidebar: false } },
  { path: "/login", component: Login, meta: { sidebar: false } },
  { path: "/register", component: Register, meta: { sidebar: false } },

  /* ===== 前台（顧客） ===== */
  { path: "/news", component: NewsPage, meta: { sidebar: false } },
  { path: "/stores", component: StoresPage, meta: { sidebar: false } },
  {
    path: "/booking/grooming",
    component: BookingGroomingPage,
    meta: { sidebar: false },
  },
  {
    path: "/booking/lodging",
    component: BookingLodgingPage,
    meta: { sidebar: false },
  },
  {
    path: "/register/customers",
    component: CustomerRegister,
    meta: { sidebar: false },
  },

  /* ===== 商家 ===== */
  {
    path: "/register/stores/:step",
    component: StoreRegister,
    meta: { sidebar: false },
  },
  {
    path: "/stores/posts/manage",
    component: StoreManage,
    meta: { sidebar: true },
  },
  {
    path: "/stores/posts/add",
    component: StorePostProcess,
    meta: { sidebar: false },
  },
  {
    path: "/stores/posts/edit/:id",
    component: StorePostProcess,
    meta: { sidebar: false },
  },
  {
    path: "/stores/posts/view/:id",
    component: StorePostView,
    meta: { sidebar: false },
  },

  /* ★ 商家預約（新增／編輯／查看） */
  {
    path: "/stores/appointments/add",
    component: StoreAppointment,
    meta: { sidebar: false },
  },
  {
    path: "/stores/appointments/edit/:id",
    component: StoreAppointment,
    meta: { sidebar: false },
  },
  {
    path: "/stores/appointments/view/:id",
    component: StoreAppointment,
    meta: { sidebar: false },
  },

  /* ★ 商家服務（新增／編輯／查看） */
  {
    // 可選參數：type = grooming | lodging；pet = dog | cat
    path: "/stores/services/add/:type?/:pet?",
    component: StoreServices,
    meta: { sidebar: false },
  },
  {
    path: "/stores/services/edit/:id",
    component: StoreServices,
    meta: { sidebar: false },
  },
  {
    path: "/stores/services/view/:id",
    component: StoreServices,
    meta: { sidebar: false },
  },

  /* ===== 管理者 ===== */
  { path: "/admin", component: Admin, meta: { sidebar: true } },
  {
    path: "/admin/stores/manage",
    component: StoreManagement,
    meta: { sidebar: true },
  },
  {
    path: "/admin/stores/:status",
    component: StoreReview,
    meta: { sidebar: false },
  },
  {
    path: "/admin/accounts/:page?",
    component: AccountManagement,
    meta: { sidebar: true },
  },
  { path: "/admin/posts", component: PostManagement, meta: { sidebar: true } },
  {
    path: "/admin/posts/:status",
    component: PostReview,
    meta: { sidebar: false },
  },
>>>>>>> Stashed changes
];

/* ─── Router 實例 ─────────────────────────────── */
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
