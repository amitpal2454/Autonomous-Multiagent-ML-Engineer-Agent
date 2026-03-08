from agents.planner_agent import planner_agent
from agents.data_agent import data_agent
from agents.feature_agent import feature_agent
from agents.ml_engineer_agent import ml_engineer_agent
from agents.evaluation_agent import evaluation_agent
from agents.deployment_agent import deployment_agent
from agents.debug_agent import debug_agent


def planner_node(state):
    state.update(planner_agent(state))
    return state


def data_node(state):
    state.update(data_agent(state))
    return state


def feature_node(state):
    state.update(feature_agent(state))
    return state


def ml_node(state):
    state.update(ml_engineer_agent(state))
    return state


def evaluation_node(state):
    state.update(evaluation_agent(state))
    return state


def deployment_node(state):
    state.update(deployment_agent(state))
    return state


def debug_node(state):
    state.update(debug_agent(state))
    state["retry_count"] += 1
    return state

from agents.monitoring_agent import monitoring_agent

def monitoring_node(state):
    state.update(monitoring_agent(state))
    return state


from utils.logger import logger


def supervisor_node(state):
    logger.info("Supervisor Checking State")

    if state.get("retry_count", 0) > 5:
        logger.error("Max retries exceeded")
        state["error_trace"] = "Max retries exceeded"
        return state

    return state