# 草药问答系统 (CaoYao-QA)

一个基于移动端的草药知识问答系统，帮助用户学习和测试中草药相关知识。

## 📱 项目特点

- **移动端优先设计**: 专为手机用户设计的界面和交互
- **用户认证系统**: 支持注册、登录、登出功能
- **随机题目抽取**: 智能随机抽取题目，支持按难度和分类筛选
- **答题统计**: 实时统计答题正确率、连续学习天数等
- **答题历史**: 查看历史答题记录和解析
- **底部导航栏**: 便捷的移动端导航体验

## 🛠 技术栈

### 前端

- **Vue 3**: 渐进式 JavaScript 框架
- **Vue Router**: 官方路由管理器
- **Pinia**: 新一代状态管理
- **Vant 4**: 轻量、可靠的移动端 Vue 组件库
- **Axios**: HTTP 客户端
- **Vite**: 下一代前端构建工具

### 后端

- **Python 3.9+**: 编程语言
- **Flask**: 轻量级 Web 框架
- **Flask-SQLAlchemy**: ORM 框架
- **Flask-JWT-Extended**: JWT 认证
- **Flask-CORS**: 跨域支持
- **PyMySQL**: MySQL 数据库驱动

### 数据库

- **MySQL 8.0+**: 关系型数据库

## 📁 项目结构

```
CaoYao-QA/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── api/             # API 接口封装
│   │   ├── components/      # 公共组件
│   │   ├── views/           # 页面组件
│   │   ├── router/          # 路由配置
│   │   ├── store/           # 状态管理
│   │   ├── styles/          # 全局样式
│   │   ├── App.vue          # 根组件
│   │   └── main.js          # 入口文件
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/                  # 后端项目
│   ├── app/
│   │   ├── __init__.py      # 应用工厂
│   │   ├── models.py        # 数据模型
│   │   ├── utils.py         # 工具函数
│   │   └── routes/          # 路由模块
│   │       ├── auth.py      # 认证接口
│   │       ├── question.py  # 题目接口
│   │       └── user.py      # 用户接口
│   ├── .env.example         # 环境配置示例
│   ├── requirements.txt     # Python 依赖
│   └── run.py              # 启动文件
├── database/
│   └── init.sql            # 数据库初始化脚本
└── docs/                   # 项目文档
    ├── API.md              # API 接口文档
    ├── DEPLOY.md           # 部署文档
    └── DEV.md              # 开发指南
```

## ✨ 功能特性

- ✅ **用户系统**
  - 用户注册与登录
  - JWT Token 认证
  - 用户资料管理
- ✅ **答题系统**
  - 随机题目抽取
  - 按难度筛选（简单/中等/困难）
  - 按分类筛选
  - 即时答案反馈
  - 详细题目解析
- ✅ **统计系统**
  - 累计答题数
  - 答题正确率
  - 连续学习天数
  - 每周答题统计
- ✅ **历史记录**
  - 答题历史查看
  - 答案与解析回顾
  - 分页加载
- ✅ **移动端优化**
  - 响应式设计
  - 触摸友好
  - 底部导航栏
  - 下拉刷新

## 🚀 快速开始

### 前置要求

- Python 3.9+
- Node.js 16+
- MySQL 8.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd CaoYao-QA
```

### 2. 数据库初始化

```bash
# 登录 MySQL
mysql -u root -p

# 执行初始化脚本
source database/init.sql

# 或使用命令
mysql -u root -p < database/init.sql
```

数据库将自动创建：

- 用户表
- 题目表（包含 10 道示例题目）
- 答题记录表
- 用户统计表

### 3. 后端启动

#### Windows (PowerShell)

```powershell
cd backend

# 创建虚拟环境
python -m venv venv
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt

# 复制并配置环境变量
copy .env.example .env
# 编辑 .env 文件，填入数据库配置

# 启动服务
python run.py
```

#### Linux/Mac

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制并配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入数据库配置

# 启动服务
python run.py
```

后端服务将运行在: **http://localhost:5000**

### 4. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将运行在: **http://localhost:3000**

## ⚙️ 环境配置

编辑 `backend/.env` 文件：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=caoyao_qa

# 应用密钥（生产环境请使用强随机密钥）
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key

# 服务器配置
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# JWT 配置
JWT_ACCESS_TOKEN_EXPIRES=3600
```

## 📱 页面展示

### 主要页面

1. **登录/注册页**: 用户认证入口
2. **首页**: 显示统计信息，选择答题方式
3. **答题页**: 答题界面，实时反馈
4. **历史记录**: 查看答题历史和解析
5. **个人中心**: 用户信息和统计数据

### 底部导航

- 🏠 首页
- 📝 历史
- 👤 我的

## 📚 文档

- [API 接口文档](docs/API.md) - 详细的 API 接口说明
- [部署文档](docs/DEPLOY.md) - 生产环境部署指南
- [开发指南](docs/DEV.md) - 开发流程和规范

## 🔐 默认账号

数据库初始化后会创建一个测试账号（密码已加密）：

- 用户名: `testuser`
- 密码: `test123`

**注意**: 生产环境请删除测试账号！

## 🎯 示例题目

系统预置了 10 道草药相关题目，涵盖：

- 补益药（人参、黄芪、枸杞等）
- 清热药（金银花、板蓝根等）
- 止血药（三七等）
- 活血药（当归、红花等）

## 🛡️ 安全建议

1. ⚠️ 生产环境务必修改 `.env` 中的密钥
2. 🔒 使用 HTTPS 协议
3. 🚫 删除或修改测试账号密码
4. 🔑 设置强密码策略
5. 📊 定期备份数据库

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👥 联系方式

如有问题或建议，欢迎联系项目维护者。

---

**项目创建时间**: 2026-01-13  
**最后更新**: 2026-01-13
