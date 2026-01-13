<template>
  <div class="page-container">
    <van-nav-bar title="首页" />

    <div class="content">
      <!-- 标题区 -->
      <div class="title-card">
        <h2 class="title-main">红色草药问答</h2>
        <p class="title-sub">学习中草药知识，弘扬红色精神</p>
      </div>

      <!-- 功能区 -->
      <div class="card">
        <h3 style="margin-bottom: 16px">开始答题</h3>
        <van-button type="primary" size="large" round block @click="startQuiz">
          随机抽题
        </van-button>
      </div>

      <!-- 分类选择 -->
      <div class="card" v-if="categories.length > 0">
        <h3 style="margin-bottom: 12px">选择分类</h3>
        <van-grid :column-num="3" :border="false">
          <van-grid-item
            v-for="category in categories"
            :key="category"
            :text="category"
            @click="startQuizByCategory(category)"
          />
        </van-grid>
      </div>

      <!-- 难度选择 -->
      <div class="card">
        <h3 style="margin-bottom: 12px">选择难度</h3>
        <van-row gutter="12">
          <van-col span="8">
            <van-button
              plain
              type="success"
              block
              @click="startQuizByDifficulty('easy')"
            >
              简单
            </van-button>
          </van-col>
          <van-col span="8">
            <van-button
              plain
              type="warning"
              block
              @click="startQuizByDifficulty('medium')"
            >
              中等
            </van-button>
          </van-col>
          <van-col span="8">
            <van-button
              plain
              block
              style="
                color: #fff;
                background: var(--primary-color);
                border-color: var(--primary-color);
              "
              @click="startQuizByDifficulty('hard')"
            >
              困难
            </van-button>
          </van-col>
        </van-row>
      </div>
    </div>

    <!-- 底部导航 -->
    <van-tabbar v-model="active" route>
      <van-tabbar-item icon="home-o" to="/home">首页</van-tabbar-item>
      <van-tabbar-item icon="notes-o" to="/history">历史</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/profile">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/store/user";
import { getCategories } from "@/api/question";

const router = useRouter();
const userStore = useUserStore();
const active = ref(0);

const categories = ref([]);

const loadCategories = async () => {
  try {
    const res = await getCategories();
    categories.value = res.data;
  } catch (error) {
    console.error("Failed to load categories:", error);
  }
};

const startQuiz = () => {
  router.push("/question");
};

const startQuizByCategory = (category) => {
  router.push(`/question?category=${category}`);
};

const startQuizByDifficulty = (difficulty) => {
  router.push(`/question?difficulty=${difficulty}`);
};

onMounted(() => {
  loadCategories();
});
</script>

<style scoped>
.content {
  padding-top: 16px;
}

.title-card {
  margin: 16px;
  padding: 32px 24px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  border-left: 4px solid #c8102e;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  position: relative;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.title-card:active {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.title-main {
  margin: 0;
  font-size: 26px;
  font-weight: 600;
  color: #c8102e;
  letter-spacing: 1px;
}

.title-sub {
  margin: 10px 0 0 0;
  font-size: 14px;
  color: #666;
  font-weight: 400;
  line-height: 1.6;
}

.title-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(200, 16, 46, 0.02) 0%,
    transparent 100%
  );
  pointer-events: none;
  border-radius: 16px;
}
</style>
