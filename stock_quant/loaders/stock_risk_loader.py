import akshare as ak
import jsonlines
import pandas as pd
import os
"""
它的主要作用是向投资者明确提示重大风险，让大家在交易这些股票时更加谨慎。
这些股票通常存在经营、财务或其他问题，投资风险较高。
交易所通过给股票简称前加“ST”或“*ST”标识、设置交易限制等方式，来警示普通投资者，避免盲目跟风炒作。
ST：其他风险警示（非退市风险），提示公司存在重大风险，但还不至于立即退市。
*ST：退市风险警示（也叫退市预警），表示公司已面临强制终止上市的风险，情况更严重，如果后续无法改善，很可能进入退市整理期甚至直接退市。
进入这个板的股票，还包括处于退市整理期的股票（交易所已决定终止上市，但还在最后交易阶段的）。
"""

# 设置 pandas 显示选项，以便在终端查看更多内容
# pd.set_option('display.max_rows', None)      # 显示所有行
# pd.set_option('display.max_columns', None)   # 显示所有列
# pd.set_option('display.width', 1000)         # 设置显示宽度，防止换行
# pd.set_option('display.unicode.ambiguous_as_wide', True) # 处理中文字符对齐
# pd.set_option('display.unicode.east_asian_width', True)   # 处理中文字符对齐

def write_stockdata_to_csv(df, filename='stock_data.csv'):
    """
    将 DataFrame 写入 CSV 文件
    """
    # 确保保存路径正确（默认保存在 data_source 目录下）
    path = os.path.join(os.path.dirname(__file__), filename)
    df.to_csv(path, index=False, encoding='utf-8-sig')
    print(f"数据已成功保存到: {path}")

# 东财风险警示板块
def GetStockRiskAlertBoard():
    """
    描述: 东方财富-风险警示板块
    限量: 单次返回所有风险警示板块
    """
    try:
        stock_zh_a_st_em_df = ak.stock_zh_a_st_em()
        #print(stock_zh_a_st_em_df)
        return stock_zh_a_st_em_df
    except Exception as e:
        print(f"获取风险警示板块失败: {e}")
        return f'获取风险警示百块失败：{e}'
# if __name__ == "__main__":
#     # 获取风险警示板块数据
#     risk_board_df = GetStockRiskAlertBoard()
#     print(type(risk_board_df))
#     if isinstance(risk_board_df, pd.DataFrame):
#         # 1. 在控制台打印（已通过 pd.set_option 设置显示全部内容）
#         print("--- 风险警示板块数据（全部显示） ---")
#         print(risk_board_df)
        
#         # 2. 保存到 CSV 文件
#         write_stockdata_to_csv(risk_board_df, f'risk_alert_board_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
#     else:
#         print(risk_board_df)
