import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

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

# Display the logo
st.image("logo_main.png", width=300)  # Adjust the width as needed

# Display the title and description
st.title("Akafay Credit Scoring Engine")
st.subheader("Find out your credit score with our ML FICO scoring engine")


# Evaluate the model on the testing data
y_pred = clf.predict(X_test_imputed)
conf_mat = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
st.write("Confusion matrix:")
st.write(conf_mat)
st.write(f"Accuracy: {accuracy}")

# Create a form for user input
with st.form(key='my_form'):
    family_size = st.number_input(label='Enter the family size', min_value=1, value=1, step=1)
    residential_area = st.selectbox('Enter the residential area', options=['URBAN', 'RURAL  '])
    person_age = st.number_input(label="Enter the person's age", min_value=18, value=18, step=1)
   # person_income = st.number_input(label="Enter the person's income", min_value=0.0, value=0.0, step=0.1)
    person_home_ownership = st.selectbox("Enter the person's home ownership status", options=['OWN', 'RENT','MORTGAGE','FAMILY'])
    person_emp_length = st.number_input(label="Enter the person's employment length (years)", min_value=0, value=0, step=1)
    loan_intent = st.selectbox("Enter the loan intent", options=['PERSONAL','ELECTRONICS','MEDICAL','HEALTHANDBEAUTY','HOMEIMPROVEMENT','FURNITURE'])
    loan_grade = st.selectbox("Enter the loan grade", options=['A', 'B', 'C', 'D', 'E'])
   # loan_amnt = st.number_input(label="Enter the loan amount", min_value=0.0, value=0.0, step=0.1)
    loan_int_rate = st.number_input(label="Enter the loan interest rate (Please do not change this value)", min_value=21.0, max_value= 21.0, value=21.0, step=0.1)
  #  loan_percent_income = st.number_input(label="Enter the loan percentage of income", min_value=0.0, value=0.0, step=0.1)
    loan_amnt = st.number_input(label="Enter the loan amount", min_value=0.0, value=0.0, step=0.1)
    person_income = st.number_input(label="Enter the person's income", min_value=0.0, value=0.0, step=0.1)
    loan_status = st.selectbox("Enter the loan status", options=['APPROVED', 'REJECTED'])



    submit_button = st.form_submit_button(label='Submit')

    st.write("Inputs to be included soon:")
    st.write("From User: Number of open accounts, Employment status.Total monthly debt(from bank), Payment history(from bank), Default history(from bank)")
    st.write("Collected From Bank: Total monthly debt, Payment history, Default history")
# Calculate the credit score using the FICO method
fico_score = 0

if submit_button:

      # Check if all fields are filled
    if not all([family_size, residential_area, person_age, person_home_ownership, person_emp_length, loan_intent, loan_grade, loan_amnt, person_income]):
        st.write("Please fill all fields.")
    else:        

        if family_size <= 3:
            fico_score += 10
        elif family_size > 3 and family_size <= 5:
            fico_score += 5
        else:
            fico_score += 0

        if residential_area == 'URBAN':
            fico_score += 5
        elif residential_area == 'RURAL':
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


        def generate_purchase_limit(credit_score):
          purchase_limit = credit_score * 1000
          return purchase_limit

        purchase_limit = generate_purchase_limit(fico_score)

        st.write(f"Your credit score is {fico_score}.")
        st.write(f"Your purchase limit is {purchase_limit}.")