import pandas as pd
import numpy as np
from app.model import explainer, preprocessor

def preprocess_input(data):
    try:
        # Create DataFrame with original string values for categorical columns
        input_dict = {
            'gender': [data.gender],
            'age': [data.age],
            'hypertension': [data.hypertension],
            'heart_disease': [data.heart_disease],
            'smoking_history': [data.smoking_history],
            'bmi': [data.bmi],
            'HbA1c_level': [data.HbA1c_level],
            'blood_glucose_level': [data.blood_glucose_level]
        }
        df = pd.DataFrame(input_dict)

        # Only convert numeric columns to numbers
        numeric_cols = ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='raise')

        # Do NOT touch 'gender' or 'smoking_history' columns!
        features = preprocessor.transform(df)
        return features
    except Exception as e:
        print(f"Preprocessing error: {str(e)}")
        raise ValueError(f"Error preprocessing input: {str(e)}")

def get_shap_values(instance):
    shap_vals = explainer(instance)
    return shap_vals.values[0].tolist()
