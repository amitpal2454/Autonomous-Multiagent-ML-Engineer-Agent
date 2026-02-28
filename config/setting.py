from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    llama_model:str="mistral"
    coder_model:str="deepseek-coder"
    temperature_planner:float=0.2
    temperature_coder:float=0.1
    performance_threshold:float=0.75
    max_retries:int=3

setting=Setting()