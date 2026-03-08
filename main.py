from graph.build_graph import build_graph
import uvicorn
from fastapi import FastAPI
from model.state_models import AgentRequest,DatasetSchema
from fastapi import UploadFile, File, Form
import pandas as pd
import os
import io
from fastapi import UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import traceback
app=FastAPI()

graph = build_graph()


@app.post("/run-agent")
async def run_agent(
    user_query: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        filename = file.filename
        extension = filename.split(".")[-1].lower()
        file_bytes = await file.read()

        # -----------------------------
        # Universal File Conversion
        # -----------------------------

        if extension == "csv":
            df = pd.read_csv(io.BytesIO(file_bytes))

        elif extension in ["xlsx", "xls"]:
            df = pd.read_excel(io.BytesIO(file_bytes))

        elif extension == "json":
            df = pd.read_json(io.BytesIO(file_bytes))

        elif extension == "txt":
            df = pd.read_csv(io.BytesIO(file_bytes), engine="python")

        elif extension == "parquet":
            df = pd.read_parquet(io.BytesIO(file_bytes))

        else:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unsupported format: {extension}"}
            )

        # -----------------------------
        # Convert to Pydantic-compatible dict
        # -----------------------------

        dataset_dict = {
            "columns": list(df.columns),
            "rows": df.to_dict(orient="records")
        }

        # -----------------------------
        # Validate using Pydantic
        # -----------------------------

        validated_dataset = DatasetSchema(**dataset_dict)

        # Save normalized CSV
        os.makedirs("data", exist_ok=True)
        normalized_path = "data/normalized_dataset.csv"
        df.to_csv(normalized_path, index=False)

        # -----------------------------
        # Build Agent State
        # -----------------------------

        state = {
            "user_query": user_query,
            "dataset_path": normalized_path,
            "problem_type": None,
            "target_column": None,
            "plan": None,
            "processed_data_path": None,
            "model_metrics": None,
            "best_model_path": None,
            "error_trace": None,
            "retry_count": 0,
            "deployment_status": None,
            "drift_detected": None
        }

        config = {"configurable": {"thread_id": "ui_run"}}

        final_state = None
        for event in graph.stream(state, config=config):
            final_state = event

        return JSONResponse(content=final_state)

    except Exception as e:
        import traceback
        print("==== SERVER ERROR ====")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",          # file_name:fastapi_variable
        host="localhost",    # localhost
        port=8000,
        reload=False
    )