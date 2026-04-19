import akshare as ak
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd


def CollectStock_Kline(symbol, start_date, end_date, adjust):
    """
    收集股票K线数据
    """
    try:
        # 获取股票列表,<class 'pandas.core.frame.DataFrame'>
        stock_list = ak.stock_zh_a_hist_tx(symbol, start_date, end_date, adjust)
        return stock_list
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        return None


def Save_To_SQLite(stock_list, db_path):
    """
    使用 SQLAlchemy 保存股票K线数据到SQLite数据库
    :param stock_list: 股票K线数据 (DataFrame)
    :param db_path: 数据库路径
    """
    if stock_list is None or stock_list.empty:
        print("数据为空，跳过保存")
        return

    try:
        # 创建数据库引擎
        engine = create_engine(f'sqlite:///{db_path}')
        
        # 使用 pandas 的 to_sql 方法，效率更高且代码简洁
        # if_exists='append' 表示追加数据，'replace' 表示覆盖
        stock_list.to_sql('stock_kline', con=engine, if_exists='append', index=False)
        print(f"成功将 {len(stock_list)} 条数据保存至 {db_path}")

    except Exception as e:
        print(f"保存股票K线数据失败: {e}")


if __name__ == "__main__":
    # 定义保存路径
    db_file = Path(__file__).parent.parent / "data" / "stock_data.db"
    db_file.parent.mkdir(parents=True, exist_ok=True)

    # 1. 获取数据
    symbol = 'sz002436'
    df = CollectStock_Kline(symbol, '20240401', '20240414', 'qfq')

    # 2. 保存数据
    if isinstance(df, pd.DataFrame):
        Save_To_SQLite(df, db_file)
    else:
        print("获取到的数据不是有效的 DataFrame")