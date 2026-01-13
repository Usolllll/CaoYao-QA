import { defineStore } from "pinia";
import { login, register, getCurrentUser } from "@/api/auth";
import router from "@/router";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: localStorage.getItem("token") || "",
    userInfo: null,
    statistics: null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    username: (state) => state.userInfo?.username || "",
    nickname: (state) => state.userInfo?.nickname || "",
  },

  actions: {
    // 登录
    async login(credentials) {
      const res = await login(credentials);
      this.token = res.data.access_token;
      this.userInfo = res.data.user;
      localStorage.setItem("token", this.token);
      return res;
    },

    // 注册
    async register(data) {
      const res = await register(data);
      this.token = res.data.access_token;
      this.userInfo = res.data.user;
      localStorage.setItem("token", this.token);
      return res;
    },

    // 登出
    logout() {
      this.token = "";
      this.userInfo = null;
      this.statistics = null;
      localStorage.removeItem("token");
      router.push("/login");
    },

    // 检查认证状态
    async checkAuth() {
      if (this.token) {
        try {
          const res = await getCurrentUser();
          this.userInfo = res.data;
        } catch (error) {
          this.logout();
        }
      }
    },

    // 更新统计信息
    updateStatistics(stats) {
      this.statistics = stats;
    },
  },
});
