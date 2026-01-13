# 部署文档

## 环境要求

### 后端环境

- Python 3.9+
- MySQL 8.0+
- pip

### 前端环境

- Node.js 16+
- npm 或 yarn

## 数据库部署

### 1. 安装 MySQL

Windows:

- 下载并安装 MySQL Community Server
- 配置 root 密码

Linux:

```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### 2. 初始化数据库

```bash
# 登录 MySQL
mysql -u root -p

# 执行初始化脚本
source database/init.sql

# 或者使用命令
mysql -u root -p < database/init.sql
```

## 后端部署

### 1. 创建虚拟环境

Windows (PowerShell):

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux/Mac:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env`:

Windows:

```powershell
copy .env.example .env
```

Linux/Mac:

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入实际配置:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=caoyao_qa

SECRET_KEY=your_random_secret_key_here
JWT_SECRET_KEY=your_random_jwt_secret_here

FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
```

**注意**: 生产环境请使用强随机密钥！

生成随机密钥:

```python
import secrets
print(secrets.token_hex(32))
```

### 4. 启动后端服务

开发环境:

```bash
python run.py
```

生产环境 (使用 Gunicorn):

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 前端部署

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 开发环境运行

```bash
npm run dev
```

访问: http://localhost:3000

### 3. 生产环境构建

```bash
npm run build
```

构建产物在 `dist` 目录。

### 4. 部署静态文件

#### 方式一: 使用 Nginx

安装 Nginx 后，配置文件:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

#### 方式二: 使用 Apache

配置 VirtualHost:

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /path/to/frontend/dist

    <Directory /path/to/frontend/dist>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted

        # 支持 HTML5 History 模式
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>

    # API 代理
    ProxyPass /api http://localhost:5000/api
    ProxyPassReverse /api http://localhost:5000/api
</VirtualHost>
```

## 使用 Docker 部署 (可选)

### 1. 创建 Dockerfile

**后端 Dockerfile** (`backend/Dockerfile`):

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

**前端 Dockerfile** (`frontend/Dockerfile`):

```dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

### 2. Docker Compose

创建 `docker-compose.yml`:

```yaml
version: "3.8"

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: caoyao_qa
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"

  backend:
    build: ./backend
    environment:
      DB_HOST: mysql
      DB_PORT: 3306
      DB_USER: root
      DB_PASSWORD: rootpassword
      DB_NAME: caoyao_qa
    ports:
      - "5000:5000"
    depends_on:
      - mysql

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  mysql_data:
```

启动:

```bash
docker-compose up -d
```

## 常见问题

### 1. 数据库连接失败

- 检查 MySQL 服务是否启动
- 检查 `.env` 中的数据库配置是否正确
- 检查数据库用户权限

### 2. CORS 跨域问题

确保后端已安装并配置 `Flask-CORS`。

### 3. 前端无法访问后端 API

- 检查后端服务是否正常运行
- 检查防火墙设置
- 检查 Nginx/Apache 代理配置

### 4. JWT Token 过期

在 `.env` 中调整 `JWT_ACCESS_TOKEN_EXPIRES` 值（单位：秒）。

## 性能优化建议

1. **数据库**:

   - 添加适当的索引
   - 定期备份数据
   - 使用连接池

2. **后端**:

   - 使用 Redis 缓存热点数据
   - 启用 Gzip 压缩
   - 使用 CDN 加速静态资源

3. **前端**:
   - 开启生产模式构建
   - 使用代码分割
   - 图片懒加载

## 安全建议

1. 使用 HTTPS
2. 定期更新依赖
3. 设置强密码策略
4. 限制 API 请求频率
5. 定期备份数据库
6. 使用环境变量管理敏感信息

## 监控与日志

建议使用:

- 日志: Python logging 模块
- 监控: Prometheus + Grafana
- 错误追踪: Sentry
