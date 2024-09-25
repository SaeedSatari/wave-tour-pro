import sys
import os

# Add the parent directory of the current file to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
from src.data_preprocessing import load_data

def train_model():
    data = load_data('data/tourism_data.csv')
    X = data[['month', 'temperature', 'local_events', 'holiday_season']]
    y = data['predicted_visitors']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    joblib.dump(model, 'models/tourism_model.pkl')
