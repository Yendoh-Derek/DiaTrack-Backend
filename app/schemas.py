from pydantic import BaseModel, Field
from typing import Dict, Any, Literal
from datetime import datetime
from uuid import UUID, uuid4

class PredictionInput(BaseModel):
    gender: Literal["Male", "Female"]
    age: int = Field(ge=0, le=120)
    hypertension: int = Field(ge=0, le=1)
    heart_disease: int = Field(ge=0, le=1)
    smoking_history: Literal["non-smoker", "current_smoker", "past_smoker"]
    bmi: float = Field(gt=0, lt=100)
    HbA1c_level: float = Field(ge=0, le=20)
    blood_glucose_level: float = Field(ge=0, le=350)

class PredictionOutput(BaseModel):
    prediction_id: UUID = Field(default_factory=uuid4)
    risk_score: float
    shap_values: Dict[str, float]
    prediction_time: datetime
    feature_input: Dict[str, Any]
    recommendation: str