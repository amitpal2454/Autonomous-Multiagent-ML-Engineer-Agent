import streamlit as st
import requests

API_URL = "http://localhost:8000/run-agent"

st.set_page_config(page_title="Autonomous ML Agent", layout="wide")

st.title("🚀 Autonomous ML Engineer Agent")

st.write("Upload Excel dataset and provide ML instruction")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

user_query = st.text_area(
    "Enter Instruction",
    "Train a regression model to predict House_Price"
)

if st.button("Run Agent"):

    if uploaded_file is None:
        st.error("Please upload an Excel file.")
    else:
        with st.spinner("Running Autonomous ML Agent..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            }

            data = {
                "user_query": user_query
            }

            response = requests.post(API_URL, files=files, data=data)

            if response.status_code == 200:
                result = response.json()

                st.success("Execution Completed")

                st.subheader("Model Metrics")
                st.json(result.get("model_metrics"))

                st.subheader("Model Location")
                st.write(result.get("best_model_path"))

                if result.get("error_trace"):
                    st.error(result.get("error_trace"))

            else:
                st.error(f"Error: {response.status_code}")