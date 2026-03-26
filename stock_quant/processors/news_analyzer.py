from news_loader import load_news
from llm_model import process_with_llm
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 导入必要的模块
from langchain.tools import tool
import pandas as pd
import os

@tool
def read_local_news_csv():
    """读取本地存储的最新财经新闻 CSV 文件内容。"""
    # 这里逻辑：找当前目录下最新的那个 CSV
    files = [f for f in os.listdir('.') if f.startswith('财经精选_') and f.endswith('.csv')]
    if not files:
        return "没有找到新闻文件，请先运行抓取程序。"
    
    latest_file = sorted(files)[-1]
    df = pd.read_csv(latest_file)
    return df.head(10).to_string() # 返回前10条给 AI 读

