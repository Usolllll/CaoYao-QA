import request from "./request";

// 获取用户资料
export function getProfile() {
  return request({
    url: "/user/profile",
    method: "get",
  });
}

// 更新用户资料
export function updateProfile(data) {
  return request({
    url: "/user/profile",
    method: "put",
    data,
  });
}

// 获取统计信息
export function getStatistics() {
  return request({
    url: "/user/statistics",
    method: "get",
  });
}

// 获取答题历史
export function getAnswerHistory(params) {
  return request({
    url: "/user/history",
    method: "get",
    params,
  });
}

// 获取每周统计
export function getWeeklyStatistics() {
  return request({
    url: "/user/statistics/weekly",
    method: "get",
  });
}
