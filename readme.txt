DiaTrack Backend

An Ensemble Learning Approach for Risk Prediction and Management of Type 2 Diabetes Mellitus

Overview

This repository contains the backend for DiaTrack, a dual-interface clinical decision support system designed for early diagnosis and personalized management of Type 2 Diabetes Mellitus (T2DM).

The backend is built with FastAPI and serves as the central hub that connects:

Clinician-facing web dashboard (Next.js)

Patient-facing mobile application (Flutter)

Machine learning risk prediction engine (stacked ensemble with SHAP interpretability)

PostgreSQL database for secure data storage

The backend handles:

Authentication & Role-based Access Control

Data validation & preprocessing

Model inference & SHAP explanations

API endpoints for frontend integration

Storage & retrieval of patient records, predictions, and recommendations

System Context

Although this repository focuses on the backend, DiaTrack consists of three main components:

Clinician Dashboard – Web app for patient management, risk assessment, and recommendation entry.

Patient App – Mobile app for patients to view predictions, recommendations, and history.

Backend (This Repo) – Core system handling API requests, database operations, and ML predictions.

Backend Architecture
Core Components

API Framework: FastAPI (with Pydantic for schema validation)

Database: PostgreSQL

ML Engine: Stacked Ensemble Model (CatBoost, HistGradientBoosting, TabNet → XGBoost meta-learner)

Interpretability: LightGBM surrogate model for SHAP value computation

Authentication: JWT-based secure login for clinicians and patients

Hosting: Render (with Uvicorn for ASGI server)

Machine Learning Workflow

Input Validation – Backend enforces schema checks for patient data using Pydantic.

Preprocessing – Numerical features scaled, categorical features one-hot encoded, feature engineering applied:

Age & BMI binning

Glucose-to-HbA1c ratio

Risk condition flags

Prediction Pipeline –

Base models generate predictions.

Predictions fed into meta-learner (XGBoost) for final risk score (0–1).

Interpretability – SHAP values generated from a LightGBM surrogate model.

Response – Risk score and SHAP explanation returned via API.

Storage – Results saved in PostgreSQL for historical tracking and frontend display.

Key Backend Features

Role-based authentication for clinicians and patients

Secure data handling with validation at both frontend and backend

API endpoints for:

Patient registration

Clinical data submission

Risk prediction retrieval

SHAP-based feature importance

Recommendation management

Integrated ML model for real-time inference

Designed for scalability and integration with lab systems

API Overview

Some core endpoints (full list in /docs when running the app):

Method	Endpoint	Description
POST	/auth/login	Authenticate user & issue JWT
POST	/patients/	Register a new patient
GET	/patients/{id}	Retrieve patient details
POST	/predict/	Submit patient data & get risk score + SHAP values
POST	/recommendations/	Add clinician recommendations
GET	/recommendations/{patient}	Retrieve patient recommendations
Performance

Backend ML engine performance (on validation set):

Metric	Value
AUC	0.978
Accuracy	0.980
Precision	0.940
Recall	0.698
F1 Score	0.800

Installation & Setup
Clone Repository
git clone https://github.com/Yendoh-Derek/diatrack-backend.git
cd diatrack-backend

Install Dependencies
pip install -r requirements.txt

Run Backend
uvicorn main:app --reload

Usage

Clinician Workflow

Login → Add patient → Enter data → Predict risk score → View SHAP explanation → Add recommendations

Patient Workflow

Login → View prediction → View recommendations → Take follow-up actions

Future Backend Enhancements

Automated lab data ingestion from hospital systems

Multi-language API support (English, Twi)

Mobile offline prediction mode

Optimized recall for improved sensitivity
