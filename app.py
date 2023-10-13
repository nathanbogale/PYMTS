from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np

app = Flask(__name__)
#app = Flask("<link>akafay</link>")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    # Load the data
    df = pd.read_csv('credit_risk_dataset.csv')

    # Preprocess the data
    df = df.drop(columns=['cb_person_default_on_file', 'cb_person_cred_hist_length', 'cb_person_cred_hist_average_value'])
    df = pd.get_dummies(df, drop_first=True)
    X = df.drop(columns=['loan_status'])
    y = df['loan_status']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale the data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Impute missing values
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    X_train_imputed = imputer.fit_transform(X_train_scaled)
    X_test_imputed = imputer.transform(X_test_scaled)

    # Train a histogram gradient boosting classifier on the training data
    clf = HistGradientBoostingClassifier()
    clf.fit(X_train_imputed, y_train)

   
    # Prepare the input data
    input_data = pd.DataFrame([data])
    input_data = pd.get_dummies(input_data, drop_first=True)

       # Ensure the input data has the same columns as the training data
    missing_cols = set(X.columns) - set(input_data.columns)
    for c in missing_cols:
        input_data[c] = 0
    input_data = input_data[X.columns]

    # Scale and impute the input data
    input_data_scaled = scaler.transform(input_data)
    input_data_imputed = imputer.transform(input_data_scaled)

    # Predict
    y_pred = clf.predict(input_data_imputed)

    # Calculate the credit score using the FICO method
    # ... your FICO score calculation ...
    # Calculate the custom credit score
    fico_score = 0  # Initialize the score

    # Add or subtract from the score based on the input data
    # ... your custom credit score calculation ...
    if data['family_size'] <= 3:
        fico_score += 10
    elif data['family_size'] > 3 and data['family_size'] <= 5:
        fico_score += 5
    else:
        fico_score += 0

    if data['residential_area'] == 'URBAN':
        fico_score += 5
    elif data['residential_area'] == 'RURAL':
        fico_score -= 5

 
        if person_age >= 21 and person_age <= 35:
            fico_score += 10
        elif person_age > 35 and person_age <= 50:
            fico_score += 5
        else:
            fico_score += 0

        if person_income >= 10000 and person_income <= 30000:
            fico_score += 2
        elif person_income >= 30000 and person_income <= 50000:
            fico_score += 5
        elif person_income >= 50000 and person_income <= 70000:
            fico_score += 8
        elif person_income > 70000 and person_income <= 100000:
            fico_score += 10
        elif person_income > 100000:
            fico_score += 15
        else:
            fico_score += 0

    # calculating the lan perscent income from income and amount
        if person_income > 0:  # Avoid division by zero
            loan_percent_income = loan_amnt / person_income
        else:
            loan_percent_income = 0

        #st.write(f"Loan percentage of income: {loan_percent_income}")


        if person_home_ownership == 'OWN':
            fico_score += 10
        elif person_home_ownership == 'MORTGAGE':
            fico_score += 5
        elif person_home_ownership == 'FAMILY':
            fico_score += 1
        elif person_home_ownership == 'RENT':
            fico_score -= 5

        if person_emp_length >= 2 and person_emp_length <= 5:
            fico_score += 10
        elif person_emp_length > 5 and person_emp_length <= 10:
            fico_score += 5
        else:
            fico_score += 0

        if loan_intent == 'PERSONAL':
            fico_score -= 10
        elif loan_intent == 'ELECTRONICS':
            fico_score += 5
        elif loan_intent == 'MEDICAL':
            fico_score += 5
        elif loan_intent == 'HEALTHANDBEAUTY':
            fico_score -= 5
        elif loan_intent == 'HOMEIMPROVEMENT':
            fico_score += 5
        elif loan_intent == 'FURNITURE':
            fico_score += 5


        if loan_grade == 'A':
            fico_score += 10
        elif loan_grade == 'B':
            fico_score += 5
        elif loan_grade == 'C':
            fico_score += 0
        elif loan_grade == 'D':
            fico_score -= 5
        else:
            fico_score -= 10

        if loan_amnt >= 10000 and loan_amnt <= 50000:
            fico_score += 5
        elif loan_amnt > 50000 and loan_amnt <= 100000:
            fico_score += 10
        else:
            fico_score += 0

        if loan_int_rate >= 20 and loan_int_rate <= 21:
            fico_score += 10
        elif loan_int_rate > 21 and loan_int_rate <= 23:
            fico_score += 5
        else:
            fico_score += 0

        if loan_status == 1:
            fico_score += 10
        elif loan_status == 0:
            fico_score -= 5

        if loan_percent_income >= 0.10 and loan_percent_income <= 0.20:
            fico_score += 10
        elif loan_percent_income > 0.20 and loan_percent_income <= 0.30:
            fico_score += 5
        else:
            fico_score += 0


    return jsonify({'fico_score': fico_score})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)