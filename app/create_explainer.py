import joblib
import shap
import os

MODEL_PATH = os.path.join("models", "ensemble_model.pkl")
EXPLAINER_PATH = os.path.join("models", "shap_explainer.pkl")

model = joblib.load(MODEL_PATH)
explainer = shap.Explainer(model)
joblib.dump(explainer, EXPLAINER_PATH)

print("Explainer re-created and saved successfully.")
