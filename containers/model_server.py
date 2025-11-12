import os
import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MLFLOW_TRACKING_URI = "http://35.184.91.21:8100"
MODEL_NAME = os.getenv("MODEL_NAME", "IRIS-classifier-dt")
MODEL_VERSION = os.getenv("MODEL_VERSION", "1")

app = FastAPI(title="🌸 Iris Classifier API")

model = None
try:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    model_uri = f"models:/{MODEL_NAME}/{MODEL_VERSION}"
    model = mlflow.sklearn.load_model(model_uri)
    print(f"Loaded model '{MODEL_NAME}' (version {MODEL_VERSION})")
except Exception as e:
    print(f"Failed to load model: {e}")

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def root():
    return {"model": MODEL_NAME, "version": MODEL_VERSION}

@app.post("/predict")
def predict(data: IrisInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    input_df = pd.DataFrame([data.dict()])
    return {"predicted_species": model.predict(input_df)[0]}
