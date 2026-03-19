import akshare as ak
import pandas as pd

def get_stock_data(symbol="000001"):
    """
    获取股票数据
    """
    df = ak.stock_zh_a_hist(symbol=symbol, period="daily")
    return df

def analyze_trend(df):
    """
    分析股票趋势
    """
    latest_close = df['收盘'].iloc[-1]
    prev_close = df['收盘'].iloc[-2]

    if latest_close > prev_close:
        return "上升"
    else:
        return "下降"

if __name__ == "__main__":
    df = get_stock_data()
    print(df)
