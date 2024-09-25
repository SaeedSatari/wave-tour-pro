import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path)
    # Additional preprocessing steps can be added here
    return data