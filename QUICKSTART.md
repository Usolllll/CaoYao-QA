# 快速开始指南

## Windows 用户

### 方式一: 使用启动脚本（推荐）

#### 1. 启动后端

```powershell
cd backend
.\start.ps1
```

#### 2. 启动前端（新开一个终端）

```powershell
cd frontend
.\start.ps1
```

### 方式二: 手动启动

#### 后端

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# 编辑 .env 文件
python run.py
```

#### 前端

```powershell
cd frontend
npm install
npm run dev
```

---

## Linux/Mac 用户

### 方式一: 使用启动脚本（推荐）

#### 1. 添加执行权限

```bash
chmod +x backend/start.sh
chmod +x frontend/start.sh
```

#### 2. 启动后端

```bash
cd backend
./start.sh
```

#### 3. 启动前端（新开一个终端）

```bash
cd frontend
./start.sh
```

### 方式二: 手动启动

#### 后端

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件
python run.py
```

#### 前端

```bash
cd frontend
npm install
npm run dev
```

---

## 数据库初始化

在启动后端之前，请先初始化数据库：

```bash
mysql -u root -p < database/init.sql
```

---

## 访问地址

- 前端应用: http://localhost:3000
- 后端 API: http://localhost:5000

---

## 默认测试账号

- 用户名: `testuser`
- 密码: `test123`

---

## 遇到问题？

1. 确保 MySQL 服务已启动
2. 确保已正确配置 `.env` 文件
3. 确保 Python 和 Node.js 版本符合要求
4. 查看完整文档: [README.md](../README.md)
