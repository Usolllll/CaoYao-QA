#!/bin/bash

echo "====================================="
echo "  草药问答系统 - 后端服务启动"
echo "====================================="
echo ""

# 检查是否在 backend 目录
if [ ! -f "requirements.txt" ]; then
    echo "错误: 请在 backend 目录下运行此脚本！"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "创建虚拟环境失败！"
        exit 1
    fi
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "检查并安装依赖..."
pip install -r requirements.txt -q

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "警告: 未找到 .env 文件！"
    echo "请先复制 .env.example 为 .env 并配置数据库信息"
    
    read -p "是否现在创建 .env 文件? (y/n) " response
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        cp .env.example .env
        echo ".env 文件已创建，请编辑该文件配置数据库"
        read -p "按回车键继续..."
    fi
fi

# 启动服务
echo ""
echo "启动后端服务..."
echo "服务地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务"
echo ""

python run.py
