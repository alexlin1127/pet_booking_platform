import { createRouter, createWebHistory } from "vue-router";
import Home from "../auth/WelcomePage.vue";

// 註冊登入
import Login from "../auth/Login.vue";
import Register from "../auth/Register.vue";
import CustomerRegister from "../pages/Customers/CustomerRegister.vue"
import StoresRegister from "../pages/Stores/StoreRegister.vue"

// 使用者畫面Router


// 商家畫面Router
import StoreRegister from "../pages/Stores/StoreRegister.vue"
import StoreManage from "../pages/Stores/Posts/Postsmanage.vue"
import StorePostProcess from "../pages/Stores/Posts/PostsProcess.vue"
import StorePostReview from "../pages/Stores/Posts/StorePostReview.vue"
import SpostManagement from '../pages/Stores/SpostManagement.vue'



// 管理者頁面Router
import Admin from "../pages/Admin/AdminDashboard.vue"
import StoresManagement from "../pages/Admin/Stores/StoreManagement.vue"
import StoresReview from "../pages/Admin/Stores/StoreReview.vue"
import AccountManagement from "../pages/Admin/Account/AccountManagement.vue"
import PostManagement from "../pages/Admin/Posts/PostManagement.vue"
import PostReview from "../pages/Admin/Posts/PostReview.vue";
import AdminDashboard from "../pages/Admin/AdminDashboard.vue";
import NewPost from "../pages/Stores/NewPost.vue"

// 前台頁面Router - 使用正確的路徑
import NewsPage from "../pages/Customers/News.vue";
import StoresPage from "../pages/Customers/StoresView.vue";
import BookingGroomingPage from "../pages/Customers/Booking/Grooming.vue";
import BookingLodgingPage from "../pages/Customers/Booking/Lodging.vue";
import StoresInfo from "../pages/Stores/StoresInfo.vue";
import EditStoresInfo from "../pages/Stores/EditStoresInfo.vue";
import OpenService from "../pages/Stores/OpenService.vue";
import ServicesManage from "../pages/Stores/ServicesManage.vue";
import NewsView from "../pages/Customers/NewsView.vue";
import ServicesList from "../pages/Customers/ServicesList.vue";
import StoresList from "../pages/Customers/StoresList.vue";




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
        path: "/news/view/:id",
        component: NewsView,
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
        path: "/booking/boarding",
        component: BookingBoardingPage,
        meta: { sidebar: false }
    },
    // 登入註冊路由
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
    // Customers頁面路由
    {
        path: "/servicelist",
        component: ServicesList,
        meta: { sidebar: false }
    },
    {
        path: '/stores/:type(grooming|lodging)',
        component: StoresList,
        meta: { sidebar: false }
    },
    // 商家頁面路由
    {
        path: "/register/stores/:step",
        component: StoresRegister,
        meta: { sidebar: false }
    },

    // 儀表板
    {
        path: "/stores/dashboard",
        component: StoresDashboard,
        meta: { sidebar: true }
    },

    // 新增預約
    {
        path: "/stores/addbookings",
        component: StoresAddBookings,
        meta: { sidebar: true }
    },

    // 美容預約管理
    {
        path: "/stores/grooming-bookings",
        component: StoresGrooming,
        meta: { sidebar: true }
    },
    {
        path: "/stores/grooming-bookings/manage",
        name: "Grooming",
        component: StoresGroomingManage,
        meta: { sidebar: true }
    },
    {
        path: "/stores/grooming-bookings/history",
        component: StoresBookingHistory,
        meta: { sidebar: true }
    },
    {
        path: "/stores/grooming/watchlists",
        component: StoresWatchLists,
        meta: { sidebar: true }
    },

    // 住宿預約管理
    {
        path: "/stores/boarding-bookings",
        component: StoresDashboard,
        meta: { sidebar: true }
    },
    {
        path: "/stores/boarding-bookings/manage",
        component: StoresBoardingManage,
        meta: { sidebar: true }
    },
    {
        path: "/stores/boarding-bookings/history",
        component: StoresBookingHistory,
        meta: { sidebar: true }
    },
    {
        path: "/stores/boarding/watchlists",
        component: StoresWatchLists,
        meta: { sidebar: true }
    },
    // 店家管理
    // 資訊
    {
        path: "/stores/info/edit",
        component: StoresEditInfo,
        meta: { sidebar: true }
    },
    {
        path: "/stores/info/manage",
        component: StoresInfoManage,
        meta: { sidebar: true }
    },
    {
        path: "/stores/openservices",
        component: StoresOpenServices,
        meta: { sidebar: true }
    },
    // 服務
    {
        path: "/stores/services/add",
        component: StoresAddServices,
        meta: { sidebar: true }
    },
    {
        path: "/stores/services/manage",
        component: StoresServicesManage,
        meta: { sidebar: true }
    },
    // 貼文
    {
        path: "/stores/posts/manage",
        component: StoresManage,
        meta: { sidebar: true }
    },
    {
        path: "/stores/posts/add",
        component: StoresPostProcess,
        meta: { sidebar: false }
    },
    {
        path: "/stores/posts/edit/:id",
        component: StoresPostProcess,
        meta: { sidebar: false }
    },
    {
        path: "/stores/posts/view/:id",
        component: StorePostReview,
        meta: { sidebar: false }
    },

    // 管理者頁面Router
    {
        path: "/admin",
        component: Admin,
        meta: { sidebar: true }
    },
    {
        path: "/admin/stores/manage",
        component: StoresManagement,
        meta: { sidebar: true }
    },
    {
        path: "/admin/stores/:status",
        component: StoresReview,
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
    
    // // 店家頁面Router
    {
        path: "/stores",
        component: AdminDashboard,
        meta: { sidebar: false }
    },
    {
        path: "/stores/store-management",
        component: SpostManagement,
        meta: { sidebar: false }
    },
    {
        path: "/stores/posts/:status",
        component: StorePostReview,
        meta: { sidebar: false }
    },
    {
        path: "/stores/newpost",
        component: NewPost,
        meta: { sidebar: false }
    },
    {
        path: "/stores/info",
        component: StoresInfo,
        meta: { sidebar: false }
    },
    {
        path: "/stores/info/edit",
        component: EditStoresInfo,
        meta: { sidebar: false }
    },    
    {
        path: "/stores/serviceactivate",
        component: OpenService,
        meta: { sidebar: false }
    },
    {
        path: "/stores/service",
        component: ServicesManage,
        meta: { sidebar: false }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (to.hash) {
            return {
                el: to.hash,
                behavior: 'smooth',
            }
        }
        if (savedPosition) {
            return savedPosition
        }
        return { top: 0 }
    },
});

export default router;