import request from "./request";

// 获取随机题目
export function getRandomQuestion(params) {
  return request({
    url: "/questions/random",
    method: "get",
    params,
  });
}

// 获取指定题目
export function getQuestion(id) {
  return request({
    url: `/questions/${id}`,
    method: "get",
  });
}

// 提交答案
export function submitAnswer(questionId, data) {
  return request({
    url: `/questions/${questionId}/answer`,
    method: "post",
    data,
  });
}

// 获取题目分类
export function getCategories() {
  return request({
    url: "/questions/categories",
    method: "get",
  });
}

// 获取题目列表
export function getQuestionList(params) {
  return request({
    url: "/questions/list",
    method: "get",
    params,
  });
}
