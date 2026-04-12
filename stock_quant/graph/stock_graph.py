from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import ToolMessage
from graph.state import AgentState
from tools.stock_tools import all_tools
from llm_model import llm, ollama_llm
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

# 1. 定义工具节点
tools_node = ToolNode(tools=all_tools)

# 2. 定义摘要节点（强制调用本地 Ollama）
def summary_node(state: AgentState):
    # 找到最后一条工具消息（即抓取到的原始数据）
    last_tool_message = [m for m in state["messages"] if isinstance(m, ToolMessage)][-1]
    raw_content = last_tool_message.content
    
    print(f"\n[Summary Node]: 正在处理原始数据 (长度: {len(raw_content)})")
    
    # 优化 Prompt：要求本地模型保留每条新闻的关键点，而不是简单总结成几句话
    prompt = f"""
    作为专业的金融数据清洗专家，请对以下原始股票/财经信息进行精炼。
    你的任务是：去除无用的 HTML 标签、推广信息和重复内容，保留每条新闻的核心事实。
    要求输出格式：
    1. 【利好/利空摘要】：简述整体市场情绪。
    2. 【核心个股/板块】：列出所有被提及的股票名称和代码。
    3. 【精炼事实列表】：按条列出最重要的 5-10 条新闻/公告详情，保留具体数字和事件。
    
    请确保信息量足够主模型进行深度分析，不要过度压缩。
    
    原始信息如下：
    {raw_content[:8000]}
    """
    
    try:
        summary = ollama_llm.invoke(prompt)
        print(f"[Summary Node]: 本地模型处理完成 (摘要长度: {len(summary)})")
    except Exception as e:
        summary = f"本地模型（Ollama）处理遇到错误: {e}"
        print(f"[Summary Node]: 错误: {e}")
    
    # 使用相同的 id 来替换原有的 ToolMessage，保持协议合法
    return {"messages": [ToolMessage(
        id=last_tool_message.id,
        content=f"----本地模型（Ollama）深度分析报告-----\n{summary}",
        tool_call_id=last_tool_message.tool_call_id
    )]}

# 3. 自定义路由逻辑：判断工具返回内容是否需要摘要
def should_summarize(state: AgentState):
    last_message = state["messages"][-1]
    if isinstance(last_message, ToolMessage):
        # 提高阈值，只有真正冗长的内容（如新闻列表、详细财报）才去摘要
        if len(last_message.content) > 500: 
            print(f"\n[Router]: 检测到长文本 ({len(last_message.content)} 字)，正在分流至 Summary 节点...")
            return "summary"
    return "agent"

# 4. Agent 节点
def agent_node(state: AgentState):
    # --- 核心修复：消息清洗逻辑 ---
    # OpenAI 协议极其严格：AIMessage(tool_calls) 后面必须紧跟 ToolMessage，且 ID 必须对应。
    # 我们之前的流程中，summary 节点产生的新消息会破坏这个序列。
    msgs = state["messages"]
    clean_messages = []
    tool_call_to_msg = {}

    # 1. 遍历所有消息，记录每个 tool_call_id 对应的【最后一条】ToolMessage
    # 这样如果有摘要，摘要后的 ToolMessage 会覆盖原始的长文本 ToolMessage
    for m in msgs:
        if isinstance(m, ToolMessage):
            tool_call_to_msg[m.tool_call_id] = m

    # 2. 重新构建发送给云端的消息列表
    for m in msgs:
        if isinstance(m, ToolMessage):
            # 只保留该 tool_call_id 的最终版本
            if m is tool_call_to_msg[m.tool_call_id]:
                clean_messages.append(m)
            continue
        clean_messages.append(m)
    
    # --- 正常推理逻辑 ---
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个专业的股票分析助手。
        你可以使用提供的工具查询财经新闻、个股 K 线、分析师排名等信息。
        如果获取到的原始数据过长，系统会自动触发本地 Ollama 模型进行摘要（你会看到以 '----本地模型（Ollama）深度分析报告-----' 开头的消息）。
        请基于这些数据（尤其是摘要报告）为用户提供专业的金融建议。"""),
        MessagesPlaceholder(variable_name="messages"),
    ])
    model = llm.bind_tools(all_tools)
    # 使用清洗后的合法消息序列调用云端模型
    response = model.invoke(prompt.invoke({"messages": clean_messages}))
    return {"messages": [response]}

# 5. 构建图
graph_builder = StateGraph(AgentState)

graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tools_node)
graph_builder.add_node("summary", summary_node) # 新增摘要节点

graph_builder.add_edge(START, "agent")

# 条件边：Agent 决定是否调用工具
graph_builder.add_conditional_edges(
    "agent", 
    tools_condition, 
    {"tools": "tools", END: END}
)

# 条件边：工具执行完后，判断是否需要去摘要
graph_builder.add_conditional_edges(
    "tools",
    should_summarize,
    {"summary": "summary", "agent": "agent"}
)

# 摘要完后，回到 Agent 总结结果
graph_builder.add_edge("summary", "agent")

# 6. 编译并持久化
conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)
stock_graph = graph_builder.compile(checkpointer=memory)
"""
当你调用 .compile() 时，LangGraph 会把你画好的图“封包”，并生成一个 CompiledGraph 对象。这个对象 天生自带 了几个核心方法：
- .invoke() ：一次性运行到底，直接给你最终结果（像发邮件）。
- .stream() ：流式运行，每经过一个节点就给你发一个通知（像看物流直播）。
"""