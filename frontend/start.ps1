# 草药问答系统 - 前端启动脚本

Write-Host "=====================================" -ForegroundColor Green
Write-Host "  草药问答系统 - 前端应用启动" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

# 检查是否在 frontend 目录
if (-not (Test-Path "package.json")) {
    Write-Host "错误: 请在 frontend 目录下运行此脚本！" -ForegroundColor Red
    exit 1
}

# 检查 node_modules
if (-not (Test-Path "node_modules")) {
    Write-Host "安装依赖..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "依赖安装失败！" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "依赖已安装" -ForegroundColor Green
}

# 启动开发服务器
Write-Host ""
Write-Host "启动前端开发服务器..." -ForegroundColor Green
Write-Host "应用地址: http://localhost:3000" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

npm run dev
