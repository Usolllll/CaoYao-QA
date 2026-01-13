# 开发指南

## 项目结构详解

### 后端结构

```
backend/
├── app/
│   ├── __init__.py          # Flask 应用工厂
│   ├── models.py            # 数据模型
│   ├── utils.py             # 工具函数
│   └── routes/              # 路由模块
│       ├── auth.py          # 认证相关接口
│       ├── question.py      # 题目相关接口
│       └── user.py          # 用户相关接口
├── .env                     # 环境配置
├── .env.example             # 环境配置示例
├── requirements.txt         # Python 依赖
└── run.py                   # 启动文件
```

### 前端结构

```
frontend/
├── src/
│   ├── api/                 # API 接口封装
│   │   ├── request.js       # Axios 配置
│   │   ├── auth.js          # 认证接口
│   │   ├── question.js      # 题目接口
│   │   └── user.js          # 用户接口
│   ├── components/          # 公共组件
│   ├── router/              # 路由配置
│   │   └── index.js
│   ├── store/               # 状态管理
│   │   └── user.js          # 用户状态
│   ├── styles/              # 全局样式
│   │   └── main.css
│   ├── views/               # 页面组件
│   │   ├── Login.vue        # 登录页
│   │   ├── Register.vue     # 注册页
│   │   ├── Home.vue         # 首页
│   │   ├── Question.vue     # 答题页
│   │   ├── History.vue      # 历史记录页
│   │   └── Profile.vue      # 个人中心页
│   ├── App.vue              # 根组件
│   └── main.js              # 入口文件
├── index.html               # HTML 模板
├── package.json             # 项目配置
└── vite.config.js           # Vite 配置
```

## 本地开发流程

### 1. 克隆项目

```bash
git clone <repository-url>
cd CaoYao-QA
```

### 2. 数据库初始化

```bash
mysql -u root -p < database/init.sql
```

### 3. 后端开发

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制配置文件
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# 编辑 .env 文件，配置数据库

# 启动服务
python run.py
```

后端服务运行在: http://localhost:5000

### 4. 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用运行在: http://localhost:3000

## 添加新功能

### 1. 添加新的数据模型

在 `backend/app/models.py` 中定义模型:

```python
class NewModel(db.Model):
    __tablename__ = 'new_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
```

### 2. 添加新的 API 接口

创建新的路由文件 `backend/app/routes/new_route.py`:

```python
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.utils import success_response, error_response

new_bp = Blueprint('new', __name__)

@new_bp.route('/endpoint', methods=['GET'])
@jwt_required()
def new_endpoint():
    return success_response({'message': 'Hello'})
```

在 `backend/app/__init__.py` 中注册:

```python
from app.routes.new_route import new_bp
app.register_blueprint(new_bp, url_prefix='/api/new')
```

### 3. 添加前端页面

创建新的页面组件 `frontend/src/views/NewPage.vue`:

```vue
<template>
  <div class="page-container">
    <van-nav-bar title="新页面" />
    <div class="content">
      <!-- 页面内容 -->
    </div>
  </div>
</template>

<script setup>
// 页面逻辑
</script>
```

在路由中注册 `frontend/src/router/index.js`:

```javascript
{
  path: '/new-page',
  name: 'NewPage',
  component: () => import('@/views/NewPage.vue'),
  meta: { requiresAuth: true }
}
```

### 4. 添加 API 接口调用

在 `frontend/src/api/` 下创建或编辑文件:

```javascript
import request from "./request";

export function newApiCall(data) {
  return request({
    url: "/new/endpoint",
    method: "post",
    data,
  });
}
```

## 代码规范

### Python (后端)

- 使用 PEP 8 代码风格
- 函数名使用小写加下划线
- 类名使用大驼峰命名
- 添加必要的文档字符串

### JavaScript/Vue (前端)

- 使用 ES6+ 语法
- 组件名使用大驼峰命名
- 变量名使用小驼峰命名
- 使用 `const` 和 `let`，避免 `var`

## 测试

### 后端测试

```bash
cd backend
pip install pytest
pytest
```

### 前端测试

```bash
cd frontend
npm run test
```

## Git 工作流

1. 从 main 分支创建功能分支:

```bash
git checkout -b feature/new-feature
```

2. 提交代码:

```bash
git add .
git commit -m "feat: add new feature"
```

3. 推送到远程:

```bash
git push origin feature/new-feature
```

4. 创建 Pull Request

## 提交信息规范

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

## 常用命令

### 后端

```bash
# 安装新依赖
pip install package-name
pip freeze > requirements.txt

# 数据库迁移 (如果使用 Flask-Migrate)
flask db init
flask db migrate -m "message"
flask db upgrade
```

### 前端

```bash
# 安装新依赖
npm install package-name

# 构建生产版本
npm run build

# 代码检查
npm run lint
```

## 调试技巧

### 后端调试

使用 Python 调试器:

```python
import pdb; pdb.set_trace()
```

或使用 VS Code 调试配置。

### 前端调试

- 使用 Vue DevTools 浏览器插件
- Chrome DevTools
- `console.log()` 调试

## 性能优化

### 后端

1. 使用数据库查询优化
2. 添加缓存层
3. 使用异步任务处理耗时操作

### 前端

1. 使用虚拟滚动
2. 图片懒加载
3. 路由懒加载
4. 组件按需加载

## 资源链接

- [Flask 文档](https://flask.palletsprojects.com/)
- [Vue 3 文档](https://vuejs.org/)
- [Vant 4 文档](https://vant-ui.github.io/vant/)
- [Pinia 文档](https://pinia.vuejs.org/)
- [MySQL 文档](https://dev.mysql.com/doc/)
