from tools.data_loader import load_dataset

def data_agent(state):
    result=load_dataset(state["dataset_path"])
    return { "data_summary":result}