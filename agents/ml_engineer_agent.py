from utils.logger import logger
from tools.train_model import train_model


def ml_engineer_agent(state):
    logger.info("ML Engineer Agent Started")

    try:
        result = train_model(
            state["processed_data_path"],
            state["target_column"]
        )

        logger.info(f"Training Result: {result}")

        return {
            "model_metrics": {
                result["metric_name"]: result["metric_value"]
            },
            "best_model_path": result["model_path"],
            "error_trace": None
        }

    except Exception as e:
        logger.error(f"Training Failed: {str(e)}")
        return {
            "error_trace": str(e)
        }