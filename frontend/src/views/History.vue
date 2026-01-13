<template>
  <div class="page-container">
    <van-nav-bar title="答题历史" />

    <div class="content">
      <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
        <van-list
          v-model:loading="loading"
          :finished="finished"
          finished-text="没有更多了"
          @load="onLoad"
        >
          <div class="history-item" v-for="record in records" :key="record.id">
            <div style="margin-bottom: 8px; color: #666; font-size: 12px">
              {{ formatDate(record.answered_at) }}
            </div>
            <div style="margin-bottom: 12px; font-size: 15px">
              {{ record.question.question_text }}
            </div>
            <van-row gutter="12">
              <van-col span="12">
                <div style="font-size: 13px; color: #999">
                  你的答案:
                  <span :class="record.is_correct ? 'correct' : 'incorrect'">{{
                    record.user_answer
                  }}</span>
                </div>
              </van-col>
              <van-col span="12">
                <div style="font-size: 13px; color: #999">
                  正确答案:
                  <span class="correct">{{
                    record.question.correct_answer
                  }}</span>
                </div>
              </van-col>
            </van-row>
            <div
              v-if="record.question.explanation"
              style="
                margin-top: 12px;
                padding: 12px;
                background: #f8f9fa;
                border-radius: 4px;
                font-size: 13px;
              "
            >
              <div style="color: #4caf50; margin-bottom: 4px">解析:</div>
              {{ record.question.explanation }}
            </div>
          </div>
        </van-list>

        <van-empty
          v-if="!loading && records.length === 0"
          description="暂无答题记录"
        />
      </van-pull-refresh>
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
import { ref } from "vue";
import { getAnswerHistory } from "@/api/user";

const active = ref(1);
const records = ref([]);
const loading = ref(false);
const finished = ref(false);
const refreshing = ref(false);
const page = ref(1);
const perPage = 20;

const onLoad = async () => {
  try {
    const res = await getAnswerHistory({ page: page.value, per_page: perPage });

    if (page.value === 1) {
      records.value = res.data.records;
    } else {
      records.value = [...records.value, ...res.data.records];
    }

    loading.value = false;

    if (
      records.value.length >= res.data.total ||
      res.data.records.length === 0
    ) {
      finished.value = true;
    } else {
      page.value++;
    }
  } catch (error) {
    console.error("Failed to load history:", error);
    loading.value = false;
  }
};

const onRefresh = async () => {
  page.value = 1;
  finished.value = false;
  await onLoad();
  refreshing.value = false;
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const diff = now - date;
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) return `${days}天前`;
  if (hours > 0) return `${hours}小时前`;
  if (minutes > 0) return `${minutes}分钟前`;
  return "刚刚";
};
</script>
