#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot 一键启动器
检查环境并启动机器人
"""

import os
import sys
import subprocess

def print_banner():
    """打印横幅"""
    print("""
╔══════════════════════════════════════════════════════╗
║                                                      ║
║     🤖 Telegram 运营助手 - 一键启动                  ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
    """)

def check_python():
    """检查 Python 版本"""
    print("📌 检查 Python 版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 版本过低: {version.major}.{version.minor}")
        print("   需要 Python 3.9 或更高版本")
        return False
    print(f"✅ Python 版本: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """检查并安装依赖"""
    print("\n📦 检查依赖...")
    
    try:
        import telegram
        print("✅ python-telegram-bot 已安装")
        return True
    except ImportError:
        print("⚠️  python-telegram-bot 未安装")
        print("🔄 正在安装...")
        
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT
            )
            print("✅ 依赖安装完成")
            return True
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败")
            return False

def check_config():
    """检查配置文件"""
    print("\n⚙️  检查配置文件...")
    
    if not os.path.exists('config.py'):
        print("❌ config.py 不存在")
        return False
    
    try:
        import config
        if not hasattr(config, 'BOT_TOKEN') or config.BOT_TOKEN == "your_bot_token_here":
            print("⚠️  请在 config.py 中配置 BOT_TOKEN")
            print("   编辑 config.py 文件，填入你的 Telegram Bot Token")
            return False
        print("✅ 配置文件检查通过")
        return True
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False

def start_bot():
    """启动机器人"""
    print("\n🚀 启动机器人...")
    print("=" * 60)
    
    try:
        # 导入并启动主程序
        import main
        print("✅ 机器人已启动！")
        print("\n📱 在 Telegram 中找到你的机器人并发送 /start")
        print("📖 发送 /help 查看所有可用指令")
        print("\n按 Ctrl+C 停止机器人\n")
        print("=" * 60)
        
        # 运行主程序
        main.main()
        
    except KeyboardInterrupt:
        print("\n\n👋 机器人已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    
    # 执行检查
    checks = [
        ("Python 版本", check_python()),
        ("依赖安装", check_dependencies()),
        ("配置文件", check_config()),
    ]
    
    # 汇总检查结果
    print("\n" + "=" * 60)
    print("📊 检查结果汇总")
    print("=" * 60)
    
    all_passed = True
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if not all_passed:
        print("\n⚠️  部分检查未通过，请解决上述问题后重试")
        print("💡 提示：")
        print("   1. 确保 Python 版本 >= 3.9")
        print("   2. 运行: pip install -r requirements.txt")
        print("   3. 编辑 config.py 填入正确的 BOT_TOKEN")
        return
    
    # 启动机器人
    start_bot()

if __name__ == "__main__":
    main()
