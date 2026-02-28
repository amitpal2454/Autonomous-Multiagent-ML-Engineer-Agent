from pydantic import BaseModel
from typing import Optional, Dict, List


class AgentRequest(BaseModel):
    user_query: str
    dataset_path: str


class MLSystemState(BaseModel):
    user_query: str
    dataset_path: str

    problem_type: Optional[str] = None
    target_column: Optional[str] = None
    plan: Optional[List[str]] = None

    processed_data_path: Optional[str] = None
    model_metrics: Optional[Dict] = None
    best_model_path: Optional[str] = None

    error_trace: Optional[str] = None
    retry_count: int = 0

    deployment_status: Optional[str] = None
    drift_detected: Optional[bool] = None