import akshare as ak
import pandas as pd

def debug_analyst(a_id, a_name):
    indicators = ["最新跟踪成分股", "历史跟踪成分股", "指数表现", "行业贡献", "个股贡献"]
    print(f"\n=== 正在调试分析师: {a_name} (ID: {a_id}) ===")
    
    for ind in indicators:
        try:
            print(f"尝试指标 '{ind}': ", end="")
            df = ak.stock_analyst_detail_em(analyst_id=a_id, indicator=ind)
            if df is not None and not df.empty:
                print(f"成功! 拿到 {len(df)} 条数据")
            else:
                print("失败 (数据为空)")
        except Exception as e:
            print(f"报错: {e}")

# 调试刚才失败的两个 ID
debug_analyst("11000445536", "滕明滔")
debug_analyst("11000279133", "韩东")
