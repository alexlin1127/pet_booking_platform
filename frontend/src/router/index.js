import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import UserRegister from "../pages/Users/Register.vue"
import ShopRegister from "../pages/Shops/Register.vue"



const routes = [
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
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;