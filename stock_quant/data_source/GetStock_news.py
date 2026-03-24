import akshare as ak
import json


def Get_News_Stock(symbol):
    try:
        stock_news_em_df = ak.stock_news_em(symbol)
        #print(stock_news_em_df)
        return stock_news_em_df
    except Exception as e:
        print(f'获取{symbol}新闻失败: {e}')
        return None


def format_news_for_llm(df):
    """
    将新闻数据处理为更适合大语言模型 (LLM) 消费的 JSON 格式
    """
    if df is None or df.empty:
        return "[]"
    
    # 选取关键字段，并转换为字典列表 (JSON)
    # 字段说明: 关键词, 新闻标题, 新闻内容, 发布时间, 文章来源, 新闻链接
    llm_data = df[['关键词', '新闻标题', '文章来源', '新闻链接']].to_dict(orient='records')
    
    # 返回不带转义的 JSON 字符串，方便大模型定位
    return json.dumps(llm_data, ensure_ascii=False, indent=2)


def Res_News_Stock(symbol):
    try:
        stock_news_em_df = Get_News_Stock(symbol)
        if stock_news_em_df is not None:
            # 使用更适合大模型的格式输出
            llm_friendly_news = format_news_for_llm(stock_news_em_df)
            print(f"--- {symbol} 股票新闻 (LLM 友好格式) ---")
            print(llm_friendly_news)
            return llm_friendly_news
    except Exception as e:
        print(f'处理{symbol}新闻失败: {e}')
        return None

if __name__ == "__main__":
    Res_News_Stock("002436")
