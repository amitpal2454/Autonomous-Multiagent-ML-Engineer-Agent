from core.azure_llm import call_llm
from tools.python_executor import execute_python
from utils.logger import logger


def feature_agent(state):
    logger.info("Feature Agent Started")

    prompt = f"""
    Dataset path: {state["dataset_path"]}
    Target column: {state["target_column"]}

    Write Python code to:
    - Handle missing values
    - Encode categorical features
    - Save processed dataset to data/processed.csv

    Return ONLY Python code.
    """

    code = call_llm(prompt, temperature=0.1)

    result = execute_python(code)

    if result["success"]:
        logger.info("Feature engineering successful")
        return {
            "processed_data_path": "data/processed.csv",
            "error_trace": None
        }
    else:
        logger.error("Feature engineering failed")
        return {
            "error_trace": result["traceback"]
        }