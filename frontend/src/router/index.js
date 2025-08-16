import { createRouter, createWebHistory } from "vue-router";
import Home from "../auth/WelcomePage.vue";

// 註冊登入
import Login from "../auth/Login.vue";
import Register from "../auth/Register.vue";
import ForgotPassword from "../auth/ForgotPassword.vue";
import CustomerRegister from "../pages/Customers/CustomerRegister.vue";
import StoresRegister from "../pages/Stores/StoreRegister.vue";

// 使用者畫面Router
import MemberProfiles from "../pages/Customers/MemberCenter/Profiles.vue";
import MemberPets from "../pages/Customers/MemberCenter/Pets.vue";
import MemberChangePassword from "../pages/Customers/MemberCenter/ChangePassword.vue";

// 商家畫面Router
import StoresDashboard from "../pages/Stores/StoresDashboard.vue";
import StoresAddBookings from "../pages/Stores/Booking/AddBookings.vue";
import StoresGrooming from "../pages/Stores/Booking/Grooming/GroomingBooking.vue";
import StoresBoarding from "../pages/Stores/Booking/Boarding/BoardingBooking.vue";
import StoresGroomingManage from "../pages/Stores/Booking/Grooming/GroomingManagement.vue";
import StoresGroomingReview from "../pages/Stores/Booking/Grooming/Review.vue";
import StoresGroomingDetails from "../pages/Stores/Booking/Grooming/Details.vue";
import StoresBoardingManage from "../pages/Stores/Booking/Boarding/BoardingManagement.vue";
import StoresBoardingReview from "../pages/Stores/Booking/Boarding/Review.vue";
import StoresBoardingDetails from "../pages/Stores/Booking/Boarding/Details.vue";
import StoresBookingHistory from "../pages/Stores/HistoryBooking/BookingHistory.vue";
import StoresWatchLists from "../pages/Stores/Booking/WatchLists.vue";
//
import StoresEditInfo from "../pages/Stores/Info/EditInfo.vue";
import StoresInfoManage from "../pages/Stores/Info/InfoManagement.vue";
import StoresOpenServices from "../pages/Stores/Info/OpenServices.vue";
//
import StoresAddServices from "../pages/Stores/Services/AddServices.vue";
import StoresServicesManage from "../pages/Stores/Services/ServicesManagement.vue";
//
import StoresManage from "../pages/Stores/Posts/Postsmanage.vue";
import StoresPostProcess from "../pages/Stores/Posts/PostsProcess.vue";
import StoresPostView from "../pages/Stores/Posts/PostsView.vue";

// 管理者頁面Router
import Admin from "../pages/Admin/AdminDashboard.vue";
import StoresManagement from "../pages/Admin/Stores/StoreManagement.vue";
import StoresReview from "../pages/Admin/Stores/StoreReview.vue";
import AccountManagement from "../pages/Admin/Account/AccountManagement.vue";
import PostManagement from "../pages/Admin/Posts/PostManagement.vue";
import PostReview from "../pages/Admin/Posts/PostReview.vue";

// 前台頁面Router - 使用正確的路徑
import NewsPage from "../pages/Customers/News.vue";
import StoresPage from "../pages/Customers/StoresLists.vue";
import BookingGroomingPage from "../pages/Customers/Booking/Grooming.vue";
import BookingBoardingPage from "../pages/Customers/Booking/Boarding.vue";
import NewsView from "../pages/Customers/NewsView.vue";

