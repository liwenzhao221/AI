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
    headers['Referer'] = 'https://quote.eastmoney.com/'

    # 3.关键：必须三回去，把修改后的headers放回去
    kwargs['headers'] = headers

    # 4. 调用原始的requests.get方法
    return original_get(*args, **kwargs)

# 替换全局requests.get方法
requests.get = patched_get

# 个股行情测试
def GetStock_Kline(symbol):
    """
    获取股票K线数据
    :param symbol: 股票代码
    :type symbol: str
    :return: 股票K线数据
    :rtype: pandas.DataFrame
    """
    max_retries = 3
    for i in range(max_retries):
        try:
            # 获取当日行情
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol, period="daily", start_date="20260310", end_date='20260323', adjust="qfq")
            
            # 只要请求成功（不抛异常），我们就认为这次尝试完成了
            if stock_zh_a_hist_df is not None:
                if not stock_zh_a_hist_df.empty:
                    print(f'成功获取 {symbol} 股票数据:')
                    pprint(stock_zh_a_hist_df)
                else:
                    print(f'{symbol} 暂无数据')
                return  # 成功获取（哪怕数据为空）就直接结束函数，不需要再 retry
                
        except Exception as e:
            # 只有发生异常（如网络被封）才重试
            wait_retry = (i + 1) * 2  # 每次重试等待时间递增
            print(f"第 {i+1} 次获取 {symbol} 数据失败: {e}，{wait_retry}秒后重试...")
            time.sleep(wait_retry)


# GetStock_News("002436")
if __name__ == "__main__":
    # 开始检测
    print('开始监控行情，已开启Headers伪装模式')
    while True:
        GetStock_Kline("002436")
        # 时间变得随机一些
        sleep_time = random.uniform(5, 10)
        print(f'预计休息{sleep_time:.2f}秒')
        time.sleep(sleep_time)# 5-10秒
