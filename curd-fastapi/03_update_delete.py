from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import os
from fastapi.responses import JSONResponse

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., examples= ['P001'])]
    name: Annotated[str, Field(...)]
    city: Annotated[str, Field(...)]
    age: Annotated[int, Field(..., gt = 0, lt = 110)]
    gender: Annotated[Literal['male', 'female', 'others', 'Male', 'Female', 'Others'], Field(...)]

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

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default= None)]
    city: Annotated[Optional[str], Field(default= None)]
    age: Annotated[Optional[int], Field(default= None, gt = 0, lt = 110)]

    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default= None)]

    height: Annotated[Optional[float], Field(default= None, gt = 0)]

    weight: Annotated[Optional[float], Field(default= None, gt = 0)]



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





@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code= 404, detail= 'Patient not found')

    existing_patient_info = data[patient_id]

    updated_paatient_info = patient_update.model_dump(exclude_unset= True)

    for key, val in updated_paatient_info.items():
        existing_patient_info[key] = val


    #existing patient info -> pydantic object ->updated bmi + verdict
    existing_patient_info['id'] = patient_id
    if 'gender' in existing_patient_info and isinstance(existing_patient_info['gender'], str):
        existing_patient_info['gender'] = existing_patient_info['gender'].lower()
    patient_pydantic_obj = Patient(**existing_patient_info)

    #pydantic object ->dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude= 'id')
    # normalize gender case in stored data
    if 'gender' in existing_patient_info and isinstance(existing_patient_info['gender'], str):
        existing_patient_info['gender'] = existing_patient_info['gender'].capitalize() if existing_patient_info['gender'] != 'others' else existing_patient_info['gender'].capitalize()
    data[patient_id] = existing_patient_info


    save_data(data)

    return JSONResponse(status_code= 200, content= {'message' : 'patient uppdated'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code= 404, detail= 'Patient not found')

    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code= 200, content= {'message': 'patient deleted'})