from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient')]

    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=110)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=None)]

    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]

    contact_details: Dict[str, str]

    @computed_field
    @property
    def calc_bmi(self) -> float:
        bmi = round(self.weight / (self.height**2), 2)

        return bmi

