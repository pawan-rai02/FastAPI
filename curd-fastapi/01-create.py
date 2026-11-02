import json
import os

from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_data():
    file_path = os.path.join(BASE_DIR, 'patients.json')
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


@app.get('/')
def hello():
    return {'message' : 'Patient managment system'}

@app.get('/about')
def about():
    return {'message' : 'A fully functional api to manage patients records'}


@app.get('/view')
def view():
    data = load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description = 'ID of the patient in the DB', example= 'P001')):
    data = load_data()
    normalized_id = patient_id.strip().upper()

    if normalized_id in data:
        return data[normalized_id]

    raise HTTPException(status_code=404, detail='patient not found')


@app.get('/sort')
def sort_patients(sort_by : str = Query(..., description= 'Sort on the basis of height, weight and bmi'), order: str = Query('asc', description= 'sort in ascending or descending order')):


    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code= 400, detail= f'Invalid fields select from {valid_fields}')


    if order not in ['asc', 'desc']:
        raise HTTPException(status_code= 400, detail= f'Invalid fields select between asc and desc')


    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key= lambda x : x.get(sort_by, 0), reverse= sort_order)

    return sorted_data