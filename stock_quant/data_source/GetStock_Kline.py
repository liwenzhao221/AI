#! /usr/bin/env python3
import akshare as ak
import time
from pprint import pprint
import random
import requests

# 伪装环节：全局注入浏览器Headers
original_get = requests.get

def patched_get(*args, **kwargs):
    # 1.拿到原始参数里的headers，如果没有就新建一个空字典
    headers = kwargs.get('headers', {})

    # 2. 修改/增加 User-Agent
    headers['User-Agent'] = random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    ])

    # 3.关键：必须三回去，把修改后的headers放回去
    kwargs['headers'] = headers

    # 4. 调用原始的requests.get方法
    return original_get(*args, **kwargs)

# 替换全局requests.get方法
requests.get = patched_get

# 个股行情测试
def GetStock_Kline(symbol):
    """
    获取股票新闻数据
    :param symbol: 股票代码
    :type symbol: str
    :return: 股票新闻数据
    :rtype: pandas.DataFrame
    """
    max_retries = 3
    for i in range(max_retries):
        try:
            # 获取当日行情
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol, period="daily", start_date="20260323", end_date='20260323', adjust="qfq")
            if not stock_zh_a_hist_df.empty:
                print(f'成功{symbol}股票数据:')
                pprint(stock_zh_a_hist_df)
                break  # 如果成功，跳出循环
        except Exception as e:
            print(f"获取股票 {symbol} 新闻数据失败: {e}")


# GetStock_News("002436")
if __name__ == "__main__":
    # 开始检测
    print('开始监控行情，已开启Headers伪装模式')
    while True:
        GetStock_Kline("002436")
        # 时间变得随机一些
        sleep_time = random.uniform(5, 10)
        time.sleep(sleep_time)# 5-10秒
