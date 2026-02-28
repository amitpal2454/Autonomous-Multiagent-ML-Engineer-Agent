import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


def call_llm(prompt: str, temperature: float = 0.2) -> str:
    logger.info("Calling Azure OpenAI")

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are an expert ML engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )

    content = response.choices[0].message.content
    logger.info("Azure OpenAI response received")

    return content