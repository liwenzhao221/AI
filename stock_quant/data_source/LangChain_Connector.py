import asyncio
from langchain_community.llms import Ollama
from langchain_classic.agents import initialize_agent, Tool, AgentType
from langchain_core.prompts import PromptTemplate
from GetStock_Infomation import get_formatted_stock_news
from Requests_Agent import fetch_finance_data
import json

# 1.初始化本地模型
llm = Ollama(model='qwen3.5:9b')

# 2.定义工具集（Tools）
def tool_get_news_list(input_str):
    """
    当需要查询某只股票最新的新闻链接时调用此工具
    :param input_str: 股票代码，例如 '002436'
    """
    # 核心修复：处理模型可能传入的 JSON 字符串
    symbol = input_str
    if isinstance(input_str, str) and "{" in input_str:
        try:
            data = json.loads(input_str)
            symbol = data.get("symbol", data.get("input", input_str))
        except:
            pass
    
    # 清理可能存在的引号
    symbol = str(symbol).strip().strip("'").strip('"')
    
    # 调用之前的函数获取股票新闻
    news_json = get_formatted_stock_news(symbol)
    return news_json

# 目前还没有加入csv功能，测试通过了，后期增加
def tool_scrape_financial_csv(input_str):
    """
    当已经有了新闻链接，需要抓取具体内容详细正文和表格之类数据时使用
    :param input_str: 目标网页URL
    """
    # 核心修复：处理模型可能传入的 JSON 字符串
    url = input_str
    if isinstance(input_str, str) and "{" in input_str:
        try:
            data = json.loads(input_str)
            url = data.get("url", data.get("input", input_str))
        except:
            pass
    
    # 清理可能存在的引号
    url = str(url).strip().strip("'").strip('"')

    # 因为爬虫是async，这里用run_until_complete桥接
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        content, tables = loop.run_until_complete(fetch_finance_data(url))
        
        if content is None:
            return "抓取失败：未能提取到内容，请检查链接是否正确。"
            
        # 将表格转换成字符串给模型看（只取前500文字正文和表格浏览）
        table_str = tables[0].head(10).to_string() if tables else "未发现表格"
        return f"正文摘要：{content[:300]}\n表格数据：\n{table_str}"
    except Exception as e:
        return f"抓取过程中发生错误: {e}"
# 3.封装LangChain识别的Tool对象
tools = [
    Tool(
        name="Get_News_List",
        func=tool_get_news_list,
        description="当需要查询某只股票最新的新闻链接时使用。请输入纯数字股票代码，如 '002436'。"
    ),
    Tool(
        name="Scrape_Financial_CSV",
        func=tool_scrape_financial_csv,
        description="当已经有了新闻链接，需要抓取具体内容详细正文和表格之类数据时使用。请输入完整的 URL。"
    )
]
# 4.初始化Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,# 这里开启后可以看到模型思考的过程，有用切精彩
    handle_parsing_errors=True
)

if __name__ == "__main__":
    # 测试用例
    test_symbol = "600644"
    test_url = "http://finance.eastmoney.com/a/202603133671786886.html"
    
    # 测试获取新闻列表
    news_list = agent.run(f"请获取{test_symbol}的最新新闻链接，并结合得出结果，帮我做一个分析，记得要把股票代码对应的名称也附上")
    print(news_list)
    
    # # 测试抓取财务数据
    # financial_data = agent.run(f"请抓取{test_url}的财务数据")
    # print(financial_data)