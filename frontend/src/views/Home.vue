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

      <!-- 分类选择 (Horizontal Scroll) -->
      <div v-if="categories.length > 0">
        <h3
          style="
            margin: 0 0 16px 4px;
            font-weight: 600;
            color: var(--text-primary);
          "
        >
          <span
            style="
              display: inline-block;
              width: 6px;
              height: 6px;
              background: var(--accent-gold);
              vertical-align: middle;
              margin-right: 12px;
              border-radius: 50%;
            "
          ></span>
          选择分类
        </h3>
        <div class="category-scroll-container">
          <div
            v-for="category in categories"
            :key="category"
            class="category-card-scroll"
            :class="{ 'shanxi-card': category === '山西' }"
            @click="startQuizByCategory(category)"
          >
            <van-icon :name="getCategoryIcon(category)" class="category-icon" />
            <div class="category-name">{{ category }}</div>
          </div>
        </div>
      </div>

      <!-- 难度选择 -->
      <div style="margin-top: 24px">
        <h3
          style="
            margin: 0 0 16px 4px;
            font-weight: 600;
            color: var(--text-primary);
          "
        >
          <span
            style="
              display: inline-block;
              width: 4px;
              height: 16px;
              background: var(--accent-gold);
              vertical-align: middle;
              margin-right: 8px;
              border-radius: 2px;
            "
          ></span>
          选择难度
        </h3>
        <div class="difficulty-group">
          <div
            class="difficulty-card easy-mode"
            :class="{ active: false }"
            @click="startQuizByDifficulty('easy')"
          >
            简单
          </div>
          <div
            class="difficulty-card medium-mode"
            :class="{ active: false }"
            @click="startQuizByDifficulty('medium')"
          >
            中等
          </div>
          <div
            class="difficulty-card hard-mode"
            :class="{ active: false }"
            @click="startQuizByDifficulty('hard')"
          >
            困难
          </div>
        </div>
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

// 图标映射表
const categoryIcons = {
  红船精神: "guide-o", // 指引方向
  井冈山精神: "flag-o", // 红旗飘飘
  延安精神: "fire-o", // 革命火种
  西柏坡精神: "todo-list-o", // 运筹帷幄
  抗美援朝精神: "shield-o", // 保家卫国
  两弹一星精神: "star-o", // 科技之星
  抗疫精神: "like-o", // 生命至上
  山西: "hotel-o", // 古建晋商
};

const getCategoryIcon = (name) => {
  return categoryIcons[name] || "flower-o";
};

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
/* Title card styles removed to use main.css global styles */
</style>
