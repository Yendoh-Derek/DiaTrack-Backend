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
