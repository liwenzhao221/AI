import akshare as ak
import json

# 获取并格式化个股新闻为 LLM 友好的 JSON 格式
def get_formatted_stock_news(symbol, top_n=10):
    """
    直接获取股票新闻并返回格式化后的 JSON 字符串
    :param symbol: 股票代码
    :param top_n: 获取最新的新闻条数，默认 10 条
    """
    try:
        # 1. 获取原始数据
        df = ak.stock_news_em(symbol)
        if df is None or df.empty:
            return "[]"        
        # 2. 选取关键字段并限制数量
        # 字段: 关键词, 新闻标题, 文章来源, 新闻链接
        llm_data = df.head(top_n)[['关键词', '新闻标题', '文章来源', '新闻链接']].to_dict(orient='records')       
        # 3. 转换为 JSON 字符串
        formatted_json = json.dumps(llm_data, ensure_ascii=False, indent=2)        
        print(f"--- {symbol} 股票新闻 (LLM 友好格式) ---")
        print(formatted_json)
        return formatted_json       
    except Exception as e:
        print(f'获取或处理 {symbol} 新闻失败: {e}')
        return "[]"

def Get_Stock_Info(symbol):
    """
    获取股票的基本信息
    :param symbol: 股票代码
    """
    try:
        stock_individual_info_em_df = ak.stock_individual_info_em(symbol=symbol)
        print(stock_individual_info_em_df)
        return stock_individual_info_em_df
    except Exception as e:
        print(f'获取或处理 {symbol} 股票基本信息失败: {e}')
        return "[]"
if __name__ == "__main__":
    #get_formatted_stock_news("600644")
    Get_Stock_Info("600644")
