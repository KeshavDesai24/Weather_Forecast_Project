from fastapi import FastAPI, HTTPException, Query
from keras.models import load_model
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Weather Forecasting API is running!"}

# Update this path based on your actual project structure
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

@app.get("/predict")
def predict(model_name: str = Query(..., description="Name of the .h5 model file")):
    model_path = os.path.join(MODEL_DIR, model_name)

    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model file not found.")

    try:
        model = load_model(model_path)
        # Dummy response — replace with actual prediction logic
        return {"message": f"Model '{model_name}' loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
