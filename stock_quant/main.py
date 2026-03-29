#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime
from typing import Optional, List

# 导入本地模块
from llm_model import get_llm
from tools.stock_tools import (
    fetch_financial_news_highlights,
    fetch_risk_alert_stocks,
    fetch_cjzc_news,
    fetch_stock_kline,
    fetch_individual_stock_news,
    save_data_to_csv,
    read_local_news_csv,
    fetch_analyst_rank,
    fetch_analyst_detail,
    batch_save_all_analysts_details
)

# LangChain 相关导入
from langchain_classic.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# --- 初始化 Agent ---

def init_agent():
    llm = get_llm()
    tools = [
        fetch_financial_news_highlights,
        fetch_risk_alert_stocks,
        fetch_cjzc_news,
        fetch_stock_kline,
        fetch_individual_stock_news,
        save_data_to_csv,
        read_local_news_csv,
        fetch_analyst_rank,
        fetch_analyst_detail,
        batch_save_all_analysts_details
    ]
    
    # 定义提示词模版
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的股票分析助手。你可以使用提供的工具查询最新的财经新闻、个股 K 线、风险警示股票、以及东方财富分析师排名和详情等信息。请根据查询到的数据为用户提供专业的分析建议。如果用户要求保存数据，请调用保存工具。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # 创建 Agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def main():
    print("=" * 50)
    print("      🚀 欢迎使用 AI 股票深度分析系统 🚀      ")
    print("=" * 50)
    print("你可以输入以下指令，或直接用自然语言与我交流：")
    print("-" * 50)
    print("1. 📰 宏观新闻：'帮我看看今天的财经新闻' 或 '成交早餐'")
    print("2. 📉 个股分析：'分析一下 000001 的近期走势' 或 '查看某股票的新闻'")
    print("3. ⚠️ 风险监控：'有哪些 ST 股票值得注意' (ST/*ST 板块)")
    print("4. 👔 专家洞察：'2024年分析师排名' 或 '韩东分析师最近在跟踪哪些股票'")
    print("5. 💾 批量处理：'批量保存 2024 年分析师详情数据'")
    print("6. 📂 数据读取：'读取本地最新的财经新闻 CSV'")
    print("-" * 50)
    print("💡 提示：输入 'exit' 或 'quit' 即可退出系统。")
    print("-" * 50)
    
    agent_executor = init_agent()
    chat_history = []

    while True:
        try:
            user_input = input("\n用户：")
            if user_input.lower() in ['exit', 'quit', '退出']:
                print("再见！")
                break
            
            if not user_input.strip():
                continue

            print("AI 正在思考中...")
            response = agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            ai_output = response["output"]
            print(f"\nAI：{ai_output}")
            
            # 更新对话历史
            chat_history.extend([
                HumanMessage(content=user_input),
                AIMessage(content=ai_output)
            ])
            
            # 限制历史长度（例如保留最近 10 次对话，即 20 条消息）
            if len(chat_history) > 20:
                chat_history = chat_history[-20:]
            
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
