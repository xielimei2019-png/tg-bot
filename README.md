# 🤖 Telegram 运营助手机器人

一个功能完整的 Telegram Bot，用于自动化运营、消息管理和云控资讯收集。

## 📋 功能特性

### 核心功能
- ✅ **自动回复消息** - 智能消息处理
- ✅ **关键词触发** - 自定义关键词自动回复
- ✅ **群发消息** - 一键向所有群组/对话发送消息
- ✅ **资讯收集** - WS云控/TG云控相关资讯
- ✅ **管理员指令** - 丰富的管理命令
- ✅ **新成员欢迎** - 自动欢迎新加入的成员

### 可用指令

#### 基本指令（所有人可用）
| 指令 | 说明 |
|------|------|
| `/start` | 启动机器人 |
| `/help` | 显示帮助信息 |
| `/status` | 查看机器人运行状态 |
| `/ping` | 测试机器人响应 |
| `/echo [消息]` | 回显消息 |
| `/news` | 打开资讯中心 |
| `/search [关键词]` | 搜索相关内容 |

#### 管理员指令
| 指令 | 说明 |
|------|------|
| `/admin` | 显示管理员帮助 |
| `/broadcast [消息]` | 群发消息到所有注册的群组 |
| `/setkeyword [关键词] [回复]` | 添加或更新关键词 |
| `/delkeyword [关键词]` | 删除关键词 |
| `/listkeywords` | 列出所有关键词 |
| `/getchatinfo` | 获取当前群组信息 |
| `/stats` | 查看统计数据 |
| `/forward [chat_id] [消息]` | 转发消息到指定chat |

## 🚀 快速开始

### 1. 安装依赖

```bash
cd telegram-bot-assistant
pip install -r requirements.txt
```

### 2. 配置机器人

编辑 `config.py` 文件：

```python
# 设置你的 Bot Token
BOT_TOKEN = "你的BOT_TOKEN"

# 设置管理员ID（可选）
ADMIN_IDS = [你的用户ID]

# 机器人名称
BOT_NAME = "你的机器人名称"
```

### 3. 运行机器人

```bash
python main.py
```

## 📱 使用指南

### 将机器人添加到群组

1. 在 Telegram 中打开你的群组
2. 点击群组名称 → 添加成员
3. 搜索并添加你的机器人
4. 给机器人添加管理员权限（建议）

### 使用示例

#### 设置关键词回复
```
/setkeyword 你好 您好！欢迎使用！
```

#### 群发消息
```
/broadcast 大家好，这是一条群发消息！
```

#### 转发消息到指定群组
```
/forward -100123456789 你好，这是转发消息！
```

## 🌐 部署到云端

### Docker 部署

创建 `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

创建 `docker-compose.yml`:

```yaml
version: '3.8'
services:
  bot:
    build: .
    restart: always
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
```

部署：
```bash
docker-compose up -d
```

### VPS/服务器部署

```bash
# 安装 Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv

# 创建虚拟环境
python3.11 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 后台运行
nohup python main.py > bot.log 2>&1 &

# 查看运行状态
tail -f bot.log
```

### 使用 systemd 管理

创建 `/etc/systemd/system/tg-bot.service`:

```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/telegram-bot-assistant
ExecStart=/path/to/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl enable tg-bot
sudo systemctl start tg-bot
sudo systemctl status tg-bot
```

## 📊 获取 Chat ID

### 方法1：使用机器人
1. 将机器人添加到目标群组
2. 在群组中发送任意消息
3. 查看机器人日志中的 chat_id

### 方法2：使用 @userinfobot
1. 在私聊中联系 @userinfobot
2. 获取你的 user_id
3. 群组的 chat_id 通常是负数（如 -100123456789）

## 🔒 安全建议

1. **保护 Token** - 不要将 BOT_TOKEN 分享给他人
2. **设置管理员** - 建议设置 ADMIN_IDS，只允许你使用管理命令
3. **定期更新** - 保持依赖库更新
4. **日志监控** - 定期检查日志文件

## 🛠️ 故障排除

### 机器人无响应
- 检查 BOT_TOKEN 是否正确
- 检查网络连接
- 查看日志文件 `bot.log`

### 消息发送失败
- 确认机器人已在群组中
- 检查是否有管理员权限
- 验证 chat_id 是否正确

### 部署问题
- 确保 Python 版本 >= 3.9
- 检查所有依赖是否正确安装
- 验证防火墙设置

## 📝 日志

日志文件 `bot.log` 记录：
- 机器人启动/停止事件
- 消息收发记录
- 命令执行情况
- 错误信息

## 🔄 更新机器人

```bash
# 停止当前运行的机器人
pkill -f main.py

# 更新代码
git pull  # 或手动下载新版本

# 安装新依赖（如果有）
pip install -r requirements.txt

# 重启机器人
python main.py
```

## 📞 获取帮助

- 查看 `/help` 获取所有指令
- 查看 `/status` 查看运行状态
- 查看 `/admin` 获取管理员帮助

## 📄 许可证

MIT License

---

💡 **提示**: 将机器人添加到你的群组后，它会自动响应关键词和新成员！