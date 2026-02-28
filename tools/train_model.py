from azure.storage.blob import BlobServiceClient
import os
import joblib
import io
import os
import pandas as pd
import joblib
import logging

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from tools.storage_tool import upload_model_to_blob



logger = logging.getLogger("agentic_ml_system")


def train_model(data_path: str, target_column: str):
    logger.info("Starting model training")

    # -------------------------------
    # 1️⃣ Validate file exists
    # -------------------------------
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at path: {data_path}")

    df = pd.read_csv(data_path)

    logger.info(f"Dataset loaded successfully. Shape: {df.shape}")

    # -------------------------------
    # 2️⃣ Validate target column
    # -------------------------------
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset")

    if df.empty:
        raise ValueError("Dataset is empty")

    # -------------------------------
    # 3️⃣ Split features and target
    # -------------------------------
    X = df.drop(columns=[target_column])
    y = df[target_column]

    if X.shape[1] == 0:
        raise ValueError("No feature columns available after dropping target")

    # -------------------------------
    # 4️⃣ Detect problem type
    # -------------------------------
    if y.dtype in ["int64", "float64"]:
        problem_type = "regression"
        model = RandomForestRegressor(random_state=42)
    else:
        problem_type = "classification"
        model = RandomForestClassifier(random_state=42)

    logger.info(f"Detected problem type: {problem_type}")

    # -------------------------------
    # 5️⃣ Train/test split
    # -------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    logger.info("Training model...")
    model.fit(X_train, y_train)

    logger.info("Model training completed")

    # -------------------------------
    # 6️⃣ Evaluate
    # -------------------------------
    preds = model.predict(X_test)

    if problem_type == "regression":
        score = r2_score(y_test, preds)
        metric_name = "r2_score"
    else:
        score = accuracy_score(y_test, preds)
        metric_name = "accuracy"

    logger.info(f"Model performance: {metric_name} = {score}")

    # -------------------------------
    # 7️⃣ Save model locally
    # -------------------------------
    # Save locally (optional)
    os.makedirs("model", exist_ok=True)
    local_model_path = "model/best_model.pkl"
    joblib.dump(model, local_model_path)

    # Upload to Azure Blob
    blob_url = upload_model_to_blob(model, "best_model.pkl")

    logger.info(f"Model saved at {blob_url}")

    # -------------------------------
    # 8️⃣ Return structured output
    # -------------------------------
    return {
    "problem_type": problem_type,
    "metric_name": metric_name,
    "metric_value": float(score),
    "model_path": blob_url
}