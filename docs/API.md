# API 接口文档

## 基础信息

- 基础 URL: `http://localhost:5000/api`
- 请求格式: JSON
- 认证方式: JWT Bearer Token

## 通用响应格式

### 成功响应

```json
{
  "success": true,
  "message": "Success",
  "code": 200,
  "data": {}
}
```

### 错误响应

```json
{
  "success": false,
  "message": "Error message",
  "code": 400
}
```

## 认证接口

### 1. 用户注册

**接口**: `POST /auth/register`

**请求参数**:

```json
{
  "username": "testuser",
  "password": "123456",
  "nickname": "测试用户"
}
```

**响应数据**:

```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "testuser",
      "nickname": "测试用户",
      "created_at": "2026-01-13T10:00:00"
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2. 用户登录

**接口**: `POST /auth/login`

**请求参数**:

```json
{
  "username": "testuser",
  "password": "123456"
}
```

**响应数据**:

```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "testuser",
      "nickname": "测试用户"
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 3. 获取当前用户信息

**接口**: `GET /auth/me`

**请求头**: `Authorization: Bearer {token}`

**响应数据**:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "testuser",
    "nickname": "测试用户"
  }
}
```

### 4. 退出登录

**接口**: `POST /auth/logout`

**请求头**: `Authorization: Bearer {token}`

## 题目接口

### 1. 获取随机题目

**接口**: `GET /questions/random`

**请求头**: `Authorization: Bearer {token}`

**查询参数**:

- `difficulty`: 难度 (可选: easy, medium, hard)
- `category`: 分类 (可选)

**响应数据**:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "question_text": "人参的主要功效是什么？",
    "options": {
      "A": "清热解毒",
      "B": "大补元气",
      "C": "活血化瘀",
      "D": "止咳平喘"
    },
    "difficulty": "easy",
    "category": "补益药"
  }
}
```

### 2. 获取指定题目

**接口**: `GET /questions/{question_id}`

**请求头**: `Authorization: Bearer {token}`

**响应数据**: 同上

### 3. 提交答案

**接口**: `POST /questions/{question_id}/answer`

**请求头**: `Authorization: Bearer {token}`

**请求参数**:

```json
{
  "answer": "B"
}
```

**响应数据**:

```json
{
  "success": true,
  "data": {
    "is_correct": true,
    "correct_answer": "B",
    "explanation": "人参具有大补元气、复脉固脱...",
    "statistics": {
      "total_questions": 10,
      "correct_answers": 8,
      "accuracy_rate": 80.0
    }
  }
}
```

### 4. 获取题目分类

**接口**: `GET /questions/categories`

**请求头**: `Authorization: Bearer {token}`

**响应数据**:

```json
{
  "success": true,
  "data": ["补益药", "清热药", "止血药", "活血药", "温里药"]
}
```

### 5. 获取题目列表

**接口**: `GET /questions/list`

**请求头**: `Authorization: Bearer {token}`

**查询参数**:

- `page`: 页码 (默认: 1)
- `per_page`: 每页数量 (默认: 10)
- `difficulty`: 难度 (可选)
- `category`: 分类 (可选)

**响应数据**:

```json
{
  "success": true,
  "data": {
    "questions": [...],
    "total": 100,
    "page": 1,
    "per_page": 10,
    "pages": 10
  }
}
```

## 用户接口

### 1. 获取用户资料

**接口**: `GET /user/profile`

**请求头**: `Authorization: Bearer {token}`

**响应数据**:

```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "testuser",
      "nickname": "测试用户"
    },
    "statistics": {
      "total_questions": 10,
      "correct_answers": 8,
      "accuracy_rate": 80.0,
      "continuous_days": 5
    }
  }
}
```

### 2. 更新用户资料

**接口**: `PUT /user/profile`

**请求头**: `Authorization: Bearer {token}`

**请求参数**:

```json
{
  "nickname": "新昵称",
  "avatar": "头像URL"
}
```

### 3. 获取统计信息

**接口**: `GET /user/statistics`

**请求头**: `Authorization: Bearer {token}`

**响应数据**:

```json
{
  "success": true,
  "data": {
    "total_questions": 10,
    "correct_answers": 8,
    "accuracy_rate": 80.0,
    "continuous_days": 5
  }
}
```

### 4. 获取答题历史

**接口**: `GET /user/history`

**请求头**: `Authorization: Bearer {token}`

**查询参数**:

- `page`: 页码 (默认: 1)
- `per_page`: 每页数量 (默认: 20)

**响应数据**:

```json
{
  "success": true,
  "data": {
    "records": [
      {
        "id": 1,
        "question_id": 1,
        "user_answer": "B",
        "is_correct": true,
        "answered_at": "2026-01-13T10:00:00",
        "question": {
          "question_text": "...",
          "correct_answer": "B",
          "explanation": "..."
        }
      }
    ],
    "total": 50,
    "page": 1,
    "per_page": 20
  }
}
```

### 5. 获取每周统计

**接口**: `GET /user/statistics/weekly`

**请求头**: `Authorization: Bearer {token}`

**响应数据**:

```json
{
  "success": true,
  "data": {
    "2026-01-13": {
      "total": 5,
      "correct": 4,
      "accuracy": 80.0
    },
    "2026-01-12": {
      "total": 3,
      "correct": 2,
      "accuracy": 66.67
    }
  }
}
```

## 错误码说明

- `200`: 成功
- `201`: 创建成功
- `400`: 请求参数错误
- `401`: 未授权/登录过期
- `404`: 资源不存在
- `500`: 服务器内部错误
