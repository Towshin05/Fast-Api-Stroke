import streamlit as st
import requests


API_URL = "http://localhost:8000/predict"

st.title("Stroke Prediction App")
st.markdown("### Enter Patient Details")

#Input fields
age=st.number_input("Age", min_value=1, max_value=120, value=30)
weight_kg=st.number_input("Weight (kg)", min_value=1.0, value=70.0)
height_m=st.number_input("Height (m)", min_value=0.1, value=1.75)
smoking=st.selectbox("Smoker", ["yes", "no"])
gender=st.selectbox("Gender", ["male", "female"])
heart_disease = st.selectbox("Heart Disease", ["yes", "no"])
hypertension = st.selectbox("Hypertension", ["yes", "no"])
Residence_type=st.text_input("City", "New York")
work_type=st.text_input("Occupation", "Part-time")
avg_glucose_level = st.number_input("Average Glucose Level", min_value=0.0, value=100.0, step=0.1)
if st.button("Predict Stroke"):
    # Prepare the data for the API request
    input_data = {
        "age":age,
        "weight_kg": weight_kg,
        "height_m": height_m,
        "smoking": smoking,
        "gender": gender,
        "heart_disease": heart_disease,
        "Residence_type": Residence_type,
        "work_type": work_type,
        "avg_glucose_level": avg_glucose_level,
        "hypertension": hypertension
    }

    try:
        response=requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            prediction = response.json()
            st.success(f"Stroke Prediction: {prediction}")
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
