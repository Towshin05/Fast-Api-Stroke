from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    prediction: str = Field(..., description="The predicted  condition based on the input data.")
    confidence: float =Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="The confidence level of the prediction, ranging from 0 to 1."
    )
    class_probabilities: dict[str, float] = Field(
        ..., 
        description="A dictionary mapping class labels to their predicted probabilities."
    )