from langchain_ollama import ChatOllama
from config.setting import setting

def get_planner_llm():
    return ChatOllama(model=setting.llama_model,
                      temperature=setting.temperature_planner)

def get_coder_llm():
    return ChatOllama(model=setting.coder_model,
                      temperature=setting.temperature_coder)