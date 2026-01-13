<template>
  <div class="page-container">
    <div class="content">
      <!-- 标题区 -->
      <div class="title-card">
        <h2 style="margin: 0; font-size: 24px; font-weight: bold">
          草药和红色精神问答
        </h2>
        <p style="margin: 8px 0 0 0; font-size: 14px; opacity: 0.8">
          学习中草药知识，弘扬红色精神
        </p>
      </div>

      <!-- 功能区 -->
      <div class="card">
        <h3 style="margin-bottom: 16px">开始答题</h3>
        <van-button
          type="primary"
          size="large"
          round
          block
          icon="fire"
          @click="startQuiz"
        >
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
              type="danger"
              block
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
  padding: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: white;
  text-align: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
</style>
