import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Generate a synthetic dataset for demonstration
np.random.seed(42)
n_samples = 1000

data = {
    'current_salary': np.random.randint(30000, 150000, n_samples),
    'employment_period': np.random.randint(1, 20, n_samples),
    'income_vs_expense_ratio': np.random.uniform(0.5, 2.5, n_samples),
    'residential_area': np.random.randint(1, 5, n_samples),
    'family_size': np.random.randint(1, 6, n_samples),
    'housing_status': np.random.randint(0, 2, n_samples),
    'credit_history': np.random.randint(1, 5, n_samples),
    'age': np.random.randint(18, 65, n_samples),
    'education_level': np.random.randint(1, 5, n_samples),
    'employment_type': np.random.randint(0, 2, n_samples),
    'outstanding_debt': np.random.randint(0, 50000, n_samples),
    'total_assets': np.random.randint(10000, 500000, n_samples),
    'credit_score': np.random.randint(0, 2, n_samples)
}

df = pd.DataFrame(data)

# Define features and target variable
X = df.drop('credit_score', axis=1)
y = df['credit_score']

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_scaled, y)

# User input for credit scoring
user_data = {
    'current_salary': float(input("Enter your current salary: ")),
    'employment_period': int(input("Enter your employment period (in years): ")),
    'income_vs_expense_ratio': float(input("Enter your income vs. expense ratio: ")),
    'residential_area': int(input("Enter your residential area (1-5): ")),
    'family_size': int(input("Enter your family size: ")),
    'housing_status': int(input("Do you own your home (1 for own, 0 for rent): ")),
    'credit_history': int(input("Enter your credit history (1-5): ")),
    'age': int(input("Enter your age: ")),
    'education_level': int(input("Enter your education level (1-5): ")),
    'employment_type': int(input("Enter your employment type (1 for employed, 0 for unemployed): ")),
    'outstanding_debt': float(input("Enter your outstanding debt amount: ")),
    'total_assets': float(input("Enter your total assets value: "))
}

# Preprocess the user's input data
user_scaled = scaler.transform([list(user_data.values())])

# Make a prediction for the user
predicted_score = clf.predict(user_scaled)

if predicted_score[0] == 0:
    prediction_result = "Not Approved"
else:
    prediction_result = "Approved"

print("Predicted Credit Score:", prediction_result)
