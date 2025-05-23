import joblib
import os

# Paths to models
BASE1_PATH = os.path.join("models", "linear_regression_model.pkl")
BASE2_PATH = os.path.join("models", "mlp_regressor_model.pkl")
BASE3_PATH = os.path.join("models", "random_forest_model.pkl")
META_PATH = os.path.join("models", "ensemble_model.pkl")
EXPLAINER_PATH = os.path.join("models", "shap_explainer.pkl")
PREPROCESSOR_PATH = os.path.join("models", "preprocessor.pkl")

# Load models
base_model1 = joblib.load(BASE1_PATH)
base_model2 = joblib.load(BASE2_PATH)
base_model3 = joblib.load(BASE3_PATH)
meta_model = joblib.load(META_PATH)
explainer = joblib.load(EXPLAINER_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)
