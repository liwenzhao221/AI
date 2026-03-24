import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import pandas as pd
from io import StringIO
import random
from datetime import datetime

async def fetch_finance_data(url):
    async with async_playwright() as p:
        # 1. 启动无头浏览器 (像真人一样打开网页)
        browser = await p.chromium.launch(headless=True)
        
        # 模拟真实的浏览器环境
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        # 注入 stealth 插件，隐藏 Playwright 特征
        stealth_config = Stealth()
        await stealth_config.apply_stealth_async(page)
        
        print(f"正在访问并渲染页面: {url}")
        try:
            # 策略调整: 
            # 1. 使用 'domcontentloaded' (只要 HTML 加载完就行，不用等广告和埋点脚本跑完)
            # 2. 设置一个更合理的超时时间 (60秒)
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # 针对东财这类动态加载的页面，稍微等一下主要内容渲染
            await page.wait_for_selector("#ContentBody", timeout=10000)
            
            # 2. 提取新闻正文 (针对东财 id='ContentBody')
            article_content = await page.inner_text("#ContentBody")
            
            # 3. 提取网页中的所有表格 (表格里往往藏着主力资金的财富密码)
            html_content = await page.content()
            tables = pd.read_html(StringIO(html_content))
            
            await browser.close()
            return article_content, tables
            
        except Exception as e:
            print(f"访问页面出错: {e}")
            await browser.close()
            return None, []

async def main():
    target_url = "https://finance.eastmoney.com/a/202603093666128049.html"
    content, tables = await fetch_finance_data(target_url)
    
    print("\n--- [1. 核心文字摘要] ---")
    print(content[:300] + "...") # 展示前300字
    
    print("\n--- [2. 发现的结构化数据表格] ---")
    for i, df in enumerate(tables):
        # 过滤掉太小的表格（通常是广告或导航）
        if len(df) > 5:
            print(f"\n表格 {i+1} 内容预览 (主力资金情况):")
            print(df.head(10)) # 打印前10行主力净流入数据
            df.to_csv(f"cpo_data{datetime.now().strftime('%Y%m%d')}-{i}.csv")

if __name__ == "__main__":
    asyncio.run(main())

