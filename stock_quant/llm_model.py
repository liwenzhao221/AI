#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 本文件包含与LLM模型交互的函数，如调用API、处理模型输出等

from langchain_openai import ChatOpenAI  # pyright: ignore[reportUnusedImport]
import os

# 定义一个函数，用于获取LLM模型实例
def get_llm():
    return ChatOpenAI(
        model_name="gpt-4.1-free",
        temperature=0.7,
        max_tokens=2048,
        api_key="sk-i5lkQOkbqVkcDsKh01D8Ee84Ac85433fB57bD39d67B1C8A8",
        base_url="https://aihubmix.com/v1",
    )
from langchain_ollama import OllamaLLM  # 使用最新的 langchain_ollama 库支持 Ollama

# 定义一个函数，用于获取本地 Ollama 模型实例
def get_ollama_llm(model_name: str = "qwen3.5:9b"):
    """
    获取本地 Ollama 模型实例
    :param model_name: Ollama 模型名称，默认为 qwen3.5:9b
    :return: OllamaLLM 实例
    """
    return OllamaLLM(model=model_name, temperature=0.7, verbose=True)

# llm = get_llm()
# response = llm.invoke("你好，请自我介绍")
# print(response.content)

# if __name__ == "__main__":
#     llm_ollama = get_ollama_llm()
#     response = llm_ollama.invoke("为啥我用python调用你，感觉好慢才能得到回复呢")
#     print(response)