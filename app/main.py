import numpy as np
from fastapi import FastAPI, HTTPException, Depends, Path, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from app.schemas import PredictionInput, PredictionOutput, UserOut
from app.utils import preprocess_input, get_shap_values
from app.model import base_model1, base_model2, base_model3, meta_model, preprocessor
from app.auth.auth_utils import (
    get_current_active_user,
    create_access_token,
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash
)
from models.user_models import User
from app.models import PredictionLog
from pydantic import BaseModel, EmailStr
from uuid import uuid4
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins (for production, specify allowed origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:59416",  # Flutter local dev
        "http://localhost:63112",
        # Add other allowed origins as needed
        # "http://localhost:3000",  # React local dev (optional)
        # "https://your-frontend-domain.com"  # Production frontend (optional)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(title="Diabetes Risk Prediction API")

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Diabetes Risk Prediction API - Please authenticate to use the services"}

@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Generate JWT token for authenticated users."""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_feature_names(column_transformer):
    output_features = []
    for name, transformer, original_features in column_transformer.transformers_:
        if transformer == 'passthrough':
            output_features.extend(original_features)
        elif hasattr(transformer, 'get_feature_names_out'):
            output_features.extend(transformer.get_feature_names_out(original_features))
        elif hasattr(transformer, 'get_feature_names'):
            if hasattr(transformer, 'categories_'):
                output_features.extend([f"{original_features[0]}_{cat}" for cat in transformer.categories_[0]])
            else:
                output_features.extend(original_features)
        else:
            output_features.extend(original_features)
    return output_features

def get_gemini_recommendation(risk_score, shap_values_dict):
    prompt = (
        f"A patient has a diabetes risk score of {risk_score}%. "
        f"The most influential factors (with SHAP values) are: "
        f"{', '.join([f'{k} ({v:+.2f})' for k, v in shap_values_dict.items()])}. "
        "Based on this, provide personalized, practical recommendations for the patient to reduce their diabetes risk."
    )
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Recommendation API quota exceeded or Gemini API error. Please try again later."

class ChatRequest(BaseModel):
    question: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if username exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_active=True
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@app.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user's info."""
    return current_user

@app.post("/chat")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Chat endpoint for authenticated users."""
    prompt = (
        f"You are a helpful diabetes assistant. "
        f"Answer the following user question in a clear and friendly way:\n"
        f"Question: {request.question}"
    )
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    try:
        response = model.generate_content(prompt)
        return {"answer": response.text.strip()}
    except Exception as e:
        return {"answer": "Sorry, I'm unable to answer right now. Please try again later."}

@app.post("/predict", response_model=PredictionOutput)
async def predict(
    data: PredictionInput,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Make prediction for authenticated users."""
    try:
        # 1. Preprocess input
        instance = preprocess_input(data)

        # 2. Get predictions from base learners
        pred1 = base_model1.predict(instance)[0]
        pred2 = base_model2.predict(instance)[0]
        pred3 = base_model3.predict(instance)[0]

        # 3. Stack predictions for meta learner
        meta_features = np.array([[pred1, pred2, pred3]])
        risk_score = float(meta_model.predict(meta_features)[0])
        risk_score_percent = round(risk_score * 100, 2)

        # 4. Get SHAP values and explanations
        shap_values = get_shap_values(instance)
        feature_names = get_feature_names(preprocessor)
        shap_pairs = list(zip(feature_names, shap_values))
        shap_pairs_sorted = sorted(shap_pairs, key=lambda x: abs(x[1]), reverse=True)
        shap_values_dict = {name: round(value, 2) for name, value in shap_pairs_sorted[:10]}

        # 5. Get recommendation
        recommendation = get_gemini_recommendation(risk_score_percent, shap_values_dict)

        # 6. Create database entry
        db_log = PredictionLog(
            prediction_id=uuid4(),
            user_id=current_user.id,
            risk_score=risk_score_percent,
            feature_input=data.dict(),
            shap_values=shap_values_dict,
            recommendation=recommendation
        )
        
        db.add(db_log)
        db.commit()
        db.refresh(db_log)

        return PredictionOutput(
            prediction_id=db_log.prediction_id,
            risk_score=risk_score_percent,
            shap_values=shap_values_dict,
            prediction_time=db_log.prediction_time,
            feature_input=data.dict(),
            recommendation=recommendation
        )
    except Exception as e:
        db.rollback()
        print(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/predictions", response_model=list[PredictionOutput])
async def list_predictions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List predictions for the authenticated user."""
    logs = db.query(PredictionLog)\
        .filter(PredictionLog.user_id == current_user.id)\
        .order_by(PredictionLog.prediction_time.desc())\
        .all()
    return [
        PredictionOutput(
            prediction_id=log.prediction_id,
            risk_score=log.risk_score,
            shap_values=log.shap_values,
            prediction_time=log.prediction_time,
            feature_input=log.feature_input,
            recommendation=log.recommendation
        )
        for log in logs
    ]

@app.get("/predictions/{prediction_id}", response_model=PredictionOutput)
async def get_prediction(
    prediction_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retrieve a single prediction if it belongs to the authenticated user."""
    log = db.query(PredictionLog)\
        .filter(
            PredictionLog.prediction_id == prediction_id,
            PredictionLog.user_id == current_user.id
        ).first()
    if not log:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return PredictionOutput(
        prediction_id=log.prediction_id,
        risk_score=log.risk_score,
        shap_values=log.shap_values,
        prediction_time=log.prediction_time,
        feature_input=log.feature_input,
        recommendation=log.recommendation
    )