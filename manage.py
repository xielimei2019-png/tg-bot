#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot 管理工具
提供机器人状态监控、日志查看、配置管理等功能
"""

import os
import sys
import json
import subprocess
from datetime import datetime

try:
    import config
except ImportError:
    print("❌ config.py 文件不存在")
    sys.exit(1)

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """打印标题"""
    print("\n" + "="*60)
    print(f"🤖 {config.BOT_NAME} 管理工具")
    print("="*60)

def show_status():
    """显示机器人状态"""
    print_header()
    print("\n📊 **机器人状态**\n")
    
    # 检查进程
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'python.*main.py'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            pid = result.stdout.strip().split('\n')[0]
            print(f"✅ 状态: 运行中 (PID: {pid})")
        else:
            print("❌ 状态: 未运行")
    except:
        print("⚠️  无法检测进程状态")
    
    # 检查日志
    if os.path.exists('bot.log'):
        with open('bot.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                print(f"📝 最后日志: {last_line[:80]}...")
    
    print()

def show_logs(lines=50):
    """显示日志"""
    print_header()
    print(f"\n📝 **最近 {lines} 条日志**\n")
    
    if not os.path.exists('bot.log'):
        print("❌ 日志文件不存在")
        return
    
    with open('bot.log', 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
        recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        for line in recent_lines:
            print(line.rstrip())
    
    print()

def show_config():
    """显示当前配置"""
    print_header()
    print("\n⚙️  **当前配置**\n")
    print(f"机器人名称: {config.BOT_NAME}")
    print(f"管理员 ID: {config.ADMIN_IDS if config.ADMIN_IDS else '未设置'}")
    print(f"关键词数量: {len(config.KEYWORD_RESPONSES)}")
    print(f"日志级别: {config.LOG_LEVEL}")
    print()

def list_keywords():
    """列出所有关键词"""
    print_header()
    print("\n🔑 **关键词列表**\n")
    
    if not config.KEYWORD_RESPONSES:
        print("📝 当前没有设置关键词")
        return
    
    for i, (keyword, response) in enumerate(config.KEYWORD_RESPONSES.items(), 1):
        response_preview = response[:50] + "..." if len(response) > 50 else response
        print(f"{i}. {keyword} → {response_preview}")
    
    print()

def add_keyword():
    """添加关键词"""
    print_header()
    print("\n➕ **添加关键词**\n")
    
    keyword = input("请输入关键词: ").strip().lower()
    if not keyword:
        print("❌ 关键词不能为空")
        return
    
    response = input("请输入回复内容: ").strip()
    if not response:
        print("❌ 回复内容不能为空")
        return
    
    # 更新配置文件
    config.KEYWORD_RESPONSES[keyword] = response
    
    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单替换（实际应用中应该更严谨）
    print(f"\n⚠️  请手动在 config.py 中添加以下内容：")
    print(f'    "{keyword}": "{response}",')

def restart_bot():
    """重启机器人"""
    print_header()
    print("\n🔄 **重启机器人**\n")
    
    try:
        # 停止现有进程
        subprocess.run(['pkill', '-f', 'python.*main.py'])
        print("✅ 已停止现有进程")
        
        # 启动新进程
        subprocess.Popen(
            ['python3', 'main.py'],
            stdout=open('bot.log', 'a'),
            stderr=subprocess.STDOUT
        )
        print("✅ 已启动新进程")
    except Exception as e:
        print(f"❌ 重启失败: {e}")

def show_help():
    """显示帮助"""
    print_header()
    print("\n📚 **管理命令**\n")
    print("  1. 查看状态      - 显示机器人运行状态")
    print("  2. 查看日志      - 显示最近日志")
    print("  3. 查看配置      - 显示当前配置")
    print("  4. 关键词列表    - 显示所有关键词")
    print("  5. 添加关键词    - 添加新的关键词回复")
    print("  6. 重启机器人    - 重启机器人服务")
    print("  7. 帮助         - 显示此帮助")
    print("  0. 退出         - 退出管理工具")
    print()

def main():
    """主函数"""
    clear_screen()
    
    while True:
        print_header()
        print("\n请选择操作:")
        print("1. 查看状态")
        print("2. 查看日志")
        print("3. 查看配置")
        print("4. 关键词列表")
        print("5. 添加关键词")
        print("6. 重启机器人")
        print("7. 帮助")
        print("0. 退出")
        
        choice = input("\n请输入选项: ").strip()
        
        if choice == '1':
            show_status()
        elif choice == '2':
            show_logs()
        elif choice == '3':
            show_config()
        elif choice == '4':
            list_keywords()
        elif choice == '5':
            add_keyword()
        elif choice == '6':
            restart_bot()
        elif choice == '7':
            show_help()
        elif choice == '0':
            print("\n👋 再见！")
            break
        else:
            print("\n❌ 无效的选项，请重试")
        
        input("\n按 Enter 继续...")

if __name__ == "__main__":
    main()
