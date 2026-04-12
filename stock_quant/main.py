#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 修复导入路径：将项目根目录添加到 sys.path
# 这样在运行 main.py 时，可以正确找到 graph、tools 等模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 导入本地模块
from graph.stock_graph import stock_graph
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

def main():
    print("=" * 50)
    print("      🚀 AI 股票深度分析系统 (LangGraph 版) 🚀      ")
    print("=" * 50)
    print("你可以输入以下指令，或直接用自然语言与我交流：")
    print("-" * 50)
    print("1. 📰 宏观新闻：'帮我看看今天的财经新闻' 或 '成交早餐'")
    print("2. 📉 个股分析：'分析一下 000001 的近期走势' 或 '查看某股票的新闻'")
    print("3. 👔 专家洞察：'2024年分析师排名' 或 '韩东分析师最近在跟踪哪些股票'")
    print("4. 💾 批量处理：'批量保存 2024 年分析师详情数据'")
    print("-" * 50)
    print("💡 提示：输入 'exit' 或 'quit' 即可退出系统。")
    print("-" * 50)
    
    # 设定 thread_id (持久化记忆的钥匙)
    # 你可以手动输入 ID，也可以默认用 default_user
    user_id = input("请输入你的用户 ID (直接回车使用 'default_user'): ").strip() or "default_user"
    config = {"configurable": {"thread_id": user_id}}
    
    print(f"\n--- 当前对话 ID: {user_id} (历史记录已自动从数据库加载) ---\n")

    while True:
        try:
            user_input = input("\n用户：")
            if user_input.lower() in ['exit', 'quit', '退出']:
                print("再见！")
                break
            
            if not user_input.strip():
                continue

            print("AI 正在思考并执行图流程...")
            
            # 使用 LangGraph 的 stream 模式来运行，以便看到节点流转
            # 输入格式必须符合 AgentState 的定义
            events = stock_graph.stream(
                {"messages": [HumanMessage(content=user_input)]}, 
                config, 
                stream_mode="values"
            )
            
            # 记录最后一条 AI 的回复
            last_ai_output = ""
            
            for event in events:
                if "messages" in event:
                    last_msg = event["messages"][-1]
                    # 只有当 last_msg 是 AIMessage 且不是工具调用时，才记录为最终回复
                    if isinstance(last_msg, AIMessage) and not last_msg.tool_calls:
                        last_ai_output = last_msg.content
            
            if last_ai_output:
                print(f"\nAI：{last_ai_output}")
            
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
