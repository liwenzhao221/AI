#! /usr/bin/env python3
import akshare as ak

def GetStock_Kline(symbol="000001", period="daily", start_date="20200101", end_date="20230801"):
    """
    获取股票K线数据
    :param symbol: 股票代码
    :type symbol: str
    :param period: 时间周期, 可选值为 "daily", "weekly", "monthly"
    :type period: str
    :param start_date: 开始日期, 格式为 "YYYYMMDD"
    :type start_date: str
    :param end_date: 结束日期, 格式为 "YYYYMMDD"
    :type end_date: str
    :return: 股票K线数据
    :rtype: pandas.DataFrame
    """
    stock_za_a_spot_em_df = ak.stock_za_a_spot_em(
        symbol=symbol, period=period, start_date=start_date, end_date=end_date
    )
    print(stock_za_a_spot_em_df)
    return stock_za_a_spot_em_df



# 个股新闻测试
def GetStock_News(symbol):
    """
    获取股票新闻数据
    :param symbol: 股票代码
    :type symbol: str
    :return: 股票新闻数据
    :rtype: pandas.DataFrame
    """
    stock_news_em_df = ak.stock_news_em(symbol=symbol)
    print(stock_news_em_df)
    return stock_news_em_df

