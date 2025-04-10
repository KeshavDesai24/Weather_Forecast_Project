import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model #type: ignore
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

DATA_DIR = './training/cleaned'
MODEL_SUFFIX = '_lstm.h5'
PREDICTION_DAYS = 7
LOOK_BACK = 30  # Must match the training window

def load_and_predict(file_path):
    print(f"\n📁 Predicting using: {os.path.basename(file_path)}")

    # Load and prepare data
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)

    # Scale data
    scaler = MinMaxScaler()
    scaled_temp = scaler.fit_transform(df[['temperature']].values)

    # Take the last LOOK_BACK days
    last_sequence = scaled_temp[-LOOK_BACK:]
    predictions = []

    current_sequence = last_sequence

    # Load the model
    model_name = os.path.basename(file_path).replace('.csv', MODEL_SUFFIX)
    model = load_model(os.path.join('./models', model_name))

    for _ in range(PREDICTION_DAYS):
        # Reshape for prediction
        input_seq = current_sequence.reshape((1, LOOK_BACK, 1))
        pred = model.predict(input_seq, verbose=0)
        predictions.append(pred[0][0])

        # Update the sequence
        current_sequence = np.append(current_sequence[1:], [[pred[0][0]]], axis=0)

    # Inverse scale predictions
    predictions_inverse = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

    # Print results
    for i, temp in enumerate(predictions_inverse):
        print(f"Day {i+1}: 🌡️ {temp:.2f}°C")

    return predictions_inverse

# Run predictions for all CSVs
if __name__ == "__main__":
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.csv'):
            file_path = os.path.join(DATA_DIR, filename)
            load_and_predict(file_path)
