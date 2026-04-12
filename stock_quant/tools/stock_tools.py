#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime
from io import StringIO
from langchain_core.tools import tool
from typing import Optional

# 导入底层数据加载模块 (统一从 loaders 目录导入)
from loaders.stock_news_main_loader import Get_news_main_cx, Save_news_to_csv
from loaders.stock_risk_loader import GetStockRiskAlertBoard
from loaders.stock_kline_loader import GetStock_Kline, GetStock_News
from loaders.stock_cjzc_loader import Tool_Stock_Info_Cjzc_Em
from loaders.stock_analyst_rank import (
    Get_stock_analyst_rank_em, 
    Get_stock_analyst_detail_em, 
    batch_save_all_analysts_details as run_batch_save_analysts
)

# 导入本地模块
from llm_model import get_ollama_llm

@tool
def fetch_financial_news_highlights():
    """
    抓取最新的财经精选新闻（财经早餐），包含标题、摘要和链接。无需输入参数。
    """
    df = Get_news_main_cx()
    if df is not None and not df.empty:
        return df.to_string(index=False)
    return "未能获取到财经新闻。"

@tool
def fetch_risk_alert_stocks():
    """
    获取 A 股市场所有的风险警示板块股票（ST 和 *ST 股票），包含代码、名称、最新价、涨跌幅等信息。无需输入参数。
    """
    df = GetStockRiskAlertBoard()
    if isinstance(df, pd.DataFrame) and not df.empty:
        total = len(df)
        return f"当前共有 {total} 只风险警示股票，以下是前 30 只：\n{df.head(30).to_string(index=False)}"
    return str(df)

@tool
def fetch_cjzc_news():
    """
    获取最新的财经早餐精选新闻（成交早餐）。无需输入参数。
    """
    df = Tool_Stock_Info_Cjzc_Em()
    if isinstance(df, pd.DataFrame) and not df.empty:
        return df.to_string(index=False)
    return str(df)

@tool
def fetch_stock_kline(symbol: str, period: str = "daily", start_date: Optional[str] = None, end_date: Optional[str] = None, adjust: str = "qfq"):
    """
    获取指定股票的 K 线历史数据。
    :param symbol: 股票代码或名称（如 000001 或 平安银行）
    :param period: 周期，可选 'daily' (日线), 'weekly' (周线), 'monthly' (月线)
    :param start_date: 开始日期 (YYYYMMDD)，如果不提供则默认为今天
    :param end_date: 结束日期 (YYYYMMDD)，如果不提供则默认为今天
    :param adjust: 复权类型，默认 'qfq' (前复权)，可选 'hfq' (后复权) 或 '' (不复权)
    """
    # 日期动态处理
    today = datetime.now().strftime("%Y%m%d")
    s_date = start_date if start_date else today
    e_date = end_date if end_date else today

    df = GetStock_Kline(symbol=symbol, period=period, start_date=s_date, end_date=e_date, adjust=adjust)
    if isinstance(df, pd.DataFrame) and not df.empty:
        return df.to_string(index=False)
    return f"未能获取到股票 {symbol} 在 {s_date} 到 {e_date} 期间的 K 线数据。请确认该日期是否为交易日，或股票代码/名称是否正确。"

@tool
def fetch_individual_stock_news(symbol: str):
    """
    获取指定个股的最新新闻资讯。
    :param symbol: 股票代码或名称（如 000001 或 平安银行）
    """
    df = GetStock_News(symbol=symbol)
    if isinstance(df, pd.DataFrame) and not df.empty:
        return df.to_string(index=False)
    return f"未能获取到股票 {symbol} 的相关新闻。请确认股票代码/名称是否正确。"

@tool
def save_data_to_csv(data_str: str, prefix: str):
    """
    将分析出的数据或查询到的数据保存为本地 CSV 文件。
    :param data_str: 要保存的数据内容（字符串形式）
    :param prefix: 文件名前缀（如 '分析结果'）
    """
    try:
        df = pd.read_csv(StringIO(data_str))
        path = Save_news_to_csv(df, prefix=prefix)
        return f"数据已成功保存至: {path}"
    except Exception as e:
        return f"保存失败: {e}"

