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
from telegram.request import requestbase
import httpx

# 自定义请求类：通过Cloudflare Workers代理访问Telegram API
class ProxyRequest(httpx.Request, httpx.Response):

    def __init__(self, proxy_url: str):
        self._proxy_url = proxy_url
        self._client = httpx.Client(timeout=30)

    def fetch(self, method: str, url: str, **kwargs) -> httpx.Response:
        # 将请求转发到代理
        proxied_url = f"{self._proxy_url}{url}"
        return self._client.request(method, proxied_url, **kwargs)

import config

# 创建自定义请求对象（用于通过代理访问Telegram API）
request = ProxyRequest(config.PROXY_URL)

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
        self.news_cache: List[dict] = []
        self.last_news_update: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        uptime = datetime.now() - self.start_time
        return {
            "运行状态": "🟢 运行中",
            "运行时间": str(uptime).split('.')[0],
            "启动时间": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "总消息数": self.total_messages,
            "总命令数": self.total_commands,
            "注册群组/对话数": len(self.registered_chats),
        }

# 全局状态实例
bot_state = BotState()

# ============ 工具函数 ============
def is_admin(user_id: int) -> bool:
    """检查用户是否为管理员"""
    if not bot_state.admin_ids:
        # 如果没有设置管理员ID，所有人都可以使用管理员命令
        return True
    return user_id in bot_state.admin_ids

async def send_long_message(update: Update, text: str, parse_mode: str = "Markdown"):
    """发送长消息，自动分段"""
    max_length = 4096
    if len(text) <= max_length:
        await update.message.reply_text(text, parse_mode=parse_mode)
    else:
        # 分段发送
        parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        for part in parts:
            await update.message.reply_text(part, parse_mode=parse_mode)

def get_chat_info_text(chat) -> str:
    """获取群组/对话信息"""
    info = []
    info.append(f"**类型**: {chat.type}")
    info.append(f"**标题**: {chat.title or 'N/A'}")
    info.append(f"**用户名**: @{chat.username or 'N/A'}")
    info.append(f"**Chat ID**: `{chat.id}`")
    if hasattr(chat, 'description'):
        info.append(f"**描述**: {chat.description or 'N/A'}")
    return "\n".join(info)

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
    
    status_info = bot_state.to_dict()
    status_text = f"📊 *{config.BOT_NAME} 运行状态*\n\n"
    for key, value in status_info.items():
        status_text += f"{key}: {value}\n"
    
    await update.message.reply_text(status_text, parse_mode="Markdown")
    logger.info(f"状态查询: {update.effective_chat.id}")

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /ping 命令"""
    bot_state.total_commands += 1
    bot_state.total_messages += 1
    
    await update.message.reply_text("🏓 *Pong!* 机器人在线！")
    logger.info(f"Ping响应: {update.effective_chat.id}")

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /admin 命令"""
    bot_state.total_commands += 1
    
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ 此命令仅限管理员使用")
        return
    
    await update.message.reply_text(config.ADMIN_HELP_MESSAGE, parse_mode="Markdown")
    logger.info(f"管理员帮助已发送至: {update.effective_user.id}")

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /broadcast 命令 - 群发消息"""
    bot_state.total_commands += 1
    
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ 此命令仅限管理员使用")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📢 *群发消息*\n\n"
            "用法: `/broadcast [消息内容]`\n\n"
            "将向所有已注册的群组/对话发送消息"
        )
        return
    
    message = ' '.join(context.args)
    sent_count = 0
    failed_count = 0
    
    status_msg = await update.message.reply_text("📤 正在群发消息...")
    
    for chat_id in bot_state.registered_chats:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"📢 *广播消息*\n\n{message}",
                parse_mode="Markdown"
            )
            sent_count += 1
            await asyncio.sleep(0.1)  # 避免触发限流
        except Exception as e:
            logger.error(f"发送消息到 {chat_id} 失败: {e}")
            failed_count += 1
    
    result_text = (
        f"✅ *群发完成*\n\n"
        f"成功发送: {sent_count}\n"
        f"发送失败: {failed_count}\n"
        f"总计注册: {len(bot_state.registered_chats)}"
    )
    await status_msg.edit_text(result_text, parse_mode="Markdown")
    logger.info(f"群发消息完成: 成功{sent_count}, 失败{failed_count}")

async def setkeyword_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /setkeyword 命令"""
    bot_state.total_commands += 1
    
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ 此命令仅限管理员使用")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "🔑 *设置关键词*\n\n"
            "用法: `/setkeyword [关键词] [回复内容]`\n\n"
            "示例: `/setkeyword 你好 您好！有什么可以帮助您的？`"
        )
        return
    
    keyword = context.args[0].lower()
    response = ' '.join(context.args[1:])
    bot_state.keyword_responses[keyword] = response
    
    await update.message.reply_text(
        f"✅ *关键词已设置*\n\n"
        f"关键词: `{keyword}`\n"
        f"回复: {response}",
        parse_mode="Markdown"
    )
    logger.info(f"新增关键词: {keyword}")

