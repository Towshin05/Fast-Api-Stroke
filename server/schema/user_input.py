
from typing import Annotated, Literal
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator


class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="The age of the patient")]
    weight_kg: Annotated[float, Field(..., gt=0, description="The weight of the patient in kg")]
    height_m: Annotated[float, Field(..., gt=0, description="The height of the patient in meters")]
    smoking: Annotated[Literal["yes", "no"], Field(..., description="Whether the patient is a smoker")]
    gender: Annotated[Literal["male", "female"], Field(..., description="The gender of the patient")]
    heart_disease: Annotated[Literal["yes", "no"], Field(..., description="Whether the patient has heart disease")]
    Residence_type: Annotated[str, Field(..., description='The city of the patient')]
    work_type: Annotated[str, Field(..., description='The occupation of the patient')]
    avg_glucose_level: Annotated[float, Field(..., gt=0, description="The average glucose level of the patient")]
    hypertension: Annotated[Literal["yes", "no"], Field(..., description="Whether the patient has hypertension")]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight_kg / (self.height_m ** 2)

    @computed_field
    @property
    def lifestyle(self) -> str:
        # Check if smoking is "yes" and calculate lifestyle
        is_smoker = self.smoking == "yes"
        calculated_bmi = self.bmi
        
        if is_smoker and calculated_bmi > 30:
            return "high"
        elif is_smoker and 20 <= calculated_bmi <= 30:
            return "medium"
        else:
            return "low"

    @field_validator('Residence_type', mode='before')
    @classmethod
    def normalize_residence_type(cls, v: str) -> str:
        v = v.strip().title()
        return v

    @field_validator('work_type', mode='before')
    @classmethod
    def normalize_work_type(cls, v: str) -> str:
        v = v.strip().title()
        return v

    @field_validator('gender', mode='before')
    @classmethod
    def normalize_gender(cls, v: str) -> str:
        v = v.strip().lower()
        return v
    