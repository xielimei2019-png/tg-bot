# 🎯 Telegram 运营助手 - 快速开始指南

## 🚀 立即开始

### 第一步：运行机器人

```bash
cd telegram-bot-assistant
pip install -r requirements.txt
python3 main.py
```

### 第二步：在 Telegram 中使用

1. 打开 Telegram 应用
2. 搜索你的机器人（@你的机器人用户名）
3. 点击 "Start" 或发送 `/start`

### 第三步：测试基本功能

发送以下命令测试：

- `/help` - 查看所有指令
- `/status` - 查看运行状态
- `/ping` - 测试响应
- `/news` - 打开资讯中心

---

## 📱 添加到群组

### 方法：

1. 打开你的 Telegram 群组
2. 点击群组名称 → "Add Member"
3. 搜索并添加你的机器人
4. **建议**：给机器人管理员权限以获得完整功能

### 群组功能：

- ✅ 自动回复关键词消息
- ✅ 新成员加入时自动欢迎
- ✅ 消息统计和监控
- ✅ 群发公告功能（管理员）

---

## 🔧 管理员功能

### 设置管理员

1. 在 Telegram 搜索 `@userinfobot`
2. 发送任意消息获取你的 User ID
3. 编辑 `config.py`：

```python
ADMIN_IDS = [你的UserID]  # 例如: ADMIN_IDS = [123456789]
```

### 管理员可用指令：

```
/admin      - 查看管理员帮助
/broadcast  - 群发消息
/setkeyword - 添加关键词
/delkeyword - 删除关键词
/listkeywords - 查看关键词
/stats      - 查看统计数据
```

---

## 🎨 自定义关键词

### 添加关键词：

```
/setkeyword 你好 您好！欢迎使用我们的服务！
```

### 删除关键词：

```
/delkeyword 你好
```

### 预置关键词：

机器人已配置以下默认关键词：
- 你好
- 帮助
- 运营
- 云控
- TG
- 群发

---

## 🌐 云端部署

### Docker 部署（推荐）

```bash
# 1. 构建镜像
docker build -t tg-assistant-bot .

# 2. 运行容器
docker run -d \
  --name tg-bot \
  -e BOT_TOKEN=你的Token \
  tg-assistant-bot
```

### VPS 部署

```bash
# 1. 上传代码到服务器
scp -r telegram-bot-assistant user@your-server:/opt/

# 2. SSH 登录服务器
ssh user@your-server

# 3. 运行一键部署脚本
cd /opt/telegram-bot-assistant
chmod +x deploy.sh
sudo ./deploy.sh
```

### systemd 服务管理

```bash
# 查看状态
sudo systemctl status tg-assistant-bot

# 查看日志
sudo journalctl -u tg-assistant-bot -f

# 重启服务
sudo systemctl restart tg-assistant-bot

# 停止服务
sudo systemctl stop tg-assistant-bot
```

---

## 📊 功能概览

### 🤖 核心功能

| 功能 | 说明 | 状态 |
|------|------|------|
| 自动回复 | 基于关键词的消息回复 | ✅ |
| 群发消息 | 向所有群组发送广播 | ✅ |
| 新成员欢迎 | 自动欢迎新成员 | ✅ |
| 资讯中心 | TG/云控行业资讯 | ✅ |
| 状态监控 | 实时运行状态 | ✅ |
| 日志记录 | 完整操作日志 | ✅ |

### 🔐 管理员功能

| 功能 | 说明 | 状态 |
|------|------|------|
| 关键词管理 | 添加/删除关键词 | ✅ |
| 统计数据 | 消息和用户统计 | ✅ |
| 群组信息 | 获取群组详细信息 | ✅ |
| 消息转发 | 转发到指定群组 | ✅ |
| 广播系统 | 批量消息发送 | ✅ |

---

## 🛠️ 故障排除

### 机器人无响应？

1. 检查 Token 是否正确
2. 确认机器人未被封禁
3. 查看日志文件：`tail -f bot.log`

### 消息发送失败？

1. 确认机器人在群组中
2. 检查是否有管理员权限
3. 验证 chat_id 是否正确

### 部署问题？

1. 确认 Python 版本 ≥ 3.9
2. 检查依赖是否完整安装
3. 验证防火墙设置

### 常见错误

```
❌ Error: Bot token invalid
   → 检查 BOT_TOKEN 是否正确

❌ Error: Chat not found
   → 确认 chat_id 正确且机器人有权限

❌ Error: Forbidden: bot was blocked by the user
   → 用户屏蔽了机器人
```

---

## 📞 获取帮助

### 常用命令

```bash
# 查看帮助
python3 manage.py

# 查看日志
tail -f bot.log

# 测试机器人
python3 test.py

# 初始化设置
python3 setup.py
```

### 日志位置

- 控制台输出
- `bot.log` 文件
- systemd: `journalctl -u tg-assistant-bot`

---

## 🔄 更新机器人

### 本地更新

```bash
# 停止当前运行
pkill -f main.py

# 更新代码
git pull  # 或手动替换文件

# 安装新依赖
pip install -r requirements.txt

# 重启
python3 main.py
```

### Docker 更新

```bash
# 重新构建
docker build -t tg-assistant-bot .
docker-compose down
docker-compose up -d
```

---

## 💡 最佳实践

### 安全建议

1. 🔒 保护好 BOT_TOKEN，不要泄露
2. 👤 设置管理员 ID，只允许你使用管理命令
3. 📝 定期检查日志，监控异常活动
4. 🔄 保持依赖库更新

### 运营建议

1. 📊 定期查看统计数据
2. 🔑 定期更新关键词库
3. 👥 收集用户反馈
4. ⚡ 监控机器人性能

### 性能优化

1. 📝 控制日志文件大小
2. 🗄️ 定期清理注册群组列表
3. 🔄 使用云端部署保证稳定性
4. 📈 监控内存和 CPU 使用

---

## 📋 检查清单

在开始使用前，请确认：

- [ ] Robot Token 已配置
- [ ] Python 3.9+ 已安装
- [ ] 依赖已安装 (`pip install -r requirements.txt`)
- [ ] 机器人已启动 (`python3 main.py`)
- [ ] 已在 Telegram 测试基本命令
- [ ] 已阅读 `/help` 指令列表
- [ ] （可选）已设置管理员 ID
- [ ] （可选）已部署到云端

---

**🎉 恭喜！你的 Telegram 运营助手已准备就绪！**

如有问题，请查看：
- 📖 README.md - 完整文档
- 🐛 bot.log - 运行日志
- 🔧 config.py - 配置文件