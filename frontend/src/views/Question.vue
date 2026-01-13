<template>
  <div class="page-container">
    <van-nav-bar title="答题" left-arrow @click-left="goBack" />

    <div class="content">
      <!-- 加载中 -->
      <van-loading v-if="loading" type="spinner" style="margin: 100px auto">
        加载题目中...
      </van-loading>

      <!-- 题目区域 -->
      <div v-else-if="question">
        <!-- 题目信息 -->
        <div class="card">
          <van-tag type="primary" style="margin-right: 8px">{{
            difficultyText
          }}</van-tag>
          <van-tag v-if="question.category">{{ question.category }}</van-tag>
          <div style="margin-top: 16px; font-size: 16px; line-height: 1.6">
            {{ question.question_text }}
          </div>
        </div>

        <!-- 选项区域 -->
        <div class="card" v-if="!answered">
          <van-radio-group v-model="userAnswer">
            <van-cell-group>
              <van-cell
                v-for="(option, key) in question.options"
                :key="key"
                :title="`${key}. ${option}`"
                clickable
                @click="userAnswer = key"
              >
                <template #right-icon>
                  <van-radio :name="key" />
                </template>
              </van-cell>
            </van-cell-group>
          </van-radio-group>

          <van-button
            type="primary"
            size="large"
            round
            block
            style="margin-top: 24px"
            :disabled="!userAnswer"
            @click="submitAnswer"
            :loading="submitting"
          >
            提交答案
          </van-button>
        </div>

        <!-- 答案解析 -->
        <div class="card" v-else>
          <van-cell-group>
            <van-cell
              v-for="(option, key) in question.options"
              :key="key"
              :title="`${key}. ${option}`"
            >
              <template #right-icon>
                <van-icon
                  v-if="key === correctAnswer"
                  name="success"
                  color="#c8102e"
                  size="20"
                />
                <van-icon
                  v-else-if="key === userAnswer"
                  name="cross"
                  color="#dc143c"
                  size="20"
                />
              </template>
            </van-cell>
          </van-cell-group>

          <!-- 结果提示 -->
          <div style="margin: 20px 0; text-align: center">
            <van-icon
              :name="isCorrect ? 'checked' : 'cross'"
              :color="isCorrect ? '#c8102e' : '#dc143c'"
              size="48"
            />
            <div style="margin-top: 12px; font-size: 18px; font-weight: bold">
              {{ isCorrect ? "回答正确！" : "回答错误" }}
            </div>
          </div>

          <!-- 解析 -->
          <div class="explanation-box" v-if="explanation">
            <div class="explanation-title">📖 题目解析</div>
            <div>{{ explanation }}</div>
          </div>

          <!-- 下一题按钮 -->
          <van-button
            type="primary"
            size="large"
            round
            block
            style="margin-top: 24px"
            @click="nextQuestion"
          >
            下一题
          </van-button>
        </div>
      </div>

      <!-- 无题目 -->
      <van-empty v-else description="暂无题目" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import {
  getRandomQuestion,
  submitAnswer as submitAnswerApi,
} from "@/api/question";
import { showToast } from "vant";

const router = useRouter();
const route = useRoute();

const loading = ref(false);
const submitting = ref(false);
const question = ref(null);
const userAnswer = ref("");
const answered = ref(false);
const isCorrect = ref(false);
const correctAnswer = ref("");
const explanation = ref("");

const difficultyMap = {
  easy: "简单",
  medium: "中等",
  hard: "困难",
};

const difficultyText = computed(() => {
  return difficultyMap[question.value?.difficulty] || "未知";
});

const loadQuestion = async () => {
  loading.value = true;
  try {
    const params = {};
    if (route.query.difficulty) {
      params.difficulty = route.query.difficulty;
    }
    if (route.query.category) {
      params.category = route.query.category;
    }

    const res = await getRandomQuestion(params);
    question.value = res.data;
    userAnswer.value = "";
    answered.value = false;
  } catch (error) {
    console.error("Failed to load question:", error);
    showToast("加载题目失败");
  } finally {
    loading.value = false;
  }
};

const submitAnswer = async () => {
  if (!userAnswer.value) {
    showToast("请选择答案");
    return;
  }

  submitting.value = true;
  try {
    const res = await submitAnswerApi(question.value.id, {
      answer: userAnswer.value,
    });
    answered.value = true;
    isCorrect.value = res.data.is_correct;
    correctAnswer.value = res.data.correct_answer;
    explanation.value = res.data.explanation;
  } catch (error) {
    console.error("Failed to submit answer:", error);
  } finally {
    submitting.value = false;
  }
};

const nextQuestion = () => {
  loadQuestion();
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  loadQuestion();
});
</script>

<style scoped>
.result-card {
  text-align: center;
  padding: 32px 16px;
  background: linear-gradient(
    135deg,
    rgba(200, 16, 46, 0.05) 0%,
    rgba(255, 255, 255, 0.9) 100%
  );
  border-radius: 16px;
  margin-bottom: 16px;
  backdrop-filter: blur(10px);
}

.result-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.result-text {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
}

.correct-answer {
  color: var(--primary-color);
  font-weight: bold;
}

.wrong-answer {
  color: var(--danger-color);
  font-weight: bold;
}
</style>
