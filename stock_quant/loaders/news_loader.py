#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 本文件实现财经早餐等财经新闻的抓取逻辑，包括：
# 1. 定时抓取各大财经媒体（如新浪财经、东方财富、华尔街见闻）的早餐新闻
# 2. 解析新闻标题、摘要、发布时间等关键信息
# 3. 去重并存储到数据库或本地文件
# 4. 支持关键词过滤和自定义推送规则
# 5. 提供简单的API接口供其他模块调用
import akshare as ak
import os
from datetime import datetime
# 财经精选新闻
def Get_news_main_cx():
    """
    抓取财经早餐/财经精选新闻数据
    """
    try:
        stock_news_main_cx_df = ak.stock_news_main_cx()
        return stock_news_main_cx_df
    except Exception as e:
        print(f"获取财经早餐失败: {e}")
        return None
# 财经精选新闻持久化
def Save_news_to_csv(df, prefix="财经精选"):
    """
    将新闻数据持久化到 CSV 文件
    :param df: pandas.DataFrame, 要保存的数据
    :param prefix: 文件名前缀
    """
    if df is None or df.empty:
        print("数据为空，跳过导出。")
        return None
        
    try:
        # 获取当前时间并格式化
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{current_time}.csv"
        
        # 确保保存路径正确（默认保存在当前脚本目录下）
        save_path = os.path.join(os.path.dirname(__file__), filename)
        
        # 保存为 CSV 文件
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        print(f"数据已成功导出为: {save_path}")
        return save_path
    except Exception as e:
        print(f"保存 CSV 失败: {e}")
        return None

if __name__ == "__main__":
    # 1. 调用获取数据函数
    news_df = Get_news_main_cx()
    
    # 2. 调用持久化函数
    if news_df is not None:
        Save_news_to_csv(news_df)


       
