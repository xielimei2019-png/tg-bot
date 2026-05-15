#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot Assistant - 主程序
一个功能完整的 Telegram 运营助手机器人
"""

import logging
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional

# 导入 python-telegram-bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# 导入配置
import config

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL),
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============ 全局状态 ============
class BotState:
    """机器人状态管理"""
    def __init__(self):
        self.start_time = datetime.now()
        self.total_messages = 0
        self.total_commands = 0
        self.registered_chats: Dict[int, dict] = {}
        self.keyword_responses: Dict[str, str] = config.KEYWORD_RESPONSES.copy()
        self.admin_ids: List[int] = config.ADMIN_IDS
        # 资讯收集关键词
        self.info_keywords = config.INFO_KEYWORDS
        # 用户ID（接收资讯的人）
        self.info_receiver_id = config.INFO_RECEIVER_ID

# 创建全局状态实例
bot_state = BotState()

# ============ 工具函数 ============
def format_uptime(start_time: datetime) -> str:
    """格式化运行时间"""
    delta = datetime.now() - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}小时{minutes}分钟"
    return f"{minutes}分钟{seconds}秒"

# ============ 命令处理器 ============
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    bot_state.total_commands += 1
    bot_state.total_messages += 1
    
    # 注册当前chat
    chat = update.effective_chat
    bot_state.registered_chats[chat.id] = {
        "title": chat.title,
        "username": chat.username,
        "type": chat.type,
        "registered_at": datetime.now().isoformat()
    }
    
    welcome = config.WELCOME_MESSAGE.format(bot_name=config.BOT_NAME)
    await update.message.reply_text(welcome, parse_mode="Markdown")
    logger.info(f"新用户启动: {chat.id} ({chat.title or chat.username})")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /help 命令"""
    bot_state.total_commands += 1
    bot_state.total_messages += 1
    
    help_text = config.HELP_MESSAGE.format(bot_name=config.BOT_NAME)
    await update.message.reply_text(help_text, parse_mode="Markdown")
    logger.info(f"帮助信息已发送至: {update.effective_chat.id}")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /status 命令"""
    bot_state.total_commands += 1
    bot_state.total_messages += 1
    
    uptime = format_uptime(bot_state.start_time)
    status_text = f"""
🤖 <b>{config.BOT_NAME} 状态报告</b>

⏱️ 运行时间：{uptime}
📊 总命令数：{bot_state.total_commands}
💬 总消息数：{bot_state.total_messages}
💬 注册群组：{len(bot_state.registered_chats)}

