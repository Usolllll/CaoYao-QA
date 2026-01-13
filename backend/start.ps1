# 草药问答系统 - 后端启动脚本

Write-Host "=====================================" -ForegroundColor Green
Write-Host "  草药问答系统 - 后端服务启动" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

# 检查是否在 backend 目录
if (-not (Test-Path "requirements.txt")) {
    Write-Host "错误: 请在 backend 目录下运行此脚本！" -ForegroundColor Red
    exit 1
}

# 检查虚拟环境
if (-not (Test-Path "venv")) {
    Write-Host "创建虚拟环境..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "创建虚拟环境失败！" -ForegroundColor Red
        exit 1
    }
}

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# 安装依赖
Write-Host "检查并安装依赖..." -ForegroundColor Yellow
pip install -r requirements.txt -q

# 检查 .env 文件
if (-not (Test-Path ".env")) {
    Write-Host "警告: 未找到 .env 文件！" -ForegroundColor Red
    Write-Host "请先复制 .env.example 为 .env 并配置数据库信息" -ForegroundColor Yellow
    
    $response = Read-Host "是否现在创建 .env 文件? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Copy-Item ".env.example" ".env"
        Write-Host ".env 文件已创建，请编辑该文件配置数据库" -ForegroundColor Green
        Write-Host "按任意键继续..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}

# 启动服务
Write-Host ""
Write-Host "启动后端服务..." -ForegroundColor Green
Write-Host "服务地址: http://localhost:5000" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

python run.py
