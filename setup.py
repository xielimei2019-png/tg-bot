#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器人初始化设置脚本
帮助用户配置机器人的基本设置
"""

import os
import json

def get_valid_token():
    """获取并验证 Bot Token"""
    while True:
        token = input("🤖 请输入你的 Telegram Bot Token: ").strip()
        if not token:
            print("❌ Token 不能为空")
            continue
        if len(token) < 20:
            print("❌ Token 格式不正确")
            continue
        return token

def get_admin_ids():
    """获取管理员 ID"""
    admin_input = input("\n👤 请输入管理员 Telegram User ID（留空跳过）: ").strip()
    if not admin_input:
        return []
    
    try:
        # 支持多个 ID，用逗号分隔
        admin_ids = [int(uid.strip()) for uid in admin_input.split(',')]
        return admin_ids
    except ValueError:
        print("⚠️  ID 格式错误，已跳过")
        return []

def get_bot_name():
    """获取机器人名称"""
    name = input("\n📛 请输入机器人名称（留空使用默认）: ").strip()
    return name if name else "TG运营助手"

def update_config(token, admin_ids, bot_name):
    """更新配置文件"""
    config_path = "config.py"
    
    # 读取现有配置
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换配置项
    content = content.replace(
        f'BOT_TOKEN = "8539940556:AAHxCyOyB6l-7a_lQegPA5n2aa1OQL5yBbs"',
        f'BOT_TOKEN = "{token}"'
    )
    
    # 处理管理员 ID
    if admin_ids:
        admin_ids_str = str(admin_ids)
        content = content.replace(
            'ADMIN_IDS = []',
            f'ADMIN_IDS = {admin_ids_str}'
        )
    
    content = content.replace(
        'BOT_NAME = "TG运营助手"',
        f'BOT_NAME = "{bot_name}"'
    )
    
    # 写回配置
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ 配置已更新！")

def create_env_file(token):
    """创建 .env 文件"""
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(f"# Telegram Bot Token\n")
        f.write(f"BOT_TOKEN={token}\n")
        f.write(f"\n# 管理员用户ID（可选）\n")
        f.write(f"ADMIN_IDS=\n")
    print("✅ .env 文件已创建！")

def print_next_steps():
    """显示下一步操作"""
    print("\n" + "="*60)
    print("🎉 初始化完成！")
    print("="*60)
    print("\n📌 下一步操作：")
    print("\n1️⃣  安装依赖：")
    print("   pip install -r requirements.txt")
    print("\n2️⃣  运行机器人：")
    print("   python main.py")
    print("\n3️⃣  启动机器人后：")
    print("   • 打开 Telegram")
    print("   • 搜索你的机器人")
    print("   • 发送 /start 开始使用")
    print("\n4️⃣  获取你的 User ID：")
    print("   • 在 Telegram 搜索 @userinfobot")
    print("   • 发送任意消息获取你的 ID")
    print("   • 将 ID 添加到 config.py 的 ADMIN_IDS")
    print("\n💡 提示：")
    print("   • 将机器人添加到群组后即可自动响应")
    print("   • 查看 README.md 了解所有功能")
    print("\n" + "="*60)

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🤖 Telegram 运营助手 - 初始化设置")
    print("="*60)
    
    # 检查 config.py 是否存在
    if not os.path.exists('config.py'):
        print("❌ config.py 文件不存在，请确保在正确的目录下运行")
        return
    
    print("\n👋 欢迎使用 Telegram 运营助手！")
    print("让我们进行一些基本配置...\n")
    
    # 获取配置
    token = get_valid_token()
    admin_ids = get_admin_ids()
    bot_name = get_bot_name()
    
    # 更新配置
    update_config(token, admin_ids, bot_name)
    create_env_file(token)
    
    # 显示下一步
    print_next_steps()

if __name__ == "__main__":
    main()
