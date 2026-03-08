from typing import TypedDict, Optional, Dict, List

class AgentState(TypedDict):
    user_query: str
    dataset_path: str

    problem_type: Optional[str]
    target_column: Optional[str]
    plan: Optional[List[str]]

    processed_data_path: Optional[str]
    model_metrics: Optional[Dict]
    best_model_path: Optional[str]

    error_trace: Optional[str]
    retry_count: int

    deployment_status: Optional[str]
    drift_detected: Optional[bool]