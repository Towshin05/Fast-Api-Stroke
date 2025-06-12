from fastapi import FastAPI,Path,HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field, computed_field
from typing import Annotated, Literal
from typing import Optional, Annotated

import json
app= FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The ID of the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="The name of the patient")]
    age: Annotated[int, Field(..., description="The age of the patient")]
    # gender: Annotated[Literal["male", "female", "other"], Field(..., description="The gender of the patient")]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description="The gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient")]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient")]
@computed_field
@property
def bmi(self) -> float:
    bmi= round(self.weight/ (self.height**2),2)
    return bmi

@computed_field
@property
def verdict(self) -> str:
    if self.bmi < 18.5:
        return "Underweight"
    elif 18.5 <= self.bmi < 24.9:
        return "Normal weight"
    elif 25 <= self.bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"
   

class PatientUpdate(BaseModel):
    

    # id: Annotated[Optional[str], Field(description="The ID of the patient", examples=['P001'])]
    name: Annotated[Optional[str], Field(description="The name of the patient")]
    age: Annotated[Optional[int], Field(description="The age of the patient")]
    gender: Annotated[Optional[Literal["male", "female", "other"]], Field(description="The gender of the patient")]
    height: Annotated[Optional[float], Field(gt=0, description="The height of the patient")]
    weight: Annotated[Optional[float], Field(gt=0, description="The weight of the patient")]

def load_data():
    with open('patients.json', 'r') as f:
        data= json.load(f)

    return data    
#home page
@app.get('/')
def home():
    return {'message': "Welcome to the Patient Management API. Use /docs for interactive API documentation."}


@app.get('/about')
def About():
    return {'message': 'This is a simple API built with FastAPI.'}





@app.get('/view/{view_id}')
def view(view_id: int= Path(..., description="The ID of the patient to view")):
    data=load_data()
    patient = data.get(f'P{view_id:02d}')


    if not patient:
        raise HTTPException(status_code=404, detail='Patient not found')

    return patient

@app.get('/sort')
def sort_patients(sort_by: str=Query(..., description="Sort patients by 'name' or 'id'"), order:str=Query('asc', description="Order of sorting: 'asc' for ascending, 'desc' for descending")):
    valid_fields=["height", "weight"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")
    data=load_data()
    patients = list(data.values())
    patients.sort(key=lambda x: x[sort_by], reverse=(order == 'desc'))
    return 

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)    

@app.post('/create')
def create_patient(patient: Patient):
    data=load_data()
    #check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='   Patient already exists')
    #if no add new patients
    data[patient.id]=patient.model_dump(exclude=['id']) # pydantic data k  dictionery te convert kore
    #save into json file
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient": patient.model_dump()})

# @app.put('/edit/{patient_id}')
@app.put('/edit/{patient_id}')

    
    

def update_patient(patient_id: str, patient_update: PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, details= "there is no such patient with this id")
    
    #update patient data
    old_patient= data[patient_id]
    new_patient=patient_update.model_dump(exclude_unset=True)  # exclude id and unset fields

    for key, value in new_patient.items():
       
        old_patient[key]=value

    old_patient['id']=patient_id

    patient_pydantic= Patient(**old_patient)
    patient_pydantic.model_dump(exclude=['id'])  # convert to pydantic model and exclude id
    #save updated data

    data[patient_id]=old_patient
    save_data(data)        

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully", "patient": patient_pydantic.model_dump()})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]

    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})