✅ 状态：运行正常
🕐 服务器时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    await update.message.reply_text(status_text, parse_mode='HTML')
    logger.info(f"状态查询: {update.effective_chat.id}")

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /ping 命令"""
    bot_state.total_commands += 1
    bot_state.total_messages += 1
    await update.message.reply_text("🏓 <b>PONG!</b> 机器人在线！", parse_mode='HTML')

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /broadcast 命令"""
    bot_state.total_commands += 1
    user_id = update.effective_user.id
    
    # 检查是否为管理员
    if bot_state.admin_ids and user_id not in bot_state.admin_ids:
        await update.message.reply_text("⛔ 此命令仅限管理员使用")
        return
    
    if not context.args:
        await update.message.reply_text("📢 请输入广播内容：\n/broadcast [消息内容]")
        return
    
    message = ' '.join(context.args)
    await update.message.reply_text("📢 开始广播...")
    
    success = 0
    failed = 0
    
    for chat_id in bot_state.registered_chats:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"📢 <b>广播消息</b>\n\n{message}",
                parse_mode='HTML'
            )
            success += 1
        except Exception as e:
            logger.error(f"广播失败 {chat_id}: {e}")
            failed += 1
    
    await update.message.reply_text(
        f"✅ <b>广播完成</b>\n\n"
        f"📨 成功：{success} 个\n"
        f"❌ 失败：{failed} 个",
        parse_mode='HTML'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /stats 命令"""
    bot_state.total_commands += 1
    bot_state.total_messages += 1
    
    uptime = format_uptime(bot_state.start_time)
    stats_text = f"""
📈 <b>详细统计</b>

⏱️ 运行时长：{uptime}
📊 命令次数：{bot_state.total_commands}
💬 消息次数：{bot_state.total_messages}
💬 注册群组：{len(bot_state.registered_chats)}

<b>群组列表：</b>
"""
    for chat_id, info in bot_state.registered_chats.items():
        title = info.get('title') or info.get('username') or str(chat_id)
        stats_text += f"• {title}\n"
    
    await update.message.reply_text(stats_text, parse_mode='HTML')

async def list_chats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /chats 命令"""
    bot_state.total_commands += 1
    bot_state.total_messages += 1
    
    if not bot_state.registered_chats:
        await update.message.reply_text("📝 当前没有注册的群组")
        return
    
    chats_text = "💬 <b>已注册群组</b>\n\n"
    for i, (chat_id, info) in enumerate(bot_state.registered_chats.items(), 1):
        title = info.get('title') or info.get('username') or '未知'
        chats_text += f"{i}. {title}\n   ID: `{chat_id}`\n"
    
    await update.message.reply_text(chats_text, parse_mode='HTML')

# ============ 消息处理器 ============
async def keyword_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理关键词和资讯收集"""
    bot_state.total_messages += 1
    text = update.message.text.lower()
    original_text = update.message.text
    
    # 注册新chat
    chat = update.effective_chat
    if chat.id not in bot_state.registered_chats:
        bot_state.registered_chats[chat.id] = {
            "title": chat.title,
            "username": chat.username,
            "type": chat.type,
            "registered_at": datetime.now().isoformat()
        }
        logger.info(f"新chat注册: {chat.id}")
    
    # 检查资讯关键词 - 转发给用户
    if bot_state.info_receiver_id:
        for keyword in bot_state.info_keywords:
            if keyword.lower() in text:
                try:
                    info_msg = f"""📢 【资讯收集】

🏷️ 来源群组: {chat.title or chat.username or '未知'}
🔑 触发关键词: {keyword}

📝 内容:
{original_text}

⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
                    await context.bot.send_message(
                        chat_id=bot_state.info_receiver_id,
                        text=info_msg
                    )
                    logger.info(f"资讯已转发: '{keyword}' from {chat.id}")
                except Exception as e:
                    logger.error(f"转发资讯失败: {e}")
                break
    
    # 检查关键词回复
    for keyword, response in bot_state.keyword_responses.items():
        if keyword in text:
            await update.message.reply_text(response)
            logger.info(f"关键词触发: '{keyword}' by {update.effective_user.id}")
            return

async def new_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理新成员加入群组"""
    bot_state.total_messages += 1
    chat = update.effective_chat
    
    # 自动注册群组
    if chat.id not in bot_state.registered_chats:
        bot_state.registered_chats[chat.id] = {
            "title": chat.title,
            "username": chat.username,
            "type": chat.type,
            "registered_at": datetime.now().isoformat()
        }
        logger.info(f"新群组注册: {chat.id}")
    
    # 欢迎新成员
    for new_member in update.message.new_chat_members:
        if new_member.is_bot:
            continue
        welcome = config.WELCOME_MESSAGE.format(bot_name=config.BOT_NAME)
        try:
            await update.message.reply_text(welcome, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"欢迎消息失败: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """错误处理"""
    logger.error(f"Error: {context.error}")

# ============ 主函数 ============
def main() -> None:
    """主函数 - 启动机器人"""
    logger.info(f"🤖 {config.BOT_NAME} 启动中...")
    
    # 创建应用
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # 添加命令处理器
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("chats", list_chats_command))
    
    # 添加消息处理器
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        keyword_handler
    ))
    
    # 处理新成员加入
    application.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        new_member_handler
    ))
    
    # 添加错误处理器
    application.add_error_handler(error_handler)
    
    # 启动机器人
    logger.info(f"✅ {config.BOT_NAME} 已启动！")
    print(f"""
╔═══════════════════════════════════════════════════╗
║     🤖 {config.BOT_NAME} 已成功启动！                  ║
╠═══════════════════════════════════════════════════╣
║  状态: 🟢 运行中                                   ║
║  资讯接收ID: {config.INFO_RECEIVER_ID or '未设置'}     ║
╠═══════════════════════════════════════════════════╣
║  发送 /start 到机器人开始使用                       ║
║  发送 /help 查看所有可用指令                        ║
╚═══════════════════════════════════════════════════╝
    """)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
