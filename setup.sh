#!/bin/bash

# 确保脚本在出错时停止执行
set -e

echo "开始配置环境..."

# 1. 安装系统级依赖 (需要 sudo 权限)
echo "正在安装系统依赖 (build-essential)..."
sudo apt update
sudo apt install -y build-essential

# 2. 检查虚拟环境并激活
if [ ! -d "venv" ]; then
    echo "正在创建虚拟环境..."
    python3 -m venv venv
fi

echo "正在激活虚拟环境并安装 Python 依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. 安装 Playwright 浏览器及其系统依赖 (如果项目中使用了 Playwright)
if pip list | grep -q "playwright"; then
    echo "正在安装 Playwright 浏览器和系统依赖..."
    # 安装浏览器内核
    ./venv/bin/playwright install chromium
    # 安装 Linux 系统缺失的库 (可能需要 sudo)
    sudo ./venv/bin/playwright install-deps
fi

echo "环境配置完成！"
