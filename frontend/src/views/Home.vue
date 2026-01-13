<template>
  <div class="page-container">
    <div class="content">
      <!-- 用户统计卡片 -->
      <div class="stats-card">
        <van-row gutter="20">
          <van-col span="8">
            <div class="stats-item">
              <div class="stats-value">
                {{ statistics?.total_questions || 0 }}
              </div>
              <div class="stats-label">总题数</div>
            </div>
          </van-col>
          <van-col span="8">
            <div class="stats-item">
              <div class="stats-value">
                {{ statistics?.correct_answers || 0 }}
              </div>
              <div class="stats-label">正确数</div>
            </div>
          </van-col>
          <van-col span="8">
            <div class="stats-item">
              <div class="stats-value">{{ accuracyRate }}%</div>
              <div class="stats-label">正确率</div>
            </div>
          </van-col>
        </van-row>
        <van-divider
          style="margin: 16px 0; border-color: rgba(255, 255, 255, 0.3)"
        />
        <div style="text-align: center">
          <span style="font-size: 14px">连续学习 </span>
          <span style="font-size: 24px; font-weight: bold">{{
            statistics?.continuous_days || 0
          }}</span>
          <span style="font-size: 14px"> 天</span>
        </div>
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
import { getStatistics } from "@/api/user";
import { getCategories } from "@/api/question";

const router = useRouter();
const userStore = useUserStore();
const active = ref(0);

const statistics = ref(null);
const categories = ref([]);

const accuracyRate = computed(() => {
  if (!statistics.value || statistics.value.total_questions === 0) return 0;
  return Math.round(statistics.value.accuracy_rate);
});

const loadStatistics = async () => {
  try {
    const res = await getStatistics();
    statistics.value = res.data;
    userStore.updateStatistics(res.data);
  } catch (error) {
    console.error("Failed to load statistics:", error);
  }
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
  loadStatistics();
  loadCategories();
});
</script>

<style scoped>
.content {
  padding-top: 16px;
}
</style>
