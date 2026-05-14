#!/bin/bash
# 快速启动脚本

echo "🚀 快速启动 Telegram 运营助手"
echo "=============================="

# 检查依赖
if ! pip show python-telegram-bot > /dev/null 2>&1; then
    echo "📦 安装依赖..."
    pip install -r requirements.txt
fi

# 启动机器人
echo "🤖 启动机器人..."
echo ""
python3 main.py
