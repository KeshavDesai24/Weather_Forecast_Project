import pandas as pd
import numpy as np
import os
from keras.models import load_model #type:ignore

MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))

def load_lstm_model(model_filename="default_lstm_model.h5"):
    model_path = os.path.join(MODELS_DIR, model_filename)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"LSTM model file not found: {model_path}")
    
    model = load_model(model_path)
    return model


def preprocess_data(df):
    # Select only the temperature column, normalize
    temperatures = df['TEMP'].values.reshape(-1, 1)
    temperatures = temperatures.astype(float)
    return temperatures / 100  # simple normalization

def predict_temperature(filename):
    filepath = os.path.join("data", filename)  # change path if needed
    if not os.path.exists(filepath):
        return ["File not found"]

    df = pd.read_csv(filepath)
    
    if df.empty or "TEMP" not in df.columns:
        return ["Invalid or empty file"]

    try:
        data = preprocess_data(df)
        X_input = data[-30:].reshape(1, 30, 1)
        predictions = model.predict(X_input)[0]
        predictions = (predictions * 100).round(2)  # de-normalize
        return [float(temp) for temp in predictions]
    except Exception as e:
        return [f"Error during prediction: {str(e)}"]

def get_forecast():
    # Temporary static dummy forecast
    return [27.2, 27.5, 27.9, 28.3, 28.8, 29.4, 30.0]

def detect_heatwave(forecast):
    heatwave_threshold = 35.0
    heatwave_days = []

    for i, temp in enumerate(forecast):
        if temp >= heatwave_threshold:
            heatwave_days.append({
                "day": f"Day {i+1}",
                "temperature": temp,
                "alert": "Heatwave Warning 🚨",
                "remedy": "Stay hydrated, avoid direct sun exposure, and rest indoors."
            })

    if not heatwave_days:
        return {"message": "No heatwave detected in the next 7 days."}
    else:
        return {"heatwave_alerts": heatwave_days}
