from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.experimental import enable_iterative_imputer  # Add this line
from sklearn.impute import IterativeImputer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

app = FastAPI()

# Load the best XGB pipeline
with open('best_pipeline.pkl', 'rb') as file:
    best_xgb_pipeline = pickle.load(file)

# Define the request body model
class CreditScoreRequest(BaseModel):
    person_age: int
    person_income: float
    person_home_ownership: str
    person_emp_length: float
    loan_intent: str
    loan_grade: str
    loan_amnt: float
    loan_int_rate: float
    loan_percent_income: float
    cb_person_default_on_file: str

@app.post("/credit_score")
async def credit_score(request: Request, data: CreditScoreRequest):
    # Create a DataFrame from the request data
    input_data = pd.DataFrame([data.dict()])

    # Preprocess the input data
    input_data['person_home_ownership'] = input_data['person_home_ownership'].map({'RENT': 0, 'MORTGAGE': 1, 'OWN': 2})
    input_data['loan_intent'] = input_data['loan_intent'].map({'DEBT_CONSOLIDATION': 0, 'CREDIT_CARD': 1, 'HOME_IMPROVEMENT': 2, 'MEDICAL': 3, 'MAJOR_PURCHASE': 4, 'SMALL_BUSINESS': 5})
    input_data['loan_grade'] = input_data['loan_grade'].map({'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6})
    input_data['cb_person_default_on_file'] = input_data['cb_person_default_on_file'].map({'Y': 1, 'N': 0})

    # Apply the best XGB pipeline to make predictions
    preds = best_xgb_pipeline.predict(input_data)
    print(type(best_xgb_pipeline))

    # Return the prediction as JSON response
    return JSONResponse(content={"credit_score": int(preds[0])})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)