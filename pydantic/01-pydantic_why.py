# def insert_patient(name : str, age : int):

#     if type(name) == str and type(age) == int:
#         print(name)
#         print(age)
#         print('inserted into database')

#     else:
#         raise TypeError('incorrect datatype')

# insert_patient('pawan', '3')


from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional

class Patient(BaseModel):

    name: str
    age: int = Field(gt=0, lt = 110)
    email: EmailStr
    weight: float = Field(gt=0)
    married: bool = False
    allergies: Optional[List[str]]
    contact_details: Dict[str, str]

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('inserted')



patient_info = {'name' : 'pawan', 'age' : 20, 'weight' : 59, 'married' : False, 'allergies' : ['pollen', 'dust', 'milk'], 'contact_details' : {'email': 'pawan@gmail.com', 'phone_number': '9999'}}

patient1 = Patient(**patient_info)

insert_patient(patient1)