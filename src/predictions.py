import joblib
import numpy as np

def load_model():
    model = joblib.load('models/tourism_model.pkl')
    return model

def make_prediction(input_data):
    model = load_model()
    prediction = model.predict(np.array(input_data).reshape(1, -1))
    return prediction[0]
