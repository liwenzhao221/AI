#! /usr/bin/env python3
import akshare as ak

def GetStock_Kline(symbol, period="daily", start_date=None, end_date=None, adjust="qfq"):
    """
    获取股票K线数据
    :param symbol: 股票代码
    :param period: 时间周期, 可选值为 "daily", "weekly", "monthly"
    :param start_date: 开始日期, 格式为 "YYYYMMDD"
    :param end_date: 结束日期, 格式为 "YYYYMMDD"
    :param adjust: 复权类型, 默认 "qfq" (前复权)
    :return: 股票K线数据
    """
    import datetime
    
    # 如果没传时间，默认今天
    today = datetime.datetime.now().strftime("%Y%m%d")
    if not start_date:
        start_date = today
    if not end_date:
        end_date = today

    try:
        # 使用正确的接口：stock_zh_a_hist
        df = ak.stock_zh_a_hist(
            symbol=symbol, 
            period=period, 
            start_date=start_date, 
            end_date=end_date,
            adjust=adjust
        )
        return df
    except Exception as e:
        print(f"获取 K 线数据失败: {e}")
        return None



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

