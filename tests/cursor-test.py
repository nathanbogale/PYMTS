import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

def load_and_preprocess_data(filepath):
    df = pd.read_csv(filepath)
    df = df.drop(columns=['cb_person_default_on_file', 'cb_person_cred_hist_length', 'cb_person_cred_hist_average_value'])
    df = pd.get_dummies(df, drop_first=True)
    X = df.drop(columns=['loan_status'])
    y = df['loan_status']
    return X, y

def split_scale_impute_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    X_train_imputed = imputer.fit_transform(X_train_scaled)
    X_test_imputed = imputer.transform(X_test_scaled)
    return X_train_imputed, X_test_imputed, y_train, y_test

def train_and_evaluate_model(X_train, X_test, y_train, y_test):
    clf = HistGradientBoostingClassifier()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    conf_mat = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    return clf, conf_mat, accuracy

def calculate_fico_score(family_size, residential_area, person_age, person_income, person_home_ownership, person_emp_length, loan_intent, loan_grade, loan_amnt, loan_int_rate, loan_status, loan_percent_income):
    fico_score = 0
    # Add conditions here to calculate fico_score based on the inputs
    # ...
    return fico_score

def main():
    st.title('Credit Score Predictor')

    # Load and preprocess data
    X, y = load_and_preprocess_data('credit_risk_dataset - added.csv')
    X_train, X_test, y_train, y_test = split_scale_impute_data(X, y)

    # Train and evaluate model
    clf, conf_mat, accuracy = train_and_evaluate_model(X_train, X_test, y_train, y_test)

    st.write(f"Model accuracy: {accuracy}")

    # User input form
    st.subheader('Enter your details')
    family_size = st.number_input("Enter the family size", min_value=1, max_value=20, value=1)
    residential_area = st.text_input("Enter the residential area (urban or rural)")
    person_age = st.number_input("Enter the person's age", min_value=1, max_value=100, value=1)
    person_income = st.number_input("Enter the person's income", min_value=1.0, value=1.0)
    person_home_ownership = st.text_input("Enter the person's home ownership status (own or rent)")
    person_emp_length = st.number_input("Enter the person's employment length (years)", min_value=1, max_value=50, value=1)
    loan_intent = st.text_input("Enter the loan intent (PERSONAL,ELECTRONICS,MEDICAL,HEALTHANDBEAUTY,HOMEIMPROVEMENT or FURNITURE)")
    loan_grade = st.text_input("Enter the loan grade (A, B, C, D, or E)")
    loan_amnt = st.number_input("Enter the loan amount", min_value=1.0, value=1.0)
    loan_int_rate = st.number_input("Enter the loan interest rate", min_value=1.0, value=1.0)
    loan_status = st.text_input("Enter the loan status (approved or denied)")
    loan_percent_income = st.number_input("Enter the loan percentage of income", min_value=1.0, value=1.0)

    if st.button('Calculate Credit Score'):
        fico_score = calculate_fico_score(family_size, residential_area, person_age, person_income, person_home_ownership, person_emp_length, loan_intent, loan_grade, loan_amnt, loan_int_rate, loan_status, loan_percent_income)
        st.write(f"Your credit score is {fico_score}.")

if __name__ == "__main__":
    main()