async def delkeyword_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /delkeyword 命令"""
    bot_state.total_commands += 1
    
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ 此命令仅限管理员使用")
        return
    
    if not context.args:
        await update.message.reply_text("用法: `/delkeyword [关键词]`")
        return
    
    keyword = context.args[0].lower()
    
    if keyword in bot_state.keyword_responses:
        del bot_state.keyword_responses[keyword]
        await update.message.reply_text(f"✅ 关键词 `{keyword}` 已删除", parse_mode="Markdown")
        logger.info(f"删除关键词: {keyword}")
    else:
        await update.message.reply_text(f"❌ 关键词 `{keyword}` 不存在", parse_mode="Markdown")

async def listkeywords_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /listkeywords 命令"""
    bot_state.total_commands += 1
    
    if not bot_state.keyword_responses:
        await update.message.reply_text("📝 当前没有设置任何关键词")
        return
    
    text = "📝 *关键词列表*\n\n"
    for keyword, response in bot_state.keyword_responses.items():
        text += f"• `{keyword}` → {response[:50]}{'...' if len(response) > 50 else ''}\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /news 命令 - 获取云控/TG行业资讯"""
    bot_state.total_commands += 1
    bot_state.total_messages += 1
    
    keyboard = [
        [
            InlineKeyboardButton("📰 最新资讯", callback_data="news_latest"),
            InlineKeyboardButton("📱 云控工具", callback_data="news_tools"),
        ],
        [
            InlineKeyboardButton("💡 使用技巧", callback_data="news_tips"),
            InlineKeyboardButton("🔄 刷新", callback_data="news_refresh"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    news_intro = """
🔍 *TG云控/WS云控 资讯中心*

👋 欢迎使用资讯功能！

请选择你感兴趣的类别：
• 📰 **最新资讯** - 行业最新动态
• 📱 **云控工具** - 推荐工具和软件
• 💡 **使用技巧** - 实用技巧和教程

点击按钮查看详情，或使用 /search [关键词] 搜索相关内容。
"""
    
    await update.message.reply_text(news_intro, parse_mode="Markdown", reply_markup=reply_markup)
    logger.info(f"资讯中心已访问: {update.effective_chat.id}")

async def news_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理资讯按钮回调"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "news_latest":
        content = """
📰 *最新行业动态*

**WS云控/TG云控 最新资讯：**

1. 🔥 多账户管理需求增长
   - 2024年企业级云控需求同比增长40%
   - 跨平台管理成为刚需

2. 📈 Telegram Bot API 更新
   - 新增更多管理功能
   - 支持更复杂的工作流

3. 🛡️ 安全合规成为焦点
   - 官方对自动化工具的政策变化
   - 合规使用的重要性

4. ⚡ 效率工具进化
   - AI驱动的自动化解决方案
   - 一站式管理平台兴起

📌 *提示*: 关注官方渠道获取最新信息
"""
    elif query.data == "news_tools":
        content = """
📱 *热门云控工具推荐*

**WS云控系统：**
• 功能全面的企业解决方案
• 支持多平台账号管理
• 自动化工作流

**TG运营助手：**
• 消息自动回复
• 关键词触发
• 群发管理

**常用工具类型：**
1. 账号管理工具
2. 消息群发工具
3. 数据分析工具
4. 自动回复工具

⚠️ *提醒*: 请选择正规渠道的工具
"""
    elif query.data == "news_tips":
        content = """
💡 *运营技巧分享*

**高效运营建议：**

1. 📊 **数据驱动**
   - 定期分析用户数据
   - 优化内容策略

2. 🤖 **自动化流程**
   - 设置关键词自动回复
   - 定时发布内容

3. 👥 **用户管理**
   - 分层管理用户
   - 个性化服务

4. 📈 **增长策略**
   - 裂变活动设计
   - 用户留存优化

5. 🛡️ **风险控制**
   - 合规操作
   - 数据备份
"""
    elif query.data == "news_refresh":
        content = "🔄 资讯已刷新！请查看最新内容。"
    
    keyboard = [
        [
            InlineKeyboardButton("📰 最新资讯", callback_data="news_latest"),
            InlineKeyboardButton("📱 云控工具", callback_data="news_tools"),
        ],
        [
            InlineKeyboardButton("💡 使用技巧", callback_data="news_tips"),
            InlineKeyboardButton("🔄 刷新", callback_data="news_refresh"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(content, parse_mode="Markdown", reply_markup=reply_markup)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /search 命令"""
    bot_state.total_commands += 1
    bot_state.total_messages += 1
    
    if not context.args:
        await update.message.reply_text(
            "🔍 *搜索功能*\n\n"
            "用法: `/search [关键词]`\n\n"
            "例如: `/search 云控`"
        )
        return
    
    keyword = ' '.join(context.args)
    
    # 简单的搜索结果（实际应用中可连接真实API）
    results = [
        f"关于「{keyword}」的搜索结果：",
        "",
        "📌 相关话题：",
        f"• {keyword}基础知识入门",
        f"• {keyword}使用技巧",
        f"• {keyword}常见问题解答",
        "",
        "💡 *提示*: 使用 /news 查看更多资讯"
    ]
    
    result_text = "\n".join(results)
    await update.message.reply_text(result_text, parse_mode="Markdown")
    logger.info(f"搜索: {keyword} - {update.effective_chat.id}")

async def getchatinfo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /getchatinfo 命令"""
    bot_state.total_commands += 1
    
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ 此命令仅限管理员使用")
        return
    
    chat = update.effective_chat
    info_text = f"💬 *当前对话信息*\n\n{get_chat_info_text(chat)}"
    await update.message.reply_text(info_text, parse_mode="Markdown")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /stats 命令"""
    bot_state.total_commands += 1
    
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ 此命令仅限管理员使用")
        return
    
    stats_text = f"""
📊 *统计数据*

**消息统计：**
• 总消息数: {bot_state.total_messages}
• 总命令数: {bot_state.total_commands}

**注册统计：**
• 注册群组/对话: {len(bot_state.registered_chats)}

**关键词统计：**
• 关键词数量: {len(bot_state.keyword_responses)}

**系统信息：**
• 运行时间: {bot_state.to_dict()['运行时间']}
• 启动时间: {bot_state.to_dict()['启动时间']}
"""
    await update.message.reply_text(stats_text, parse_mode="Markdown")

async def forward_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /forward 命令 - 转发消息到指定chat"""
    bot_state.total_commands += 1
    
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ 此命令仅限管理员使用")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "🔄 *转发消息*\n\n"
            "用法: `/forward [chat_id] [消息]`\n\n"
            "示例: `/forward -100123456789 你好！`"
        )
        return
    
    try:
        target_chat_id = int(context.args[0])
        message = ' '.join(context.args[1:])
        
        await context.bot.send_message(
            chat_id=target_chat_id,
            text=message,
            parse_mode="Markdown"
        )
        await update.message.reply_text(f"✅ 消息已转发至 {target_chat_id}")
        logger.info(f"消息转发至: {target_chat_id}")
    except ValueError:
        await update.message.reply_text("❌ 无效的 chat_id，请输入数字")

async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /echo 命令 - 回显消息"""
    bot_state.total_commands += 1
    
    if not context.args:
        await update.message.reply_text("用法: `/echo [消息]`")
        return
    
    message = ' '.join(context.args)
    await update.message.reply_text(message)

# ============ 消息处理器 ============

async def keyword_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理关键词自动回复"""
    bot_state.total_messages += 1
    text = update.message.text.lower()
    
    # 检查关键词
    for keyword, response in bot_state.keyword_responses.items():
        if keyword in text:
            await update.message.reply_text(response)
            logger.info(f"关键词触发: '{keyword}' by {update.effective_user.id}")
            return
    
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

async def new_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理新成员加入群组"""
    bot_state.total_messages += 1
    
    for member in update.message.new_chat_members:
        welcome_text = f"""
👋 *欢迎 {member.first_name}！*

欢迎加入 {update.message.chat.title}！

我是 *{config.BOT_NAME}*，这里是我的运营助手。

发送 /help 查看我的功能！
"""
        await update.message.reply_text(welcome_text, parse_mode="Markdown")
        logger.info(f"新成员加入: {member.first_name} in {update.message.chat.title}")

async def left_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理成员离开群组"""
    logger.info(f"成员离开: {update.message.left_chat_member.first_name} from {update.message.chat.title}")

# ============ 错误处理 ============

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理错误"""
    logger.error(f"错误: {context.error} - Update: {update}")

# ============ 主函数 ============

def main():
    """主函数 - 启动机器人"""
    logger.info(f"🤖 {config.BOT_NAME} 启动中...")
    
    # 创建应用（使用代理）
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # 添加命令处理器
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("setkeyword", setkeyword_command))
    application.add_handler(CommandHandler("delkeyword", delkeyword_command))
    application.add_handler(CommandHandler("listkeywords", listkeywords_command))
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("getchatinfo", getchatinfo_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("forward", forward_command))
    application.add_handler(CommandHandler("echo", echo_command))
    
    # 添加回调处理器
    application.add_handler(CallbackQueryHandler(news_callback))
    
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
    
    # 处理成员离开
    application.add_handler(MessageHandler(
        filters.StatusUpdate.LEFT_CHAT_MEMBER,
        left_member_handler
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
║  Token: {config.BOT_TOKEN[:20]}...                   ║
║  管理员ID: {config.ADMIN_IDS if config.ADMIN_IDS else '未设置(所有人可用)'}     ║
╠═══════════════════════════════════════════════════╣
║  发送 /start 到机器人开始使用                       ║
║  发送 /help 查看所有可用指令                        ║
╚═══════════════════════════════════════════════════╝
    """)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
