from core.azure_llm import call_llm
from tools.python_executor import execute_python
from utils.logger import logger


def debug_agent(state):
    error = state.get("error_trace")

    if not error:
        return {}

    logger.warning("Debug Agent Triggered")

    prompt = f"""
    The following error occurred in an ML pipeline:

    {error}

    Provide corrected Python code only.
    """

    corrected_code = call_llm(prompt, temperature=0.1)

    result = execute_python(corrected_code)

    if result["success"]:
        logger.info("Debug successful")
        return {"error_trace": None}
    else:
        logger.error("Debug failed again")
        return {"error_trace": result["traceback"]}