#!/bin/bash
# 一键部署脚本 - 适用于 Ubuntu/Debian 服务器

set -e

echo "🚀 Telegram 运营助手一键部署脚本"
echo "================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ 请使用 sudo 运行此脚本${NC}"
    exit 1
fi

# 获取当前用户
CURRENT_USER=$(whoami)

echo -e "${YELLOW}📌 检测到用户: $CURRENT_USER${NC}"

# 更新系统
echo -e "${YELLOW}🔄 更新系统包...${NC}"
apt update && apt upgrade -y

# 安装 Python
echo -e "${YELLOW}🔄 安装 Python...${NC}"
apt install -y python3 python3-pip python3-venv

# 创建应用目录
echo -e "${YELLOW}🔄 创建应用目录...${NC}"
APP_DIR="/opt/telegram-bot-assistant"
mkdir -p $APP_DIR

# 复制应用文件
echo -e "${YELLOW}🔄 复制应用文件...${NC}"
# 注意：需要先将项目文件复制到服务器
cp -r . $APP_DIR/

# 创建虚拟环境
echo -e "${YELLOW}🔄 创建虚拟环境...${NC}"
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo -e "${YELLOW}🔄 安装 Python 依赖...${NC}"
pip install -r requirements.txt

# 设置权限
chown -R $CURRENT_USER:$CURRENT_USER $APP_DIR

# 创建 systemd 服务
echo -e "${YELLOW}🔄 创建 systemd 服务...${NC}"
cat > /etc/systemd/system/tg-assistant-bot.service <<EOF
[Unit]
Description=Telegram Assistant Bot
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=append:$APP_DIR/bot.log
StandardError=append:$APP_DIR/bot.log

[Install]
WantedBy=multi-user.target
EOF

# 重新加载 systemd
echo -e "${YELLOW}🔄 重新加载 systemd...${NC}"
systemctl daemon-reload

# 启用并启动服务
echo -e "${YELLOW}🔄 启动机器人服务...${NC}"
systemctl enable tg-assistant-bot
systemctl start tg-assistant-bot

# 检查服务状态
sleep 2
if systemctl is-active --quiet tg-assistant-bot; then
    echo -e "${GREEN}✅ 机器人已成功启动！${NC}"
else
    echo -e "${RED}❌ 机器人启动失败，请检查日志${NC}"
    systemctl status tg-assistant-bot
fi

echo ""
echo "================================"
echo -e "${GREEN}🎉 部署完成！${NC}"
echo ""
echo "📌 使用命令："
echo "   • 查看状态: systemctl status tg-assistant-bot"
echo "   • 查看日志: tail -f $APP_DIR/bot.log"
echo "   • 重启服务: systemctl restart tg-assistant-bot"
echo "   • 停止服务: systemctl stop tg-assistant-bot"
echo ""
echo -e "${YELLOW}⚠️  请记得配置 config.py 中的 BOT_TOKEN 和 ADMIN_IDS${NC}"
echo ""
