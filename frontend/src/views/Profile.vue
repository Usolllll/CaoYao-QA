<template>
  <div class="page-container">
    <van-nav-bar title="个人中心" />

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

      <!-- 用户信息卡片 -->
      <div class="card">
        <van-cell-group>
          <van-cell title="用户名" :value="userStore.username" />
          <van-cell title="昵称" :value="userStore.nickname || '未设置'" />
          <van-cell
            title="注册时间"
            :value="formatDate(profile?.user?.created_at)"
          />
        </van-cell-group>
      </div>

      <!-- 功能菜单 -->
      <div class="card">
        <van-cell-group>
          <van-cell title="修改昵称" is-link @click="showEditNickname = true" />
          <van-cell title="清除缓存" is-link @click="clearCache" />
          <van-cell title="关于我们" is-link @click="showAbout = true" />
        </van-cell-group>
      </div>

      <!-- 退出登录 -->
      <div style="margin: 24px 16px">
        <van-button
          type="danger"
          size="large"
          round
          block
          @click="handleLogout"
        >
          退出登录
        </van-button>
      </div>
    </div>

    <!-- 底部导航 -->
    <van-tabbar v-model="active" route>
      <van-tabbar-item icon="home-o" to="/home">首页</van-tabbar-item>
      <van-tabbar-item icon="notes-o" to="/history">历史</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/profile">我的</van-tabbar-item>
    </van-tabbar>

    <!-- 修改昵称弹窗 -->
    <van-dialog
      v-model:show="showEditNickname"
      title="修改昵称"
      show-cancel-button
      @confirm="updateNickname"
    >
      <van-field v-model="newNickname" placeholder="请输入新昵称" />
    </van-dialog>

    <!-- 关于我们弹窗 -->
    <van-dialog
      v-model:show="showAbout"
      title="关于我们"
      confirm-button-text="知道了"
    >
      <div style="padding: 20px; text-align: center">
        <h3>草药问答系统 v1.0</h3>
        <p style="margin-top: 12px; color: #666">
          一个帮助用户学习中草药知识的移动端应用
        </p>
        <p style="margin-top: 8px; color: #999; font-size: 12px">
          © 2026 CaoYao-QA
        </p>
      </div>
    </van-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useUserStore } from "@/store/user";
import { getProfile, updateProfile as updateProfileApi } from "@/api/user";
import { showToast, showConfirmDialog } from "vant";

const userStore = useUserStore();
const active = ref(2);

const profile = ref(null);
const statistics = ref(null);
const showEditNickname = ref(false);
const showAbout = ref(false);
const newNickname = ref("");

const accuracyRate = computed(() => {
  if (!statistics.value || statistics.value.total_questions === 0) return 0;
  return Math.round(statistics.value.accuracy_rate);
});

const loadProfile = async () => {
  try {
    const res = await getProfile();
    profile.value = res.data;
    statistics.value = res.data.statistics;
    newNickname.value = res.data.user.nickname || "";
  } catch (error) {
    console.error("Failed to load profile:", error);
  }
};

const updateNickname = async () => {
  try {
    await updateProfileApi({ nickname: newNickname.value });
    showToast("修改成功");
    loadProfile();
  } catch (error) {
    console.error("Failed to update nickname:", error);
  }
};

const clearCache = async () => {
  try {
    await showConfirmDialog({
      title: "提示",
      message: "确定要清除缓存吗？",
    });
    // 这里可以添加清除缓存的逻辑
    showToast("缓存已清除");
  } catch {
    // 用户取消
  }
};

const handleLogout = async () => {
  try {
    await showConfirmDialog({
      title: "提示",
      message: "确定要退出登录吗？",
    });
    userStore.logout();
    showToast("已退出登录");
  } catch {
    // 用户取消
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "-";
  const date = new Date(dateString);
  return date.toLocaleDateString("zh-CN");
};

onMounted(() => {
  loadProfile();
});
</script>
