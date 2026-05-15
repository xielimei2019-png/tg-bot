# Telegram Bot Assistant - 配置文件

# 你的 Telegram Bot Token (从 @BotFather 获取)
BOT_TOKEN = "8539940556:AAHxCyOyB6l-7a_lQegPA5n2aa1OQL5yBbs"

# 主人/管理员的用户ID (可以从 @userinfobot 获取)
# 设置为你自己的 Telegram 用户ID，这样只有你能使用管理命令
ADMIN_IDS = []  # 例如: [123456789, 987654321]

# 资讯收集功能配置
# 接收资讯的用户ID（机器人会把收集到的资讯发给你）
INFO_RECEIVER_ID = 7684503671  # 你的 Telegram 用户ID

# 资讯关键词列表（当群里有这些关键词时，机器人会转发给你）
INFO_KEYWORDS = [
    "WS拉群",
    "WS精准粉",
    "WS引流",
    "WS云控",
    "WS6段协议号",
    "WS拉群号",
    "WS解禁组",
    "WS反禁用群组",
    "TG拉群",
    "TG精准粉",
    "TG引流",
    "TG云控",
    "Telegram拉群",
    "Telegram云控",
    "精准粉",
    "云控系统",
    "WS群发",
    "TG群发",
    "Telegram群发",
    "批量注册",
    "养号",
    "矩阵",
    "多开",
    "聚星云控",
]

# 机器人名称
BOT_NAME = "TG运营助手"

# 关键词自动回复配置
# 格式: {"关键词": "回复内容"}
KEYWORD_RESPONSES = {
    "你好": "你好！有什么我可以帮助你的吗？",
    "帮助": "发送 /help 查看所有可用指令",
    "运营": "欢迎使用TG运营助手！我可以帮你管理群组、收集资讯等",
    "云控": "WS云控/TG云控相关资讯请发送 /news 查看",
    "TG": "Telegram运营助手为你服务！发送 /help 查看功能",
    "群发": "群发消息请使用 /broadcast [消息内容] 命令",
}

# 欢迎消息
WELCOME_MESSAGE = """
👋 欢迎使用 {bot_name}！

我是你的 Telegram 运营助手，可以帮助你：

🤖 【核心功能】
• 自动回复消息
• 关键词触发回复
• 群发消息
• 资讯收集
• 主人指令执行

📋 【可用指令】
发送 /help 查看所有指令

💡 【使用提示】
• 将机器人添加到群组即可自动响应
• 管理员可使用高级功能
"""

# 帮助信息
HELP_MESSAGE = """
📚 **{bot_name} - 指令帮助**

*基本指令（所有人可用）：*
/start - 启动机器人
/help - 显示此帮助信息
/status - 查看机器人运行状态
/ping - 测试机器人响应

*关键词回复：*
机器人会自动回复常见关键词

*管理员指令：*
/admin - 查看管理员指令
/broadcast [消息] - 群发消息
/setkeyword [关键词] [回复] - 设置关键词
/delkeyword [关键词] - 删除关键词
/listkeywords - 列出所有关键词

*资讯功能：*
/news - 获取云控/TG行业资讯

*广播功能：*
/forward [chat_id] [消息] - 转发消息到指定chat
"""

# 管理员指令帮助
ADMIN_HELP_MESSAGE = """
🔐 *管理员指令*

/admin - 显示此帮助
/broadcast [消息] - 向所有已注册chat发送消息
/setkeyword [关键词] [回复] - 添加/更新关键词
/delkeyword [关键词] - 删除关键词
/listkeywords - 查看关键词列表
/getchatinfo - 获取当前chat的信息
/stats - 查看统计数据
/shutdown - 关闭机器人（需要确认）
"""

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = "bot.log"
