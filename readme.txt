DiaTrack
An Ensemble Learning Approach for Risk Prediction and Management of Type 2 Diabetes Mellitus

Abstract
DiaTrack is a dual-interface clinical decision support system designed for early diagnosis and personalized management of Type 2 Diabetes Mellitus (T2DM). It combines a clinician-facing web dashboard with a patient-facing mobile application, linked to a backend powered by a stacked ensemble learning model for accurate risk prediction.

The ensemble integrates CatBoost, HistGradientBoosting, and TabNet as base learners, with XGBoost as the meta-learner, and uses a LightGBM surrogate model for SHAP-based interpretability. The system is deployed via FastAPI (backend, hosted on Render), with Next.js for the web dashboard and Flutter for the mobile app.

DiaTrack achieved AUC: 0.978, Accuracy: 0.98, Precision: 0.94, and F1: 0.80, making it a high-performing and clinically relevant tool. Designed with stakeholder input, it ensures clinician oversight, strong security, and usability, with future support for Twi language and automated lab data integration.

System Overview

Clinician Dashboard (Web – Next.js): Patient registration, risk assessment, recommendation entry.

Patient App (Mobile – Flutter): View predictions, recommendations, history.

Backend (FastAPI): Handles authentication, data validation, model inference, and API endpoints.

Database: Stores patient profiles, clinical data, predictions, and recommendations.

ML Engine: Stacked ensemble model with SHAP-based interpretability.

Ensemble Architecture

Base Learners:

CatBoost

HistGradientBoosting

TabNet

Meta-Learner:

XGBoost

Surrogate Model:

LightGBM for SHAP value computation.

Workflow:

Input features are preprocessed (scaling for numerical, one-hot encoding for categorical).

Predictions from base models are passed to the meta-learner.

The meta-learner outputs a final risk score (0–1).

SHAP values are generated via the surrogate model for interpretability.

Data Flow

Data Collection – Patient data entered via clinician dashboard or patient app.

Data Validation – Both frontend and backend enforce schema and range checks.

Preprocessing – Missing value handling, feature scaling, encoding, and feature engineering (e.g., glucose-to-HbA1c ratio, risk condition flags).

Prediction – Stacked ensemble produces risk score.

Interpretation – SHAP explains feature contributions.

Storage – Prediction results and SHAP explanations stored in the database.

Display – Results shown on clinician and patient dashboards.

Key Features
Clinician-controlled prediction workflow.

Stacked ensemble model for high predictive accuracy.

SHAP interpretability for transparency.

Secure authentication for both user roles.

Role-based dashboards.

Multilingual support (English, Twi in development).

Designed for scalability and lab system integration.

Performance Metrics
Metric	Value
AUC	0.978
Accuracy	0.98
Precision	0.94
Recall	0.698
F1 Score	0.80

Stakeholder Engagement
KNUST Hospital Diabetes Clinic – feedback shaped clinician-first workflow.

Dr. Dorothy Araba Yakoba Agyapong – supervision and domain guidance.

Dr. Prince Agyei – advised on data validation, usability, and local language support.

Patients – confirmed value of remote monitoring and personalized recommendations.

Technology Stack
Backend: FastAPI, Pydantic, Uvicorn

ML: CatBoost, HistGradientBoosting, TabNet, XGBoost, LightGBM, SHAP

Web Frontend: Next.js, Tailwind CSS

Mobile Frontend: Flutter

Database: PostgreSQL

Hosting: Render (Backend), Firebase (Frontend)

Installation
Backend:

bash
Copy
Edit
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
Web App:

bash
Copy
Edit
cd web
npm install
npm run dev
Mobile App:

bash
Copy
Edit
cd mobile
flutter pub get
flutter run
Usage
Clinician: Login → Add patient → Enter data → Predict → View results & add recommendations.

Patient: Login → View predictions & recommendations → Follow-up actions.

Future Work
Automated lab data ingestion.

Expanded language support.

Mobile offline mode.

Further optimization for recall.

Contributors
Derek Yendoh – Team Lead, ML & Backend Development

M. A. Aseda Obeng Baah – Mobile App Development

Elizabeth Ofori – Web App Development

Supervisor – Dr. (Mrs.) Dorothy Araba Yakoba Agyapong

License
MIT License – see LICENSE file.

I can also prepare a visually enhanced PDF of this README for the award submission, including these diagrams inline, so it’s presentation-ready.

Do you want me to go ahead and produce that PDF version? It would help with the Presentation & Communication criteria.



Temporarily allows script execution: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
Activate the virtual environment: .\.venv\Scripts\Activate

Summary of recommended versions:
shap==0.41.0
numba==0.56.4
cloudpickle version: 1.6.0

Prompts to start application:
1. Temporarily allows script execution: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
2. Activate the virtual environment: .\.venv\Scripts\Activate
3. start the application: uvicorn app.main:app --reload
