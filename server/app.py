
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.predict import predict_output 



from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field, field_validator
from fastapi.responses import JSONResponse
from typing import List
from typing import Annotated, Literal, Optional
import pickle
import pandas as pd

from schema.user_input import UserInput
import numpy as np

from schema.output_response import PredictionResponse


app = FastAPI()

@app.get('/')
def home():
    return {'message': "Welcome to the Disease Prediction API. Use /docs for interactive API documentation."}


@app.get('/health')
def health_check():
    return JSONResponse(status_code=200, content={"status": "healthy"})


@app.post('/predict', response_model=PredictionResponse)
def predict_disease(data: UserInput):
    user_input = {
        'bmi': data.bmi,
        'lifestyle': data.lifestyle,
        'age': data.age,
        'gender': data.gender,
        'avg_glucose_level': data.avg_glucose_level,
        'hypertension': data.hypertension,
        'heart_disease': data.heart_disease,
        'Residence_type': data.Residence_type,
        'work_type': data.work_type,
    }

    try:
        prediction = predict_output(user_input)
        
        # Convert numpy types to Python types
        if hasattr(prediction, 'item'):
            # For numpy scalars
            prediction = prediction.item()
        elif isinstance(prediction, np.ndarray):
            # For numpy arrays
            prediction = prediction.tolist()
        elif hasattr(prediction, 'dtype'):
            # For other numpy types
            prediction = int(prediction) if 'int' in str(prediction.dtype) else float(prediction)

        return JSONResponse(status_code=200, content={
            'prediction': prediction,
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={
            'error': f'An error occurred while processing the request: {str(e)}'
        })