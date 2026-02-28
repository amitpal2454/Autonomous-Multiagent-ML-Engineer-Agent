# tools/storage_tool.py

import os
import io
import joblib
from azure.storage.blob import BlobServiceClient
from utils.logger import logger


def upload_model_to_blob(model, blob_name: str) -> str:
    logger.info("Uploading model to Azure Blob Storage")

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    if not connection_string:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING not set")

    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string
    )

    container_name = "ml-models"

    # Ensure container exists
    container_client = blob_service_client.get_container_client(container_name)
    if not container_client.exists():
        logger.info("Creating Azure container: ml-models")
        container_client.create_container()

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=blob_name
    )

    buffer = io.BytesIO()
    joblib.dump(model, buffer)
    buffer.seek(0)

    blob_client.upload_blob(buffer, overwrite=True)

    logger.info("Model uploaded successfully")

    return blob_client.url