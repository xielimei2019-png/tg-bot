# 📁 项目文件说明

## 目录结构

```
telegram-bot-assistant/
├── 📄 核心文件
│   ├── main.py              # 🤖 主程序入口
│   ├── config.py            # ⚙️ 配置文件
│   └── requirements.txt     # 📦 Python 依赖
│
├── 📚 文档文件
│   ├── README.md            # 📖 完整说明文档
│   ├── QUICKSTART.md        # 🚀 快速开始指南
│   └── FILES.md             # 📁 本文档
│
├── 🔧 脚本文件
│   ├── run.sh               # ▶️ 启动脚本
│   ├── start.sh             # 🚀 快速启动
│   ├── setup.py             # ⚙️ 初始化设置
│   ├── test.py              # 🧪 功能测试
│   ├── manage.py            # 🛠️ 管理工具
│   └── deploy.sh            # 🌐 一键部署脚本
│
├── 🐳 部署文件
│   ├── Dockerfile           # 📦 Docker 配置
│   ├── docker-compose.yml   # 📦 Docker Compose 配置
│   └── .env.example         # 📝 环境变量示例
│
├── ⚙️ 系统服务
│   └── tg-assistant-bot.service  # 🔧 systemd 服务配置
│
├── 📊 日志文件（运行时生成）
│   └── bot.log              # 📝 运行日志
│
└── 📦 其他
    └── __pycache__/         # 🐍 Python 缓存
```

---

## 📄 核心文件详解

### 1. main.py - 主程序
**作用**：机器人的核心逻辑，包含所有命令处理器和消息处理逻辑

**功能**：
- 处理所有用户命令
- 关键词自动回复
- 群发消息
- 资讯中心
- 状态监控

**运行方式**：
```bash
python3 main.py
```

---

### 2. config.py - 配置文件
**作用**：存储机器人的所有配置信息

**主要配置项**：
- `BOT_TOKEN` - Telegram Bot Token
- `ADMIN_IDS` - 管理员用户ID列表
- `BOT_NAME` - 机器人名称
- `KEYWORD_RESPONSES` - 关键词回复字典
- `WELCOME_MESSAGE` - 欢迎消息
- `HELP_MESSAGE` - 帮助信息

**重要**：请在首次运行前配置 `BOT_TOKEN`

---

### 3. requirements.txt - 依赖文件
**作用**：列出项目所需的所有 Python 包

**当前依赖**：
```
python-telegram-bot==21.7
```

**安装方式**：
```bash
pip install -r requirements.txt
```

---

## 📚 文档文件说明

### 1. README.md
完整的项目文档，包含：
- 功能特性
- 快速开始
- 部署指南
- 故障排除
- 安全建议

### 2. QUICKSTART.md
快速开始指南，包含：
- 快速启动步骤
- 基本使用说明
- 管理员设置
- 常见问题

### 3. FILES.md (本文档)
项目文件说明，帮助理解每个文件的作用

---

## 🔧 脚本文件详解

### 1. run.sh - 启动脚本
**功能**：检查环境并启动机器人

**特点**：
- 自动检查 Python 版本
- 自动安装依赖（如缺失）
- 创建日志文件

**使用**：
```bash
./run.sh
```

---

### 2. start.sh - 快速启动
**功能**：快速启动机器人的简化脚本

**特点**：
- 最小化依赖检查
- 快速启动

**使用**：
```bash
./start.sh
```

---

### 3. setup.py - 初始化设置
**功能**：引导用户完成首次配置

**特点**：
- 交互式配置
- 自动更新 config.py
- 生成 .env 文件

**使用**：
```bash
python3 setup.py
```

---

### 4. test.py - 功能测试
**功能**：测试机器人的各项功能

**测试项目**：
- 机器人信息获取
- 命令列表检查
- Webhook 配置
- 消息发送测试

**使用**：
```bash
python3 test.py
```

---

### 5. manage.py - 管理工具
**功能**：命令行管理界面

**功能**：
- 查看运行状态
- 查看日志
- 管理关键词
- 重启服务

**使用**：
```bash
python3 manage.py
```

---

### 6. deploy.sh - 一键部署
**功能**：在服务器上一键部署机器人

**特点**：
- 自动安装所有依赖
- 配置 systemd 服务
- 启动并验证

**使用**：
```bash
sudo ./deploy.sh
```

---

## 🐳 部署文件说明

### 1. Dockerfile
**作用**：Docker 容器配置

**特点**：
- 基于 Python 3.11 slim 镜像
- 自动安装依赖
- 持久化日志

**构建**：
```bash
docker build -t tg-assistant-bot .
```

---

### 2. docker-compose.yml
**作用**：Docker Compose 编排配置

**特点**：
- 环境变量配置
- 自动重启
- 日志持久化

**启动**：
```bash
docker-compose up -d
```

---

### 3. .env.example
**作用**：环境变量配置示例

**变量**：
- `BOT_TOKEN` - 机器人 Token
- `ADMIN_IDS` - 管理员 ID

**使用**：复制为 `.env` 并填写实际值

---

## ⚙️ 系统服务文件

### tg-assistant-bot.service
**作用**：systemd 服务单元配置

**功能**：
- 开机自启
- 自动重启
- 日志管理

**安装**：
```bash
sudo cp tg-assistant-bot.service /etc/systemd/system/
sudo systemctl enable tg-assistant-bot
sudo systemctl start tg-assistant-bot
```

---

## 📊 运行时生成文件

### bot.log
**作用**：记录机器人运行日志

**内容**：
- 启动/停止事件
- 消息收发记录
- 命令执行日志
- 错误信息

**查看**：
```bash
tail -f bot.log
```

---

## 🗂️ 文件权限

所有脚本文件都已设置可执行权限：

```bash
chmod +x *.sh *.py
```

---

## 📥 下载和安装

### 方式一：Git 克隆
```bash
git clone <repository-url>
cd telegram-bot-assistant
```

### 方式二：直接下载
下载所有文件到本地目录

---

## ✅ 推荐的工作流程

### 首次设置
1. 复制项目文件
2. 运行 `python3 setup.py` 完成配置
3. 测试 `python3 test.py`
4. 启动 `python3 main.py`

### 日常使用
1. 启动：`python3 main.py`
2. 管理：`python3 manage.py`
3. 监控：查看 `bot.log`

### 服务器部署
1. 上传文件
2. 运行 `sudo ./deploy.sh`
3. 管理：`sudo systemctl start tg-assistant-bot`

---

## 🔄 备份建议

定期备份以下文件：
- `config.py` - 配置文件
- `bot.log` - 运行日志
- `keyword_responses.json` - 关键词数据（如果单独存储）

---

## 🧹 清理建议

### 删除 Python 缓存
```bash
rm -rf __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### 清理日志
```bash
# 清空日志文件
> bot.log

# 或删除旧日志
rm bot.log
```

---

## 📞 技术支持

如遇问题，请检查：
1. 📖 README.md - 完整文档
2. 🔍 bot.log - 错误日志
3. ⚙️ config.py - 配置是否正确
4. 🐛 Google/Bing - 搜索错误信息

---

**📌 提示**：保持所有文件在同一目录结构中，不要修改文件名和相对路径！
