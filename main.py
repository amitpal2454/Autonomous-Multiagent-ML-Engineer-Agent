from fastapi import FastAPI
from model.state_models import AgentRequest, MLSystemState
from orchestrator.run_pipeline import run_agent_pipeline
from utils.logger import logger
import uvicorn

app = FastAPI()





@app.post("/run-agent", response_model=MLSystemState)
async def run_agent(request: AgentRequest):
    logger.info("Received agent execution request")

    # Initialize structured state
    state = MLSystemState(
        user_query=request.user_query,
        dataset_path=request.dataset_path
    )

    final_state = run_agent_pipeline(state)

    logger.info("Agent execution completed")

    return final_state

if __name__ == "__main__":
    uvicorn.run(
        "main:app",          # file_name:fastapi_variable
        host="localhost",    # localhost
        port=8000,
        reload=False
    )