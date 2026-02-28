from typing import TypedDict,List,Optional,Dict

class MLSystemState(TypedDict):
    user_query: str
    dataset_path: str

    problem_type: Optional[str]
    target_column: Optional[str]
    plan:Optional[str]

    processsed_data_path:Optional[str]
    model_metrics: Optional[str]
    best_model_path: Optional[str]

    error_trace: Optional[str]
    retry_count:int
    
    deployement_status:Optional[str]
    drift_Detected:Optional[str]
    