import os
import requests
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Healthcare Predictor", page_icon="🏥", layout="centered"
)

st.title("🏥 Patient Outcome Predictor")
st.markdown(
    "Select patient parameters from the dropdowns below to predict the test"
    " result."
)

# Create two columns for a clean layout
col1, col2 = st.columns(2)

with col1:
  age = st.slider("Patient Age", min_value=1, max_value=120, value=45)

  gender = st.selectbox("Gender", ["Male", "Female"])

  blood_type = st.selectbox(
      "Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
  )

  medical_condition = st.selectbox(
      "Medical Condition",
      ["Cancer", "Diabetes", "Asthma", "Obesity", "Arthritis", "Hypertension"],
  )

with col2:
  admission_type = st.selectbox(
      "Admission Type", ["Urgent", "Emergency", "Elective"]
  )

  medication = st.selectbox(
      "Medication",
      ["Aspirin", "Lipitor", "Penicillin", "Paracetamol", "Ibuprofen"],
  )

  insurance = st.selectbox(
      "Insurance Provider",
      ["Medicare", "UnitedHealthcare", "Aetna", "Cigna", "Blue Cross"],
  )

  billing = st.number_input(
      "Billing Amount ($)", min_value=0.0, value=12500.50, step=500.0
  )

st.divider()

# Submit button
if st.button("🔍 Predict Outcome", use_container_width=True):
  # Construct the JSON payload exactly as FastAPI expects it
  payload = {
      "Age": age,
      "Gender": gender,
      "Blood_Type": blood_type,
      "Medical_Condition": medical_condition,
      "Admission_Type": admission_type,
      "Medication": medication,
      "Insurance_Provider": insurance,
      "Billing_Amount": billing,
  }

  with st.spinner("Analyzing patient data..."):
    try:
      # Get API URL from environment variable (Docker compatible), default to localhost
      api_url = os.getenv("API_URL", "http://127.0.0.1:8000/predict")
      response = requests.post(api_url, json=payload)

      if response.status_code == 200:
        result = response.json()
        prediction = result["predicted_test_result"]
        confidence = result["confidence_score"] * 100

        # Display results nicely based on outcome
        if prediction.lower() == "abnormal":
          st.error(f"### Predicted Result: {prediction}")
        elif prediction.lower() == "normal":
          st.success(f"### Predicted Result: {prediction}")
        else:
          st.warning(f"### Predicted Result: {prediction}")

        st.info(f"**AI Confidence Score:** {confidence:.2f}%")
      else:
        st.error(f"API Error: {response.text}")

    except requests.exceptions.ConnectionError:
      st.error(
          "🚨 Connection Failed! Please make sure your FastAPI server is"
          " running."
      )