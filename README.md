# AI
AI瞎搞搞

## 环境配置

本项目需要一些系统级依赖（如 `build-essential`）来编译特定的 Python 模块（如 `akquant`）。

### 快速入门 (推荐)

如果你是第一次拉取代码或在新机器上运行，可以直接运行项目根目录下的 `setup.sh` 脚本。该脚本会自动处理：
1. 安装系统编译工具 (`build-essential`)
2. 安装 Rust 环境（使用国内镜像加速）
3. 创建虚拟环境并安装 Python 依赖

```bash
chmod +x setup.sh
./setup.sh
```

### 手动配置

1. **安装系统依赖**：
   ```bash
   sudo apt update
   sudo apt install -y build-essential
   ```

2. **配置 Python 环境**：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
“原生 SDK” 和 “LangChain 框架” 之间的关系：
openai.OpenAI：这是 OpenAI 官方提供的“毛坯房”工具（原生 SDK）。它直接和 API 通信，你要自己管理对话历史、自己解析返回的 JSON、自己处理复杂的逻辑。
ChatOpenAI (来自 LangChain)：这是基于原生 SDK 封装好的“精装修”框架。它把 OpenAI 的功能变成了 LangChain 体系里的一个“组件”，让你能更方便地实现“新闻抓取 -> 提取 -> 总结”这种多步骤的流水线。