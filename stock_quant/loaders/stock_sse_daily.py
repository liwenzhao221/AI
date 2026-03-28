#! /usr/bin/env python3
#! -*- coding: utf-8 -*-
# 历史行情东财数据
import akshare as ak
from datetime import datetime
import os

def Get_stock_zh_a_hist(symbol, period="daily", start_date=datetime.now().strftime("%Y%m%d"), end_date=datetime.now().strftime("%Y%m%d"), adjust="qfq"):
    """
    抓取股票日线数据
    """
    try:
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust)
        print(stock_zh_a_hist_df)
        return stock_zh_a_hist_df
    except Exception as e:
        print(f"获取股票日线数据失败: {e}")
        return None
def Save_stock_zh_a_hist_to_csv(df, prefix="股票日线"):
    """
    将股票日线数据持久化到 CSV 文件
    :param df: pandas.DataFrame, 要保存的数据
    :param prefix: 文件名前缀
    """
    if df is None or df.empty:
        print("数据为空，跳过导出。")
        return None
    else:
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
    stock_zh_a_hist_df = Get_stock_zh_a_hist(symbol="600869")
    
    # # 2. 调用持久化函数
    # if stock_zh_a_hist_df is not None:
    #     Save_stock_zh_a_hist_to_csv(stock_zh_a_hist_df)
    Save_stock_zh_a_hist_to_csv(stock_zh_a_hist_df, prefix="600869远东股份股票日线")
