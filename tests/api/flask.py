from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np

#app = Flask(__name__)
app = Flask("<link>akafay</link>")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    # Load the data
    df = pd.read_csv('credit_risk_dataset - added.csv')

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

    # Predict
    y_pred = clf.predict(np.array(data['X_test_imputed']).reshape(1, -1))

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

    if data['person_age'] >= 21 and data['person_age'] <= 35:
        fico_score += 10
    elif data['person_age'] > 35 and data['person_age'] <= 50:
        fico_score += 5
    else:
        fico_score += 0

    # ... continue with the rest of your FICO score calculation ...

    return jsonify({'fico_score': fico_score})
if __name__ == '__main__':
    app.run(port=5000, debug=True)