import os
import joblib
import pandas as pd
from database.db_connection import engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier


def train_pipeline():
  print("[1/4] Pulling dataset from Aiven PostgreSQL database...")
  query = "SELECT * FROM raw_healthcare_data;"
  df = pd.read_sql(query, con=engine)
  print(f"Loaded {len(df)} records from cloud database.")

  print("[2/4] Preprocessing features and encoding labels...")
  # Define target and non-predictive identifier columns
  target_col = "Test Results"
  ignore_cols = [
      "Name",
      "Room Number",
      "Date of Admission",
      "Discharge Date",
      "Doctor",
      "Hospital",
  ]

  # Filter columns present in dataset
  feature_cols = [
      c for c in df.columns if c not in ignore_cols and c != target_col
  ]

  X = df[feature_cols].copy()
  y = df[target_col].copy()

  # Categorical feature encoding
  encoders = {}
  for col in X.select_dtypes(include=["object"]).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le

  target_encoder = LabelEncoder()
  y = target_encoder.fit_transform(y.astype(str))

  # Split into train and test sets
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, random_state=42
  )

  print("[3/4] Training XGBoost Classifier...")
  model = XGBClassifier(
      n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42
  )
  model.fit(X_train, y_train)

  accuracy = model.score(X_test, y_test)
  print(f"[SUCCESS] Model trained with Test Accuracy: {accuracy:.4f}")

  print("[4/4] Saving model artifacts to 'models/' directory...")
  os.makedirs("models", exist_ok=True)
  joblib.dump(model, "models/xgboost_model.joblib")
  joblib.dump(encoders, "models/encoders.joblib")
  joblib.dump(target_encoder, "models/target_encoder.joblib")
  joblib.dump(feature_cols, "models/feature_cols.joblib")

  print("[SUCCESS] All artifacts saved successfully!")


if __name__ == "__main__":
  train_pipeline()