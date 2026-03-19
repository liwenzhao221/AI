import akshare as ak
import jsonlines

def get_stock_full_data():
    """
    获取A股市场总貌
    描述: 上海证券交易所-股票数据总貌

    限量: 单次返回最近交易日的股票数据总貌(当前交易日的数据需要交易所收盘后统计)
    """
    stock_sse_summary_df = ak.stock_szse_area_summary()
    print(stock_sse_summary_df)
    return stock_sse_summary_df

def write_stockdata_to_jsonl(data):
    """
    将股票全貌数据写入 JSONL 文件
    """
    with jsonlines.open('stock_quant/data_source/stock_full_data.jsonl', 'w') as writer:
        writer.write_all(data)

def StockSzseSummary(date):
    """
    获取指定日期的股票数据总貌
    目前只到2.28
    """
    stock_sse_summary_df = ak.stock_szse_area_summary(date=date)
    print(stock_sse_summary_df)
    return stock_sse_summary_df
def StockSzseSectorSummary(symbol, date):
    """
    描述: 深圳证券交易所-统计资料-股票行业成交数据
    限量: 单次返回指定 symbol 和 date 的统计资料-股票行业成交数据
    :param symbol: choice of {"当月", "当年"}
    :type symbol: str
    :param date: 交易年月
    :type date: str
    :return: 股票行业成交数据
    :rtype: pandas.DataFrame
    """
    stock_szse_sector_summary_df = ak.stock_szse_sector_summary(symbol=symbol, date=date)
    print(stock_szse_sector_summary_df)
    return stock_szse_sector_summary_df

def StockIndividualInfoEm(symbol):
    """
    描述: 东方财富-个股-股票信息
    限量: 单次返回指定 symbol 的个股信息
    """
    stock_individual_info_em_df = ak.stock_individual_info_em(symbol=symbol)    
    print(stock_individual_info_em_df)
    return stock_individual_info_em_df

def StockIndividualBasicInfoXQ(symbol):
    """
    描述: 雪球财经-个股-公司概况-公司简介
    限量: 单次返回指定 symbol 的个股信息
    限定科创版
    """
    stock_individual_basic_info_xq_df = ak.stock_individual_basic_info_xq(symbol=symbol)
    print(stock_individual_basic_info_xq_df)
    return stock_individual_basic_info_xq_df

if __name__ == "__main__":
    # df = get_stock_full_data()
    # write_stockdata_to_jsonl(df.to_dict(orient='records'))
    # StockSzseSummary("20260301")
    # StockSzseSectorSummary("当月", "202602")
    # StockIndividualInfoEm("002436")
    StockIndividualBasicInfoXQ("SH920010")