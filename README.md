# 🚀 Stock_AI: 智能股票深度分析系统

基于 LangChain + Ollama/OpenAI 的自动化股票数据分析平台，集成了财经新闻抓取、分析师排名跟踪、个股 K 线分析等功能。

## 🌟 核心功能

- **📰 宏观新闻监控**：实时抓取财经早餐、成交早餐等宏观经济资讯。
- **📊 分析师深度洞察**：支持获取东方财富分析师排名、个股跟踪详情，并支持批量导出 CSV 数据。
- **📈 个股 K 线分析**：支持日线、周线、月线历史数据查询，支持前复权、后复权调整。
- **⚠️ 风险警示监控**：实时监控 A 股市场 ST 和 *ST 风险警示股票动态。
- **🤖 智能 Agent 对话**：基于 LangChain 架构，支持通过自然语言直接进行复杂的数据查询与深度分析。
- **💾 数据持久化**：所有抓取的数据均支持自动保存为 CSV 格式，方便后续复盘。

## 📂 项目结构

```text
Stock_AI/
├── loaders/            # 数据加载层 (Loaders): 负责与底层数据源交互 (akshare, etc.)
├── tools/              # 工具定义层 (Tools): 将数据加载功能封装为 AI 可调用的工具
├── processors/         # 数据处理层 (Processors): 负责数据清洗与深度分析逻辑
├── data_source/        # (旧) 原始脚本目录
├── venv/               # Python 虚拟环境
├── main.py             # 系统入口: 初始化 AI Agent 并启动交互式对话
├── setup.sh            # 自动化环境配置脚本
└── requirements.txt    # 项目依赖清单
```

## 🛠️ 环境配置

本项目需要一些系统级依赖（如 `build-essential`）以及特定的 Python 环境。

### 快速入门 (推荐)

如果你是第一次拉取代码或在新机器上运行，直接运行根目录下的 `setup.sh`：

```bash
chmod +x setup.sh
./setup.sh
```

该脚本会自动完成：
1. 安装系统编译工具 (`build-essential`)。
2. 配置 Rust 环境（使用国内镜像加速）。
3. 创建虚拟环境并安装所有 Python 依赖。

### 手动配置

1. **系统依赖**：
   ```bash
   sudo apt update && sudo apt install -y build-essential
   ```

2. **Python 环境**：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## 🚀 运行系统

激活虚拟环境后，直接运行主程序：

```bash
python3 stock_quant/main.py
```

## 💡 开发提示

- **AI 模型配置**：在 `stock_quant/llm_model.py` 中配置你的 API Key 或本地 Ollama 模型名称。
- **新增功能**：如需增加新工具，请在 `loaders/` 中编写数据加载逻辑，并在 `tools/stock_tools.py` 中注册工具装饰器。

---
*注：本项目仅供学习与研究使用，不构成任何投资建议。*