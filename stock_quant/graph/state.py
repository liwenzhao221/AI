from typing import Annotated, TypedDict, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]   # 对话历史
    stock_code: Optional[str]          # 当前关注的股票
    start_date: Optional[str]
    end_date: Optional[str]
    data: Optional[dict]               # 加载的K线/财务数据
    factors: Optional[dict]            # 计算后的因子结果
    backtest_results: Optional[dict]   # 回测结果
    analysis_report: Optional[str]     # 生成的报告