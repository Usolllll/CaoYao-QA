import axios from "axios";
import { showToast } from "vant";
import { useUserStore } from "@/store/user";

const request = axios.create({
  baseURL: "/api",
  timeout: 10000,
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const userStore = useUserStore();
    if (userStore.token) {
      config.headers["Authorization"] = `Bearer ${userStore.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const res = response.data;
    if (res.success) {
      return res;
    } else {
      showToast(res.message || "请求失败");
      return Promise.reject(new Error(res.message || "请求失败"));
    }
  },
  (error) => {
    if (error.response) {
      const status = error.response.status;
      if (status === 401) {
        const userStore = useUserStore();
        userStore.logout();
        showToast("登录已过期，请重新登录");
      } else if (status === 404) {
        showToast("请求的资源不存在");
      } else if (status === 422) {
        showToast("请求格式错误 (422)");
        console.error("422 Error - Check token format and JWT configuration");
      } else if (status === 500) {
        showToast("服务器错误");
      } else {
        showToast(error.response.data?.message || "请求失败");
      }
    } else {
      showToast("网络连接失败");
    }
    return Promise.reject(error);
  }
);

export default request;
