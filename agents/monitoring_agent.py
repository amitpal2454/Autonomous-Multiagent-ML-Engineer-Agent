import random
from utils.logger import logger


def monitoring_agent(state):
    logger.info("Monitoring Agent Started")

    # Placeholder drift detection logic
    drift_detected = random.choice([False, False, True])  # simulate

    if drift_detected:
        logger.warning("Drift Detected")
        return {"drift_detected": True}
    else:
        logger.info("No Drift Detected")
        return {"drift_detected": False}