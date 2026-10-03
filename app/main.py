import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Healthcare Prediction API",
    description="End-to-End ML API for Patient Health Outcome Predictions",
    version="1.0.0",
)

# Load saved ML model and artifacts
MODEL_PATH = "models/xgboost_model.joblib"
ENCODERS_PATH = "models/encoders.joblib"
TARGET_ENCODER_PATH = "models/target_encoder.joblib"
FEATURE_COLS_PATH = "models/feature_cols.joblib"

try:
  model = joblib.load(MODEL_PATH)
  encoders = joblib.load(ENCODERS_PATH)
  target_encoder = joblib.load(TARGET_ENCODER_PATH)
  feature_cols = joblib.load(FEATURE_COLS_PATH)
except Exception as e:
  print(f"[WARNING] Model artifacts not found: {e}")


class PatientData(BaseModel):
  Age: int
  Gender: str
  Blood_Type: str = "O+"
  Medical_Condition: str
  Admission_Type: str
  Medication: str
  Insurance_Provider: str
  Billing_Amount: float


@app.get("/")
def home():
  return {"status": "online", "message": "Healthcare ML API is operational"}


@app.post("/predict")
def predict(data: PatientData):
  try:
    raw_input = {
        "Age": data.Age,
        "Gender": data.Gender,
        "Blood Type": data.Blood_Type,
        "Medical Condition": data.Medical_Condition,
        "Admission Type": data.Admission_Type,
        "Medication": data.Medication,
        "Insurance Provider": data.Insurance_Provider,
        "Billing Amount": data.Billing_Amount,
    }

    input_df = pd.DataFrame([raw_input])

    # Transform categorical variables using fitted label encoders
    for col, le in encoders.items():
      if col in input_df.columns:
        val = str(input_df[col].iloc[0])
        if val in le.classes_:
          input_df[col] = le.transform([val])[0]
        else:
          input_df[col] = 0

    input_df = input_df[feature_cols]

    # Generate prediction and confidence score
    prediction_num = model.predict(input_df)[0]
    prediction_label = target_encoder.inverse_transform([prediction_num])[0]

    probabilities = model.predict_proba(input_df)[0]
    confidence = float(np.max(probabilities))

    return {
        "predicted_test_result": prediction_label,
        "confidence_score": round(confidence, 4),
    }

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))