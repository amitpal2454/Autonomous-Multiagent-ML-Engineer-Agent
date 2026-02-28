from agents.planner_agent import planner_agent
from agents.data_agent import data_agent
from agents.feature_agent import feature_agent
from agents.ml_engineer_agent import ml_engineer_agent
from agents.evaluation_agent import evaluation_agent
from agents.deployment_agent import deployment_agent
from agents.debug_agent import debug_agent
from utils.logger import logger
from model.state_models import MLSystemState


def run_agent_pipeline(state: MLSystemState) -> MLSystemState:
    logger.info("Starting agent orchestration")

    state_dict = state.dict()

    state_dict.update(planner_agent(state_dict))
    state_dict.update(data_agent(state_dict))
    state_dict.update(feature_agent(state_dict))

    # Retry loop (basic orchestration logic)
    while state_dict.get("error_trace") and state_dict["retry_count"] < 3:
        logger.warning("Error detected. Running debug agent.")
        state_dict["retry_count"] += 1
        state_dict.update(debug_agent(state_dict))

    state_dict.update(ml_engineer_agent(state_dict))
    state_dict.update(evaluation_agent(state_dict))
    state_dict.update(deployment_agent(state_dict))

    logger.info("Agent orchestration completed")

    return MLSystemState(**state_dict)