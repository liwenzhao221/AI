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

llm = get_llm()
# response = llm.invoke("你好，请自我介绍")
# print(response.content)