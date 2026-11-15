import streamlit as st
import requests
import json

st.set_page_config(page_title="Insurance Premium Predictor", page_icon="💊", layout="centered")

st.title("Insurance Premium Predictor")
st.markdown("Enter your details to predict insurance premium category")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=1, max_value=119, value=30)
        weight = st.number_input("Weight (kg)", min_value=0.1, value=70.0, step=0.1)
        height = st.number_input("Height (m)", min_value=0.1, max_value=3.4, value=1.75, step=0.01)
        income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0, step=0.1)
    
    with col2:
        smoker = st.selectbox("Smoker", options=[False, True], format_func=lambda x: "Yes" if x else "No")
        city = st.text_input("City", value="Mumbai")
        occupation = st.selectbox(
            "Occupation",
            options=[
                "private_job",
                "self_employed",
                "government_job",
                "business_owner",
                "student",
                "unemployed",
                "retired",
                "homemaker"
            ]
        )
    
    submitted = st.form_submit_button("Predict Premium")

if submitted:
    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }
    
    try:
        with st.spinner("Predicting..."):
            response = requests.post("http://127.0.0.1:8002/predict", json=payload)
            response.raise_for_status()
            result = response.json()
            prediction = result.get("predicted_category", "Unknown")
            
            st.success(f"Predicted Premium Category: **{prediction}**")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure the FastAPI server is running on http://127.0.0.1:8002")
    except requests.exceptions.HTTPError as e:
        st.error(f"API Error: {e}")
        st.text(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
