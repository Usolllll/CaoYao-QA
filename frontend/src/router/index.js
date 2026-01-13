import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/store/user";
import { showToast } from "vant";

const routes = [
  {
    path: "/",
    redirect: "/home",
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Login.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("@/views/Register.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/home",
    name: "Home",
    component: () => import("@/views/Home.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/question",
    name: "Question",
    component: () => import("@/views/Question.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/history",
    name: "History",
    component: () => import("@/views/History.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/profile",
    name: "Profile",
    component: () => import("@/views/Profile.vue"),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const requiresAuth = to.meta.requiresAuth !== false;

  if (requiresAuth && !userStore.isLoggedIn) {
    showToast("请先登录");
    next("/login");
  } else if (
    !requiresAuth &&
    userStore.isLoggedIn &&
    (to.path === "/login" || to.path === "/register")
  ) {
    next("/home");
  } else {
    next();
  }
});

export default router;
