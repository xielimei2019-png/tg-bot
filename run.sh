#!/bin/bash
# Telegram Bot 启动脚本

echo "🤖 Telegram 运营助手启动中..."

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "📌 Python 版本: $python_version"

# 检查依赖
echo "📦 检查依赖..."
if ! pip show python-telegram-bot > /dev/null 2>&1; then
    echo "⚠️  python-telegram-bot 未安装，正在安装..."
    pip install -r requirements.txt
fi

# 创建日志文件
touch bot.log

# 启动机器人
echo "🚀 启动机器人..."
python3 main.py