const routes = [
  {
    path: "/",
    component: Home,
    meta: { sidebar: false },
  },
  {
    path: "/news",
    component: NewsPage,
    meta: { sidebar: false },
  },
  {
    path: "/news/views/:id",
    component: NewsView,
    meta: { sidebar: false },
  },
  {
    path: "/stores",
    component: StoresPage,
    meta: { sidebar: false },
  },
  {
    path: "/booking/grooming",
    component: BookingGroomingPage,
    meta: { sidebar: false },
  },
  {
    path: "/booking/boarding",
    component: BookingBoardingPage,
    meta: { sidebar: false },
  },
  // 登入註冊路由
  {
    path: "/login",
    component: Login,
    meta: { sidebar: false },
  },
  {
    path: "/register",
    component: Register,
    meta: { sidebar: false },
  },
  {
    path: "/password/forgot",
    component: ForgotPassword,
    meta: { sidebar: false },
  },
  {
    path: "/password/change",
    component: ForgotPassword,
    meta: { sidebar: false },
  },
  {
    path: "/register/customers",
    component: CustomerRegister,
    meta: { sidebar: false },
  },
  {
    path: "/register/stores/:step",
    component: StoresRegister,
    meta: { sidebar: false },
  },
  // 會員中心
  {
    path: "/members/profiles",
    component: MemberProfiles,
    meta: { sidebar: true },
  },
  {
    path: "/members/pets",
    component: MemberPets,
    meta: { sidebar: true },
  },
  {
    path: "/members/profiles/password/change",
    component: MemberChangePassword,
    meta: { sidebar: true },
  },
  // 商家頁面路由
  {
    path: "/register/stores/:step",
    component: StoresRegister,
    meta: { sidebar: false },
  },

  // 儀表板
  {
    path: "/stores/dashboard",
    component: StoresDashboard,
    meta: { sidebar: true },
  },

  // 新增預約
  {
    path: "/stores/addbookings",
    component: StoresAddBookings,
    meta: { sidebar: true },
  },

  // 美容預約管理
  {
    path: "/stores/grooming-bookings",
    component: StoresGrooming,
    meta: { sidebar: true },
  },
  {
    path: "/stores/grooming-bookings/manage",
    name: "Grooming",
    component: StoresGroomingManage,
    meta: { sidebar: true },
  },
  {
    path: "/stores/grooming-bookings/review",
    component: StoresGroomingReview,
    meta: { sidebar: false },
  },
  {
    path: "/stores/grooming-bookings/details",
    component: StoresGroomingDetails,
    meta: { sidebar: false },
  },
  {
    path: "/stores/grooming-bookings/history",
    component: StoresBookingHistory,
    meta: { sidebar: true },
  },
  {
    path: "/stores/grooming/watchlists",
    component: StoresWatchLists,
    meta: { sidebar: true },
  },

  // 住宿預約管理
  {
    path: "/stores/boarding-bookings",
    component: StoresBoarding,
    meta: { sidebar: true },
  },
  {
    path: "/stores/boarding-bookings/manage",
    component: StoresBoardingManage,
    meta: { sidebar: true },
  },
  {
    path: "/stores/boarding-bookings/review",
    component: StoresBoardingReview,
    meta: { sidebar: false },
  },
  {
    path: "/stores/boarding-bookings/details",
    component: StoresBoardingDetails,
    meta: { sidebar: false },
  },
  {
    path: "/stores/boarding-bookings/history",
    component: StoresBookingHistory,
    meta: { sidebar: true },
  },
  {
    path: "/stores/boarding/watchlists",
    component: StoresWatchLists,
    meta: { sidebar: true },
  },
  // 店家管理
  // 資訊
  {
    path: "/stores/info/edit",
    component: StoresEditInfo,
    meta: { sidebar: true },
  },
  {
    path: "/stores/info/manage",
    component: StoresInfoManage,
    meta: { sidebar: true },
  },
  {
    path: "/stores/openservices",
    component: StoresOpenServices,
    meta: { sidebar: true },
  },
  // 服務
  {
    path: "/stores/services/add",
    component: StoresAddServices,
    meta: { sidebar: true },
  },
  {
    path: "/stores/services/edit/:id/:type",
    component: StoresAddServices,
    meta: { sidebar: true },
  },
  {
    path: "/stores/services/manage",
    component: StoresServicesManage,
    meta: { sidebar: true },
  },
  // 貼文
  {
    path: "/stores/posts/manage",
    component: StoresManage,
    meta: { sidebar: true },
  },
  {
    path: "/stores/posts/add",
    component: StoresPostProcess,
    meta: { sidebar: false },
  },
  {
    path: "/stores/posts/edit/:id",
    component: StoresPostProcess,
    meta: { sidebar: false },
  },
  {
    path: "/stores/posts/view/:id",
    component: StoresPostView,
    meta: { sidebar: false },
  },

  // 管理者頁面Router
  {
    path: "/admin",
    component: Admin,
    meta: { sidebar: true },
  },
  {
    path: "/admin/stores/manage",
    component: StoresManagement,
    meta: { sidebar: true },
  },
  {
    path: "/admin/stores/details/:id",
    component: StoresReview,
    meta: { sidebar: false },
  },
  {
    path: "/admin/accounts/:page?",
    component: AccountManagement,
    meta: { sidebar: true },
  },
  {
    path: "/admin/posts",
    component: PostManagement,
    meta: { sidebar: true },
  },
  {
    path: "/admin/posts/:status",
    component: PostReview,
    meta: { sidebar: false },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: "smooth",
      };
    }
    if (savedPosition) {
      return savedPosition;
    }
    return { top: 0 };
  },
});

export default router;
