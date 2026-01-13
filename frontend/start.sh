#!/bin/bash

echo "====================================="
echo "  草药问答系统 - 前端应用启动"
echo "====================================="
echo ""

# 检查是否在 frontend 目录
if [ ! -f "package.json" ]; then
    echo "错误: 请在 frontend 目录下运行此脚本！"
    exit 1
fi

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "安装依赖..."
    npm install
    if [ $? -ne 0 ]; then
        echo "依赖安装失败！"
        exit 1
    fi
else
    echo "依赖已安装"
fi

# 启动开发服务器
echo ""
echo "启动前端开发服务器..."
echo "应用地址: http://localhost:3000"
echo "按 Ctrl+C 停止服务"
echo ""

npm run dev
