from langchain_community.llms import Ollama

llm = Ollama(model='qwen3.5:9b')
print(llm.invoke("你好"))