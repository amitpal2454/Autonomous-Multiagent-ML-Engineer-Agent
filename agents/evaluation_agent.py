from config.setting import setting

def evaluation_agent(state):
    metrics = state.get("model_metrics")

    if not metrics:
        return {}

    score = metrics.get("r2_score", 0)

    if score >= 0.75:
        return {"deployment_status": "approved"}
    else:
        return {"deployment_status": "rejected"}