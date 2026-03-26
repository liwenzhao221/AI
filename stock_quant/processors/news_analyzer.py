from news_loader import load_news
from llm_model import process_with_llm
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 导入必要的模块
def handle_news():
    # 加载新闻数据
    news_data = load_news()
    
    # 调用LLM模型处理新闻数据
    result = process_with_llm(news_data)
    
    # 返回处理结果
    return result

if __name__ == "__main__":
    # 主函数入口
    output = handle_news()
    print("处理完成：", output)

