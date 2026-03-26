import akshare as ak
import time

def Tool_Stock_Info_Cjzc_Em(max_retries=3, delay=2):
    """
    获取股票信息，并带有重试机制
    :param max_retries: 最大重试次数
    :param delay: 每次重试之间的等待时间（秒）
    """
    for attempt in range(max_retries):
        try:
            stock_info_cjzc_em_df = ak.stock_info_cjzc_em()
            return stock_info_cjzc_em_df
        except Exception as e:
            print(f"第 {attempt + 1} 次尝试获取股票信息失败: {e}")
            if attempt < max_retries - 1:
                print(f"正在等待 {delay} 秒后重试...")
                time.sleep(delay)
            else:
                print("已达到最大重试次数，获取数据失败。")
                return f"获取股票信息失败: {e}"

if __name__ == "__main__":
    df = Tool_Stock_Info_Cjzc_Em()
    if not isinstance(df, str):
        print(df)
    else:
        print(df)
