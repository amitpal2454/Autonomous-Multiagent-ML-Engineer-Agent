import pandas as pd

def load_dataset(path:str):
    df=pd.read_csv(path)

    return {
        "columns":df.columns,
        "shape":df.shape,
        "missing_values":df.isnull().sum().to_dict()
    }