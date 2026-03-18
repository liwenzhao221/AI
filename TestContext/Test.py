import akshare as ak
import pandas as pd

def get_stock_data(symbol="000001"):
    """
    获取股票数据
    """
    df = ak.stock_zh_a_hist(symbol=symbol, period="daily")
    return df

if __name__ == "__main__":
    df = get_stock_data()
    print(df)
