#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime
from typing import Optional, List

# 导入本地模块
from llm_model import get_llm
from loaders.news_loader import Get_news_main_cx, Save_news_to_csv
from data_source.Stock_RiskAlertInfo import GetStockRiskAlertBoard
from data_source.GetStock_Kline import GetStock_Kline, GetStock_News

# LangChain 相关导入
from langchain_classic.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

# --- 定义 LangChain 工具 ---

@tool
def fetch_financial_news_highlights():
    """
    抓取最新的财经精选新闻（财经早餐），包含标题、摘要和链接。
    """
    df = Get_news_main_cx()
    if df is not None and not df.empty:
        # 将结果转换为字符串，以便 LLM 阅读，限制长度以防超出上下文
        return df.to_string(index=False)
    return "未能获取到财经新闻。"

@tool
def fetch_risk_alert_stocks():
    """
    获取 A 股市场所有的风险警示板块股票（ST 和 *ST 股票），包含代码、名称、最新价、涨跌幅等信息。
    """
    df = GetStockRiskAlertBoard()
    if isinstance(df, pd.DataFrame) and not df.empty:
        # 风险警示股票可能很多，这里只返回前 30 条供分析，并告知总数
        total = len(df)
        return f"当前共有 {total} 只风险警示股票，以下是前 30 只：\n{df.head(30).to_string(index=False)}"
    return str(df)

@tool
def fetch_stock_kline(symbol: str, period: str = "daily", start_date: str = "20240101", end_date: str = "20240327"):
    """
    获取指定股票的 K 线数据。
    :param symbol: 股票代码（如 000001）
    :param period: 周期（daily, weekly, monthly）
    :param start_date: 开始日期 (YYYYMMDD)
    :param end_date: 结束日期 (YYYYMMDD)
    """
    df = GetStock_Kline(symbol=symbol, period=period, start_date=start_date, end_date=end_date)
    if isinstance(df, pd.DataFrame) and not df.empty:
        return df.to_string(index=False)
    return f"未能获取到股票 {symbol} 的 K 线数据。"

@tool
def fetch_individual_stock_news(symbol: str):
    """
    获取指定个股的最新新闻资讯。
    :param symbol: 股票代码（如 000001）
    """
    df = GetStock_News(symbol=symbol)
    if isinstance(df, pd.DataFrame) and not df.empty:
        return df.to_string(index=False)
    return f"未能获取到股票 {symbol} 的相关新闻。"

@tool
def save_data_to_csv(data_str: str, prefix: str):
    """
    将分析出的数据或查询到的数据保存为本地 CSV 文件。
    :param data_str: 要保存的数据内容（字符串形式）
    :param prefix: 文件名前缀（如 '分析结果'）
    """
    # 简单模拟：将字符串转换为 DataFrame 后保存
    # 实际应用中可以根据需要调整
    try:
        from io import StringIO
        df = pd.read_csv(StringIO(data_str))
        path = Save_news_to_csv(df, prefix=prefix)
        return f"数据已成功保存至: {path}"
    except Exception as e:
        return f"保存失败: {e}"

# --- 初始化 Agent ---

def init_agent():
    llm = get_llm()
    tools = [
        fetch_financial_news_highlights,
        fetch_risk_alert_stocks,
        fetch_stock_kline,
        fetch_individual_stock_news,
        save_data_to_csv
    ]
    
    # 定义提示词模版
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的股票分析助手。你可以使用提供的工具查询最新的财经新闻、个股 K 线、风险警示股票等信息。请根据查询到的数据为用户提供专业的分析建议。如果用户要求保存数据，请调用保存工具。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # 创建 Agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def main():
    print("=== 欢迎使用 AI 股票分析系统 ===")
    print("你可以输入类似：'帮我看看今天的财经新闻'、'分析一下 000001 的近期走势' 或 '有哪些 ST 股票值得注意' 等内容。输入 'exit' 退出。")
    
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
            
            # 更新对话历史（可选）
            # chat_history.extend([
            #     ("human", user_input),
            #     ("ai", ai_output)
            # ])
            
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
