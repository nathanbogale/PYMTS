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

# Evaluate the model on the testing data
y_pred = clf.predict(X_test_imputed)
conf_mat = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
print("Confusion matrix:")
print(conf_mat)
print(f"Accuracy: {accuracy}")

# Ask the user to provide the inputs
family_size = int(input("Enter the family size: "))
residential_area = input("Enter the residential area (urban or rural): ")
person_age = int(input("Enter the person's age: "))
person_income = float(input("Enter the person's income: "))
person_home_ownership = input("Enter the person's home ownership status (own or rent): ")
person_emp_length = int(input("Enter the person's employment length (years): "))
loan_intent = input("Enter the loan intent (PERSONAL,ELECTRONICS,MEDICAL,HEALTHANDBEAUTY,HOMEIMPROVEMENT or FURNITURE): ")
loan_grade = input("Enter the loan grade (A, B, C, D, or E): ")
loan_amnt = float(input("Enter the loan amount: "))
loan_int_rate = float(input("Enter the loan interest rate: "))
loan_status = input("Enter the loan status (approved or denied): ")
loan_percent_income = float(input("Enter the loan percentage of income: "))

# Calculate the credit score using the FICO method
fico_score = 0
if family_size <= 3:
    fico_score += 10
elif family_size > 3 and family_size <= 5:
    fico_score += 5
else:
    fico_score += 0

if residential_area == 'urban':
    fico_score += 5
elif residential_area == 'rural':
    fico_score -= 5

if person_age >= 21 and person_age <= 35:
    fico_score += 10
elif person_age > 35 and person_age <= 50:
    fico_score += 5
else:
    fico_score += 0

if person_income >= 50000 and person_income <= 75000:
    fico_score += 10
elif person_income > 75000 and person_income <= 100000:
    fico_score += 5
else:
    fico_score += 0

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
elif loan_grade == 'B''APPROVED'
    fico_score += 5
elif loan_grade == 'C':
    fico_score += 0
elif loan_grade == 'D':
    fico_score -= 5
else:
    fico_score -= 10

if loan_amnt >= 10000 and loan_amnt <= 50000:
    fico_score += 10
elif loan_amnt > 50000 and loan_amnt <= 100000:
    fico_score += 5
else:
    fico_score += 0

if loan_int_rate >= 20 and loan_int_rate <= 21:
    fico_score += 10
elif loan_int_rate > 21 and loan_int_rate <= 23:
    fico_score += 5
else:
    fico_score += 0

if loan_status == 'APPROVED':
    fico_score += 10
elif loan_status == 'REJECTED':
    fico_score -= 5

if loan_percent_income >= 0.10 and loan_percent_income <= 0.20:
    fico_score += 10
elif loan_percent_income > 0.20 and loan_percent_income <= 0.30:
    fico_score += 5
else:
    fico_score += 0

# Print the credit score
print(f"Your credit score is {fico_score}.")