import json
from core.azure_llm import call_llm
from utils.logger import logger


def planner_agent(state):
    logger.info("Planner Agent Started")

    prompt = f"""
    User request: {state["user_query"]}

    Return JSON:
    {{
      "problem_type": "regression or classification",
      "target_column": "column_name",
      "high_level_plan": ["step1", "step2"]
    }}
    """

    response = call_llm(prompt)

    try:
        parsed = json.loads(response)
        logger.info(f"Planner Output: {parsed}")
    except Exception as e:
        logger.error(f"Planner JSON parsing failed: {e}")
        parsed = {}

    return {
        "problem_type": parsed.get("problem_type"),
        "target_column": parsed.get("target_column"),
        "plan": parsed.get("high_level_plan"),
    }