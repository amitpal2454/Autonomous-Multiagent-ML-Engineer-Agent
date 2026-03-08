from utils.logger import logger
from config.setting import setting


def evaluation_agent(state):
    logger.info("Evaluation Agent Started")

    metrics = state.get("model_metrics")

    if not metrics:
        return {}

    # dynamic metric
    metric_name = list(metrics.keys())[0]
    score = metrics[metric_name]

    logger.info(f"Evaluation Score: {score}")

    if score >= setting.performance_threshold:
        logger.info("Model Approved")
        return {"deployment_status": "approved"}
    else:
        logger.warning("Model Performance Below Threshold")
        return {"deployment_status": "improve"}