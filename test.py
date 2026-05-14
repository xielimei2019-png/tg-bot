#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot 测试脚本
测试机器人的各项功能
"""

import asyncio
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 使用配置的 TOKEN
import config

async def test_bot_info():
    """测试：获取机器人信息"""
    print("\n📡 测试：获取机器人信息...")
    bot = Bot(token=config.BOT_TOKEN)
    bot_info = await bot.get_me()
    print(f"✅ 机器人名称: {bot_info.first_name}")
    print(f"✅ 用户名: @{bot_info.username}")
    print(f"✅ Bot ID: {bot_info.id}")

async def test_send_message():
    """测试：发送消息（需要 chat_id）"""
    print("\n📤 测试：发送测试消息...")
    chat_id = input("请输入你的 Chat ID（留空跳过）: ").strip()
    
    if not chat_id:
        print("⏭️  跳过发送消息测试")
        return
    
    try:
        bot = Bot(token=config.BOT_TOKEN)
        await bot.send_message(
            chat_id=int(chat_id),
            text=f"🧪 *测试消息*\n\n你好！这是一条来自 {config.BOT_NAME} 的测试消息！\n\n机器人运行正常！✅"
        )
        print("✅ 消息发送成功！")
    except Exception as e:
        print(f"❌ 消息发送失败: {e}")

async def test_webhook():
    """测试：检查 Webhook 配置"""
    print("\n🔗 测试：检查 Webhook 配置...")
    bot = Bot(token=config.BOT_TOKEN)
    webhook_info = await bot.get_webhook_info()
    print(f"Webhook URL: {webhook_info.url or '未设置'}")
    print(f"待处理更新: {webhook_info.pending_update_count}")

async def test_commands():
    """测试：列出可用命令"""
    print("\n📋 测试：检查命令列表...")
    commands = await Bot(token=config.BOT_TOKEN).get_my_commands()
    if commands:
        print("已注册的命令：")
        for cmd in commands:
            print(f"  • /{cmd.command} - {cmd.description}")
    else:
        print("⚠️  未注册任何命令（可通过 BotFather 设置）")

async def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("🧪 Telegram 运营助手 - 功能测试")
    print("="*60)
    
    try:
        await test_bot_info()
        await test_commands()
        await test_webhook()
        await test_send_message()
        
        print("\n" + "="*60)
        print("✅ 所有测试完成！")
        print("="*60)
        print("\n📌 后续步骤：")
        print("1. 在 Telegram 中搜索你的机器人")
        print("2. 发送 /start 开始使用")
        print("3. 尝试发送 /help 查看帮助")
        print("4. 添加机器人到群组测试群功能")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n请检查：")
        print("1. BOT_TOKEN 是否正确")
        print("2. 网络连接是否正常")
        print("3. 机器人是否已激活")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
