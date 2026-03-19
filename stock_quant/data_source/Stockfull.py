import akshare as ak
import jsonlines

def get_stock_full_data():
    """
    获取A股市场总貌
    """
    stock_sse_summary_df = ak.stock_szse_area_summary()
    return stock_sse_summary_df

def write_stockdata_to_jsonl(data):
    """
    将股票数据写入 JSONL 文件
    """
    with jsonlines.open('stock_quant/data_source/stock_full_data.jsonl', 'w') as writer:
        writer.write_all(data)

if __name__ == "__main__":
    df = get_stock_full_data()
    write_stockdata_to_jsonl(df.to_dict(orient='records'))
    
