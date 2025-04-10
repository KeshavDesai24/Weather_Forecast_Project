import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import joblib

CLEANED_DATA_DIR = "../datafiles/cleaned/"
MODEL_DIR = "../models/"
os.makedirs(MODEL_DIR, exist_ok=True)

def train_xgboost_on_dataset(file_path, file_name):
    print(f"\n📁 Training XGBoost on: {file_name}")
    try:
        df = pd.read_csv(file_path)

        # Basic check
        if 'temperature' not in df.columns or 'date' not in df.columns:
            print("❌ Skipping: Missing 'temperature' or 'date' column")
            return

        # Fill any missing data again (safety net)
        df.interpolate(method='linear', inplace=True)
        df.fillna(method='bfill', inplace=True)

        # Define features & target
        target_col = "temperature"
        feature_cols = [col for col in df.columns if col != target_col and col != 'date']
        
        if len(feature_cols) == 0:
            print("⚠️ Skipping: Not enough feature columns")
            return

        X = df[feature_cols]
        y = df[target_col]

        # Split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model
        model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
        model.fit(X_train, y_train)

        # Evaluate
        preds = model.predict(X_test)
        rmse = mean_squared_error(y_test, preds, squared=False)
        print(f"✅ RMSE: {rmse:.2f}")

        # Save model
        model_name = f"xgboost_{file_name.replace('.csv', '')}.json"
        model.save_model(os.path.join(MODEL_DIR, model_name))
        print(f"✅ Model saved: {model_name}")

    except Exception as e:
        print(f"❌ Error with {file_name}: {e}")

# Loop through all cleaned datasets
for file in os.listdir(CLEANED_DATA_DIR):
    if file.endswith(".csv"):
        path = os.path.join(CLEANED_DATA_DIR, file)
        train_xgboost_on_dataset(path, file)
