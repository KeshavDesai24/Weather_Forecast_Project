import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential #type:ignore
from tensorflow.keras.layers import LSTM, Dense #type: ignore
from sklearn.preprocessing import MinMaxScaler
import joblib

def create_dataset(data, look_back=5):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:i + look_back])
        y.append(data[i + look_back])
    return np.array(X), np.array(y)

# Corrected directory path
DATA_DIR = "./cleaned"
LOOK_BACK = 5

if not os.path.exists(DATA_DIR):
    print(f"❌ Directory not found: {DATA_DIR}")
else:
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("cleaned_") and filename.endswith(".csv"):
            file_path = os.path.join(DATA_DIR, filename)
            print(f"\n📁 Training on: {filename}")

            df = pd.read_csv(file_path)

            if 'temperature' not in df.columns:
                print("❌ Skipping (missing 'temperature' column)")
                continue

            try:
                temp_values = df['temperature'].values.reshape(-1, 1)
                scaler = MinMaxScaler()
                scaled = scaler.fit_transform(temp_values)

                X, y = create_dataset(scaled, look_back=LOOK_BACK)
                X = X.reshape((X.shape[0], X.shape[1], 1))

                model = Sequential([
                    LSTM(64, input_shape=(X.shape[1], 1)),
                    Dense(1)
                ])
                model.compile(loss='mean_squared_error', optimizer='adam')
                model.fit(X, y, epochs=10, batch_size=32, verbose=0)

                model_name = filename.replace(".csv", "_lstm.h5")
                scaler_name = filename.replace(".csv", "_scaler.save")

                model.save(model_name)
                joblib.dump(scaler, scaler_name)

                prk(f"✅ Model trained and saved as: {model_name}")
            except Exception as e:
                print(f"❌ Training failed: {e}")


