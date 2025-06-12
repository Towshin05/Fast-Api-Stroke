
from fastapi import FastAPI
from fastapi.responses import JSONResponse  
from pydantic import BaseModel, Field, computed_field, field_validator
import pickle
import pandas as pd
from schema.user_input import UserInput

# Import the ML model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Get class labels
class_labels = model.classes_.tolist()
def predict_output(user_input: dict):
    input_df = pd.DataFrame([user_input])
    
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)
    class_probs = dict(zip(class_labels, map(lambda x: round(x, 4), probabilities)))
    result = model.predict(input_df)[0]

    return {
        'prediction': str(result),  # Convert to string
        'confidence': float(confidence),  # Convert to Python float
        'class_probabilities': {k: float(v) for k, v in class_probs.items()}  # Convert all values to Python float
    }