@tool
def read_local_news_csv():
    """读取本地存储的最新财经新闻 CSV 文件内容。无需参数。"""
    loader_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'loaders')
    if not os.path.exists(loader_dir):
        return "本地数据目录不存在。"
        
    files = [f for f in os.listdir(loader_dir) if f.startswith('财经精选_') and f.endswith('.csv')]
    if not files:
        return "没有找到新闻文件，请先运行抓取程序。"
    
    latest_file = os.path.join(loader_dir, sorted(files)[-1])
    df = pd.read_csv(latest_file)
    return df.head(10).to_string()

@tool
def fetch_analyst_rank(year: str = "2024"):
    """
    获取指定年份的东方财富分析师排名。
    此工具可以列出分析师的姓名、单位、指数、更新日期等。
    :param year: 年份，如 '2024', '2026' 等。默认为 '2024'。
    """
    df = Get_stock_analyst_rank_em(year=year)
    if isinstance(df, pd.DataFrame) and not df.empty:
        return df.to_string(index=False)
    return f"未能获取到 {year} 年的分析师排名。请确认该份是否为有效年份。"

@tool
def fetch_analyst_detail(analyst_id: str, analyst_name: str = "未知"):
    """
    获取指定东方财富分析师的个股跟踪详情（包括最新跟踪和历史跟踪）。
    :param analyst_id: 分析师 ID (从排名列表中获取)
    :param analyst_name: 分析师姓名（可选，用于输出提示）
    """
    # 注意：底层 Get_stock_analyst_detail_em 现在返回 (df, indicator)
    df, indicator = Get_stock_analyst_detail_em(analyst_id=analyst_id)
    if isinstance(df, pd.DataFrame) and not df.empty:
        return f"分析师 [{analyst_name}] ({indicator}) 的跟踪个股如下：\n{df.to_string(index=False)}"
    return f"未能获取到分析师 {analyst_name} (ID: {analyst_id}) 的详情。请确认 ID 是否正确。"

@tool
def batch_save_all_analysts_details(year: str = "2024", indicator: str = "最新跟踪成分股", limit: int = None):
    """
    【批量导出工具】批量保存东方财富分析师的详情数据到本地 CSV。
    :param year: 年份
    :param indicator: 详情类型，'最新跟踪成分股' 或 '历史跟踪成分股'
    :param limit: 限制抓取的人数（如果不设置，则抓取全部，建议初次测试设为 5-10）
    """
    run_batch_save_analysts(year=year, indicator=indicator, limit=limit)
    return f"已成功启动批量保存任务，正在处理 {year} 年 {indicator} 数据。请查看控制台日志或 loaders 目录下的 CSV 文件。"

@tool
def local_intensive_reading(content: str):
    """
    【强制性深度清洗工具】当抓取的新闻、公告、分析师详情等原始文本超过 200 字时，必须且只能调用此工具进行本地摘要分析。
    此工具集成了本地 Ollama (qwen3.5:9b) 的专业金融清洗模型，能从杂乱的原始数据中精准提取利好利空、股票名称和资金动向。
    严禁主模型（GPT）直接处理超过 200 字的原始数据，必须先由本工具进行预处理。
    :param content: 抓取到的长篇原始文本内容。
    """
    # 在工具内部实例化Ollama
    llm_ollama = get_ollama_llm()
    # 构造专门针对本地模型的指令
    prompt = f"""
    作为专业的金融数据分析员，请帮我分析对给你的信息进行清洗，并得出分析结果。
    信息会有主模型传递给你，你需要根据信息进行分析。
    最终反馈给主模型的内容要言简意赅。
    要求：
    - 提取核心利好/利空事件。
    - 识别所有提及的股票代码或名称。
    - 总结主力资金的动向（如有数据）。
    原始信息如下：
    {content[:8000]}  # 截取前8000字，防止本地显存溢出
    """
    try:
        summary = llm_ollama.invoke(prompt)
        return f"----本地模型（Ollama）深度分析报告-----\n{summary}"
    except Exception as e:
        return f"本地模型（Ollama）分析失败: {e}"

# 定义所有工具的列表，供 LangGraph 等框架调用
all_tools = [
    fetch_financial_news_highlights,
    fetch_risk_alert_stocks,
    fetch_cjzc_news,
    fetch_stock_kline,
    fetch_individual_stock_news,
    save_data_to_csv,
    read_local_news_csv,
    fetch_analyst_rank,
    fetch_analyst_detail,
    batch_save_all_analysts_details,
    local_intensive_reading
]
  
