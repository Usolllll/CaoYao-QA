<template>
  <div class="page-container">
    <van-nav-bar title="注册" left-arrow @click-left="goBack" />

    <div class="content">
      <van-form @submit="onSubmit">
        <van-cell-group inset>
          <van-field
            v-model="formData.username"
            name="username"
            label="用户名"
            placeholder="请输入用户名"
            :rules="[
              { required: true, message: '请输入用户名' },
              {
                pattern: /^[a-zA-Z0-9_]{4,20}$/,
                message: '用户名为4-20位字母数字下划线',
              },
            ]"
          />
          <van-field
            v-model="formData.nickname"
            name="nickname"
            label="昵称"
            placeholder="请输入昵称（可选）"
          />
          <van-field
            v-model="formData.password"
            type="password"
            name="password"
            label="密码"
            placeholder="请输入密码"
            :rules="[
              { required: true, message: '请输入密码' },
              { min: 6, message: '密码至少6位' },
            ]"
          />
          <van-field
            v-model="confirmPassword"
            type="password"
            name="confirmPassword"
            label="确认密码"
            placeholder="请再次输入密码"
            :rules="[
              { required: true, message: '请确认密码' },
              { validator: validatePassword, message: '两次密码不一致' },
            ]"
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
            注册
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
  nickname: "",
  password: "",
});

const confirmPassword = ref("");
const loading = ref(false);

const validatePassword = () => {
  return formData.value.password === confirmPassword.value;
};

const onSubmit = async () => {
  loading.value = true;
  try {
    await userStore.register(formData.value);
    showToast("注册成功");
    router.push("/home");
  } catch (error) {
    console.error("Register failed:", error);
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.back();
};
</script>

<style scoped>
.content {
  padding-top: 16px;
}

.login-header {
  text-align: center;
  padding: 60px 0 40px;
}

.title {
  font-size: 36px;
  font-weight: bold;
  background: linear-gradient(135deg, #c8102e 0%, #e63946 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
  letter-spacing: 2px;
}

.subtitle {
  font-size: 15px;
  color: #666;
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
</style>
