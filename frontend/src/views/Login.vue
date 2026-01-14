<template>
  <div class="page-container">
    <div class="content">
      <div class="title-card">
        <h1 class="title-main">草药问答</h1>
        <p class="title-sub">学习中草药知识 · 弘扬红色精神</p>
      </div>

      <van-form @submit="onSubmit" class="card">
        <van-cell-group inset>
          <van-field
            v-model="formData.username"
            name="username"
            label="用户名"
            placeholder="请输入用户名"
            :rules="[{ required: true, message: '请输入用户名' }]"
          />
          <van-field
            v-model="formData.password"
            type="password"
            name="password"
            label="密码"
            placeholder="请输入密码"
            :rules="[{ required: true, message: '请输入密码' }]"
          />
        </van-cell-group>

        <div style="margin: 24px 16px">
          <van-button
            round
            block
            type="primary"
            native-type="submit"
            :loading="loading"
          >
            登录
          </van-button>
          <van-button round block class="register-btn" @click="goToRegister">
            注册账号
          </van-button>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/store/user";
import { showToast } from "vant";

const router = useRouter();
const userStore = useUserStore();

const formData = ref({
  username: "",
  password: "",
});

const loading = ref(false);

const onSubmit = async () => {
  loading.value = true;
  try {
    await userStore.login(formData.value);
    showToast("登录成功");
    router.push("/home");
  } catch (error) {
    console.error("Login failed:", error);
  } finally {
    loading.value = false;
  }
};

const goToRegister = () => {
  router.push("/register");
};
</script>

<style scoped>
.login-header {
  text-align: center;
  padding: 80px 0 50px;
}

.title {
  font-size: 36px;
  font-weight: 800;
  color: #c62828;
  margin-bottom: 12px;
  letter-spacing: 2px;
}

.subtitle {
  font-size: 16px;
  color: #6b7280;
  font-weight: 500;
}

/* 输入框毛玻璃效果 */
.van-cell-group--inset {
  margin: 16px;
  background: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(200, 16, 46, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* 注册按钮白色样式 */
.register-btn {
  margin-top: 12px;
  background: white !important;
  color: #c8102e !important;
  border: 1px solid #c8102e !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.register-btn:active {
  background: #f5f5f5 !important;
  transform: scale(0.98);
}
</style>
