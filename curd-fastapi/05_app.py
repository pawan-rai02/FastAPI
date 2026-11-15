from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Literal, Annotated
import pickle
import pandas as pd
from fastapi.responses import JSONResponse

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120)]
    weight: Annotated[float, Field(..., gt=0)]
    height: Annotated[float, Field(..., gt=0, lt=3.5, description='Height in meters')]
    income_lpa: Annotated[float, Field(..., gt=0, description='Annual salary in lpa')]
    smoker: Annotated[bool, Field(...)]
    city: Annotated[str, Field(...)]
    occupation: Annotated[Literal['self_employed', 'private_job', 'unemployed', 'government_job', 'student', 'business_owner', 'retired', 'homemaker'], Field(...)]


@app.post('/predict')
def predict_premium(data: UserInput):
    bmi = data.weight / (data.height ** 2)
    
    if data.smoker and bmi > 30:
        lifestyle_risk = "high"
    elif data.smoker and bmi > 27:
        lifestyle_risk = "medium"
    else:
        lifestyle_risk = "low"
    
    if data.age < 25:
        age_group = "young"
    elif data.age < 45:
        age_group = "adult"
    elif data.age < 60:
        age_group = "middle_aged"
    else:
        age_group = "senior"
    
    if data.city in tier_1_cities:
        city_tier = 1
    elif data.city in tier_2_cities:
        city_tier = 2
    else:
        city_tier = 3
    
    input_df = pd.DataFrame([{
        'bmi': bmi,
        'age_group': age_group,
        'lifestyle_risk': lifestyle_risk,
        'city_tier': city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    pred = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'predicted_category': pred})
