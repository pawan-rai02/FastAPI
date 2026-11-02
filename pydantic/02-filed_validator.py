from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
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

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains = ['hdfc.com', 'icici.com']

        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('not a valid domain')

        return value

    @field_validator('age', mode= 'before')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value

        else:
            raise ValueError('age should be inbetween 0 and 100')
    