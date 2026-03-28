import akshare as ak
import os
import time
from datetime import datetime

def Get_stock_analyst_rank_em(year='2024'):
    """
    抓取股票分析师排名数据
    """
    try:
        stock_analyst_rank_em_df = ak.stock_analyst_rank_em(year=year)
        return stock_analyst_rank_em_df
    except Exception as e:
        print(f"获取 {year} 年股票分析师排名数据失败: {e}")
        return None

def save_analyst_rank_csv(year='2024'):
    """
    将股票分析师排名数据持久化到 CSV 文件
    """
    df = Get_stock_analyst_rank_em(year=year)
    if df is not None and not df.empty:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"股票分析师排名_{year}_{current_time}.csv"
        save_path = os.path.join(os.path.dirname(__file__), filename)
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        print(f"排名数据已成功导出为: {save_path}")
        return df
    return None

def Get_stock_analyst_detail_em(analyst_id, indicator="最新跟踪成分股"):
    """
    抓取单个股票分析师详情数据
    支持自动重试：如果 '最新跟踪成分股' 为空，则尝试抓取 '历史跟踪成分股'
    """
    indicators = [indicator]
    if indicator == "最新跟踪成分股":
        indicators.append("历史跟踪成分股")
    elif indicator == "历史跟踪成分股":
        indicators.insert(0, "最新跟踪成分股")

    for ind in indicators:
        try:
            df = ak.stock_analyst_detail_em(analyst_id=analyst_id, indicator=ind)
            if df is not None and not df.empty:
                return df, ind
        except TypeError as te:
            # akshare 内部在处理空数据时可能会抛出 'NoneType' object is not subscriptable
            continue
        except Exception as e:
            print(f"获取分析师 {analyst_id} 详情 ({ind}) 遇到错误: {e}")
            continue
    
    return None, indicator

def save_analyst_detail_csv(analyst_id, analyst_name="未知", indicator="最新跟踪成分股"):
    """
    将单个股票分析师详情数据持久化到 CSV 文件
    """
    df, final_indicator = Get_stock_analyst_detail_em(analyst_id=analyst_id, indicator=indicator)
    if df is not None and not df.empty:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 如果最终使用的 indicator 与请求的不一致，在文件名中体现
        filename = f"分析师详情_{analyst_name}_{analyst_id}_{final_indicator}_{current_time}.csv"
        save_path = os.path.join(os.path.dirname(__file__), filename)
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        if final_indicator != indicator:
            print(f"已导出分析师 [{analyst_name}] 的详情数据 (注: '{indicator}' 为空，自动切换至 '{final_indicator}')。")
        else:
            print(f"已导出分析师 [{analyst_name}] 的详情数据。")
        return True
    
    print(f"分析师 [{analyst_name}] (ID: {analyst_id}) 无有效数据 (已尝试所有指标)。")
    return False

def batch_save_all_analysts_details(year='2024', indicator="最新跟踪成分股", limit=None):
    """
    【新增方法】循环遍历排名列表，批量持久化所有分析师的详情数据
    :param year: 排名年份
    :param indicator: 详情类型
    :param limit: 限制抓取的人数（如果不设置，则抓取全部，建议初次测试设为 5-10）
    """
    print(f"--- 开始批量抓取 {year} 年分析师详情 ({indicator}) ---")
    
    # 1. 先拿到分析师排名列表
    rank_df = Get_stock_analyst_rank_em(year=year)
    if rank_df is None or rank_df.empty:
        print("未获取到排名列表，无法进行批量抓取。")
        return

    # 2. 确定抓取范围
    if limit:
        rank_df = rank_df.head(limit)
    
    total = len(rank_df)
    success_count = 0

    # 3. 循环遍历并保存
    for index, row in rank_df.iterrows():
        a_id = row['分析师ID']
        a_name = row['分析师名称']
        
        print(f"[{index + 1}/{total}] 正在处理分析师: {a_name} (ID: {a_id})...")
        
        if save_analyst_detail_csv(analyst_id=a_id, analyst_name=a_name, indicator=indicator):
            success_count += 1
        
        # 频率控制：避免请求过快被封
        time.sleep(0.5)

    print(f"--- 批量抓取结束！成功: {success_count}, 失败: {total - success_count} ---")

if __name__ == "__main__":
    # 示例：批量抓取 2024 年排名前 5 的分析师详情
    batch_save_all_analysts_details(year='2026', limit=5)
