<template>
  <div class="page-container">
    <div class="content">
      <div class="login-header">
        <h1 class="title">草药问答</h1>
        <p class="subtitle">学习中草药知识</p>
      </div>

      <van-form @submit="onSubmit">
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
          <van-button
            round
            block
            plain
            type="primary"
            @click="goToRegister"
            style="margin-top: 12px"
          >
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
  padding: 60px 0 40px;
}

.title {
  font-size: 32px;
  font-weight: bold;
  color: #4caf50;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: #999;
}
</style>
