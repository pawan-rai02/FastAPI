from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import os
from fastapi.responses import JSONResponse

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., examples= ['P001'])]
    name: Annotated[str, Field(...)]
    city: Annotated[str, Field(...)]
    age: Annotated[int, Field(..., gt = 0, lt = 110)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(...)]

    height: Annotated[float, Field(..., gt = 0, lt = 300)]
    weight: Annotated[float, Field(..., gt = 0)]

    @computed_field
    @property
    def bmi(self) ->float:
        bmi = round(self.weight / (self.height ** 2) , 2)

        return bmi

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 27:
            return 'Normal'
        else:
            return 'Overweight'



BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_data():
    file_path = os.path.join(BASE_DIR, 'patients.json')
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    file_path = os.path.join(BASE_DIR, 'patients.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)



@app.post('/create')
def create_patient(patient: Patient):

    #load data
    data = load_data()

    #check if patient is already present
    if patient.id in data:
        raise HTTPException(status_code= 400, detail= 'Patient already exists')

    #add new patient to the database
    data[patient.id] = patient.model_dump(exclude= ['id'])

    #save into the json file
    save_data(data)

    return JSONResponse(status_code= 201, content= {'message' : 'patient created successfully'})



